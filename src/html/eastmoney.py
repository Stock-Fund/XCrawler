from crawlerdata.mainboardcrawler import getSHBoard
from crawlerdata.stockcustomcrawler import getStockData_datareader
from crawlerdata.stocktimecrawler import getStocksTime
bashPath = "http://quote.eastmoney.com"
enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"


# 获取主板数据
def getSHBoard(self,url,enginstr):
   getSHBoard(self,url,enginstr)


# 获取某个股票的分时数据
def getStocksTime(self,stockNum,stockName,enginstr):
    getStocksTime(self,stockNum,stockName,enginstr)


# 通过第三方获取某个股票的价位数据
def getStockData_datareader(self,stockNum,stockName,enginstr):
    getStockData_datareader(self,stockNum,stockName,enginstr)
    


