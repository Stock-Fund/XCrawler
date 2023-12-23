import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# A股所有股票页面
url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"


def xcrawlerStockData(soup):
    print("开始爬取数据")


def get_allstock_data(driver):
    driver.get(url)
    driver.implicitly_wait(30)

    # next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='next paginate_button']")))
    index = 1
    while True:
       
        soup = BeautifulSoup(driver.page_source, "lxml")
        xcrawlerStockData(soup)
        print(f"第{index}页完成")
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@class='next paginate_button']")
                )
            )
        except (StaleElementReferenceException, TimeoutException) as e:
            print("页面加载超时或元素未找到:", e)
            break
        except Exception as e:
            print("发生异常:", e)
            break
      #   # 判断是否包含disabled类
      #   if "disabled" in next_button.get_attribute("class"):
      #       print("已经是最后一页!")
      #       break
      #   else:
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

    # driver.find_element_by_xpath("//a[@href='/stockdata/']").click()
    # driver.implicitly_wait(10)
    # driver.find_element_by_xpath("//a[@href='/stockdata/']").click()
    # driver.implicitly_wait(10)


def getAllStock():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    get_allstock_data(driver)
