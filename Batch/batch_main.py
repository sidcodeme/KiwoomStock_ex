''' 
    상위 폴더 의 모듈 가져오기위함 ==================================
'''
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

'''   =====================================  '''

from db.db_helper import *
import time
import pythoncom
from api.kiwoom import Kiwoom
from PyQt5.QtWidgets import QApplication
from util.const import *
import logging as log

class BatchMain():
    """
        UI창을 띄우기 위함
    """
    app = QApplication(sys.argv)
    # 코스피 : 0,  코스탁 : 10
    KOSPI_CODE = '0'
    KOSDAQ_CODE = '10'
    
    def __init__(self):
        super().__init__()
        
        '''
            변수 
        '''
        self.per_val = 1      # PER 정보 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE 
        self.connected = False  # 로그인 대기
        self.recive = False     # TR데이터 대기
        self.has_next_tr_date = False    # tr_data 연속성 여부
        
        ''' 
            키움 모듈 로드 및 시그널 슬롯 
        '''
        self.kiwoom = Kiwoom()          # 키움 API 상속
        self._set_kiwoom_signal_slots() # 키움 시그널 처리 
        self.comm_connect()      # 로그인
        
        
        '''
            로그인 완료 후 기본 호출 정보
        '''
        self.base_load_info() # 로그인 후 로드 될 항목

 
         
    '''
        ===================================================================================
        100.Kiwoom 시그널 처리 
        ===================================================================================
    '''           
    def _set_kiwoom_signal_slots(self):
        self.kiwoom.OnEventConnect.connect(self._login_event_connect)           # login_event_connect 로그인 이벤트 처리 
        self.kiwoom.OnReceiveTrData.connect(self._on_receive_tr_data)           # CommRqData 전문 송수신 처리
        self.kiwoom.OnReceiveMsg.connect(self._on_receive_msg)                  # 수신 메시지 이벤트
        
         
    '''
        ===================================================================================
        110.Kiwoom 로그인 처리 
        ===================================================================================
    '''       
    def comm_connect(self):
        self.kiwoom.comm_connect()      # 로그인
        # 응답 완료 여부
        self.connected = False
        # 처리 될 동안 대기
        while not self.connected:
            pythoncom.PumpWaitingMessages()
    
           
    def _login_event_connect(self, error_code):
        '''
            로그인 커넥션 이벤트 응답 처리
        '''        
        if error_code == 0 :
            self.connected = True

        log.info("로그인 성공" if self.connected else "로그인 실패")
        
 
    
    
    '''
        ===================================================================================
        150.Kiwoom 로그인 후 처리 
        ===================================================================================
    '''          
    def base_load_info(self):
        '''
            로그인 완료 후 기본 호출 정보
        '''
        now = datetime.datetime.now()
        print(f"시작 시간 : {now}")
        """ 100.주가정보 가저오기 """
         #업종코드 = 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
        print(f"100.주가정보 가저오기 시작 시간 : {now}")
        self.get_stock_price_info() # 주식 가격 정보 003 : 중형주
        
        now = datetime.datetime.now()
        print(f"100.주가정보 가저오기 종료 시간 : {now}")    
        print("================================================")    
        print("")    
        print("")    
        
                
        """ 110.감리정보 가저오기 """
        now = datetime.datetime.now()
        print(f"110.감리정보 가저오기 시작 시간 : {now}")
        self.get_master_construction() # per 정보              
        
        now = datetime.datetime.now()
        print(f"110.감리정보 가저오기 종료 시간 : {now}")   
        print("================================================")    
        print("")    
        
             
        """ 150.주가 시가총액 가저오 """
        now = datetime.datetime.now()
        print(f"150.주가 시가총액 가저오기 시작 시간 : {now}")
        self.get_stock_all_money_info() # 주식 가격 정보 003 : 중형주
        
        now = datetime.datetime.now()
        print(f"150.주가 시가총액 가저오기 종료 시간 : {now}")         
        print("================================================")    
        print("")    
                   
            
        """ 200.주식일봉차트조회요청 """
        now = datetime.datetime.now()
        print(f"200.주식일봉차트조회요청 시작 시간 : {now}")
        self.get_all_stock_info() # 주식일봉차트조회요청
        
        now = datetime.datetime.now()
        print(f"200.주식일봉차트조회요청 종료 시간 : {now}")  
        print("================================================")    
        print("")    
        
                
        
        """ 300.주가PER정보 가저오기 """
        now = datetime.datetime.now()
        print(f"300.주가PER정보 가저오기 시작 시간 : {now}")
        self.get_while_high_per_info()          
        
        self.per_val = 1
        now = datetime.datetime.now()
        print(f"300.주가PER정보 가저오기 종료 시간 : {now}")            
        print("================================================")    
        print("")    
                
        
        """ 종료  """
        now = datetime.datetime.now()
        print(f"종료 시간 : {now}")
        
        now = datetime.datetime.now()
        print(f"배치처리 모두 완료 하여 프로그램을 종료합니다.{now}")
        sys.exit()

        
    '''
        ===================================================================================
        200.전문 송수신 
        ===================================================================================
    ''' 
    
    def get_set_inputvalue(self, tr_id, value):
        """
        - TR 입력값을 설정하는 메서드
        - param 
            - id    : TR INPUT의 아이템명
            - value : 입력 값
        - return
            - None
        """
        self.kiwoom.set_inputvalue(tr_id, value)
        
        
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
        # print("_on_receive_tr_data: {}".format(sRQName))
        tr_cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
        
        res_data = []
        res_data.append(str(sScrNo))
        res_data.append(str(sRQName))
        res_data.append(str(sTrCode))
        res_data.append(str(sRecordName))
        res_data.append(str(sPreNext))
        res_data.append(str(tr_cnt))
        
        self.has_next_tr_date = True if sPreNext == '2' else False
        
        if sRQName == "opt10026_req" : 
            ''' Per 정보 '''
            # print(f"sPreNext : {sPreNext}")
            self.opt10026_req(sTrCode, sRQName, tr_cnt)
            
        elif sRQName == "opt20002_req" :
            ''' 업종일봉조회요청 (나는 두가지만 / 003:중형주, 004:소형주 )'''
            # print(f"sPreNext : {sPreNext}")
            self.opt20002_req(sTrCode, sRQName, tr_cnt)
            
        elif sRQName == "opt10081_req" :
            '''종목 현재가 검색'''
            self.opt10081_req(sTrCode, sRQName, tr_cnt)
            
        elif sRQName == "opt10001_req" :
            '''시가총액 업데이트'''
            self.opt10001_req(sTrCode, sRQName, tr_cnt)
                        
        self.recive = True
  
  
  
  
  
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
        
 
    '''
        ===================================================================================
        300.전문 셋팅 
        ===================================================================================
    ''' 
              
    def get_high_per_info(self):
        """
            opt10026 : 고저PER요청
            - param
                - PER구분 = 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE
            SetInputValue("PER구분"	,  "1");      
        """
        batch_name = "opt10026"
        req_name   = "opt10026_req"
        
        ''' 가져올값 선택 '''
        if int(self.per_val) == 1:
            batch_history_ins(batch_name)
            
        try :
            self.get_set_inputvalue("PER구분", self.per_val)
            self.com_rq_data(req_name, batch_name, 0, get_screen_no("BATCH_고저PER"))
            
            # 응답 완료 여부
            self.recive = False
            # 처리 될 동안 대기
            while not self.recive:
                pythoncom.PumpWaitingMessages()
            
            while self.has_next_tr_date:
                self.get_set_inputvalue("PER구분",self.per_val)
                self.com_rq_data(req_name, batch_name, 2, get_screen_no("BATCH_고저PER"))
                # 응답 완료 여부
                self.recive = False
                # 처리 될 동안 대기
                while not self.recive:
                    pythoncom.PumpWaitingMessages()
                    
                time.sleep(0.3)
                
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")
            # 종료 후 초기화 
            batch_history_upd(batch_name, e)

                
            
              
    def get_stock_price_info(self):
        """
            [ opt20002 : 업종별주가요청 ]

            1. Open API 조회 함수 입력값을 설정합니다.
                시장구분 = 0:코스피, 1:코스닥, 2:코스피200
                SetInputValue("시장구분"	,  "1");

                업종코드 = 0:코스피 [001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주] 
                           1:코스닥 [101:종합(KOSDAQ)], 
                            201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
                SetInputValue("업종코드"	,  "003");


            2. Open API 조회 함수를 호출해서 전문을 서버로 전송합니다.
                CommRqData( "RQName"	,  "OPT20002"	,  "0"	,  "화면번호");    
        """
        batch_name = "opt20002"
        req_name   = "opt20002_req"
        batch_cnt = get_this_batch_today_run(batch_name)
        
        if 1 > int(batch_cnt) :
            batch_history_ins(batch_name)
            try : 
                
                market_cd_kospi = ("0", "003")
                market_cd_kosdaq = ("1", "101")
                for i, x in market_cd_kospi, market_cd_kosdaq :
                    now = datetime.datetime.now()
                    print(f"{batch_name} : 업종별주가요청 시장구분:{i} / 업종코드 : {x}  시각 : {now}")
                    
                    ''' 가져올값 선택 '''
                    self.get_set_inputvalue("시장구분", i)
                    self.get_set_inputvalue("업종코드", x)
                        
                        
                    self.com_rq_data(req_name, batch_name, 0, get_screen_no("BATCH_업종별주가요청"))
                    
                    # 응답 완료 여부
                    self.recive = False
                    # 처리 될 동안 대기
                    while not self.recive:
                        pythoncom.PumpWaitingMessages()
                    
                    while self.has_next_tr_date:
                        ''' 가져올값 선택 '''
                        self.get_set_inputvalue("시장구분", i)
                        self.get_set_inputvalue("업종코드", x)
                        
                        self.com_rq_data(req_name, batch_name, 2, get_screen_no("BATCH_업종별주가요청"))
                        
                        # 응답 완료 여부
                        self.recive = False
                        # 처리 될 동안 대기
                        while not self.recive:
                            pythoncom.PumpWaitingMessages()
                            
                    # 과부화 방지 
                    time.sleep(0.3)
            except pymysql.Error as e :
                print(f"DB_ERROR : {e}")
                # 종료 후 초기화 
                batch_history_upd(batch_name, e)
                
            else : 
                batch_history_upd(batch_name)
        else :
            print(f"        {batch_name} : 업종별주가요청 이미 당일배치 처리 완료................")
            
              
    def get_stock_all_money_info(self):
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
        batch_name = "opt10001"
        req_name   = "opt10001_req"
        batch_cnt = get_this_batch_today_run(batch_name)
        
        if 1 > int(batch_cnt) :
            # 응답 완료 여부
            self.recive = False
            code = {}
            code = get_all_stock_code_list()
            code_cnt = len(code)
            print(f"총 시가총액 업데이트 대상건수 : {code_cnt}")
            
            batch_history_ins(batch_name)
            try : 
                for i in code :    
                    ''' 가져올값 선택 '''
                    self.get_set_inputvalue("종목코드", i[0])
                    self.com_rq_data(req_name, batch_name, 0, get_screen_no("BATCH_주식시가총액"))
                    
                    # 응답 완료 여부
                    self.recive = False
                    # 처리 될 동안 대기
                    while not self.recive:
                        pythoncom.PumpWaitingMessages()
                        
                    # 과부화 방지  건단 3.6초 해야 오류안남
                    time.sleep(3.6)
                    
            except pymysql.Error as e :
                print(f"DB_ERROR : {e}")
                # 종료 후 초기화 
                batch_history_upd(batch_name, e)
                
            else : 
                batch_history_upd(batch_name)
                
        else :
            print(f"        {batch_name} : 주식기본정보요청 이미 당일배치 처리 완료................")    
            
            
            
                
    def get_all_stock_info(self):
        """
            종목 상장일 부터 가장 최근 일짜 까지의 일봉 정보 
            * 30일 데이터만 추출하기로함 (2021.11.26)
            - param 
                - self.main_window.tb2_textEdit_search_stock_code.toPlainText() : 종목 코드
                - self.main_window.tb_textEdit_search_stock_modif.toPlainText() : 수정주가구분
            - return 
                df : pandas 형 리턴
        """
        batch_name = "opt10081"
        req_name   = "opt10081_req"
        batch_cnt = get_this_batch_today_run(batch_name)
        
        if 1 > int(batch_cnt) :
            # 응답 완료 여부
            self.recive = False
            code = {}
            code = get_all_dailly_stock_code_list()
            
            batch_history_ins(batch_name)
            try : 
                for i in code :                
                    # 전문 요청 세부 항목값 ID, VALUE
                    # print(f"code :  {i[0]}")
                    self.get_set_inputvalue("종목코드", i[0])    
                    self.get_set_inputvalue("수정주가구분", "1")
                    
                    # 전문 요청
                    self.com_rq_data(req_name, batch_name, 0, get_screen_no("BATCH_종목가격전체정보"))
                    
                    # 응답 완료 여부
                    self.recive = False
                    # 처리 될 동안 대기
                    while not self.recive:
                        pythoncom.PumpWaitingMessages()
                        
                    
                    # while self.has_next_tr_date:
                    #     # 전문 요청 세부 항목값 ID, VALUE
                    #     self.get_set_inputvalue("종목코드", i)    
                    #     self.get_set_inputvalue("수정주가구분", "1")
                    #     # 전문 요청
                    #     self.com_rq_data(req_name, batch_name, 2, get_screen_no("BATCH_종목가격전체정보"))
                        
                    #     # 응답 완료 여부
                    #     self.recive = False
                    #     # 처리 될 동안 대기
                    #     while not self.recive:
                    #         pythoncom.PumpWaitingMessages()
                            
                    # time.sleep(0.5)    
                    
            except pymysql.Error as e :
                print(f"DB_ERROR : {e}")
                # 종료 후 초기화 
                batch_history_upd(batch_name, e)
                
            else : 
                batch_history_upd(batch_name)
                
        else :
            print(f"        {batch_name} : 종목가격전체정보(30일치싱글데이터) 이미 당일배치 처리 완료................")    
            
            
            
                
    def get_master_construction(self):
        """
            입력한 종목코드에 해당하는 종목의 감리구분을 전달합니다.
             (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)
            - return  
                - (* 종목코드 입력시 바로 위의 상태값 리턴)

        """
        batch_name = "getmasterconstruction"
        req_name   = "getmasterconstruction_req"
        batch_cnt = get_this_batch_today_run(batch_name)
        
        if 1 > int(batch_cnt) :
            # 응답 완료 여부
            code = {}
            code = get_all_stock_supervising_code_list()
            
            batch_history_ins(batch_name)
            try : 
                for i in code :                
                    this_code = i[0]
                    # 전문 호출 종목코드 입력
                    result = self.kiwoom.get_master_construction(this_code)
                    
                    get_upd_stock_all_master_construction(this_code, (0 if "정상" == result else 1))
                    time.sleep(0.2)                           
                    
            except pymysql.Error as e :
                print(f"DB_ERROR : {e}")
                # 종료 후 초기화 
                batch_history_upd(batch_name, e)
                
            else : 
                batch_history_upd(batch_name)
                
        else :
            print(f"        {batch_name} : 감리구분 이미 당일배치 처리 완료................")    
            



    '''
        ===================================================================================
        500. 화면출력 및 로직 처리 구간 
        ===================================================================================
    '''         

    def opt10026_req(self, trcode, rqname, tr_cnt):
        """
            opt10026_req :  고저PER요청, 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE
            - param
                - tr_ode   : TR목록 코드
                - req_mame : TR목록 응답 명
                - tr_cnt   : TR응답 카운트
            """
        # print("Total : {}".format(tr_cnt))
        # 초기화 
        # self.per_list = {}
        order_name = ["종목코드", "종목명", "PER", "현재가", "전일대비기호", "전일대비", "등락률", "현재거래량", "매도호가"]
        per_list = {}      # PER 정보 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE 
        per_list_free = {}      # PER 정보 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE 
        
        try :
            for i in range(tr_cnt) :
                code                   = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[0])
                code_name              = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[1])
                per                    = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[2])
                current_price          = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[3])
                pre_sign               = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[4])
                pre_av                 = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[5])
                fluctuation_rate       = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[6])
                current_trading_volume = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[7])
                sell_ask_price         = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[8])
                
                code                   = code.strip()                  
                code_name              = code_name.strip()             
                per                    = float(per)
                current_price_free     = int(current_price)
                current_price          = int(current_price)  #####################
                pre_sign               = int(pre_sign)
                pre_av                 = str(pre_av).strip()
                fluctuation_rate       = str(fluctuation_rate).strip()
                current_trading_volume = int(current_trading_volume.replace(",", ""))
                sell_ask_price_free    = int(sell_ask_price)
                sell_ask_price         = int(sell_ask_price)  ########################
                    
                per_list[code] = {
                    '종목코드'      :   code                  
                    ,'종목명'       :   code_name             
                    ,'PER'          :   per                   
                    ,'현재가'       :   current_price         
                    ,'전일대비기호' :   pre_sign              
                    ,'전일대비'     :   pre_av                
                    ,'등락률'       :   fluctuation_rate      
                    ,'현재거래량'   :   current_trading_volume 
                    ,'매도호가'     :   sell_ask_price  
                }
                    
                per_list_free[code] = {
                    'code'                    : code                  
                    ,'code_name'              : code_name             
                    ,'per'                    : per                   
                    ,'current_price'          : current_price_free         
                    ,'pre_sign'               : pre_sign              
                    ,'pre_av'                 : pre_av                
                    ,'fluctuation_rate'       : fluctuation_rate      
                    ,'current_trading_volume' : current_trading_volume 
                    ,'sell_ask_price'         : sell_ask_price_free  
                    ,'per_val'                : self.per_val
                }
                # print(per_list[code])
                get_insert_per_info(per_list_free[code])
            
            # self.tr_data = per_list
        
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")
            # 종료 후 초기화 
            batch_history_upd("opt10026", e)
        
        


    def opt20002_req(self, trcode, rqname, tr_cnt):
        """
            opt20006 : 업종일봉조회요청
            - 업종코드 = 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
        """
            
        # print("Total : {}".format(tr_cnt))
        # 초기화 
        # self.per_list = {}
        order_name = ["종목코드", "종목명", "현재가", "전일대비기호", "전일대비", "등락률", "현재거래량", "매도호가", "매수호가", "시가", "고가", "저가"]
        price_list = {}      
        
        try :
            for i in range(tr_cnt) :
                val0  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[0])  # 종목코드
                val1  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[1])  # 종목명
                val2  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[2])  # 현재가
                val3  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[3])  # 전일대비기호
                val4  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[4])  # 전일대비
                val5  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[5])  # 등락률
                val6  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[6])  # 현재거래량
                val7  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[7])  # 매도호가
                val8  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[8])  # 매수호가
                val9  = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[9])  # 시가
                val10 = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[10]) # 고가
                val11 = self.kiwoom.get_comm_data(trcode, rqname, i, order_name[11]) # 저가
                
                val0  = val0.strip()  # 종목코드
                val1  = val1.strip()  # 종목명
                val2  = int(val2.lstrip('+').lstrip('-'))     # 현재가
                val3  = int(val3)     # 전일대비기호
                val4  = int(val4)     # 전일대비
                val5  = float(val5)   # 등락률
                val6  = int(val6)     # 현재거래량
                val7  = int(val7.lstrip('+').lstrip('-'))     # 매도호가
                val8  = int(val8.lstrip('+').lstrip('-'))     # 매수호가
                val9  = int(val9.lstrip('+').lstrip('-'))     # 시가
                val10 = int(val10.lstrip('+').lstrip('-'))    # 고가
                val11 = int(val11.lstrip('+').lstrip('-'))    # 저가
                    
                price_list[val0] = {
                    'code'                    : val0  # 종목코드
                    ,'code_name'              : val1  # 종목명
                    ,'current_price'          : val2  # 현재가
                    ,'pre_sign'               : val3  # 전일대비기호
                    ,'pre_av'                 : val4  # 전일대비
                    ,'fluctuation_rate'       : val5  # 등락률
                    ,'current_trading_volume' : val6  # 현재거래량
                    ,'sell_ask_price'         : val7  # 매도호가
                    ,'bid_price'              : val8  # 매수호가
                    ,'market_price'           : val9  # 시가
                    ,'high_price'             : val10 # 고가
                    ,'low_price'              : val11 # 저가
                }
                    
                get_insert_stock_price_info(price_list[val0])
            # print("===============================")
            # print(price_list)
            # print("===============================")
            

            # self.tr_data = price_list;
            
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")
            # 종료 후 초기화 
            batch_history_upd("opt20002", e)
            
            

 
    def opt10081_req(self, tr_code, req_mame, tr_cnt):
        """
            opt10081 : 주식일봉차트조회요청 (30일치)
            - param
                - tr_ode   : TR목록 코드
                - req_mame : TR목록 응답 명
                - tr_cnt   : TR응답 카운트
        """
        res_names = ["종목코드", "일자", "시가", "고가", "저가", "현재가", "거래량", "거래대금"] # 응답에 대한 필요 항목명
        daily_price_list = {}
        max_len = 30
        # print("tr_cnt : ", tr_cnt)
        try :
            for i in range(max_len):
                if i == 0:  
                    code = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[0])  # 종목코드    
                    
                date_val    = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[1])  # 일자    
                open_price  = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[2])  # 시가    
                high_price  = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[3])  # 고가    
                low_price   = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[4])  # 저가    
                close_price = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[5])  # 현재가   
                vol         = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[6])  # 거래량   
                vol_price   = self.kiwoom.get_comm_data(tr_code, req_mame, i, res_names[7])  # 거래대금
                
                if open_price.strip() :
                    code = code.strip()
                    
                    daily_price_list[code] = {
                        'code'          : code              # 종목코드     
                        ,'date_val'     : date_val.strip()  # 일자     
                        ,'open_price'   : int(open_price)   # 시가     
                        ,'high_price'   : int(high_price)   # 고가     
                        ,'low_price'    : int(low_price)    # 저가     
                        ,'close_price'  : int(close_price)  # 현재가 
                        ,'volume'       : int(vol)          # 거래량 
                        ,'volume_price' : int(vol_price)    # 거래대금 
                    }
                    
                    get_all_stock_price_info(daily_price_list[code])
                    
                else :
                    i = max_len
                    log.debug(f"opt10081 : 주식일봉차트조회요청 (30일치) ==> code : {code}, open_price : {open_price}")
                    
                # print("===============================")
                # print(daily_price_list[code])
                # print("===============================")
                # 과부화 방지        
                time.sleep(0.3)
            
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")
            # 종료 후 초기화 
            batch_history_upd("opt10081", e)
 
 
 
 
    def opt10001_req(self, tr_code, req_mame, tr_cnt):
        """
            opt10001 : 주식기본정보요청 시가총액 업데이트
            - param
                - tr_ode   : TR목록 코드
                - req_mame : TR목록 응답 명
                - tr_cnt   : TR응답 카운트
        """
        res_names = ["종목코드", "종목명", "시가총액"] # 응답에 대한 필요 항목명
        daily_stock_total_price_list = {}
        # print("tr_cnt : ", tr_cnt)
        try :
            code            = self.kiwoom.get_comm_data(tr_code, req_mame, 0, res_names[0])  # 종목코드    
            code_name       = self.kiwoom.get_comm_data(tr_code, req_mame, 0, res_names[1])  # 종목명
            total_vol_price = self.kiwoom.get_comm_data(tr_code, req_mame, 0, res_names[2])  # 시가총액
            
            code = code.strip()
            daily_stock_total_price_list[code] = {
                'code'             : code                 # 종목코드     
                ,'code_name'       : code_name            # 종목명     
                ,'total_vol_price' : int(total_vol_price) # 시가총액 
            }
                
            get_upd_stock_all_price_info(daily_stock_total_price_list[code])
            
            # print("===============================")
            # print(daily_stock_total_price_list[code])
            # print("===============================")
                # 과부화 방지        
                # time.sleep(0.5)
            
        except pymysql.Error as e :
            print(f"DB_ERROR : {e}")
            # 종료 후 초기화 
            batch_history_upd("opt10001", e)
            



    '''
        ===================================================================================
        550. 재귀 호출 등 전문 셋팅 관련 하여 처리 구간
        ===================================================================================
    '''   
    def get_while_high_per_info(self) :
        """
            opt10026 : 고저PER요청
            - 해당 PER구분 전체  돌리기 (1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE)
            SetInputValue("PER구분"	,  "1");      
            SetInputValue("PER구분"	,  "2");      
            ................
            SetInputValue("PER구분"	,  "6");      
            
        """
        batch_name = "opt10026"
        batch_cnt = get_this_batch_today_run(batch_name)
        
        if 1 > int(batch_cnt) :        
            try :
                while int(self.per_val) < 7 :
                    self.get_high_per_info()
                    self.per_val =  int(self.per_val) + 1   
                    # print(f"self.per_val : {self.per_val}")
                    
            except pymysql.Error as e :
                print(f"DB_ERROR : {e}")
                # 종료 후 초기화 
                batch_history_upd(batch_name, e)    
                
            else :
                batch_name = "opt10026"
                batch_history_upd(batch_name)
                self.per_val = 1; 
        else :
            print(f"        {batch_name} : 고저PER요청 이미 당일배치 처리 완료................")     
            
            
    '''
        ===================================================================================
        600.기타 처리 구간
        ===================================================================================
    '''           
        
    def get_company_name(self, code):
        """
            업체명 가져오기
        """
        # 업체명 가져오기
        code_name = self.kiwoom.get_sotck_name(code)
        return code_name
        
        

    '''
        ===================================================================================
        9999.테스트 로직 처리 구간
        ===================================================================================
    '''
    
    def get_end_time(self):
        print("모든 배치처리완료")


if __name__ == "__main__":
    batch_main = BatchMain()
