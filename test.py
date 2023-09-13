from selenium import webdriver
import time
 
driver = webdriver.Chrome()             # 创建Chrome对象
driver.get('https://www.baidu.com')     # 访问百度.
time.sleep(200)   #两秒后关闭
driver.quit()