import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication
 
 
class Example(QMainWindow):
 
    def __init__(self):
        super().__init__()
 
        self.initUI()
 
 
    def initUI(self):
 
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)
 
        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)
 
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
 
        self.statusBar()
 
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Event sender')
        self.show()
 
 
    def buttonClicked(self):
 
        sender = self.sender()
 
        msg = f'{sender.text()} was pressed'
        self.statusBar().showMessage(msg)
 
 
def main():
 
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
 
 
if __name__ == '__main__':
    main()