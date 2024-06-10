''' 
    상위 폴더 의 모듈 가져오기위함 ==================================
'''
import os
import sys

from PyQt5 import QtGui

from util.made_price import *



sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

'''   =====================================  '''

from db.db_helper import *
import datetime
import time
from util.enc_dec import my_decrypt
import pythoncom
from api.kiwoom import Kiwoom
from mainwindow.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from util.const import *
import logging as log
import pandas as pd
import threading

class KiwoomController():
    """
        UI창을 띄우기 위함
    """
    app = QApplication(sys.argv)
    # 코스피 : 0,  코스탁 : 10
    KOSPI_CODE = '0'
    KOSDAQ_CODE = '10'
    
    SELL_WIN_RATE  = 0   # 익절치
    SELL_LOSE_RATE = 0 # 손절
    
    def __init__(self):
        super().__init__()
        
        '''
            변수 
        '''
        self.add_real_reg    = 0   # 실시간 등록 ( 최초등록시 0, 추가 등록할경우 1로 취환(추가 등록 후 전체 실시간 원할경우 1))
        self.sid_money       = 0   # 예수금        
        self.per_val         = 1   # PER 정보 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE 
        self.target_code     = ""  # 대상 종목 선택된 코드
        self.order_code      = ""  # 주문 종목코드
        self.order_code_name = ""  # 주문 종목명
        
        self.reald_data_on           = False # 실시간 데이터  초기값
        self.connected               = False # 로그인 대기
        self.recive                  = False # TR데이터 대기
        self.has_next_tr_date        = False # tr_data 연속성 여부
        self.get_company_name_loaded = False # 종목명 대기 
        self.today = datetime.datetime.today().strftime("%Y%m%d") # 오늘날짜 20211119
        
        self.tr_data                    = {} # tr 응답 데이타
        self.get_today_order_stock_dict = {} # 오늘 대상 종목 코드 받아오기
        self.order                      = {} # 종목 코드를 키 값으로 해당 종목의 주문 정보를 담은 딕셔너리
        self.balance                    = {} # 종목 코드를 키 값으로 해당 종목의 매수 정보를 담은 딕셔너리
        
        ''' 
            키움 모듈 로드 및 시그널 슬롯 
        '''
        self.kiwoom = Kiwoom()          # 키움 API 상속
        self._set_kiwoom_signal_slots() # 키움 시그널 처리 
        
        '''로그인'''
        self._comm_connect()      # 로그인
        
        # '''  
        #     UI 로드 및 시그널  설정
        self.main_window = MainWindow() # UI 상속
        
        # 시그널 슬롯 구현 불가로 아래  시그널 리스닝
        '''tab1'''
        self.main_window.tb1_tableWidget_stock_target_info_list01.cellClicked.connect(self.get_tb1_tableWidget_stock_target_info_code) # TAB1.대상종목 선택시 대상 종목 코드 가져옴
        self.main_window.tb1_pushButton_stock_auto_order_start.clicked.connect(self.get_send_auto_order_buy)                           # TAB1.종목 자동 매수 주문          
        self.main_window.tb1_pushButton_stock_auto_sell_order_start.clicked.connect(self.get_deposit)                                  # TAB1.예수금 가져오기        
        self.main_window.tb1_textEdit_sell_win_lose_save.clicked.connect(self.get_sell_win_lose_save)                                  # TAB1.매매기준퍼센트저장
        self.main_window.tb1_pushButton_stock_searh_handle.clicked.connect(self.get_search_where_code)                                 # TAB1.대상 종목 목록 재조회
        
        
        '''tab2'''
        self.main_window.tb2_pushButton_stock_balance_info.clicked.connect(self.get_stock_balance_info)  # TAB2.보유잔고 관련 정보
        
        '''tab3'''
    
    
    
        '''
            로그인 완료 후 기본 호출 정보
        '''
        self._base_load_info() # 계좌정보        


  

            
    '''
        ===================================================================================
        100.Kiwoom 시그널 처리 
        ===================================================================================
    '''           
    def _set_kiwoom_signal_slots(self):
        self.kiwoom.OnEventConnect.connect(self._login_event_connect)               # login_event_connect 로그인 이벤트 처리 
        self.kiwoom.OnReceiveTrData.connect(self._on_receive_tr_data)               # CommRqData 전문 송수신 처리
        self.kiwoom.OnReceiveMsg.connect(self._on_receive_msg)                      # 수신 메시지 이벤트
        self.kiwoom.OnReceiveChejanData.connect(self._on_receive_chejan_data)       # 주문 접수/확인 수신시 이벤트
        self.kiwoom.OnReceiveRealData.connect(self._on_receive_real_data)           # 실시간데이터를 받은 시점을 알려준다.
        self.kiwoom.OnReceiveConditionVer.connect(self._on_receive_condition_ver)   # 서버에 저장된 조건식 처리 
        self.kiwoom.OnReceiveTrCondition.connect(self._on_receive_tr_condition_ver) # 서버에 저장된 조건식 처리 
        
      
      
      
         
    '''
        ===================================================================================
        105. Thread 처리 구간
        ===================================================================================
    '''       
    def call_sell_sign(self) :
        """
            자동 매도 사인 체크후 매도 
        """
        print(" 자동 매도 사인 체크후 매도 작동중.....")
        
        while True :
            result = get_call_sell_sign_point_info()
            for code, quantity in result :
                print(f"자동매도 대상 ==> {result}")
                print(f"자동매도 종목코드 ====> {code}")
                # 응답 대기
                self.recive = False
                
                self.get_send_auto_order_point_sell(code, quantity)
                
                # # 처리 될 동안 대기
                # while not self.recive :
                #     pythoncom.PumpWaitingMessages()  
                
            time.sleep(1)
            
    def call_auto_buy(self) :
        """
            잔고 매수 건수 체크후 자동 매수
        """
        print(" 잔고 매수 건수 체크후 자동 매수 작동중.....")
        
        while True :
            sell_cnt = get_call_sell_count_info()
            # print(f"sell_cnt ==> {sell_cnt}")
            sell_cnt = int(sell_cnt[0][0])
            
            if sell_cnt < 1 :
                print(f"현재 매수 잔고 건수 ==> {sell_cnt} 으로 추가 5종목 매수 시도.")
                # '''매수 항목이없으면 다시 읽어오기'''    
                # self.get_search_where_code()
                self.get_send_auto_order_buy()
                    
                print(" 자동 매수 데몬 작동중.....")
    
            time.sleep(5)
            
            
            
    # def call_auto_money_info(self) :
    #     """
    #         예수금  데몬 호출
    #     """
    #     print(" 예수금 데몬 호출 작동중.....")
        
    #     while True :
    #         self.get_deposit()                 # 예수금 가져오기
    #         # self.get_stock_balance_info()      # 보유잔고 관련 정보

    #         time.sleep(5)
            
            
    # def call_auto_balance_stock_info(self) :
    #     """
    #         잔고 데몬 호출
    #     """
    #     print(" 잔고 데몬 호출 작동중.....")
        
    #     while True :
    #         self.get_stock_balance_info()      # 보유잔고 관련 정보

    #         time.sleep(5)
         
         
         
         
         
         
         
    '''
        ===================================================================================
        110.Kiwoom 로그인 처리 
        ===================================================================================
    '''       
    def _comm_connect(self):
        self.kiwoom.comm_connect()      # 로그인
        # 응답 완료 여부
        self.connected = False
        # 처리 될 동안 대기
        while not self.connected:
            pythoncom.PumpWaitingMessages()
            
            
          
    def _base_load_info(self):
        '''
            로그인 완료 후 기본 호출 정보
        '''
        self.main_window.label_login_info.setText("로그인 성공" if self.connected else "로그인 실패")
        self.get_account_number()          # 계좌정보
        self.get_server_zone()             # 서버 정보
        self.get_search_where_code()       # 조건 검색 후 조건 검색 조회된 데이터 가져오기
        self.get_deposit()                 # 예수금 가져오기
        self.get_stock_balance_info()      # 보유잔고 관련 정보
        self.get_stock_real_balance_info() # 보유종목 실시간 정보처리
        
        
        self.main_window_show()           # UI 로드
        
        ''' 자동 매도 사인 체크 및 매도 처리할 데몬 호출 '''
        call_sell_sign_run = threading.Thread(target=self.call_sell_sign, name="call_sell_sign", args=())
        call_sell_sign_run.daemon = True
        call_sell_sign_run.start()     
        
        ''' 잔고 매수 건수 체크후 자동 매수 처리할 데몬 호출 '''
        call_auto_buy_run = threading.Thread(target=self.call_auto_buy, name="call_auto_buy", args=())
        call_auto_buy_run.daemon = True
        call_auto_buy_run.start()     
        
        # ''' 예수금 데몬 호출 '''
        # call_auto_buy_run = threading.Thread(target=self.call_auto_money_info, name="call_auto_money_info", args=())
        # call_auto_buy_run.daemon = True
        # call_auto_buy_run.start()     
        
        # ''' 잔고 데몬 호출 '''
        # call_auto_buy_run = threading.Thread(target=self.call_auto_balance_stock_info, name="call_auto_balance_stock_info", args=())
        # call_auto_buy_run.daemon = True
        # call_auto_buy_run.start()     
              
        self.app.exec_()  

        
        
        
        
        
        
    def _login_event_connect(self, error_code):
        '''
            로그인 커넥션 이벤트 응답 처리
        '''        
        if error_code == 0 :
            self.connected = True

        log.info("로그인 성공" if self.connected else "로그인 실패")
        
      
    def main_window_show(self):
        ''' 
            화면 UI 실행
        '''
        self.main_window.show()
        
        # self.app.exec_()  

    '''
        ===================================================================================
        120.기본 정보 처리 라인
        ===================================================================================
    '''   
    def get_account_number(self):
        '''
            계좌번호 
        '''    
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_cust_nm = self.kiwoom.get_login_info("USER_NAME")
        log.info(account_cust_nm)
        log.info(account_number)
        
        self.account_number = account_number

        account_name_number = []
        for acc_no in account_number:
            account_name_number.append(account_cust_nm + " : " + acc_no)
            log.info(account_name_number)

        self.main_window.comboBox_account_info.addItems(account_name_number)
        
    def get_server_zone(self):
        '''
            서버구분
        '''
        server_zone = self.kiwoom.get_server_zone()
        log.info(server_zone)
        self.main_window.statusbar.showMessage(server_zone)

    '''
        ===================================================================================
        150. 실시간 정보 관련
        ===================================================================================
    ''' 
    def set_real_reg(self, strScreenNo, strCodeList, strFidList):
        """
            종목별 실시간 등록
            - param
                - strScreenNo : 실시간 등록할 화면 번호
                - strCodeList : 실시간 등록할 종목코드(복수종목가능 – “종목1;종목2;종목3;….”)
                - strFidList  : 실시간 등록할 FID(“FID1;FID2;FID3;…..”)
                
                - strRealType : “0”, “1” 타입  "self.add_real_reg" 대체 사용
                
            - Descript
              - 
                    strRealType이 “0” 으로 하면 같은화면에서 다른종목 코드로 실시간 등록을 하게 되면 마지막
                    에 사용한 종목코드만 실시간 등록이 되고 기존에 있던 종목은 실시간이 자동 해지됨.
                    “1”로 하면 같은화면에서 다른 종목들을 추가하게 되면 기존에 등록한 종목도 함께 실시간 시세
                    를 받을 수 있음.
                    꼭 같은 화면이여야 하고 최초 실시간 등록은 “0”으로 하고 이후부터 “1”로 등록해야함.
                
        """
        if self.reald_data_on :
            print("set_real_reg({} / {} / {})".format(strScreenNo, strCodeList, strFidList))
            
            self.kiwoom.set_real_reg(strScreenNo, strCodeList, strFidList, self.add_real_reg)
            self.add_real_reg = 1 # 최초 등록 0 이 후에 1로 변경아혀 기존 등록도 실시간 동일 처리 되도록 
            # time.sleep(0.5)


        
        
        
    '''
        ===================================================================================
        200.전문 수신 
        ===================================================================================
    ''' 
    
    def _on_receive_msg(self, sScrNo ,sRQName, sTrCode, sMsg):
        """
            서버통신 후 메시지를 받은 시점을 알려준다.
            - param
                - sScrNo  : 화면번호
                - sRQName : 사용자구분 명
                - sTrCode : Tran 명
                - sMsg    : 서버메시지
        """
        print("_on_receive_msg : {} / {} / {} / msg : {}".format(sScrNo ,sRQName, sTrCode, sMsg))
        
        if "22000" == sScrNo and str(sMsg).find("장종료") != -1:
            msg = self.order_code_name + "[" + self.order_code + "]"
            self.main_window.tb1_textBrowser_stock_send_order.append("=======================================")
            self.main_window.tb1_textBrowser_stock_send_order.append(msg)
            self.main_window.tb1_textBrowser_stock_send_order.append("=====> " + sMsg)
            self.main_window.tb1_textBrowser_stock_send_order.append("=======================================")
    
    
    
    # 전문 송신 처리
    def _on_receive_tr_data(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, none_1, none_2, none_3, none_4):
        ''' 
            전문 수신 응답
            - param
                - sScrNo        : 화면번호
                - sRQName       : 사용자 구분 요청 명
                - sTrCode       : Tran 명
                - sRecordName   : Record 명
                - sPreNext      : 연속조회 유무
                - nDataLength   : 1.0.0.1 버전 이후 사용하지 않음.
                - sErrorCode    : 1.0.0.1 버전 이후 사용하지 않음.
                - sMessage      : 1.0.0.1 버전 이후 사용하지 않음.
                - sSplmMsg      : 1.0.0.1 버전 이후 사용하지 않음
        '''
        print("_on_receive_tr_data: {}".format(sRQName))
        tr_cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
        
        res_data = []
        res_data.append(str(sScrNo))
        res_data.append(str(sRQName))
        res_data.append(str(sTrCode))
        res_data.append(str(sRecordName))
        res_data.append(str(sPreNext))
        res_data.append(str(tr_cnt))
        
        self.has_next_tr_date = True if sPreNext == '2' else False
        
        if sRQName == "opt10081_req" :
            '''종목 현재가 검색'''
            self.set_reciv_ohlcv(sTrCode, sRQName, tr_cnt)
            self.opt10081_req(sTrCode, sRQName, tr_cnt)
            
        elif sRQName == "opt10081_get_price_req" :
            '''종목가격전체정보'''
            self.set_reciv_ohlcv(sTrCode, sRQName, tr_cnt)
            
        elif sRQName == "opw00001_req" :
            '''예수금 조회'''
            self.set_parser_diposit(sTrCode, sRQName)        
            
        elif sRQName == "opt10001_req" :
            ''' 주식기본정보요청 '''
            self.opt10001_req(sTrCode, sRQName, tr_cnt)    
                    
        elif sRQName == "send_auto_buy_order" :
            ''' 자동 매수주문 00:지정가'''
            print("매수 : ", res_data)
            
                    
        elif sRQName == "send_auto_sell_order" :
            ''' 자동 매도주문 00:지정가'''
            print("매도 : ", res_data)
            
        elif sRQName == "send_auto_point_sell_order" :
            ''' 자동 매도 신호 매도 주문 '''
            print("자동 매도 신호 매도 주문 : ", res_data)
            
        elif sRQName == "opw00018_req" :
            '''계좌평가잔고  내역요청'''
            self.opw00018_req(sTrCode, sRQName, tr_cnt)        
                                
        self.recive = True
  
        
        
    def _on_receive_chejan_data(self, sGubun, nItemCnt, sFidList):
        """
            체결데이터를 받은 시점을 알려준다.
            - param
               - sGubun   : 체결구분 0 (접수및 체결), 1 (매수하여 잔고로 이동), 2 (매수취소)
               - nItemCnt : 아이템갯수
               - sFidList : 데이터리스트
            - return
                - sGubun   : 0:주문체결통보, 1:잔고통보, 3:특이신호
                - sFidList : 데이터 구분은 ‘;’ 이다.
        """
        print("_on_receive_chejan_data : {} / {} / {}".format(sGubun, nItemCnt, sFidList))
        
        order_list = []   # 주먼 정보
        balance_list = [] # 체결 잔고 정보 
        
        for fid in sFidList.split(";") :
            if fid in FID_CODES :
                code = self.kiwoom.get_chejan_data('9001')[1:] # 9001(종목코드 호출값), 업종코드 [1:] 은 앞에 한글자 영문을 제거하기위함 ( 예 : A005930 )
                data = self.kiwoom.get_chejan_data(fid)        # fid 값 
                data = data.strip().lstrip('+').lstrip('-')    # 데이타에 부호가 붙으면 +(매수), -(매도) 제거
                
                if data.isdigit() : # 수신된 문자형 데이터 중 숫자인 항목을 숫자로 바꿈
                    data = int(data)
                
                # print(data)
                fid_name = FID_CODES[fid] # fid 코드의 항목명 을 가져옴
                # print("{} : {}".format(fid_name, data))    
                log.debug("{} : {}".format(fid_name, data))
                
                order_type_val = str(data)

                # print(f"{fid_name} == 주문구분 and {order_type_val} == 매수취소")
                if int(sGubun) == 0 : # 접수(0) self.order 저장, 체결(1)잔고이동이면 slef.balance에 저장
                    if code not in self.order.keys() : # 코드가 없다면 신규 생성
                        self.order[code] = {}
                
                    self.order[code].update({fid_name: data}) # order 에 저장
                    order_list.append(fid_name + " : " + str(data))
                    
                    # 매수 매도 상태 업데이트 
                    if fid_name == "주문구분" and order_type_val == "매수" : # 매수 
                        ''' 매수 주문 업데이트 '''
                        order_no = self.kiwoom.get_chejan_data('9203')        # 주문번호 가져오기
                        buy_price = 0
                        buy_price = self.kiwoom.get_chejan_data('910')        # 체결가 가져오기
                        buy_price = buy_price.strip().lstrip('+').lstrip('-')
                        get_update_order_buy_last_stock(code, "1", buy_price, order_no) 
                        self.get_deposit()  # 거래 가능 금액조회
                        # print(f"매수 주문 가 ===> {buy_price}")
                        
                    elif  fid_name == "주문구분" and order_type_val == "매도" : # 매도 
                        ''' 매도 주문 업데이트 '''
                        order_no = self.kiwoom.get_chejan_data('9203')        # 주문번호 가져오기
                        sell_price = 0
                        sell_price = self.kiwoom.get_chejan_data('910')           # 체결가 가져오기
                        sell_price = sell_price.strip().lstrip('+').lstrip('-')
                        get_update_order_sell_last_stock(code, "3", sell_price, order_no) 
                        self.get_deposit()  # 거래 가능 금액조회
                        # print(f"매도 주문 가 ===> {sell_price}")
                        
                    elif  fid_name == "주문구분" and order_type_val == "매수취소" : # 매수취소 
                        ''' 매수취소 업데이트 '''
                        order_no = self.kiwoom.get_chejan_data('9203')        # 주문번호 가져오기
                        print(f"매수취소 : {code}, order_no = {order_no}")
                        get_update_cancel_order_buy_stock(code, order_no) 
                        self.get_deposit()  # 거래 가능 금액조회
                    

                elif int(sGubun) == 1 :
                    if code not in self.balance.keys() : # 코드가 없다면 신규 생성
                        self.balance[code] = {}
                        
                    self.balance[code].update({fid_name: data}) # balance 에 저장
                    balance_list.append(fid_name + " : " + str(data))

                    # 매수 매도 상태 업데이트 
                    if fid_name == "매도/매수구분" and order_type_val == "2" : # 매수 
                        ''' 매수 주문 업데이트 '''
                        get_update_order_stock(code, "2") 
                        self.get_stock_real_balance_info() # 매수 후 실시간 조회 종목 변경
                        
                    elif fid_name == "매도/매수구분" and order_type_val == "1" : # 매도 
                        ''' 매도 주문 업데이트 '''
                        get_update_order_stock(code, "4") 
                        self.get_stock_real_balance_info() # 매도 후 실시간 조회 종목 변경
                    
                    
                
        if int(sGubun) == 0: # 결과 출력
            # print("# 주문 출력")
            # print(self.order)
            
            self.main_window.tb1_textBrowser_stock_send_order.append("=======================================")
            
            for val_text in order_list :
                self.main_window.tb1_textBrowser_stock_send_order.append(val_text)
            
            self.main_window.tb1_textBrowser_stock_send_order.append("=======================================")
            
        elif int(sGubun) == 1: # 결과 출력
            # print("# 매매처리완료")
            # print(self.balance)
            self.main_window.tb1_textBrowser_stock_buy_sell_success_view.append("=======================================")
            
            for val_text in balance_list :
                self.main_window.tb1_textBrowser_stock_buy_sell_success_view.append(val_text)
                
            self.main_window.tb1_textBrowser_stock_buy_sell_success_view.append("=======================================")
            
            
    
    def _on_receive_real_data(self, s_code, real_type, real_data):
        """
            실시간데이터를 받은 시점을 알려준다.
            - param
                - s_code    : 
                - real_type : 
                - real_data : 
        """
        real_data_code = {}
        
        if real_type == "장시작시간" and self.reald_data_on:
            market_division = self.kiwoom.get_comm_real_data(s_code, get_fid('장운영구분'))
            market_last_time = self.kiwoom.get_comm_real_data(s_code, get_fid('장시작예상잔여시간'))
            market_last_time = int(market_last_time)
            
            
            ''' 장종료 10분전 부터 모든 종목 시장가 매도(동시호가거래시간) '''
            # if market_division == '2':
            #     print(f"market_division : {market_division}, 장종료 10분전 신호 뜸?!!!!")
            
            if market_division == '3' :
                ''' 장시작시 매수 (아직 보류 테스트 후 처리)'''
                pass 
            
            elif market_division == '2' and market_last_time <= 1000 :
                ''' 장종료 10분전 부터 모든 종목 시장가 매도(동시호가거래시간) '''
                market_end_time = int(market_last_time / 100)
                print(f"장종료 => {market_end_time} 분 전")
                # get_end_update_order_sell_point_stock()
                
        
        elif real_type == "주식체결" and self.reald_data_on:
    
            market_price     = self.kiwoom.get_comm_real_data(s_code, get_fid('현재가'))
            market_price = abs(int(market_price))

            top_priority_ask = self.kiwoom.get_comm_real_data(s_code, get_fid('(최우선)매도호가'))
            top_priority_ask = abs(int(top_priority_ask))

            top_priority_bid = self.kiwoom.get_comm_real_data(s_code, get_fid('(최우선)매수호가'))
            top_priority_bid = abs(int(top_priority_bid))
            
            ''' 매도 포인트 업데이트(sell = 1) [실제 매도시에는 시장가로 매도]'''
            codes = get_point_sell_stock_code_info(s_code)
            for code, code_name, current_price in codes :
                current_price = current_price.replace('-', '')
                
                ''' 등락률에의한 매도 신호 업데이트 '''
                fluctuation_rate = get_fluctuation_rate(market_price, current_price)
                
                sell_rate = get_sell_rate()
                # print(f"sell_rate{sell_rate}")
                for win_rate, lose_rate in sell_rate : # 조회된 조회값 처리
                    if self.SELL_WIN_RATE != int(win_rate) or self.SELL_LOSE_RATE != int(lose_rate) :
                        print(f"익절 기준 : {win_rate}, 손절 기준 : {lose_rate}")
                        
                    self.SELL_WIN_RATE = int(win_rate)
                    self.SELL_LOSE_RATE = int(lose_rate)
                    
                        
                
                if float(fluctuation_rate) >= self.SELL_WIN_RATE :
                    # sell = True
                    print(f"익절 : s_code:{s_code}, market_price:{market_price}, scurrent_price:{current_price}")
                    get_update_order_sell_point_stock(code)
                    
                elif float(fluctuation_rate) <= self.SELL_LOSE_RATE :
                    # sell = True
                    print(f"손절 : s_code:{s_code}, market_price:{market_price}, current_price:{current_price}")
                    get_update_order_sell_point_stock(code)
            
            
            
            


    def _on_receive_condition_ver(self, lret, smsg):
        """
            조건검색 전용 함수와 이벤트
            - GetConditionLoad (사용자 호출) -> OnReceiveConditionVer (이벤트 발생) -> GetConditionNameList (사용자 호출)
            
            - param
                - lRet : 호출 성공여부, 1: 성공, 나머지 실패
                - sMsg : 호출결과 메시지
            
            - 전체 로직
                -  GetConditionLoad (사용자 호출) -> OnReceiveConditionVer (이벤트 발생) -> GetConditionNameList (사용자 호출)
                   -> SendCondition (사용자 호출) -> OnReceiveTrCondition (이벤트 발생) -> [실시간요청시]OnReceiveRealCondition (이벤트 발생)
        """
        print(f"lret : {lret}, smsg : {smsg}")
        if lret == 1:
         self.condition_loaded = True
         
          
  
    def _on_receive_tr_condition_ver(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        """
            조건검색 전용 함수와 이벤트
            - SendCondition (사용자 호출) -> OnReceiveTrCondition (이벤트 발생) -> OnReceiveRealCondition (이벤트 발생)
            
            - param
                - sScrNo           : 화면번호
                - strCodeList      : 종목코드 리스트
                - strConditionName : 조건식 이름
                - nIndex           : 조건 고유번호
                - nNext            : 연속조회 여부
                    
            - 전체 로직
                -  GetConditionLoad (사용자 호출) -> OnReceiveConditionVer (이벤트 발생) -> GetConditionNameList (사용자 호출)
                   -> SendCondition (사용자 호출) -> OnReceiveTrCondition (이벤트 발생) -> [실시간요청시]OnReceiveRealCondition (이벤트 발생)
        """
        print("sScrNo:{}, strCodeList:{}, strConditionName:{}, nIndex:{}, nNext:{}".format(sScrNo, strCodeList, strConditionName, nIndex, nNext))
        codes = strCodeList.split(';')[:-1]
        self.tr_condition_data = codes
        self.tr_condition_loaded= True
        # print(self.tr_condition_data)           
  
  
        
        
        
        
    '''
        ===================================================================================
        300. 기본 전문 요청값 설정 구간
        ===================================================================================
    ''' 
        
    def get_set_inputvalue(self, id, value):
        """
        - TR 입력값을 설정하는 메서드
        - param 
            - id    : TR INPUT의 아이템명
            - value : 입력 값
        - return
            - None
        """
        self.kiwoom.set_inputvalue(id, value)
        
        
    def com_rq_data(self, req_name, tr_code, pre_next, screen_no):
        '''
            전문 발신
            - param 
                - req_name  : 사용자 구분 요청 명
                - tr_code   : TR코드
                - pre_next  : 정보 연속성 여부(0 : 단일, 2 : 연속)
                - screen_no : 사용자 지정 화면 번호
        '''
        self.kiwoom.com_rq_data(req_name, tr_code, pre_next, screen_no)
  






      
    '''
        ===================================================================================
        400. TR요청 구간
        ===================================================================================
    '''    
    def get_search_where_code(self) :
        '''
            조건 검색 후 조건 검색 조회된 데이터 가져오기
            
            - 호출 함수 
                1. [GetConditionLoad() 함수]
                    - 서버에 저장된 사용자 조건검색 목록을 요청합니다. 
                    - 조건검색 목록을 모두 수신하면 OnReceiveConditionVer()이벤트가 발생됩니다.
                    - 조건검색 목록 요청을 성공하면 1, 아니면 0을 리턴합니다.
                 
                2. [GetConditionNameList() 함수]
                    - 서버에서 수신한 사용자 조건식을 조건식의 고유번호와 조건식 이름을 한 쌍으로 하는 문자열들로 전달합니다.
                    - 조건식 하나는 조건식의 고유번호와 조건식 이름이 구분자 '^'로 나뉘어져 있으며 각 조건식은 ';'로 나뉘어져 있습니다.
                    - 이 함수는 OnReceiveConditionVer()이벤트에서 사용해야 합니다.
                    - 
                    - 예) "1^내조건식1;2^내조건식2;5^내조건식3;,,,,,,,,,,"   
            
                3. 
                   - SendCondition(
                        - BSTR strScrNo,          // 화면번호
                        - BSTR strConditionName,  // 조건식 이름
                        - int nIndex,             // 조건식 고유번호
                        - int nSearch             // 실시간옵션. 0:조건검색만, 1:조건검색+실시간 조건검색
                    )
                    - 서버에 조건검색을 요청하는 함수입니다.
                    - 마지막 인자값으로 조건검색만 할것인지 실시간 조건검색도 수신할 것인지를 지정할 수 있습니다.
                    - GetConditionNameList()함수로 얻은 조건식 이름과 고유번호의 쌍을 맞춰서 사용해야 합니다.
                    - 리턴값 1이면 성공이며, 0이면 실패입니다.
                    - 요청한 조건식이 없거나 조건 고유번호와 조건명이 서로 안맞거나 조회횟수를 초과하는 경우 실패하게 됩니다.
        '''
        print("조건식 가져오기 시작")
        result= self.kiwoom.dynamicCall("GetConditionLoad()")
        
        self.condition_loaded = False
        
        while not self.condition_loaded:
            pythoncom.PumpWaitingMessages()
            
        print(f"조건식 가져오기 result : {result}")
        
        print("조건식 가져오기 시작")
        ret = self.kiwoom.dynamicCall("GetConditionNameList()")
        ret = ret.split(";")[:-1]
        
        res = []
        for ret_result in ret :
            ret_index, ret_code = ret_result.split('^')
            res.append((ret_index, ret_code))
        
        print(res)
        # print(f"name : {res[0][1]}, index :{res[0][0]}")
        ''' 
            성장주     : [0][1], [0][0] 
            시초가매매 : [1][1], [1][0] 
            종가매매   : [2][1], [2][0]
            스윙테스트 : [3][1], [3][0]
            당일단타   : [4][1], [4][0]
        '''
        search_code = "2" # 기본 호출값
        search_no = get_search_number()
        for no in search_no : # 조회된 조회값 처리
            search_code = str(no[0])  # 조건식 1. 성장, 2 시초, 3 종가
            
            
        print(f"search_code====> {search_code}")
        
        condition_name = ""  # 검색 명
        condition_no   = ""  # 검색 번호
        
        # search_code = "1" # 조건식 1. 성장, 2 시초, 3 종가, 4 스윙테스트, 5 당일단타
        if search_code == "1" : # 성장주
            condition_name = res[0][1]
            condition_no   = res[0][0]
            
        elif search_code == "2" : # 시초가매매
            condition_name = res[1][1]
            condition_no   = res[1][0]            
            
        elif search_code == "3" : # 종가매매
            condition_name = res[2][1]
            condition_no   = res[2][0]
            
        elif search_code == "4" : # 스윙테스트
            condition_name = res[3][1]
            condition_no   = res[3][0]
            
        elif search_code == "5" : # 당일단타
            condition_name = res[4][1]
            condition_no   = res[4][0]
            
        ''' 조건식 보내기'''
        self.kiwoom.dynamicCall("SendCondition(QString, QString, int, int)", "1050", condition_name, condition_no, 0)
        self.tr_condition_loaded = False
        
        while not self.tr_condition_loaded:
            pythoncom.PumpWaitingMessages()
                
        print(f"self.tr_condition_data ==> {self.tr_condition_data}")
        
        """
            전 영업일 매수 요청 후 미체결 요청건에대하여 초기화 처리
        """
        self.get_send_order_auto_cancel()
        # 과부화 방지 
        time.sleep(2)
        
        
        stock_list = self.tr_condition_data
        if len(stock_list) < 1 :
            print("===============================================================")
            print("===============================================================")
            print("===============================================================")
            print("조건 검색 후 조건 검색 조회된 데이터 당일 조건 검색 [대상 없음]")
            print("===============================================================")
            print("===============================================================")
            print("===============================================================")
            
        else :    
            code_list = []
            code_name_list = []
            code_price_list = []
            today_order_stock_dict = {}
            today_order_stock_db = {}
            try : 
                for i in stock_list: 
                    code = i
                    
                    code_name = self.get_company_name(code)
                    
                    while not self.get_company_name_loaded:
                        pythoncom.PumpWaitingMessages()
                    
                    
                    ''' 오늘 대상 종목 리스트  '''
                    self.get_stock_all_money_info(code) # 종가(현재가) 가져오기
                    # print("self.tr_data ==> ", self.tr_data)
                    current_price = self.tr_data[code]['current_price']
                    code_price_list.append(current_price)
                    code_list.append(code)
                    code_name_list.append(code_name)
                    
                    # db_result = get_stock_code_info(code)
                    
                
                    today_order_stock_db[code] = {
                        'code'       : code
                        ,'code_name' : code_name
                        ,'price'     : current_price
                    }
                    
                    today_order_stock_dict = {
                        'code'       : code_list
                        ,'code_name' : code_name_list
                        ,'price'     : code_price_list
                    }
                    # 내역 DB저장
                    get_insert_today_stock_list(today_order_stock_db[code])
                    
            except pymysql.Error as e :
                print(f"조건 검색 후 조건 검색 DB_ERROR : {e}")
                        
            # print("self.tr_data ==> ", self.tr_data)
            
            self.get_today_order_stock_dict = today_order_stock_dict
            # print("1 : ", today_order_stock_dict)
            
            df = pd.DataFrame(today_order_stock_dict, columns=['code_name', 'code', 'price'], index=today_order_stock_dict['code'])
            self.get_target_stock_list(df) # TAB 1 화면 대상 종목에 출력
  
        
    def get_send_order_auto_cancel(self):
        """
            종목정보 업데이트 시 
            전 영업일 매수 접수 후 미 체결 대상 종목에 대하여 취소 신청 후 DB 정보 업데이트 
            
            - param
                - code : 종목 코드 
        """
        codes = get_buy_unsuccess_order_count_info()
        
        for code, quantity, order_no in codes :
            # self.kiwoom.get_send_order("send_hand_buy_cancel_order", get_screen_no("TAB2_매수취소"), self.account_number[0], 
            #                         3, # 주문휴형 1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
            #                         code,     # 주식 종목코드
            #                         quantity, # 주문수량
            #                         0,        # 주문단가
            #                         '00', 
            #                         order_no # 주문번호
            #                         )       
            
            print(f"취소 처리 : code : {code}, order_no : {order_no}")
            ''' 해당 종목 DB 업데이트 처리 '''
            get_buy_unsuccess_order_update(code, order_no)
            # 과부화 방지용 
            time.sleep(0.3)


    def get_deposit(self):
        """
            예수금 정보
            - param
                - self.account_number[0] : 계좌번호
        """
        self.get_set_inputvalue("계좌번호", self.account_number[0])  
        self.get_set_inputvalue("비밀번호입력매체구분", "00")  
        self.get_set_inputvalue("조회구분", "2")  
        # 전문 요청
        self.com_rq_data("opw00001_req", "opw00001", 0, get_screen_no("TAB2_예수금"))
        
        # # 응답 대기
        # self.recive = False
        # # 처리 될 동안 대기
        # while not self.recive :
        #     pythoncom.PumpWaitingMessages()  

    def get_sell_win_lose_save(self):
        """
            매매기준 퍼센트 저장
        """
        win_rate = self.main_window.tb1_textEdit_sell_win_rate.toPlainText()  
        lose_rate = self.main_window.tb1_textEdit_sell_lose_rate.toPlainText()  
        print(f"매도 기준 변경 ==> 익절 기준 : {win_rate}, 손절 기준 : {lose_rate}")
        get_sell_rate_update(win_rate, lose_rate)
            
            
            
    def set_parser_diposit(self, tr_code, req_name):
        """
            예수금 응답값 화면에 표시 
            - param
                - tr_code  : TR코드
                - req_mame : 사용자 구분 요청 명
        """
        deposit = self.kiwoom.get_comm_data(tr_code, req_name, 0, "주문가능금액")   # 일자 값 호출 
        '''
            우선 100만원 으로 합시다.!!
        '''
        # self.sid_money = int(deposit)
        ''' 임의로 100만원 만 처리되록 계산 수식 넣음'''
        self.sid_money = int(int(deposit) - 9000000) # 총 액수 1000만원에서 100만원만 사용하려고 900만원 뺌
        
        print(self.sid_money)
        
        self.get_parser_diposit()
        
    
    
    
    def get_stock_all_money_info(self, code):
        """
            [ opt10001 : 주식기본정보요청 ]

            [ 주의 ] 
            PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨

            1. Open API 조회 함수 입력값을 설정합니다.
                종목코드 = 전문 조회할 종목코드
                SetInputValue("종목코드"	,  "000080");


            2. Open API 조회 함수를 호출해서 전문을 서버로 전송합니다.
                CommRqData( "RQName"	,  "opt10001"	,  "0"	,  "화면번호"); 
        """
        tr_code = "opt10001"
        tr_name = "opt10001_req"
        
        # 응답 완료 여부
        self.recive = False
        try : 
            ''' 가져올값 선택 '''
            self.get_set_inputvalue("종목코드", code)
            self.com_rq_data(tr_name, tr_code, 0, get_screen_no("TAB1_주식시가총액"))
            
            # 응답 완료 여부
            self.recive = False
            # 처리 될 동안 대기
            while not self.recive:
                pythoncom.PumpWaitingMessages()
                
            # 과부화 방지  건단 3.6초 해야 오류안남
            time.sleep(0.3)
                
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")    
    
    
 
 
    def get_send_auto_order_buy(self):
        """
            종목 자동 매수 주문
            - param
                - code : 종목코드 
        """
        codes = get_stock_target_code_info()
        
        sid = self.sid_money
        
        ''' 주문 수량 (임시로 100만원) '''
        # sid = 1000000
        order_sid = int(int(sid) / 5)              # sid머니 생성
        
        for code, code_name, current_price in codes :
            current_price = current_price.replace('-', '')
            
            ''' 주문수량 생성 '''
            buy_price = made_buy_price(current_price) # -1% 시초가 설정
            
            order_quantity = get_quantity(order_sid, buy_price) #int(int(order_sid) / int(buy_price)) # 주문 수량 계산 
            
            
            print(f"get_send_auto_order_buy ==> code : {code}, price : {current_price}, buy_price : {buy_price} ")
            self.kiwoom.get_send_order("send_auto_buy_order", get_screen_no("TAB1_자동매수주문"), self.account_number[0], 
                                       1,             # 주문휴형 1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
                                       code,          # 주식 종목코드
                                       order_quantity,             # 주문수량
                                       buy_price, # 주문단가
                                       '00'           # 00:지정가, 06:최유리 지정가, 03:시장가
                                       )
            # self.kiwoom.get_send_order("send_auto_buy_order", get_screen_no("TAB1_자동매수주문"), self.account_number[0], 
            #                            1,             # 주문휴형 1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
            #                            code,          # 주식 종목코드
            #                            order_quantity,             # 주문수량
            #                            0, # 주문단가
            #                            '03'           # 00:지정가, 06:최유리 지정가, 03:시장가
            #                            )
            # print("buy_price : ", buy_price)
            # 주문 후 0.2초 대기
            time.sleep(0.2)
            self.order_code = code
            self.order_code_name = code_name
            
            # 응답 대기
            # self.recive = False
            # # 처리 될 동안 대기
            # while not self.recive :
            #     pythoncom.PumpWaitingMessages()  
            
            get_update_order_buy_price_stock(code, 0, order_quantity)
            
        # self.get_deposit() # 예수금
        # # 종목 {코드 / 명} 초기화
        self.order_code = ""
        self.order_code_name = ""
            
    
 
    def get_send_auto_order_point_sell(self, code, quantity):
        """
            종목 자동 매도 주문
            - param
                - code : 종목코드 
        """    
        
        self.kiwoom.get_send_order("send_auto_point_sell_order", get_screen_no("TAB1_자동매도신호주문"), self.account_number[0], 
                                    2,             # 주문휴형 1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
                                    code,          # 주식 종목코드
                                    quantity,             # 주문수량
                                    0, # 주문단가
                                    '03'           # 00:지정가, 06:최유리 지정가, 03:시장가
                                    )    
    
            # 주문 후 0.2초 대기
        time.sleep(0.2)
        # self.order_code = code
        # self.order_code_name = code_name
        
        print(f"1sell : [ code : {code} ] / self.recive = ", self.recive)
        
    
            
    
    
    def get_stock_balance_info(self):
        """
            잔고내역요청        
        """
        self.main_window.tb2_textBrowser_stock_balance_info.clear()
        self.get_set_inputvalue("계좌번호", self.account_number[0])
        
        # '''비밀번호 = 사용안함(공백)'''
        # self.get_set_inputvalue("비밀번호", my_decrypt())
        
        '''비밀번호입력매체구분 = 00'''
        self.get_set_inputvalue("비밀번호입력매체구분", "00")
        
        '''조회구분 = 1:합산, 2:개별'''
        self.get_set_inputvalue("조회구분", "1")
        
        # 전문 요청
        self.kiwoom.com_rq_data("opw00018_req", "opw00018", 0, get_screen_no("TAB1_잔고내역요청")) 
        
        # # 응답 완료 여부
        # self.recive = False
        # # 처리 될 동안 대기
        # while not self.recive:
        #     pythoncom.PumpWaitingMessages()

        # time.sleep(0.5)
        # self.get_stock_balance_info()



    def get_stock_real_balance_info(self):
        """
            실시간 주식 정보 조회
        """
        self.reald_data_on = True # 실시간 데이터  실행
        real_stock_code_list = "";
        code_list = get_real_time_stock_code_info()
        print("code_list : ", code_list)
        
        if len(code_list) > 0 :
            for code in code_list:
                real_stock_code_list = real_stock_code_list + str(code[0])  + ";" 
            
            print("real_stock_code_list : ", real_stock_code_list)
            ''' 요청할 fid '''
            f_id = get_fid("등락율") + ";"
            f_id = f_id + get_fid("시가") + ";"
            f_id = f_id + get_fid("(최우선)매수호가") + ";"
            f_id = f_id + get_fid("(최우선)매수호가") + ";"
            
            self.set_real_reg(get_screen_no("TAB1_실시간주식정보조회"), real_stock_code_list, f_id )
        
        else :
            print("당일 매수 종목이 존재하지않습니다.")

    
    

    '''
        ===================================================================================
        450. 전문 응답 값 처리 구간
        ===================================================================================
    '''         
    def opt10001_req(self, tr_code, req_mame, tr_cnt):
        """
            opt10001 : 주식기본정보요청 시가총액 업데이트
            - param
                - tr_ode   : TR목록 코드
                - req_mame : TR목록 응답 명
                - tr_cnt   : TR응답 카운트
        """
        daily_stock_total_price_list = {}
        # print("tr_cnt : ", tr_cnt)
        try :
            code           = self.kiwoom.get_comm_data(tr_code, req_mame, 0, '종목코드') # 종목코드    
            code_name      = self.kiwoom.get_comm_data(tr_code, req_mame, 0, '종목명')   # 종목명
            current_price  = self.kiwoom.get_comm_data(tr_code, req_mame, 0, '현재가')   # 현재가
            
            code = code.strip()
            daily_stock_total_price_list[code] = {
                'code'             : code              # 종목코드     
                ,'code_name'       : code_name.strip() # 종목명     
                ,'current_price' : int(current_price)  # 시가총액 
            }
                
            self.tr_data = daily_stock_total_price_list
            
            # print("===============================")
            # print(daily_stock_total_price_list[code])
            # print("===============================")
            # 과부화 방지        
            # time.sleep(0.5)
            
            
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")

            
            
    
    def opw00018_req(self, trcode, rqname, tr_cnt):
        """
            opw00018_req : 계좌평가잔고내역요청
            - param
                - tr_ode   : TR목록 코드
                - req_mame : TR목록 응답 명
                - tr_cnt   : TR응답 카운트
        """
        # print( "opw00018_req : " + str(trcode) + " ##/ " + rqname + " ##/ " + str(tr_cnt))
        order_name = ["종목번호", "종목명", "보유수량", "매입가", "수익률(%)", "현재가", "매입금액", "매매가능수량", "총수익률(%)", "총평가손익금액"]
        for i in range(tr_cnt):
            code                 = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[0])# 종목번호 
            code_name            = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[1])# 종목명 
            quantity             = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[2])# 보유수량 
            purchase_price       = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[3])# 매입가 
            return_rate          = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[4])# 수익률(%) 
            current_price        = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[5])# 현재가 
            total_purchase_price = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[6])# 매입금액 
            available_quantity   = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[7])# 매매가능수량 
            
            if i == 0 :
                total_rate  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[8]) # 총수익률(%)
                totla_price = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[9]) # 총평가손익금액
                total_rate  = float(total_rate)
                totla_price = int(totla_price)

            
            # 데이터 형변환 및 가공
            code                 = code.strip()[1:]
            code_name            = code_name.strip()
            quantity             = int(quantity)
            purchase_price       = int(purchase_price)
            return_rate          = float(return_rate)
            current_price        = int(current_price)
            total_purchase_price = int(total_purchase_price)
            available_quantity   = int(available_quantity)
            
            ''' 인터넷이 끊어진 후 잔고조회시 보유 잔고를 기반으로 매수여부 DB 업데이트 '''
            get_balance_info_update_buy_stock_info(code, purchase_price)
            

            # code를 key값으로 한 딕셔너리 변환
            self.balance[code] = {
                '종목명'        : code_name,
                '보유수량'      : quantity,
                '매입가'        : purchase_price,
                '수익률'        : return_rate,
                '현재가'        : current_price,
                '매입금액'      : total_purchase_price,
                '매매가능수량'  : available_quantity,
                
            }
            self.main_window.tb2_textBrowser_stock_balance_info.append("=======================================")
            self.main_window.tb2_textBrowser_stock_balance_info.append("종목명 : {}".format(str(code_name)))
            self.main_window.tb2_textBrowser_stock_balance_info.append("보유수량 : {}".format(str(quantity)))
            self.main_window.tb2_textBrowser_stock_balance_info.append("매입가 : {}".format(str(format(purchase_price, ','))))
            self.main_window.tb2_textBrowser_stock_balance_info.append("수익률 : {}".format(str(return_rate)))
            self.main_window.tb2_textBrowser_stock_balance_info.append("현재가 : {}".format(str(format(current_price, ','))))
            self.main_window.tb2_textBrowser_stock_balance_info.append("매입금액 : {}".format(str(format(total_purchase_price, ','))))
            self.main_window.tb2_textBrowser_stock_balance_info.append("매매가능수량 : {}".format(str(available_quantity)))
            self.main_window.tb2_textBrowser_stock_balance_info.append("=======================================")
             
            self.main_window.tb2_textEdit_stock_total_rate.setText(str(return_rate) + " %")
            self.main_window.tb2_textEdit_stock_total_price.setText(str(format(totla_price, ',')) + " 원")
            
        # print(self.balance)
        # self.tr_data = self.balance
        time.sleep(0.5)    
    
    
    

    '''
        ===================================================================================
        500. 화면출력 및 로직 처리 구간 
        ===================================================================================
    '''         
    def get_parser_diposit(self):        
        ''' 예수금 화면에 출력 구간 '''
        self.main_window.tb1_textEdit_stock_deposit_view.setText(format(self.sid_money, ','))            



 
    def get_target_stock_list(self, df):        
        ''' TAB 1 화면 대상 종목에 출력 '''
        table = self.main_window.tb1_tableWidget_stock_target_info_list01
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        # res_names = ["일자", "시가", "고가", "저가", "현재가", "거래량"] # 응답에 대한 필요 항목명
        res_names = ["회사명", "종목코드", "종가(현재가)" ] # 응답에 대한 필요 항목명
        table.setHorizontalHeaderLabels(res_names)
        for df_idx in range(len(df.index)):
            for df_col in range(len(df.columns)):
                format_str = df.iloc[df_idx, df_col] if type(df.iloc[df_idx, df_col]) == type("A") else format(df.iloc[df_idx, df_col], ',')
                table.setItem(df_idx, df_col, QTableWidgetItem(str(format_str.replace('-', ''))))
                
            str_split = str(format_str).split("-")
            qt_str_color = QtGui.QColor(10, 128, 255) if '' == str_split[0] else QtGui.QColor(255, 128, 128)
            table.item(df_idx, 2).setBackground(qt_str_color)
 






        

    '''
        ===================================================================================
        600.기타 처리 구간
        ===================================================================================
    ''' 
    def get_company_name(self, code):
        '''
            업체명 가져오기
        '''
        # 업체명 가져오기
        code_name = self.kiwoom.get_sotck_name(code)
        self.get_company_name_loaded = True
        
        return code_name
    
        
                       
   
    def get_tb1_tableWidget_stock_target_info_code(self):
        '''
            대상종목 선택시 대상 종목 코드 가져옴
            -return 
                - 종목코드
        '''
        row = self.main_window.tb1_tableWidget_stock_target_info_list01.currentItem().row() # 몇번째 로우 인지 가져온다
        
        item = self.main_window.tb1_tableWidget_stock_target_info_list01.item(row, 1).text() # item(row, 원하는 column 번호)
        self.target_code = item # 선택 종목코드 등록
        # print(item)             
        

    '''
        ===================================================================================
        9999.테스트 로직 처리 구간
        ===================================================================================
    '''
    
    def testButton(self):
        print("검색!!")
