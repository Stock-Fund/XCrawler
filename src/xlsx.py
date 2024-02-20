import pandas as pd
import csv

def SaveToXlsx(data,path="Assets/data.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(path, index=False,header=False)

def SaveToCsv(data,headers,path="Assets/data.csv", index=False):
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(path,index)
    # rows = [headers] + data
    # with open(path, "w", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(rows)
    # # print(len(header), len(df.columns))
    # df.to_csv(f, index)

def SaveToJson(data,path="Assets/data.json",ignore_index = None):
    df = pd.DataFrame(data,ignore_index)
    df.to_json(path, orient="records")
