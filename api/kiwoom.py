from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QAxWidget):
    # 기본 계좌번호 
    def __init__(self):
        super().__init__()
        self._make_kiwoom_instance()

    # Kiwoom class가 키움 증권 API OCX 컨트롤러 할 수있도록 등록
    def _make_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
    
    
    # 로그인 실행     
    def comm_connect(self):
        """
            로그인된 사용자의 계좌 정보
            - param
            - return : OnEventConnect.connect 호출 
        """
        self.dynamicCall("CommConnect()")


    def get_login_info(self, tag):
        """
            로그인한 사용자 정보를 반환하는 메서드
            - param 
                - tag: 
                    - ACCOUNT_CNT          : 보유계좌 갯수를 반환합니다.
                    - ACCLIST 또는 ACCNO   : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
                    - USER_ID              : 사용자 ID를 반환합니다.
                    - USER_NAME            : 사용자 이름을 반환합니다.
                    - GetServerGubun       : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실거래서버)
                    - KEY_BSECGB           : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
                    - FIREW_SECGB          : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)
            - return
                - tag에 대한 데이터 값
        """
        data = self.dynamicCall("GetLoginInfo(QString)", tag)

        if tag == "ACCNO":
            return data.split(';')[:-1]
        else:
            return data

    
    def get_login_check(self):
        data = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        return data.split(';')[:-1]
    
    def get_server_zone(self, tag="GetServerGubun"):
        """
            현재 서버의 종류 표시
            - param 
                - tag:  
                    - GetServerGubun       : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실거래서버)
            - return 
                - 0: 운영서버
                - 1: 모의투자 서버
        """
        server_zone = "모의투자 서버 접속" if self.dynamicCall("GetLoginInfo(Qstring)", tag) == "1" else "운영서버"
        return server_zone
    
    def get_kospi_w_kosdaq_list(self, tag="0"):
        """
            시장 정보 를 기준으로 상품 목록 가져오기
            - param 
                - tag: 
                    - 0	 코스피
                    - 3	 ELW
                    - 4	 뮤추얼펀드
                    - 5  신주인수권
                    - 6  리츠
                    - 8	 ETF
                    - 9	 하이얼펀드
                    - 10 코스닥
                    - 30 K-OTC
                    - 50 코넥스
            - return 
                - 각 시장 의 주식 목록
        """
        stock_code_name_list = []
        codes = self.dynamicCall("GetCodeListByMarket(Qstring)", tag)
        stock_code_list = codes.split(';')[:-1]
        
        for i in stock_code_list:
            code_name = self.get_sotck_name(i)
            stock_code_name_list.append(i + " : " +  code_name)
            
        return stock_code_name_list
        
    
    def get_sotck_name(self, code):
        """
            해당 코드의 대한 회사 명 반환
            - param :
                - code : 주식 업체 코드

            - Returns:
                - 회사명 리턴
        """
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        # print(code_name)
        return code_name
    
    def com_rq_data(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        """
            TR을 서버로 송신합니다.
            - param 
               - sRQName   : 사용자 구분 요청 명
               - sTrCode   : Tran명 입력
               - nPrevNext : 0:조회, 2:연속
               - sScreenNo : 4자리의 화면번호
            - return: None
            - ERROR_CODE 
                - OP_ERR_SISE_OVERFLOW   : 과도한 시세조회로 인한 통신불가
                - OP_ERR_RQ_STRUCT_FAIL  : 입력 구조체 생성 실패
                - OP_ERR_RQ_STRING_FAIL  : 요청전문 작성 실패
                - OP_ERR_NONE            : 정상처리
        """
        self.dynamicCall("CommRqData(QString, QString, int, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)  
        

    def get_comm_data(self, sTrCode, sRQName, idx, get_data_name):
        """
            수신 데이터를 반환한다.
            - param 
               - sTrCode       : Tran명 입력
               - sRQName       : 사용자 구분 요청 명
               - idx           : data index
               - get_data_name : 수신 데이터 명칭
            - return: 
                - data : 해당 값의 수신 데이타 
        """
        data = self.dynamicCall("GetCommData(Qstring, Qstring, int, Qstring)", sTrCode, sRQName, idx, get_data_name) 
        return data
    
    def get_comm_real_data(self, sTrCode, nFid):
        """
            실시간 수신 데이터를 반환한다.
            - param 
               - strCode : 종목코드
               - nFid    : 실시간 아이템
            - return: 
                - data 실시간 수신 데이타 수신 데이터
        """
        data = self.dynamicCall("GetCommRealData(Qstring, int)", sTrCode, nFid) 
        return data
    

    def set_inputvalue(self, id, value):
        """
            TR 입력값을 설정하는 메서드
            - param 
                - id ([type]): [description]
                - value ([type]): [description]
        """
        self.dynamicCall("SetInputValue(QString, QString)", id, value)
        
    def get_send_order(self, sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo=""):
        """
            주식 주문을 서버로 전송한다.
            - param
                - sRQName     : 사용자 구분 요청 명
                - sScreenNo   : 화면번호[4]
                - sAccNo      : 계좌번호[10]
                - nOrderType  : 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
                - sCode,      : 주식종목코드
                - nQty        : 주문수량
                - nPrice      : 주문단가
                - sHogaGb     : 거래구분
                    - 00:지정가
                    - 03:시장가
                    - 05:조건부지정가 
                    - 06:최유리지정가 
                    - 07:최우선지정가
                    - 10:지정가IOC
                    - 13:시장가IOC
                    - 16:최유리IOC
                    - 20:지정가FOK
                    - 23:시장가FOK
                    - 26:최유리FOK
                    - 61:장전시간외종가
                    - 62:시간외단일가
                    - 81:장후시간외종가
                - sOrgOrderNo : 원주문번호
                    
            ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 
              장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다
            ex) 시장가 주문시 : "nPrice = 0", 취소시 "nPrice = 0"
        """     
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo])
        
        
    def get_chejan_data(self, fid):
        """
            체결&잔고 데이터를 반환한다
            - param
                - fid ([type]): 입력값
            - return
                - 요청 fid에 대한 값
        """
        data = self.dynamicCall("GetChejanData(int)", fid)
        return data
    
    
    def set_real_reg(self, strScreenNo, strCodeList, strFidList, strRealType):
        """
            종목별 실시간 등록
            - param
                - strScreenNo : 실시간 등록할 화면 번호
                - strCodeList : 실시간 등록할 종목코드(복수종목가능 – “종목1;종목2;종목3;….”)
                - strFidList  : 실시간 등록할 FID(“FID1;FID2;FID3;…..”)
                - strRealType : “0”, “1” 타입
                
            - Descript
              - 
                    strRealType이 “0” 으로 하면 같은화면에서 다른종목 코드로 실시간 등록을 하게 되면 마지막
                    에 사용한 종목코드만 실시간 등록이 되고 기존에 있던 종목은 실시간이 자동 해지됨.
                    “1”로 하면 같은화면에서 다른 종목들을 추가하게 되면 기존에 등록한 종목도 함께 실시간 시세
                    를 받을 수 있음.
                    꼭 같은 화면이여야 하고 최초 실시간 등록은 “0”으로 하고 이후부터 “1”로 등록해야함.
                
        """
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", strScreenNo, strCodeList, strFidList, strRealType)
        
            
    def set_real_remove(self, strScreenNo, strDelCode):
        """
            설명 종목별 실시간 해제.
            - param
                - strScreenNo : 실시간 등록할 화면 번호
                - strDelCode  : 실시간 등록할 종목코드(복수종목가능 – “종목1;종목2;종목3;….”)
        """
        self.ocx.dynamicCall("SetRealRemove(QString, QString)", strScreenNo, strDelCode)
        
        
        
    def dis_connect_real_data(self, strScreenNo):
        """ 
            화면 내 모든 화면번호와 관련된 리얼데이터 요청을 제거한다.
            - param
                - strScreenNo : 화면번호
        """
        self.dynamicCall("DisConnectRealData(QString)", strScreenNo)
        
    def get_master_construction(self, code):
        """ 
            감리구분         
            입력한 종목코드에 해당하는 종목의 감리구분을 전달합니다.
            - (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)
        """
        result = self.dynamicCall("GetMasterConstruction(QString)", code)
        return result