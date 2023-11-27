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

   
    # if boo :
    df = pd.read_sql_table("time", enginestr)
    df.loc[df['id'] == formatted , "value"] = timestamp
    # 将更新后的DataFrame写回MySQL数据库表
    df.to_sql('time', con=engine, if_exists='replace', index=False)
    # else :
    #     time_table = pd.DataFrame([[formatted,timestamp]],columns=['id','value'])
    #     time_table.to_sql(name='time',con=engine,if_exists="append",index=False)
    
    
    print(head)
    data_rows = [datas[i:i+num_columns] for i in range(0, num_rows, num_columns)]
    data_table = pd.DataFrame(data_rows,columns=head)
    data_table['time_id'] = pd.to_datetime(formatted)
    data_table.to_sql(name=table,con=engine,if_exists="append",index=False)
    engine.dispose()
  
def check_dataform(table,enginestr,param,id):
     # 读取数据表到DataFrame
     df = pd.read_sql_table(table, enginestr, index_col=param)
     existing_data = df[df.index == id]
     if not existing_data.empty:
       # 如果存在，更新现有行的值
        return True
     else:
       # 如果不存在，插入新行
        return False