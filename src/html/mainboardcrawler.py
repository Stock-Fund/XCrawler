from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import src.data_processor as data_processor


def get_Data_FromSoup(soup):
    headers = []
    datas = []
    table_element = soup.select_one("table#table_wrapper-table.table_wrapper-table")

    now = datetime.datetime.now()
    # 格式化为字符串
    formatted = now.strftime("%Y-%m-%d")
    tr_elements = soup.select("tr[role='row']")
    for tr_element in tr_elements:
        th_elements = tr_element.find_all("th")
        for th_element in th_elements:
            data = th_element.get_text()
            if len(data) != 0 and data != "加自选":
                headers.append(data)
                if data == "市净率":
                    # 给时间表插入时间列
                    headers.append("日期")
    max = len(headers)
    for body in table_element.select("tbody"):
        for tr in body.select("tr"):
            index = 1
            for td in tr.select("td"):
                data1 = td.get_text()
                if len(data1) != 0:
                    index += 1
                    datas.append(data1)
                    if index == max:
                        datas.append(formatted)
    datas = list(map(str, datas))
    headers = list(map(str, headers))
    return datas, headers


def get_Mainboard_data(driver, url, enginstr):
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, "lxml")

    datas, headers = get_Data_FromSoup(soup)
    data_processor.SaveToCsv(datas, headers, "Assets/sh_data.csv")
    data_processor.SaveToXlsx(datas, headers, "Assets/sh_data.xlsx")
    data_processor.SaveToJson(datas, "Assets/sh_data.json")

    # 已mysql为例,如果已localhost为host,那port端口一般为3306
    # enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stock"
    data_processor.SaveTosql(datas, headers, enginstr, "stock")
    print("上证主板前十股票数据 crawle completed")
    return soup


# 爬取上证交易所股票
def getSHBoard(url, enginstr):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    # options.add_argument('--disable-tabs')
    driver = webdriver.Chrome(options=options)
    #    url = "http://quote.eastmoney.com/center/gridlist.html#sh_a_board"
    # while True:
    get_Mainboard_data(driver, url, enginstr)
    #  time.sleep(10)
