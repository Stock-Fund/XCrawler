import pandas as pd

def SaveToXlsx(data,path="Assets/data.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(path, index=False,header=False)

def SaveToCsv(data,path="Assets/data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False,header=False)

def SaveToJson(data,path="Assets/data.json",ignore_index = None):
    df = pd.DataFrame(data,ignore_index)
    df.to_json(path, orient="records")