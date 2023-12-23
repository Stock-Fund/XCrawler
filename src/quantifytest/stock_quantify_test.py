import src.data_processor as data_processor
import src.html as html
from algorithm.stock import Stock
from datetime import datetime, time
import pandas as pd

def startQuantifytest(stockNum,now,enginstr):
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    date_part, time_part = formatted.split(' ')
    base_time_part = "00:00:00"
    if now.time() >= time(15, 0, 0):
        time_part = '15:00:00'
    name = data_processor.GetDataFromSql("代码库","代码","名称",stockNum,enginstr)
    if name == "":
      html.getStocksTime(stockNum,enginstr)
      name = data_processor.GetDataFromSql("代码库","代码","名称",stockNum,enginstr)
    timename = name + "分时"

    #custom_index 1,2,3,4,5
    #time_index 0，1，6，7
    value = date_part + " " + base_time_part
    # 某只股票所有的第三方数据
    stockCustomData = data_processor.GetAllDataFromTable(name,enginstr)
    # 某一天的第三方数据
    # stockCustomData = data_processor.GetDatasFromSql1(name,"Date",value,enginstr)
    stockTimeData = data_processor.GetDatasFromSql2(timename,{"id":"日期","value":date_part},{"id":"时间","value":time_part},enginstr)
    # stockData = {"Close":stockCustomData[4],"Open":stockCustomData[1],"High":stockCustomData[2],"Low":stockCustomData[3],"Volume":stockCustomData[6]}
    stockData = pd.DataFrame({
    'Close': stockCustomData.loc[0:,"Close"],
    'Open': stockCustomData.loc[0:,"Open"],
    'High': stockCustomData.loc[0:,"High"],
    'Low': stockCustomData.loc[0:,"Low"],
    'Volume': stockCustomData.loc[0:,"Volume"]
     })
    Chipsconcentrations = 1 #算法未处理
    saveTime = datetime.strptime(date_part+" "+time_part, "%Y-%m-%d %H:%M:%S").time()
    datas = [saveTime,stockTimeData[0],stockTimeData[1],stockTimeData[6],stockTimeData[7],Chipsconcentrations]
    stock_instance = Stock(stockData, datas)
    volumsBoo = stock_instance.checkVolums()
    # 检查今天成交量是否超过昨天的成交量
    print(f"{name}今日成交量超过昨日成交量:{volumsBoo}")