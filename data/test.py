from selenium import webdriver
from bs4 import BeautifulSoup
import time
 
driver = webdriver.Chrome()       
# 每隔5S遍历一次网页的数据
while True:      # 创建Chrome对象
     url = driver.get('http://quote.eastmoney.com/zs000001.html') 
     driver.implicitly_wait(2)
     soup = BeautifulSoup(driver.page_source,'lxml')
# print(driver.page_source)    # 访问东方财富.
     table = soup.find_all('table',class_='zjl1')


     for ta in table:
    # print(ta.text)
          for body in ta.find_all('tbody'):
              for tr in body.find_all('tr'):
               print(tr.get_text())
     time.sleep(5)


# time.sleep(200)   #两秒后关闭
# driver.quit()