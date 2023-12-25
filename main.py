import sys
import os
from PyQt6 import QtWebEngineWidgets
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QSizePolicy
from PyQt6.QtGui import QIcon, QGuiApplication  # 导入引用图标的函数
from PyQt6.QtCore import QUrl, QPoint
from selenium import webdriver
import pymysql
import src
import talib
import numpy as np


def main():
    app = QApplication(sys.argv)
    path = os.path.join(
        os.path.dirname(sys.modules[__name__].__file__), "./Assets/star.png"
    )
    app.setWindowIcon(QIcon(path))
    # 读取本地账号密码
    with open("./Assets/password.txt", "r") as file:
        lines = file.readlines()
    # 解析键值对
    credentials = {}
    for line in lines:
        key, value = line.strip().split(":")
        credentials[key] = value
    # 启动数据库
    conn = pymysql.connect(
        host=credentials.get("host"),
        user=credentials.get("user"),
        password=credentials.get("password"),
        db=credentials.get("db"),
        charset="utf8",
    )

    window = Window()
    window.show()

    ## todo use js code crawling web data

    sys.exit(app.exec())


class Window(QWidget):
    def button_clicked(self):
        src.start()

    def button_Allclicked(self):
        src.getAllStock()

    def button_check(self):
        src.check()

    def button_find(self, stockNum):
        src.find(stockNum)

    def on_text_changed(self, text):
        self.inputText = text
        # print("输入的文字:", text)

    def __init__(self):
        super().__init__()  # 用于访问父类的方法和属性
        self.setGeometry(200, 200, 800, 480)  # 设置初始位置与窗口大小
        self.setWindowTitle("散户救星")  # 设置标题
        self.setStyleSheet("background-color:green")  # 设置窗口内背景颜色
        layout = QtWidgets.QVBoxLayout()
        # self.setWindowOpacity(0.5)  # 设置窗口透明度
        # self.setFixedWidth(700)  # 不生效，被禁用了
        # self.setFixedHeight(400)  # 不生效，被禁用了
        self.ui()
        # 爬取数据按钮
        xcrawlerBtn = QtWidgets.QPushButton("button", self)
        xcrawlerBtn.setText("抓取")
        xcrawlerBtn.clicked.connect(lambda: self.button_clicked())

        xcrawlerAllBtn = QtWidgets.QPushButton("button", self)
        xcrawlerAllBtn.setText("全局抓取")
        xcrawlerAllBtn.clicked.connect(lambda: self.button_Allclicked())
        xcrawlerAllBtn.move(300, 0)

        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("请输入")
        # 限制输入15个字符
        self.input.setMaxLength(15)
        self.input.setFixedSize(200, 30)
        self.input.textChanged.connect(self.on_text_changed)
        findBtn = QtWidgets.QPushButton("button", self)
        findBtn.setText("查询")
        findBtn.clicked.connect(lambda: self.button_find(self.inputText))
        findBtn.move(100, 0)

        checkBtn = QtWidgets.QPushButton("button", self)
        checkBtn.setText("检测")
        checkBtn.clicked.connect(lambda: self.button_check())
        checkBtn.move(200, 0)

        layout.addWidget(self.input)
        self.setLayout(layout)
        self.center()
        self.resizeEvent = self.handleResize

    def ui(self):
        self.widget = QtWebEngineWidgets.QWebEngineView(self)
        self.widget.move(0, 0)
        self.widget.resize(self.width(), self.height())
        self.widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.widget.loadFinished.connect(self.handle_load_finished)
        self.widget.load(QUrl("http://quote.eastmoney.com/zs000001.html"))

    def center(self):
        screen = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move(
            QPoint(
                (screen.width() - size.width()) >> 1,
                (screen.height() - size.height()) >> 1,
            )
        )

    def handleResize(self, event):
        # 调整视图大小
        self.widget.resize(self.width(), self.height())

    # 槽函数
    def handle_load_finished(self):
        src.try_start()


if __name__ == "__main__":
    main()
