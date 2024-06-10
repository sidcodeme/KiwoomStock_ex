import sys
from PyQt5 import uic 
from PyQt5.QtWidgets import QApplication, QMainWindow


#form_class = uic.loadUiType("./test.ui")[0]

form_ui_class = uic.loadUiType("./ui/stock.ui")[0]
# 코스피 : 0,  코스탁 : 10
KOSPI_CODE = '0'
KOSDAQ_CODE = '10'

class MainWindow(QMainWindow, form_ui_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("sidcode`s Stock (Will Ai)")  
        