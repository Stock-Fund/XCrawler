import pandas as pd
from sqlalchemy import create_engine
import datetime
import time

def SaveToXlsx(datas,head,path="Assets/data.xlsx"):
    num_columns = len(head)
    num_rows = len(datas)
    data_rows = [datas[i:i+num_columns] for i in range(0, num_rows, num_columns)]
    df = pd.DataFrame(data_rows,columns=head)
    df.to_excel(path, index=False)

def SaveToCsv(datas,head,path="Assets/data.csv"):
    num_columns = len(head)
    num_rows = len(datas)
    data_rows = [datas[i:i+num_columns] for i in range(0, num_rows, num_columns)]
    df = pd.DataFrame(data_rows,columns=head)
    df.to_csv(path,index=False)

def SaveToJson(datas,path="Assets/data.json",ignore_index = None):
    df = pd.DataFrame(datas,ignore_index)
    df.to_json(path, orient="records")
    

def SaveTosql(datas,head,enginestr,table):
    timestamp = datetime.datetime.fromtimestamp(time.time())
    now = datetime.datetime.now()
    # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d")
    engine = create_engine(enginestr)
    num_columns = len(head)
    num_rows = len(datas)
    print(num_columns)
    print(num_rows)

   
    # time table
    time_table = pd.read_sql_table("time", enginestr)
    if (time_table['id'] == formatted).any():
        time_table.loc[time_table['id'] == formatted , "value"] = timestamp
        # 将更新后的DataFrame写回MySQL数据库表
        time_table.to_sql('time', con=engine, if_exists='replace', index=False)
    else :
        time_table = pd.DataFrame([[formatted,timestamp]],columns=['id','value'])
        time_table.to_sql(name='time',con=engine,if_exists="append",index=False)
    
    # data table
    data_table = pd.read_sql_table(table, enginestr)
    if (data_table['日期'] == formatted).any():
        data_rows = [datas[i:i+num_columns] for i in range(0, num_rows, num_columns)]
        data_table = pd.DataFrame(data_rows,columns=head)
        # 重建表格数据 初始化
        data_table.to_sql(name=table,con=engine,if_exists="replace",index=False)
    else :
       data_rows = [datas[i:i+num_columns] for i in range(0, num_rows, num_columns)]
       data_table = pd.DataFrame(data_rows,columns=head)
       # 插入表格数据 更新
       data_table.to_sql(name=table,con=engine,if_exists="append",index=False)
    
    engine.dispose()
