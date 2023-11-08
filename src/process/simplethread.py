# simplethread.py
import requests
from bs4 import BeautifulSoup
import threading

class SimpleThread:

  def __init__(self, urls):
    self.urls = urls

  def get_page(self, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')  
    title = soup.select_one('title').text
    print(title)  

  def run(self):  
    threads = []
    for url in self.urls:
      t = threading.Thread(target=self.get_page, args=(url,))
      threads.append(t)
      t.start()
      
    for t in threads:
      t.join()