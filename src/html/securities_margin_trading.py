import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# 融资融券交易数据爬取
# https://data.eastmoney.com/rzrq/total.html 全局全量融资融券数据
# https://data.eastmoney.com/rzrq/detail/all.html 个股融资融券数据


def xcrawlerMarginData(soup):
    div_element = soup.find("div", id="rzrq_detail_table")
    table_element = div_element.find("table", class_="table-model")
    thead_element = table_element.find("thead")
    tbody_element = table_element.find("tbody")
    # header
    headers = []
    headers_1 = []
    headIndex = 0
    index = 0
    for tr in thead_element.find_all("tr"):
        index = 0
        for th in tr.find_all("th"):
            data = th.get_text()
            if headIndex == 0:
                if index >= 6 and index <= 9:
                    headers_1.append(data)
                else:
                    headers.append(data)
            elif headIndex == 1:
                if index >= 0 and index <= 4:
                    prestr = headers_1[0]
                elif index >= 5:
                    prestr = headers_1[1]
                headers.append(f"{prestr}:{data}")
            index += 1
        headIndex += 1
    headers.append(headers_1[2])
    headers.append(headers_1[3])

    # body
    datas = []
    for tr in tbody_element.find_all("tr"):
        for td in tr.find_all("td"):
            data = td.get_text()
            datas.append(data)
    datas = list(map(str, datas))
    headers = list(map(str, headers))
    print(datas)
    return datas, headers


def get_margin_data(driver, url, now, enginstr):
    formatted = now.strftime("%Y-%m-%d")
    driver.get(url)
    driver.implicitly_wait(30)
    index = 1
    datas = []
    headers = []
    while True:
        soup = BeautifulSoup(driver.page_source, "lxml")
        _datas, _headers = xcrawlerMarginData(soup)
        datas.extend(_datas)
        if index == 1:
            headers.extend(_headers)
        print(f"第{index}页融资融券数据获取完成")
        # try:
        next_page = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//a[text()='下一页']",
                    )
                )
            )
        # except (StaleElementReferenceException, TimeoutException) as e:
        #     print("页面加载超时或元素未找到:", e)
        #     break
        # except Exception as e:
        #     print("发生异常:", e)
        #     break
        if next_page:
            try:
                # 点击按钮
                next_page.click()
            except StaleElementReferenceException:
                print("最后一页加载超时!")
                continue

            # 增加延时，模拟人类操作间隔
            time.sleep(8)  # 可根据实际情况调整延时时间
            # 等待页面加载完成
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='rzrq_detail_table']")
                )
            )
            index += 1
        else:
            print("数据获取完成")
            break


# 获取融资融券交易明细
def getmargindata(url, now, enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    get_margin_data(driver, url, now, enginstr)


# ==================================================


def get_margin_total_data(driver, url, now, enginstr):
    formatted = now.strftime("%Y-%m-%d")
    driver.get(url)
    driver.implicitly_wait(30)
    soup = BeautifulSoup(driver.page_source, "lxml")
    div_element = soup.find("div", id="rzrq_history_table")


# 获取融资融券交易总量
def getmargintotaldata(url, now, enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    get_margin_total_data(driver, url, now, enginstr)
