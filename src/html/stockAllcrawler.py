import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from src.html.mainboardcrawler import get_Data_FromSoup
import src.data_processor as data_processor
from src.html.stockutils import getStockTimeUrl, getStockSuffix
from pandas_datareader import data as pdr
import yfinance as yf
import asyncio
import pandas as pd

# A股所有股票页面数据爬取
url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"

delay_time = 30
sleep_time = 8
def xcrawlerStockData(soup):
    datas, headers = get_Data_FromSoup(soup)
    return datas, headers


def get_allstock_data(key,token,pushover,driver, enginstr):
    driver.get(url)
    driver.implicitly_wait(30)
    index = 1
    datas = []
    headers = []
    while True:
        soup = BeautifulSoup(driver.page_source, "lxml")
        _datas, _headers = xcrawlerStockData(soup)
        datas.extend(_datas)
        if index == 1:
            headers.extend(_headers)
        print(f"第{index}页A股数据获取完成")
        try:
            next_button = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (
                        # 通过判断是否包含 next  , paginate_button 来找next_button,但当找到的next_button中包含disabled则表明已经是最后一页
                        By.XPATH,
                        "//a[contains(concat(' ', normalize-space(@class), ' '), ' next ') and contains(concat(' ', normalize-space(@class), ' '), ' paginate_button ')]",
                    )
                )
            )
        except (StaleElementReferenceException, TimeoutException) as e:
            print("页面加载超时或元素未找到:", e)
            break
        except Exception as e:
            print("发生异常:", e)
            break
        # 判断是否包含disabled类
        if "disabled" in next_button.get_attribute("class"):
            print("已经是最后一页!")
            break
        else:
            try:
                # 点击按钮
                next_button.click()
            except StaleElementReferenceException:
                print("最后一页加载超时!")
                continue

            # 增加延时，模拟人类操作间隔
            time.sleep(sleep_time)  # 可根据实际情况调整延时时间
            # 等待页面加载完成
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='listview full']")
                )
            )
            index += 1
    now = datetime.datetime.now()
    # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d")
    data_processor.SaveToCsv(datas, headers, "Assets/allstock_data.csv")
    data_processor.SaveToXlsx(datas, headers, "Assets/allstock_data.xlsx")
    data_processor.SaveToJson(datas, "Assets/allstock_data.json")
    data_processor.SaveTosql(datas, headers, enginstr, f"{formatted}-allstock")
    pushover(key,token,"全局股票数据获取完成")


# 获取所有股票数据
def getAllStock(key,token,pushover,enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    get_allstock_data(key,token,pushover,driver, enginstr)


# =========================================


# 从数据库中获取所有股票数据并返回
async def checkAllStock(table, value, start, end_single, end_total, enginestr):
    yf.pdr_override()
    # 获取某个表格的所有数据
    datas = data_processor.GetAllStockCode(table, value, enginestr)
    outDatas = []
    index = 0
    for stockNum in datas:
        # 从前1000支股票开始选取
        if index >= 100:
            print("get table data complete")
            break

        lastcode = getStockSuffix(stockNum)
        # 北证暂时不处理
        if lastcode == "":
            print(f"{stockNum} is not in sh,sz")
            continue
        code = stockNum + lastcode
        await asyncio.sleep(delay_time)  # 等待30秒，防止触发网站反爬机制
        # stockBaseData = await pdr.get_data_yahoo(code, start)
        stockBaseData = await asyncio.to_thread(
            pdr.get_data_yahoo, code, start, end_single
        )
        # Calculate daily returns
        daily_returns = stockBaseData.pct_change().dropna()
        print(f"{daily_returns}")
        # print(stockBaseData)
        stockBaseData[value] = stockNum
        # 某一个股票的单位时间内的所有数据
        rowDatas = []
        for date, row in stockBaseData.iterrows():
            open_value = row["Open"]
            high_value = row["High"]
            low_value = row["Low"]
            close_value = row["Close"]
            adj_close_value = row["Adj Close"]
            volume_value = row["Volume"]
            stockNum = row["代码"]
            rowDatas.append(
                [
                    date,
                    open_value,
                    high_value,
                    low_value,
                    close_value,
                    adj_close_value,
                    volume_value,
                    stockNum,
                ]
            )
        _stockData = pd.DataFrame(
            rowDatas,
            columns=[
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Adj Close",
                "Volume",
                "代码",
            ],
        )
        # 低于5年的股票剔除
        closevalue_len = len(_stockData["Close"].tolist())
        if closevalue_len < 250 * 5:
            print(f"{stockNum},close value len is {closevalue_len}, too short")
            continue
        print(f"{stockNum},close value len is {closevalue_len}")
        print(f"股票索引{index}")
        index += 1
        outDatas.append(_stockData)
    return outDatas