import tushare as ts
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import src.data_processor as data_processor
import src.html as html
import src.quantifytest as quantifytest
from src.html.stockutils import getStockSuffix
import datetime
import src.data_processor as data_processor


# 第三方tushare获取股票数据
def getStockData(stockNum):
    dd = ts.get_hist_data(stockNum)  # 爬取股票近三年的全部日k信息
    # dd.applymap('002837'+'.xlsx') #将信息导出到excel表格中


def showStockData(stockNum, enginstr):
    now = datetime.datetime.now()
    # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d")
    name = f"{formatted}-allstock"
    data = data_processor.GetDatasFromSql1(name, "代码", stockNum, enginstr)
    if data is None:
        print(f"{formatted} table is not exist")
    else:
        print(data)


# pandas_datareader通过yahoo获取股票数据
def getStockData_datareader(stockNum, now, start, enginstr, check, ma=5):
    yf.pdr_override()
    if start is not None:
        formatted_date = start
    else:
        formatted_date = "2023-10-01"
    code = stockNum + getStockSuffix(stockNum)
    stockData = pdr.get_data_yahoo(code, formatted_date)
    stockData = stockData.round(2)
    stockData.to_csv("Assets/" + code + ".csv")
    stockData.to_excel("Assets/" + code + ".xlsx")
    stockData.to_json("Assets/" + code + ".json")

    # stockData.index = pd.to_datetime(stockData.index)
    # 周级别数据
    weekdata = stockData.resample("W").last()

    # 月级别数据
    mouthdata = stockData.resample("M").last()

    # 开始时间
    # print(stockData.index[0])
    # 结束时间
    # print(stockData.index[-1])
    # 已mysql为例,如果已localhost为host,那port端口一般为3306
    # enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stockData"
    name = data_processor.GetDataFromSql("代码库", "代码", "名称", stockNum, enginstr)
    if name == "":
        html.getStocksTime(stockNum, now, enginstr)
        name = data_processor.GetDataFromSql(
            "代码库", "代码", "名称", stockNum, enginstr
        )
        if name == "":
            print(f"{stockNum} table is not exist")
            return
    else:
        data_processor.customDataSavetosql(name, enginstr, stockData)
        data_processor.customDataSavetosql(name+"_周", enginstr, weekdata)
        data_processor.customDataSavetosql(name+"_月", enginstr, mouthdata)
        
        if check:
            quantifytest.startQuantifytest(stockNum, now, formatted_date, enginstr, ma)

        # print(f"{name} customDatareader crawle completed")

    # 5日收盘价均价
    # mean_price_5 = stock['Close'].rolling(window=5).mean()
    # mean_price_10 = stock['Close'].rolling(window=10).mean()
    # mean_price_20 = stock['Close'].rolling(window=20).mean()
    # mean_price_30 = stock['Close'].rolling(window=30).mean()
    # mean_price_40 = stock['Close'].rolling(window=40).mean()
    # mean_price_60 = stock['Close'].rolling(window=60).mean()
    # 绘制均线逻辑
    # zonghe_data=pd.concat([mean_price_5,mean_price_10,mean_price_20,mean_price_30,mean_price_40,mean_price_60],axis=1)
    # zonghe_data.columns = ['MA5','MA10','MA20','MA30','MA40','MA60']
    # zonghe_data[ ['MA5','MA10','MA20','MA30','MA40','MA60']].plot(subplots=False,style=['r','g','b','m'],grid=True)
    # print(f"MA5: {mean_price_5} MA10: {mean_price_10} MA30: {mean_price_30}")
    # plt.show()
