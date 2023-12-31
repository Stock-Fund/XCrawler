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

# A股所有股票页面
url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"


def xcrawlerStockData(soup):
    datas, headers = get_Data_FromSoup(soup)
    return datas, headers


def get_allstock_data(driver, enginstr):
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
        print(f"第{index}页完成")
        try:
            next_button = WebDriverWait(driver, 10).until(
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
            time.sleep(8)  # 可根据实际情况调整延时时间
            # 等待页面加载完成
            WebDriverWait(driver, 30).until(
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


def getAllStock(enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    get_allstock_data(driver, enginstr)
