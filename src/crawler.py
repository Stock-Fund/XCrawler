from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import requests
import os
from io import BytesIO
import pytesseract
import src.timeutil
from PIL import Image
import schedule
import src.xlsx
from src.process.simplethread import SimpleThread
from src.process.simpleprocess import SimpleProcess

bashPath = "http://quote.eastmoney.com"
bashUrl = 'http://quote.eastmoney.com/zs000001.html'
driver = webdriver.Chrome()     
image = None
basesoup = None

# 创建Chrome对象
def _get_Data(tmpUrl):
   # if soup is None:
      bashUrl = tmpUrl
      url = driver.get(tmpUrl) 
      driver.implicitly_wait(2)
      soup = BeautifulSoup(driver.page_source,'lxml')
      # print(driver.page_source)    # 访问东方财富.
      # soup select寻找的方式更加效率
      table = soup.select('table.zjl1')
      logo = soup.select('a.logolink2')
      # soup find all方式寻找效率低些，但基于递归的数据用find_all就比较合适
      # table = soup.find_all('table',class_='zjl1')
      # logo = soup.find_all('a',class_='logolink2')
      # 线上抓图，识图
      for a_tag in logo:
      #    text = a_tag.text  # 获取<a>标签内的文本内容
        href = a_tag['href']  # 获取<a>标签的href属性值
      #    print(f"文本内容: {text}")
        print(f"链接地址: {href}")
        img_tag = a_tag.find('img')
        if img_tag:
               img_src = img_tag['src']
               img_alt = img_tag['alt']
               print(f"图片地址: {img_src}")
               print(f"图片描述: {img_alt}")
               img_url = urljoin(bashPath, img_src)
               print(f"原始图片地址: {img_url}")
                # 发送GET请求下载图片
               img_response = requests.get(img_url)

               # 使用Image.open打开图片
               image = Image.open(BytesIO(img_response.content))
               image = image.convert('L')
               # 设置 pytesseract 参数
               custom_config = r'--psm 6 --oem 2'
               text = pytesseract.image_to_string(image,lang='chi_sim',config=custom_config)
               print('123:'+text)
   # else:
   #   print("soup is not none")


      datas = []
      
     
    # 线上抓数据
      for ta in table:
    # print(ta.text)
          for body in ta.select('tbody'):
              for tr in body.select('tr'):
               data = tr.get_text()
               datas.append(data)
               print(tr.get_text())
      datas = list(map(str, datas))
       # 写入xlsx title
      datas.insert(0, "数据")
      src.xlsx.SaveToXlsx(datas,"Assets/data.xlsx")
      src.xlsx.SaveToCsv(datas,"Assets/data.csv")
      src.xlsx.SaveToJson(datas,"Assets/data.json")
      return soup
    
def _run_get_Data():
  _get_Data(bashUrl)


def _run_cycle():
  # 每天9:30遍历一次网页的数据
  while True: 
     print("cycle=====")
     localtime = src.timeutil.get_local_time()
     print(bashUrl)
     if basesoup:
         schedule.every().day.at("09:30").do(_run_get_Data)
         print("time is 09:30")  
     else: 
         basesoup = _get_Data(bashUrl)
         # basesoup = _get_Data()
         print("basesoup is none")
         
     urls=[
         'https://www.zhihu.com/question/51359754/answer/3024289861',
         'https://www.zhihu.com/question/278798145/answer/3266830271',
         'https://www.youtube.com/'
     ]    

     thread = SimpleThread(urls)
     thread.run()
    
    #  time.sleep(1)

def try_start():
     urls=[
         'http://quote.eastmoney.com/zs000001.html',
         'http://quote.eastmoney.com/zs000001.html',
         'http://quote.eastmoney.com/zs000001.html'
        #  'https://www.zhihu.com/question/51359754/answer/3024289861',
        #  'https://www.zhihu.com/question/278798145/answer/3266830271',
        #  'https://www.youtube.com/'
     ]  
     processes = []
     for url in urls:
        bashUrl = url
        p = SimpleProcess(target=_run_cycle)
        p.start()
        processes.append(p)
        
     for p in processes:
        p.join()

# _run_get_Data()
# time.sleep(2000)   #两秒后关闭
# driver.quit()