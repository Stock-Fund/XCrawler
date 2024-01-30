import sys
import os
from PyQt6 import QtWebEngineWidgets
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QSizePolicy, QSlider, QLabel
from PyQt6.QtGui import QIcon, QGuiApplication  # 导入引用图标的函数
from PyQt6.QtCore import QUrl, QPoint, Qt
from selenium import webdriver
import pymysql
import src
import talib
import numpy as np
from datetime import datetime


def main():
    app = QApplication(sys.argv)
    path = os.path.join(
        os.path.dirname(sys.modules[__name__].__file__), "./Assets/bullmarket.jpg"
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

    def button_AllMarginclicked(self):
        src.getMarginAllData()

    def button_showStockData(self, stockNum):
        src.showStockData(stockNum)

    def button_check(self):
        if len(self.inputText) == 0:
            src.check()
        else:
            date_string = "2023-12-01 15:00:00"
            date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            src.check([self.inputText], self.ma, date_object)

    def button_filter(self):
        src.filter()

    def button_find(self, stockNum):
        if len(self.inputText) == 0:
            print("请输入股票代码")
            return
        src.find(stockNum, self.ma)

    # 输入框事件
    def on_text_changed(self, text):
        self.inputText = text
        # print("输入的文字:", text)

    # 滑块事件
    def slider_value_changed(self, value):
        selected_value = self.tick_values[value]
        self.ma = selected_value
        self.label.setText(f"{self.ma}日 均线值")

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
        # ============== 第一排按钮
        # 爬取数据按钮
        xcrawlerBtn = QtWidgets.QPushButton("button", self)
        xcrawlerBtn.setText("自选股票数据")
        xcrawlerBtn.clicked.connect(lambda: self.button_clicked())

        xcrawlerAllBtn = QtWidgets.QPushButton("button", self)
        xcrawlerAllBtn.setText("全局股票数据")
        xcrawlerAllBtn.clicked.connect(lambda: self.button_Allclicked())
        xcrawlerAllBtn.move(100, 0)

        marginAllBtn = QtWidgets.QPushButton("button", self)
        marginAllBtn.setText("全局融资融券数据")
        marginAllBtn.clicked.connect(lambda: self.button_AllMarginclicked())
        marginAllBtn.move(200, 0)

        # ============== 第四排输入框
        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("请输入股票代码")
        self.inputText = ""
        # 限制输入15个字符
        self.input.setMaxLength(15)
        self.input.setFixedSize(200, 30)
        self.input.textChanged.connect(self.on_text_changed)
        self.input.move(300, 200)
        # ============== 第二排按钮
        findBtn = QtWidgets.QPushButton("button", self)
        findBtn.setText("查询股票数据")
        findBtn.clicked.connect(lambda: self.button_find(self.inputText))
        findBtn.move(0, 100)

        showDataBtn = QtWidgets.QPushButton("button", self)
        showDataBtn.setText("显示股票数据")
        showDataBtn.clicked.connect(lambda: self.button_showStockData(self.inputText))
        showDataBtn.move(100, 100)

        checkBtn = QtWidgets.QPushButton("button", self)
        checkBtn.setText("股票条件检测")
        checkBtn.clicked.connect(lambda: self.button_check())
        checkBtn.move(200, 100)

        filterBtn = QtWidgets.QPushButton("button", self)
        filterBtn.setText("全局筛选")
        filterBtn.clicked.connect(lambda: self.button_filter())
        filterBtn.move(300, 100)

        # ============== 第三排文本
        # 滑块选择N日周期，判断是否上穿/下穿对应周期的均线
        self.ma = 5
        self.label = QLabel(f"{self.ma}日 均线值", self)
        # 设置标签的尺寸
        # self.label.setMinimumSize(200, 30)

        self.slider = QtWidgets.QSlider(Qt.Orientation.Horizontal, self)
        # 设置滑块的尺寸
        self.slider.setMinimumSize(200, 30)
        self.slider.setMinimum(0)
        self.slider.setMaximum(5)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        # 设置刻度标签的显示格式
        self.tick_values = [5, 10, 20, 30, 40, 60]
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider_value_changed(0)

        self.label.move(5, 150)
        self.slider.move(0, 200)

        # layout.addWidget(self.input)
        # layout.addWidget(self.slider)
        # layout.addWidget(self.label)
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
