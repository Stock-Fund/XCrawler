from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import src.xlsx as xlsx

def get_SHBoard_data(driver,tmpUrl,enginstr):
     headers = []
     datas = []
     url = driver.get(tmpUrl) 
     driver.implicitly_wait(2)
     soup = BeautifulSoup(driver.page_source,'lxml')
     table = soup.select("table.table_wrapper-table")
     
     timestamp = datetime.datetime.fromtimestamp(time.time())
     now = datetime.datetime.now()
     # 格式化为字符串
     formatted = now.strftime("%Y-%m-%d")
     for ta in table:
        for body in ta.select('thead'):
           for tr in body.select('tr'):
             for th in tr.select('th'):
                data = th.get_text()
                if len(data) != 0 and data != "加自选":
                    headers.append(data)
                    if data == "市净率":
                        # 给时间表插入时间列
                        name="日期"
                        headers.append("日期")
        max = len(headers)
        for body in ta.select('tbody'):
           for tr in body.select('tr'):
             index = 1
             for td in tr.select('td'):
               data1 = td.get_text()
               if len(data1) != 0:
                  index += 1
                  datas.append(data1)
                  if index == max:
                     datas.append(formatted)               
    
    
     datas = list(map(str, datas))
     headers = list(map(str, headers))
     xlsx.SaveToCsv(datas,headers,"Assets/sh_data.csv")
     xlsx.SaveToXlsx(datas,headers,"Assets/sh_data.xlsx")
     xlsx.SaveToJson(datas,"Assets/sh_data.json")
     
     # 已mysql为例,如果已localhost为host,那port端口一般为3306
     # enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"
     xlsx.SaveTosql(datas,headers,enginstr,"stock")
     print("SHBoardData crawle completed")
     return soup

# 爬取上证交易所股票 
def getSHBoard(url,enginstr):
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   options.add_argument('--disable-notifications')
   # options.add_argument('--disable-tabs')
   driver = webdriver.Chrome(options = options)
#    url = "http://quote.eastmoney.com/center/gridlist.html#sh_a_board"
   # while True:
   get_SHBoard_data(driver,url,enginstr)
      #  time.sleep(10)