from crawlerdata.mainboardcrawler import cycleSHBoard
from crawlerdata.stockcustomcrawler import getStockData_datareader
from crawlerdata.stocktimecrawler import cycleStocksTime
bashPath = "http://quote.eastmoney.com"
enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"


# 循环获取主板数据
def cycleSHBoard(self,url,enginstr):
   cycleSHBoard(self,url,enginstr)


# 循环获取某个股票的分时数据
def cycleStocksTime(self,stockNum,stockName,enginstr):
    cycleStocksTime(self,stockNum,stockName,enginstr)


# 通过第三方获取某个股票的价位数据
def getStockData_datareader(self,stockNum,stockName,enginstr):
    getStockData_datareader(self,stockNum,stockName,enginstr)


