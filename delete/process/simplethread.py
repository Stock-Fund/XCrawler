# simplethread.py
import src.process

class SimpleThread:

  def __init__(self, urls):
    self.urls = urls

  def get_page(self, url):
    response = src.process.requests.get(url)
    soup = src.process.BeautifulSoup(response.text, 'html.parser')  
    title = soup.select_one('title').text
    # print(title)  

  def run(self):  
    threads = []
    for url in self.urls:
      t = src.process.threading.Thread(target=self.get_page, args=(url,))
      threads.append(t)
      t.start()
      
    for t in threads:
      t.join()