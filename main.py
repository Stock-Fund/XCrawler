
import sys
import os
from PyQt6 import QtWebEngineWidgets
from PyQt6.QtWidgets import QWidget,QApplication,QSizePolicy
from PyQt6.QtGui import QIcon,QGuiApplication  # 导入引用图标的函数
from PyQt6.QtCore import QUrl,QPoint
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
         self.widget.load(QUrl('https://google.com'))
    
    def center(self)    :
        screen = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move(QPoint((screen.width() - size.width())>>1,
                  (screen.height() - size.height())>>1))
        
    def handleResize(self, event):
        # 调整视图大小
        self.widget.resize(self.width(), self.height())

if __name__ == '__main__':
    main()