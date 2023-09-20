
def main():

    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), './Assets/face.jpeg')
    app.setWindowIcon(QIcon(path))
    window = Window()
    window.show()

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

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon  # 导入引用图标的函数
class Window(QWidget):
    def __init__(self):
        super().__init__()  # 用于访问父类的方法和属性

        self.setGeometry(200, 200, 700, 400)  # 设置初始位置与窗口大小
        self.setWindowTitle("主页")  # 设置标题
        self.setStyleSheet('background-color:green')  # 设置窗口内背景颜色
        self.setWindowOpacity(0.5)  # 设置窗口透明度
        # self.setFixedWidth(700)  # 不生效，被禁用了
        # self.setFixedHeight(400)  # 不生效，被禁用了

if __name__ == '__main__':
    main()