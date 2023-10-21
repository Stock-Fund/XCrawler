from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import requests
import os
from io import BytesIO
import pytesseract
from PIL import Image

bashPath = "http://quote.eastmoney.com"
driver = webdriver.Chrome()       
# 每隔5S遍历一次网页的数据
while True:      # 创建Chrome对象
     url = driver.get('http://quote.eastmoney.com/zs000001.html') 
     driver.implicitly_wait(2)
     soup = BeautifulSoup(driver.page_source,'lxml')
     # print(driver.page_source)    # 访问东方财富.
     table = soup.find_all('table',class_='zjl1')
     logo = soup.find_all('a',class_='logolink2')


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

     

     # 线上抓数据
     for ta in table:
    # print(ta.text)
          for body in ta.find_all('tbody'):
              for tr in body.find_all('tr'):
               print(tr.get_text())
     time.sleep(60)


# time.sleep(200)   #两秒后关闭
# driver.quit()