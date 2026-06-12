from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class ChildWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('子窗口')
        self.resize(280, 230)


class FatherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('TestWindow')
        self.resize(400, 300)

        self.btn = QPushButton('打开新窗口', self)
        self.btn.clicked.connect(self.btnClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)

        self.show()

    def btnClicked(self):
        self.chile_Win = ChildWindow()
        self.chile_Win.show()
        self.chile_Win.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建主窗口
    window = FatherWindow()
    # 显示窗口
    window.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())

