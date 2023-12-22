
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
# A股所有股票页面
url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"


def get_allstock_data(driver):
    driver.get(url)
    driver.implicitly_wait(30)
    soup = BeautifulSoup(driver.page_source,'lxml')
    # next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='next paginate_button']")))
    while True:
        try:
           next_button = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//a[@class='next paginate_button']")))
           # todo xcrawler data
           # 判断是否包含disabled类
        except StaleElementReferenceException:
           print("页面加载超时!")
           continue
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
            # 等待页面加载完成
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='listview full']")))
            print("切页完成")

    # driver.find_element_by_xpath("//a[@href='/stockdata/']").click()
    # driver.implicitly_wait(10)
    # driver.find_element_by_xpath("//a[@href='/stockdata/']").click()
    # driver.implicitly_wait(10)

def getAllStock():
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   driver = webdriver.Chrome(options = options)
   get_allstock_data(driver)