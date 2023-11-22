import pandas as pd
from sqlalchemy import create_engine
import pymysql

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
    engine = create_engine(enginestr)
    num_columns = len(head)
    num_rows = len(datas)
    data_rows = [datas[i:i+num_columns] for i in range(0, num_rows, num_columns)]
    df = pd.DataFrame(data_rows,columns=head)
    df.to_sql(name=table,con=engine,if_exists="append",index=False)
    engine.dispose()
    
