import src.html
import time
from selenium import webdriver
bashPath = "http://quote.eastmoney.com"

def get_Data(driver,tmpUrl):
      print("east is runing")
      print(tmpUrl)
      url = driver.get(tmpUrl) 
      driver.implicitly_wait(2)
      soup = src.html.BeautifulSoup(driver.page_source,'lxml')
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
        # print(f"链接地址: {href}")
        img_tag = a_tag.find('img')
        if img_tag:
               img_src = img_tag['src']
               img_alt = img_tag['alt']
              #  print(f"图片地址: {img_src}")
              #  print(f"图片描述: {img_alt}")
               img_url = src.html.urljoin(bashPath, img_src)
              #  print(f"原始图片地址: {img_url}")
                # 发送GET请求下载图片
               img_response = src.html.requests.get(img_url)

               # 使用Image.open打开图片
               image = src.html.Image.open(src.html.BytesIO(img_response.content))
               image = image.convert('L')
               # 设置 pytesseract 参数
               custom_config = r'--psm 6 --oem 2'
               text = src.html.pytesseract.image_to_string(image,lang='chi_sim',config=custom_config)
              #  print('picture:'+text)

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

# 循环爬取主版股票
def cycle():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  # options.add_argument('--disable-tabs')
  driver = webdriver.Chrome(options = options)
  url = "http://quote.eastmoney.com/zs000001.html"
  # http://quote.eastmoney.com/sh603496.html
  while True:
     get_Data(driver,url)
     time.sleep(10)
     
def get_stock_data(driver,url):
    datas = []
    driver.get(url) 
    driver.implicitly_wait(2)
    soup = src.html.BeautifulSoup(driver.page_source,'lxml')
    namediv = soup.select_one('div.quote_title_l')
    namespan =  namediv.find('span', class_="quote_title_name quote_title_name_190")
    class_mm = soup.select_one('div.mm')
    table = class_mm.find('table')
    for body in table.select('tbody'):
        for tr in body.select('tr'):
            data = tr.get_text()
            datas.append(data)
            print(tr.get_text())
    datas = list(map(str, datas))
    nameStr = namespan .get('title')
    datas.insert(0, nameStr)
    src.xlsx.SaveToXlsx(datas,"Assets/stocks.xlsx")
    src.xlsx.SaveToCsv(datas,"Assets/stocks.csv")
    src.xlsx.SaveToJson(datas,"Assets/stocks.json")
    print("finished")
  


# 循环爬取制定股票数据
def cycleStocks(stockNum):
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   # options.add_argument('--disable-tabs')
   driver = webdriver.Chrome(options = options)
   url = f"http://quote.eastmoney.com/sh{stockNum}.html"
   while True:
       get_stock_data(driver,url)
       time.sleep(10)

def get_SHBoard_data(driver,tmpUrl):
     headers = []
     datas = []
     url = driver.get(tmpUrl) 
     driver.implicitly_wait(2)
     soup = src.html.BeautifulSoup(driver.page_source,'lxml')
     table = soup.select("table.table_wrapper-table")
     for ta in table:
        for body in ta.select('thead'):
           for tr in body.select('tr'):
             for th in tr.select('th'):
                data = th.get_text()
                headers.append(data)
                print(data)
        for body in ta.select('tbody'):
           for tr in body.select('tr'):
             for td in tr.select('td'):
               data1 = td.get_text()
               datas.append(data1)
               

             
        
     datas = list(map(str, datas))

    #  print(datas)
     print(headers)
     headers.pop(0)
     print(headers)
     headers = list(map(str, headers))
    #  print(headers)
     src.xlsx.SaveToCsv(datas,headers,"Assets/sh_data.csv")
     src.xlsx.SaveToXlsx(datas,"Assets/sh_data.xlsx")
    #  src.xlsx.SaveToCsv(datas,"Assets/sh_data.csv")
     src.xlsx.SaveToJson(datas,"Assets/sh_data.json")
     return soup


# 爬取上证交易所股票 
def cycleSHBoard():
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   # options.add_argument('--disable-tabs')
   driver = webdriver.Chrome(options = options)
   url = "http://quote.eastmoney.com/center/gridlist.html#sh_a_board"
   while True:
       get_SHBoard_data(driver,url)
       time.sleep(10)