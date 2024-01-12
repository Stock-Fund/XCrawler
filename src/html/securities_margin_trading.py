from bs4 import BeautifulSoup
from selenium import webdriver

# 融资融券交易数据爬取
# http://www.sse.com.cn/market/othersdata/margin/detail/ 各标的融资融券数据
# https://data.eastmoney.com/rzrq/total.html 全局全量融资融券数据


def get_margin_data(driver, url, now, enginstr):
    formatted = now.strftime("%Y-%m-%d")
    driver.get(url)
    driver.implicitly_wait(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    # 上海证券交易所网址利用js轮询请求数据，常规手段无法爬取融资融券数据



def getmargindata(url, now, enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    get_margin_data(driver, url, now, enginstr)
