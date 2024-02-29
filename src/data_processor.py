import pandas as pd
from sqlalchemy import create_engine, inspect
from datetime import datetime
import time


def checkTableExist(table, engine, enginestr):
    inspector = inspect(engine)
    # 检查表是否存在
    if table in inspector.get_table_names():
        df = pd.read_sql_table(table, enginestr)
        if df.empty:
            print(f"{table} does not exist")
            return None
        return df
    else:
        return None


def checkTableExist1(table, engine):
    query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table}')"
    result = engine.execute(query)
    exists = result.scalar()
    return exists


def SaveToXlsx(datas, head, path="Assets/data.xlsx"):
    num_columns = len(head)
    num_rows = len(datas)
    data_rows = [datas[i : i + num_columns] for i in range(0, num_rows, num_columns)]
    df = pd.DataFrame(data_rows, columns=head)
    df.to_excel(path, index=False)


def SaveToCsv(datas, head, path="Assets/data.csv"):
    num_columns = len(head)
    num_rows = len(datas)
    data_rows = [datas[i : i + num_columns] for i in range(0, num_rows, num_columns)]
    df = pd.DataFrame(data_rows, columns=head)
    df.to_csv(path, index=False)


def SaveToJson(datas, path="Assets/data.json", ignore_index=None):
    df = pd.DataFrame(datas, ignore_index)
    df.to_json(path, orient="records")


def SaveTosql(datas, head, enginestr, table):
    timestamp = datetime.fromtimestamp(time.time())
    now = datetime.now()
    # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d")
    engine = create_engine(enginestr)
    num_columns = len(head)
    num_rows = len(datas)

    # time table
    try:
        time_table = pd.read_sql_table("time", enginestr)
    except:
        time_table = pd.DataFrame(columns=["id", "value"])
    if (time_table["id"] == formatted).any():
        time_table.loc[time_table["id"] == formatted, "value"] = timestamp
        # 将更新后的DataFrame写回MySQL数据库表
        time_table.to_sql("time", con=engine, if_exists="replace", index=False)
    else:
        time_table = pd.DataFrame([[formatted, timestamp]], columns=["id", "value"])
        time_table.to_sql(name="time", con=engine, if_exists="append", index=False)

    # data table
    try:
        data_table = pd.read_sql_table(table, enginestr)
    except:
        data_table = None
    if data_table is not None and (data_table["日期"] == formatted).any():
        update_rows = [
            datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
        ]
        update_data_table = pd.DataFrame(update_rows, columns=head)
        update_table = update_data_table["日期"].unique()
        # 逐条更新
        for id in update_table:
            row_idx = data_table["日期"] == id
            data_table.loc[row_idx] = update_data_table[update_data_table["日期"] == id]
        # print("update mysql data complete")
    else:
        data_rows = [
            datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
        ]
        data_table = pd.DataFrame(data_rows, columns=head)
        # 插入表格数据 更新
        data_table.to_sql(name=table, con=engine, if_exists="append", index=False)
    #    print("create mysql data complete")
    engine.dispose()


# 分时数据存储
def SaveTosqlMinutes(datas, head, enginestr, timepart, table):
    # timestamp = datetime.fromtimestamp(time.time())
    now = datetime.now()
    # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d")
    engine = create_engine(enginestr)
    num_columns = len(head)
    num_rows = len(datas)
    # data table
    try:
        data_table = pd.read_sql_table(table, enginestr)
    except:
        data_table = None
        print(f"datatable {table} is None")
    if data_table is not None and (data_table["日期"] == formatted).any():
        update_rows = [
            datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
        ]
        update_data_table = pd.DataFrame(update_rows, columns=head)
        # 获取日期这一列
        update_table = update_data_table["日期"].unique()

        datalen = len(data_table)
        hasData = False
        # 逐条更新，当找到当前时间的数据则更新，若没有找到则在后续if判断中插入新数据
        for id in update_table:
            row_idx = data_table["日期"] == id
            # 当前时间
            now = datetime.strptime(timepart, "%H:%M:%S").time()
            if "时间" in data_table.loc[row_idx]:
                value = data_table.loc[row_idx]["时间"]
                # 对存在的索引值进行操作
                # 数据库内存入的时间
                data_time = datetime.strptime(value[datalen - 1], "%H:%M:%S").time()
                # 找到当前的时间
                if data_time == now:
                    data_table.loc[row_idx] = update_data_table[
                        update_data_table["日期"] == id
                    ]
                    hasData = True
                    break

        if not hasData:
            # 当存在一张空白的表格时，需要用replace，而不是append，否则找不到对应的列
            data_rows = [
                datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
            ]
            data_table = pd.DataFrame(data_rows, columns=head)
            # 插入表格数据 更新
            data_table.to_sql(name=table, con=engine, if_exists="append", index=False)
    else:
        print("create new table" + f"{head}")
        # 当存在一张空白的表格时，需要用replace，而不是append，否则找不到对应的列
        data_rows = [
            datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
        ]
        data_table = pd.DataFrame(data_rows, columns=head)
        # 插入表格数据 更新
        data_table.to_sql(name=table, con=engine, if_exists="replace", index=False)
    #    print("create mysql data complete")
    engine.dispose()


# 存储股票名字跟代码
def SaveStockNameByNum(key, name, head, enginestr, table):
    datas = [key, name]
    datas = list(map(str, datas))
    num_columns = len(head)
    num_rows = len(datas)
    engine = create_engine(enginestr)
    try:
        data_table = pd.read_sql_table(table, enginestr)
    except:
        data_table = None
    if data_table is not None:
        id = "代码"
        value = "名字"
        update_rows = [
            datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
        ]
        update_data_table = pd.DataFrame(update_rows, columns=head)
        # 获取股票代码这一列
        update_table = update_data_table[id].unique()
        for updateid in update_table:
            if updateid in data_table[id].values:
                # updateid存在,跳过
                # print('Data already exists')
                continue
            else:
                # print('Data not found, need to insert')
                update_data_table.to_sql(
                    name=table, con=engine, if_exists="append", index=False
                )
    else:
        data_rows = [
            datas[i : i + num_columns] for i in range(0, num_rows, num_columns)
        ]
        data_table = pd.DataFrame(data_rows, columns=head)
        data_table.to_sql(name=table, con=engine, if_exists="append", index=False)
    engine.dispose()


# 清空某个表
def ClearsqlTable(enginestr, table):
    engine = create_engine(enginestr)
    table = pd.read_sql_table(table, enginestr)
    if not table.empty:
        table.to_sql(name=table, con=engine, if_exists="replace")
    engine.dispose()


# 第三方库数据存储
def customDataSavetosql(table, enginestr, datas):
    engine = create_engine(enginestr)
    df = checkTableExist(table, engine, enginestr)
    if df is not None:
        print(table, "存在")
        datas.to_sql(name=table, con=engine, if_exists="replace")
    else:
        print(table, "不存在")
        datas.to_sql(name=table, con=engine, if_exists="append")
    engine.dispose()


# 获取数据库某个table中所有数据
def GetAllDataFromTable(table, enginestr, start="", end=""):
    engine = create_engine(enginestr)
    df = checkTableExist(table, engine, enginestr)
    if df is not None:
        if start != "" and end != "":
            query = f"SELECT * FROM {table}  WHERE Date BETWEEN '{start}' AND '{end}'"
        elif start != "" and end == "":
            query = f"SELECT * FROM {table}  WHERE Date >= '{start}'"
        else:
            query = f"SELECT * FROM {table}"
        data = pd.read_sql(query, engine)
        engine.dispose()
        return data
    else:
        return None


# 从数据库获取某个数据
def GetDataFromSql(table, id, value, stockNum, enginestr):
    engine = create_engine(enginestr)
    df = checkTableExist(table, engine, enginestr)
    if df is not None:
        data = ""
        try:
            data = df.loc[df[id] == stockNum, value].values[0]
        except IndexError:
            print("data does not exist")
        engine.dispose()
        return data
    else:
        return None


# 从数据库获取某一行数据 简单判断
def GetDatasFromSql1(table, id, value, enginestr):
    engine = create_engine(enginestr)
    df = checkTableExist(table, engine, enginestr)
    if df is not None:
        data = ""
        try:
            data = df.loc[df[id] == value].values[0]
        except IndexError:
            print("data does not exist")
        engine.dispose()
        return data
    else:
        return None


# 从数据库复合判断获取某一行数据
def GetDatasFromSql2(table, obj1, obj2, enginestr):
    engine = create_engine(enginestr)
    df = checkTableExist(table, engine, enginestr)
    if df is not None:
        datas = ""
        data = None
        try:
            datas = df.loc[df[obj1["id"]] == obj1["value"]].values
            # 默认返回最新数据，即最后一位数据
            data = datas[len(datas) - 1]
        except IndexError:
            print("data does not exist")
        engine.dispose()
        return data
    else:
        return None


# 从数据库中某个表内获取列名为value的那一列所有数据
def GetAllStockCode(table, value, enginestr):
    engine = create_engine(enginestr)
    df = checkTableExist(table, engine, enginestr)
    if df is not None:
        datas = df[value].tolist()
        return datas
    else:
        print("none")
        return None
