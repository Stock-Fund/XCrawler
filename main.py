
import sys
import os
from PyQt6 import QtWebEngineWidgets
from PyQt6.QtWidgets import QWidget,QApplication,QSizePolicy
from PyQt6.QtGui import QIcon,QGuiApplication  # 导入引用图标的函数
from PyQt6.QtCore import QUrl,QPoint
from selenium import webdriver
import src

def main():

    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), './Assets/star.png')
    app.setWindowIcon(QIcon(path))
    
    window = Window()   
    window.show()
    
    ## todo use js code crawling web data
    # src.crawler.try_start()
    # # label
    # label = QLabel('Hello World!')
    # label.show()

    # # window
    # w = QWidget()
    # w.resize(250, 200)
    # # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()

    sys.exit(app.exec())



class Window(QWidget):
    def __init__(self):
        super().__init__()  # 用于访问父类的方法和属性

        self.setGeometry(200, 200, 800, 480)  # 设置初始位置与窗口大小
        self.setWindowTitle("A股爬虫")  # 设置标题
        self.setStyleSheet('background-color:green')  # 设置窗口内背景颜色
        # self.setWindowOpacity(0.5)  # 设置窗口透明度
        # self.setFixedWidth(700)  # 不生效，被禁用了
        # self.setFixedHeight(400)  # 不生效，被禁用了
        self.ui()
        self.center()
        self.resizeEvent = self.handleResize

    def ui(self):
         self.widget = QtWebEngineWidgets.QWebEngineView(self)
         self.widget.move(0,0)
         self.widget.resize(self.width(), self.height())
         self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
         self.widget.loadFinished.connect(self.handle_load_finished)
         self.widget.load(QUrl('https://www.zhihu.com/question/51359754/answer/3024289861'))
    
    def center(self)    :
        screen = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move(QPoint((screen.width() - size.width())>>1,
                  (screen.height() - size.height())>>1))
        
    def handleResize(self, event):
        # 调整视图大小
        self.widget.resize(self.width(), self.height())

    # 槽函数
    def handle_load_finished(self):
        # frame = self.view.page().mainFrame()
        # html = frame.toHtml()
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.zhihu.com/question/51359754/answer/3024289861')
        self.driver.implicitly_wait(2)
        soup = src.html.BeautifulSoup(self.driver.page_source,'lxml')
        
    #     table = soup.select('table.zjl1')
    #     logo = soup.select('a.logolink2')
    #   # soup find all方式寻找效率低些，但基于递归的数据用find_all就比较合适
    #   # table = soup.find_all('table',class_='zjl1')
    #   # logo = soup.find_all('a',class_='logolink2')
    #   # 线上抓图，识图
    #     for a_tag in logo:
    #   #    text = a_tag.text  # 获取<a>标签内的文本内容
    #        href = a_tag['href']  # 获取<a>标签的href属性值
    #   #    print(f"文本内容: {text}")
    #        print(f"链接地址: {href}")
    #        img_tag = a_tag.find('img')
    #        if img_tag:
    #            img_src = img_tag['src']
    #            img_alt = img_tag['alt']
    #            print(f"图片地址: {img_src}")
    #            print(f"图片描述: {img_alt}")
    #            img_url = src.html.urljoin("http://quote.eastmoney.com", img_src)
    #            print(f"原始图片地址: {img_url}")
    #             # 发送GET请求下载图片
    #            img_response = src.html.requests.get(img_url)

    #            # 使用Image.open打开图片
    #            image = src.html.Image.open(src.html.BytesIO(img_response.content))
    #            image = image.convert('L')
    #            # 设置 pytesseract 参数
    #            custom_config = r'--psm 6 --oem 2'
    #            text = src.html.pytesseract.image_to_string(image,lang='chi_sim',config=custom_config)
    #            print('123:'+text)

    #     datas = []
      
     
    # # 线上抓数据
    #     for ta in table:
    # # print(ta.text)
    #       for body in ta.select('tbody'):
    #           for tr in body.select('tr'):
    #            data = tr.get_text()
    #            datas.append(data)
    #            print(tr.get_text())
    #     datas = list(map(str, datas))
    #    # 写入xlsx title
    #     datas.insert(0, "数据")
    #     src.xlsx.SaveToXlsx(datas,"Assets/data.xlsx")
    #     src.xlsx.SaveToCsv(datas,"Assets/data.csv")
    #     src.xlsx.SaveToJson(datas,"Assets/data.json")

if __name__ == '__main__':
    main()