FID_CODES = {
    "10": "현재가",
    "11": "전일 대비",
    "12": "등락율",
    "13": "누적거래량",
    "14": "누적거래대금",
    "15": "거래량",
    "16": "시가",
    "17": "고가",
    "18": "저가",
    "20": "체결시간",
    "21": "호가시간",
    "23": "예상체결가",
    "24": "예상체결 수량",
    "25": "전일대비기호",
    "26": "전일거래량 대비(계약,주)",
    "27": "(최우선)매도호가",
    "28": "(최우선)매수호가",
    "29": "거래대금 증감",
    "30": "전일거래량 대비(비율)",
    "31": "거래회전율",
    "32": "거래비용",
    "41": "매도호가1",
    "42": "매도호가1",
    "43": "매도호가3",
    "44": "매도호가4",
    "45": "매도호가5",
    "46": "매도호가6",
    "47": "매도호가7",
    "48": "매도호가8",
    "49": "매도호가9",
    "50": "매도호가10",
    "51": "매수호가1",
    "52": "매수호가2",
    "53": "매수호가3",
    "54": "매수호가4",
    "55": "매수호가5",
    "56": "매수호가6",
    "57": "매수호가7",
    "58": "매수호가8",
    "59": "매수호가9",
    "60": "매수호가10",
    "61": "매도호가 수량1",
    "62": "매도호가 수량2",
    "63": "매도호가 수량3",
    "64": "매도호가 수량4",
    "65": "매도호가 수량5",
    "66": "매도호가 수량6",
    "67": "매도호가 수량7",
    "68": "매도호가 수량8",
    "69": "매도호가 수량9",
    "70": "매도호가 수량10",
    "71": "매수호가 수량1",
    "72": "매수호가 수량2",
    "73": "매수호가 수량3",
    "74": "매수호가 수량4",
    "75": "매수호가 수량5",
    "76": "매수호가 수량6",
    "77": "매수호가 수량7",
    "78": "매수호가 수량8",
    "79": "매수호가 수량9",
    "80": "매수호가 수량10",
    "81": "매도호가 직전대비1",
    "82": "매도호가 직전대비2",
    "83": "매도호가 직전대비3",
    "84": "매도호가 직전대비4",
    "85": "매도호가 직전대비5",
    "86": "매도호가 직전대비6",
    "87": "매도호가 직전대비7",
    "88": "매도호가 직전대비8",
    "89": "매도호가 직전대비9",
    "90": "매도호가 직전대비10",
    "91": "매수호가 직전대비1",
    "92": "매수호가 직전대비2",
    "93": "매수호가 직전대비3",
    "94": "매수호가 직전대비4",
    "95": "매수호가 직전대비5",
    "96": "매수호가 직전대비6",
    "97": "매수호가 직전대비7",
    "98": "매수호가 직전대비8",
    "99": "매수호가 직전대비9",
    "100": "매수호가 직전대비10",
    "101": "매도호가 건수1",
    "102": "매도호가 건수2",
    "103": "매도호가 건수3",
    "104": "매도호가 건수4",
    "105": "매도호가 건수5",
    "111": "매수호가 건수1",
    "112": "매수호가 건수2",
    "113": "매수호가 건수3",
    "114": "매수호가 건수4",
    "115": "매수호가 건수5",
    "121": "매도호가 총잔량",
    "122": "매도호가 총잔량 직전대비",
    "123": "매도호가 총 건수",
    "125": "매수호가 총잔량",
    "126": "매수호가 총잔량 직전대비",
    "127": "매수호가 총 건수",
    "128": "순매수잔량(총매수잔량-총매도잔량)",
    "129": "매수비율",
    "131": "시간외 매도호가 총잔량",
    "132": "시간외 매도호가 총잔량 직전대비",
    "135": "시간외 매수호가 총잔량",
    "136": "시간외 매수호가 총잔량 직전대비",
    "137": "호가 순잔량",
    "138": "순매도잔량(총매도잔량-총매수잔량)",
    "139": "매도비율",
    "141": "매도 거래원1",
    "142": "매도 거래원2",
    "143": "매도 거래원3",
    "144": "매도 거래원4",
    "145": "매도 거래원5",
    "146": "매도 거래원 코드1",
    "147": "매도 거래원 코드2",
    "148": "매도 거래원 코드3",
    "149": "매도 거래원 코드4",
    "150": "매도 거래원 코드5",
    "151": "매수 거래원1",
    "152": "매수 거래원2",
    "153": "매수 거래원",
    "154": "매수 거래원4",
    "155": "매수 거래원5",
    "156": "매수 거래원 코드1",
    "157": "매수 거래원 코드2",
    "158": "매수 거래원 코드3",
    "159": "매수 거래원 코드4",
    "160": "매수 거래원 코드5",
    "161": "매도 거래원 수량1",
    "162": "매도 거래원 수량2",
    "163": "매도 거래원 수량3",
    "164": "매도 거래원 수량4",
    "165": "매도 거래원 수량5",
    "166": "매도 거래원별 증감1",
    "167": "매도 거래원별 증감2",
    "168": "매도 거래원별 증감3",
    "169": "매도 거래원별 증감4",
    "170": "매도 거래원별 증감5",
    "171": "매수 거래원 수량1",
    "172": "매수 거래원 수량2",
    "173": "매수 거래원 수량3",
    "174": "매수 거래원 수량4",
    "175": "매수 거래원 수량5",
    "176": "매수 거래원별 증감1",
    "177": "매수 거래원별 증감2",
    "178": "매수 거래원별 증감3",
    "179": "매수 거래원별 증감4",
    "180": "매수 거래원별 증감5",
    "181": "미결제 약정 전일대비",
    "182": "이론가",
    "183": "시장베이시스",
    "184": "이론베이시스",
    "185": "괴리도",
    "186": "괴리율",
    "187": "내재가치",
    "188": "시간가치",
    "189": "내재변동성(I.V.)",
    "190": "델타",
    "191": "감마",
    "192": "베가",
    "193": "세타",
    "194": "로",
    "195": "미결제약정",
    "196": "미결제 증감",
    "197": "KOSPI200",
    "200": "예상체결가 전일종가 대비",
    "201": "예상체결가 전일종가 대비 등락율",
    "214": "장시작예상잔여시간",
    "215": "장운영구분",  # (0:장시작전, 2:장종료전, 3:장시작, 4,8:장종료, 9:장마감)
    "216": "투자자별 ticker",
    "219": "선물 최근 월물지수",
    "228": "체결강도",
    "238": "예상체결가 전일종가 대비기호",
    "246": "시초미결제 약정수량",
    "247": "최고미결제 약정수량",
    "248": "최저미결제 약정수량",
    "251": "상한종목수",
    "252": "상승종목수",
    "253": "보합종목수",
    "254": "하한종목수",
    "255": "하락종목수",
    "256": "거래형성 종목수",
    "257": "거래형성 비율",
    "261": "외국계매도추정합",
    "262": "외국계매도추정합 변동",
    "263": "외국계매수추정합",
    "264": "외국계매수추정합 변동",
    "267": "외국계순매수추정합",
    "268": "외국계순매수 변동",
    "271": "매도거래원색깔1",
    "272": "매도거래원색깔2",
    "273": "매도거래원색깔3",
    "274": "매도거래원색깔4",
    "275": "매도거래원색깔5",
    "281": "매수거래원색깔1",
    "282": "매수거래원색깔2",
    "284": "매수거래원색깔4",
    "285": "매수거래원색깔5",
    "290": "장구분",
    "291": "예상체결가",
    "292": "예상체결량",
    "293": "예상체결가 전일대비기호",
    "294": "예상체결가 전일대비",
    "295": "예상체결가 전일대비등락율",
    "299": "전일거래량대비예상체결률",
    "302": "종목명",
    "307": "기준가",
    "311": "시가총액(억)",
    "337": "거래소구분 (1, KOSPI, 2:KOSDAQ, 3:OTCCBB, 4:KOSPI200선물, 5:KOSPI200옵션, 6:개별주식옵션, 7:채권)",
    "391": "기준가대비 시고등락율",
    "392": "기준가대비 고가등락율",
    "393": "기준가대비 저가등락율",
    "397": "주식옵션거래단위",
    "621": "LP매도호가 수량1",
    "622": "LP매도호가 수량2",
    "623": "LP매도호가 수량3",
    "624": "LP매도호가 수량4",
    "625": "LP매도호가 수량5",
    "626": "LP매도호가 수량6",
    "627": "LP매도호가 수량7",
    "628": "LP매도호가 수량8",
    "629": "LP매도호가 수량9",
    "630": "LP매도호가 수량10",
    "631": "LP매수호가 수량1",
    "632": "LP매수호가 수량2",
    "633": "LP매수호가 수량3",
    "634": "LP매수호가 수량4",
    "635": "LP매수호가 수량5",
    "636": "LP매수호가 수량6",
    "637": "LP매수호가 수량7",
    "638": "LP매수호가 수량8",
    "639": "LP매수호가 수량9",
    "640": "LP매수호가 수량10",
    "691": "K,O 접근도 (ELW조기종료발생 기준가격, 지수)",
    "900": "주문수량",
    "901": "주문가격",
    "902": "미체결수량",
    "903": "체결누계금액",
    "904": "원주문번호",
    "905": "주문구분",
    "906": "매매구분",
    "907": "매도수구분",
    "908": "주문시간",
    "909": "체결번호",
    "910": "체결가",
    "911": "체결량",
    "912": "주문업무분류",  # (JJ:주식주문, FJ:선물옵션, JG:주식잔고, FG:선물옵션잔고)
    "913": "주문상태",  # (10:원주문, 11:정정주문, 12:취소주문, 20:주문확인, 21:정정확인, 22:취소확인, 90-92:주문거부)
    "914": "단위체결가",
    "915": "단위체결량",
    "916": "대출일",
    "917": "신용구분",
    "918": "만기일",
    "930": "보유수량",
    "931": "매입단가",
    "932": "총매입가",
    "933": "주문가능수량",
    "938": "당일매매 수수료",
    "939": "당일매매세금",
    "945": "당일순매수량",
    "946": "매도/매수구분",
    "950": "당일 총 매도 손익",
    "951": "예수금",
    "957": "신용금액",
    "958": "신용이자",
    "959": "담보대출수량",
    "990": "당일실현손익(유가)",
    "991": "당일실현손익률(유가)",
    "992": "당일실현손익(신용)",
    "993": "당일실현손익률(신용)",
    "8019": "손익율",
    "9001": "종목코드",
    "9201": "계좌번호",
    "9203": "주문번호",
    "9205": "관리자사번"
}

"""
    에러 코드 표 
"""
ERROR_CODE_LIST = {
    "0"    : "정상처리"					            # OP_ERR_NONE 				    정상처리
    ,"-10"  : "실패"						        # OP_ERR_FAIL 				    실패
    ,"-100" : "사용자정보교환실패"			        # OP_ERR_LOGIN 				    사용자정보교환실패
    ,"-101" : "서버접속실패"					    # OP_ERR_CONNECT 			    서버접속실패
    ,"-102" : "버전처리실패"					    # OP_ERR_VERSION 			    버전처리실패
    ,"-103" : "개인방화벽실패"				        # OP_ERR_FIREWALL 			    개인방화벽실패
    ,"-104" : "메모리보호실패"				        # OP_ERR_MEMORY				    메모리보호실패
    ,"-105" : "함수입력값오류"				        # OP_ERR_INPUT 				    함수입력값오류
    ,"-106" : "통신연결종료"					    # OP_ERR_SOCKET_CLOSED 		    통신연결종료
    ,"-200" : "시세조회과부하"				        # OP_ERR_SISE_OVERFLOW 		    시세조회과부하
    ,"-201" : "전문작성초기화실패"				    # OP_ERR_RQ_STRUCT_FAIL 		전문작성초기화실패
    ,"-202" : "전문작성입력값오류"				    # OP_ERR_RQ_STRING_FAIL 		전문작성입력값오류
    ,"-203" : "데이터없음."					        # OP_ERR_NO_DATA 			    데이터없음.
    ,"-204" : "조회가능한종목수초과"			    # OP_ERR_OVER_MAX_DATA 		    조회가능한종목수초과
    ,"-205" : "데이터수신실패"				        # OP_ERR_DATA_RCV_FAIL 		    데이터수신실패
    ,"-206" : "조회가능한FID수초과"			        # OP_ERR_OVER_MAX_FID 		    조회가능한FID수초과
    ,"-207" : "실시간해제오류"				        # OP_ERR_REAL_CANCEL 		    실시간해제오류
    ,"-300" : "입력값오류"					        # OP_ERR_ORD_WRONG_INPUT 	    입력값오류
    ,"-301" : "계좌비밀번호없음"				    # OP_ERR_ORD_WRONG_ACCTNO 	    계좌비밀번호없음
    ,"-302" : "타인계좌사용오류"				    # OP_ERR_OTHER_ACC_USE 		    타인계좌사용오류
    ,"-303" : "주문가격이20억원을초과"			    # OP_ERR_MIS_2BILL_EXC 		    주문가격이20억원을초과
    ,"-304" : "주문가격이50억원을초과"			    # OP_ERR_MIS_5BILL_EXC 		    주문가격이50억원을초과
    ,"-305" : "주문수량이총발행주수의1%초과오류"	# OP_ERR_MIS_1PER_EXC 		    주문수량이총발행주수의1%초과오류
    ,"-306" : "주문수량은총발행주수의3%초과오류"	# OP_ERR_MIS_3PER_EXC 		    주문수량은총발행주수의3%초과오류
    ,"-307" : "주문전송실패"					    # OP_ERR_SEND_FAIL 			    주문전송실패
    ,"-308" : "주문전송과부하"				        # OP_ERR_ORD_OVERFLOW   		주문전송과부하
    ,"-309" : "주문수량300계약초과"			        # OP_ERR_MIS_300CNT_EXC 		주문수량300계약초과
    ,"-310" : "주문수량500계약초과"			        # OP_ERR_MIS_500CNT_EXC 		주문수량500계약초과
    ,"-340" : "계좌정보없음"					    # OP_ERR_ORD_WRONG_ACCTINFO 	계좌정보없음
    ,"-500" : "종목코드없음"					    # OP_ERR_ORD_SYMCODE_EMPTY 	    종목코드없음
}

"""
    화면별 번호 정의
    - 조회 (10000 ~ 20000)
    - 매수 (30000 ~ 40000)
    - 매도 (50000 ~ 60000)
    - 실시간 조회(70000 ~ 80000)
    - 기타(90000 ~ 10000)
"""
SCREEN_NO_LIST = {
    # =================== 조회  ========================="""
    "TAB1_주식시가총액"        : "11000"
    ,"TAB1_실시간주식정보조회" : "11001"
    ,"TAB1_잔고내역요청"       : "11002"
    
    ,"TAB2_종목현재가검색"     : "12000"
    ,"TAB2_종목가격전체정보"   : "12001"
    ,"TAB2_예수금"             : "12002"
      
    ,"TAB3_주문정보조회"       : "13000"
    
    
    # =================== 매수  ========================="""
    ,"TAB1_자동매수주문"    : "22000"
    ,"TAB2_매수주문"        : "22001"
    ,"TAB2_매수취소"        : "22002"
    ,"TAB2_매수정정"        : "22003"
    
    
    # =================== 매도  ========================="""
    ,"TAB1_자동매도주문"     : "52000"
    ,"TAB2_매도주문"         : "52001"
    ,"TAB2_매도취소"         : "52002"
    ,"TAB2_매도정정"         : "52003"
    ,"TAB1_자동매도신호주문" : "52004"
    
    
    # =================== 실시간  ========================="""
    
    
    # =================== 기타  ========================="""
    ,"BATCH_고저PER"           : "90000"
    ,"BATCH_업종별주가요청"    : "90001"
    ,"BATCH_종목가격전체정보"  : "90002"
    ,"BATCH_주식시가총액"      : "90003"
    ,"BATCH_감리구분"          : "90004"
    
    ,"ETC"    : "99999"
}


RES_NAMES = {
    'OPT10001': ['종목코드',              
                 '종목명',
                 '결산월',
                 '액면가',
                 '자본금',
                 '상장주식',
                 '신용비율',
                 '연중최고',
                 '시가총액',
                 '시가총액비중',
                 '외인소진률',
                 '대용가'
                 'PER',
                 'EPS',
                 'ROE',
                 'PBR',
                 'EV',
                 'BPS',
                 '매출액',
                 '영업이익',
                 '당기순이익',
                 '250최고',
                 '250최저',
                 '시가',
                 '고가',
                 '저가',
                 '상한가',
                 '하한가',
                 '기준가',
                 '예상체결가',
                 '예상체결수량',
                 '250최고가일',
                 '250최고가대비율',
                 '250최저가일',
                 '250최저가대비율',
                 '현재가',
                 '대비기호',
                 '전일대비',
                 '등락율',
                 '거래량',
                 '거래대비',
                 '액면가단위',
                 '유통주식',
                 '유통비율',
                 ],
}

def get_screen_no(search_val):
    """
        사용할 화면 번호 검색
        - param
            - search_val : 스크린명칭 ( ex) TAB2의 주식검색 ==> TAB2_주식검색
        - return
            - screen_no
            
        ## 화면정의
            - 조회 (10000 ~ 20000)
            - 매수 (30000 ~ 40000)
            - 매도 (50000 ~ 60000)
            - 실시간 조회(70000 ~ 80000)
    """
    value = [value for key, value in SCREEN_NO_LIST.items() if key == search_val]
    return value[0]

def get_error_code(search_val):
    """
        에러 코드 표
        - param
            - search_val : 에러코드
        - return
            - 에러코드 설명
    """
    value = [value for key, value in ERROR_CODE_LIST.items() if key == search_val]
    return value[0]


# print(get_screen_no("ETC"))


# 찾고자 하는 항목명의 FID를 찾아주는 함수
def get_fid(search_value):
    """
        사용예
        fid = get_fid("고가")
        # fid = 17
    """
    keys = [key for key, value in FID_CODES.items() if value == search_value]
    return keys[0]


# 발급 받은 LINE 토큰을 붙여 넣습니다.
RSI_STRATEGY_MESSAGE_TOKEN = "TOKEN"