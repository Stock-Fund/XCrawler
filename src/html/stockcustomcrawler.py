import tushare as ts
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import efinance as ef
import src.data_processor as data_processor
import src.html as html
import src.quantifytest as quantifytest
from src.html.stockutils import getStockSuffix
from src.util.timeutil import *
import datetime
import src.data_processor as data_processor
from typing import Dict

# 第三方tushare获取股票数据
def getStockData(stockNum):
    dd = ts.get_hist_data(stockNum)  # 爬取股票近三年的全部日k信息
    da = ts.get_realtime_quotes(stockNum) # 爬取股票实时行情信息
    # dd.applymap('002837'+'.xlsx') #将信息导出到excel表格中

# 通过efinace获取股票的实时数据
def getStockMinutesData(stockNum,freq):
    freq = 1
    # 获取最新一个交易日的分钟级别股票行情数据
    df = ef.stock.get_quote_history(stockNum, klt=freq)
    return df

# 每间隔 1 分钟获取一次单只股票分钟行情数据
def getStockData_Minutes_Normal(stockNum, freq = 1):
    status = {stockNum: 0}
    while 1:
        # 获取最新一个交易日的分钟级别股票行情数据
        df = getStockMinutesData(stockNum, freq)
        # 现在的时间
        now = str(datetime.today()).split('.')[0]
        # 将数据存储到 csv 文件中
        df.to_csv(f'{stockNum}.csv', encoding='utf-8-sig', index=None)
        print(f'已在 {now}, 将股票: {stockNum} 的行情数据存储到文件: {stockNum}.csv 中！')
        if len(df) == status[stockNum]:
            print(f'{stockNum} 已收盘')
            break
        status[stockNum] = len(df)
        print('暂停 60 秒')
        time.sleep(60)
        print('-'*10)

# 每间隔 1 分钟获取一次多只股票分钟行情数据(普通版)
def getStockDatas_Minutes_Normal(stockNums, freq = 1):
    status = {stock_code: 0 for stock_code in stockNums}
    while len(stockNums) != 0:
        for stock_code in stockNums.copy():
            # 现在的时间
            now = str(datetime.today()).split('.')[0]
            # 获取最新一个交易日的分钟级别股票行情数据
            df = ef.stock.get_quote_history(stock_code, klt=freq)
            # 将数据存储到 csv 文件中
            df.to_csv(f'{stock_code}.csv', encoding='utf-8-sig', index=None)
            print(f'已在 {now}, 将股票: {stock_code} 的行情数据存储到文件: {stock_code}.csv 中！')
            if len(df) == status[stock_code]:
                # 移除已经收盘的股票代码
                stockNums.remove(stock_code)
                print(f'股票 {stock_code} 已收盘！')
            status[stock_code] = len(df)
        if len(stockNums) != 0:
           print('暂停 60 秒')
           time.sleep(60)
        print('-'*10)

# 每间隔 1 分钟获取一次多只股票分钟行情数据(高速版)  
def getStockDatas_Minutes_Advanced(stockNums, freq = 1):
    status = {stock_code: 0 for stock_code in stockNums}
    while len(stockNums) != 0:
        # 获取最新一个交易日的分钟级别股票行情数据
        stocks_df: Dict[str, pd.DataFrame] = ef.stock.get_quote_history(
            stockNums, klt=freq)
        for stock_code, df in stocks_df.items():
            # 现在的时间
            now = str(datetime.today()).split('.')[0]
            # 将数据存储到 csv 文件中
            df.to_csv(f'{stock_code}.csv', encoding='utf-8-sig', index=None)
            print(f'已在 {now}, 将股票: {stock_code} 的行情数据存储到文件: {stock_code}.csv 中！')
            if len(df) == status[stock_code]:
                # 移除已经收盘的股票代码
                stockNums.remove(stock_code)
                print(f'股票 {stock_code} 已收盘！')
            status[stock_code] = len(df)
        if len(stockNums) != 0:
            print('暂停 60 秒')
            time.sleep(60)
        print('-'*10)

    print('全部股票已收盘')
    

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
        start_date = start
    else:
        start_date = "2023-10-01"
    code = stockNum + getStockSuffix(stockNum)
    # 获取今天的日期
    today = datetime.datetime.today().date()
    adjusted_date = adjust_date_to_weekday(today)
    print(f"调整后的日期{adjusted_date}")
    # 格式化日期
    end_date = adjusted_date.strftime("%Y-%m-%d")  # 假设需要的格式为 "YYYY-MM-DD"
    stockData = pdr.get_data_yahoo(code, start_date, end_date)
    stockData = stockData.round(2)
    stockData.to_csv("Assets/" + code + ".csv")
    stockData.to_excel("Assets/" + code + ".xlsx")
    stockData.to_json("Assets/" + code + ".json")

    stockData.index = pd.to_datetime(stockData.index)
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
        data_processor.customDataSavetosql(name + "_周", enginstr, weekdata)
        data_processor.customDataSavetosql(name + "_月", enginstr, mouthdata)

        if check:
            quantifytest.startQuantifytest(stockNum, now, start_date, enginstr, end_date, ma)

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
