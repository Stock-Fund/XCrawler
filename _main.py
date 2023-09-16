# from requests_html import HTMLSession

# session=HTMLSession()

# url=session.get('http://quote.eastmoney.com/zs000001.html')
# title = url.html.find('#app > div > div > div.quote3l > div.quote3l_r > div:nth-child(1) > div.sidertabbox_c.false > div > table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(1)',first = True)
# content = url.html.find('#app > div > div > div.quote3l > div.quote3l_r > div:nth-child(1) > div.sidertabbox_c.false > div > table:nth-child(1) > tbody > tr:nth-child(1) > td.tar',first =True)
# div = content.find('div')
# p = div.find('class')
# span = p.find('span')
# print(span)
# print(content)
# print(title.text)
# session.close()

from lxml import etree
import requests
url = 'http://quote.eastmoney.com/zs000001.html'
response = requests.get(url)
response.encoding=response.apparent_encoding
label=etree.HTML(response.text)
#提取这个页面中所有的标签信息
content=label.xpath('//span[@class="price_up"]/text()')
#提取span标签中class名为"price_up"的内容信息,并且存入一个列表中
print(content[0])