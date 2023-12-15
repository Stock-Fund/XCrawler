from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import src.data_processor as data_processor

# 获取指定股票的数据
def get_stock_data(stockNum,driver,url,enginstr):
    datas = []
    driver.get(url) 
    driver.implicitly_wait(2)
    soup = BeautifulSoup(driver.page_source,'lxml')
    namediv = soup.select_one('div.quote_title_l')
    namespan =  namediv.find('span', class_="quote_title_name quote_title_name_190")
    baseName = namespan.get_text()
    name = baseName + "分时"
    # 将stockNum,stockName存储到数据库，以便后续使用
    titles = ['代码','名称']
    titles = list(map(str,titles))
    data.SaveStockNameByNum(stockNum,baseName,titles,enginstr,"代码库")
    
    class_mm = soup.select_one('div.mm')
    table = class_mm.find('table')
    headers = []
    now = datetime.datetime.now()
     # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    for body in table.select('tbody'):
        titleIndex = 0
        for tr in body.select('tr'):
           index = 0
           titleStr = ""
           value = ""
           for td in tr.select('td'):
              data = td.get_text()
              if index ==0 and titleIndex !=5 :
                 titleStr= data
                 headers.append(titleStr)
              if index == 1:
                 value=data
              elif index == 2:
                 data=data+"--价位:"+value
                 datas.append(data)
              index = index + 1
           titleIndex = titleIndex + 1
    headers.append("日期")
    datas.append(formatted)
    datas = list(map(str, datas))
    headers = list(map(str, headers))
   #  src.data_processor.SaveToXlsx(datas,headers,f"Assets/{stockNum}_time.xlsx")
   #  src.data_processor.SaveToCsv(datas,headers,f"Assets/{stockNum}_time.csv")
   #  src.data_processor.SaveToJson(datas,f"Assets/{stockNum}_time.json")
    data.SaveTosqlMinutes(datas,headers,enginstr,name)
    print(f"{baseName} stockminutesdata crawle completed")

# 循环爬取制定股票数据
def getStocksTime(stockNum,enginstr):
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   # options.add_argument('--disable-tabs')
   driver = webdriver.Chrome(options = options)
   url = f"http://quote.eastmoney.com/sh{stockNum}.html"
   # while True:
   get_stock_data(stockNum,driver,url,enginstr)
      #  time.sleep(10)
      
      