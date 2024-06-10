
import sys
from PyQt5.QtWidgets import QApplication

from kiwoom_controller.kiwoom_controller import KiwoomController
from mainwindow.mainwindow import MainWindow
import logging as log

log.basicConfig(filename="log/log.log", level=log.DEBUG, format='[%(levelname)s][%(asctime)s]:[%(funcName)s]:%(message)s', datefmt ='%m/%d %I:%M:%S %p')

''' 
    키움 컨트롤러 모듈 로드  
'''
kiwoom_controller = KiwoomController() 


 