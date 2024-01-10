from bs4 import BeautifulSoup
from selenium import webdriver

# 融资融券交易数据爬取
# http://www.sse.com.cn/market/othersdata/margin/detail/ 各标的融资融券数据
# https://data.eastmoney.com/rzrq/total.html 全局全量融资融券数据


def get_margin_data(driver, url, now, enginstr):
    driver.get(url)
    driver.implicitly_wait(2)
    soup = BeautifulSoup(driver.page_source, "lxml")


def getmargindata(url, now, enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    get_margin_data(driver, url, now, enginstr)
