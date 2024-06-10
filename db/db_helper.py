import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pymysql
from util.enc_dec import *

""" 전역 변수 영역 """

def get_db_connection():
    try :
        conn = pymysql.connect(host="localhost", user=db_user(), password=db_pass(), db="my_stock_world", charset="utf8")
    except pymysql.Error as e :
            print(f"DB_ERROR : {e}")
    
    return conn

        
def get_update_order_stock(code, success):
    """ 
        당일 거래 대상 종목
        거래여부(0:대기, 1:매수, 2:매수성공, 3:매도, 4:매도성공)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # sql_insert_query = """ UPDATE today_target_stock SET success = %s, buy_price = %s WHERE code = %s """
    
    if success == "1" or success == "2" :
        sql_insert_query =  """ UPDATE today_target_stock SET success = %s WHERE code = %s """
        
    elif success == "3" or success == "4" :
        sql_insert_query =  """ UPDATE today_target_stock SET success = %s WHERE code = %s """
                            
    val = (success, code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()
        
def get_update_order_stock(code, success):
    """ 
        당일 거래 대상 종목
        거래여부(0:대기, 1:매수, 2:매수성공, 3:매도, 4:매도성공)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # sql_insert_query = """ UPDATE today_target_stock SET success = %s, buy_price = %s WHERE code = %s """
    
    if success == "1" or success == "2" :
        sql_insert_query =  """ UPDATE today_target_stock SET success = %s WHERE code = %s """
        
    elif success == "3" or success == "4" :
        sql_insert_query =  """ UPDATE today_target_stock SET success = %s WHERE code = %s """
                            
    val = (success, code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()
        
        
def get_update_order_buy_price_stock(code, price, quantity):
    """ 
        [매수] 당일 거래 대상 종목
        거래여부(0:대기, 1:매수, 2:매수성공, 3:매도, 4:매도성공)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # print(f"code : {code}, price : {price}")
    sql_insert_query =  """ UPDATE today_target_stock SET buy_price = %s, quantity = %s  WHERE code = %s """
                            
    val = (price, quantity, code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()
    
    
        
def get_update_order_sell_point_stock(code):
    """ 
        [매도] 매도포인트(0: 대기, 1:매도)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql_insert_query =  """ UPDATE today_target_stock SET sell = 1 WHERE code = %s and sell = 0 """
                            
    val = (code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()    
    
    
        
def get_end_update_order_sell_point_stock():
    """ 
        [장종료 매도] 매도포인트(0: 대기, 1:매도)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql_insert_query =  """ UPDATE today_target_stock SET sell = 1 WHERE success = 2 and sell = 0 """
                            
    cur.execute(sql_insert_query)
    conn.commit()

    cur.close()
    conn.close()    
    
    
        
def get_update_order_buy_last_stock(code, success, pirce, order_no):
    """ 
        [매수] 대상종목 매수 
        거래여부(0:대기, 1:매수, 2:매수성공, 3:매도, 4:매도성공)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql_insert_query =  """ UPDATE today_target_stock SET success = %s, buy_price = %s, order_no = %s WHERE code = %s AND success != 9 """
                            
    val = (success, pirce, order_no, code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()    
        
def get_update_cancel_order_buy_stock(code, order_no):
    """ 
        [매수취소]
        거래여부(9:기타처리)
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql_insert_query =  """ UPDATE today_target_stock SET success = 9, order_no = %s WHERE code = %s """
                            
    val = (order_no, code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()    
    
        
def get_update_order_sell_last_stock(code, success, pirce, order_no):
    """ 
        [매도] 대상종목 매도 
        거래여부(0:대기, 1:매수, 2:매수성공, 3:매도, 4:매도성공)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql_insert_query =  """ UPDATE today_target_stock SET success = %s, sell_price = %s, sell_order_no = %s WHERE code = %s """
                            
    val = (success, pirce, order_no, code)
    
    cur.execute(sql_insert_query, val)
    conn.commit()

    cur.close()
    conn.close()    
    
    
    
def get_insert_today_stock_list(stock_data):
    """ 
        당일 거래 대상 종목

    """
    conn = get_db_connection()
    cur = conn.cursor()

    ''' 1영업일전 날의 매매거래 일어나지 않은 종목을 9로 업데이트 해준다.'''    
    sql_last_day_stock_update = " UPDATE today_target_stock SET success = 9 WHERE success = 0 AND DATE(m_date) < DATE(NOW()) "
    cur.execute(sql_last_day_stock_update)

    
    sql_eixist = " SELECT COUNT(1) FROM today_target_stock WHERE CODE = %s AND DATE(m_date) = DATE(NOW()) "
    cnt_val = (stock_data['code'])
    cur.execute(sql_eixist, cnt_val)
    resultlist = cur.fetchall()
    
    aready_cnt = "0";
    for result in resultlist :
        aready_cnt = result[0]
        
    # print(aready_cnt)
    if "0" == str(aready_cnt):
        sql_insert_query =  """INSERT INTO today_target_stock(code, code_name, current_price) VALUES (%(code)s, %(code_name)s, %(price)s)"""
        # print(stock_data)
                                
        val = stock_data
        
        cur.execute(sql_insert_query, val)
        conn.commit()
    #     print("not_aready : {}, {}".format(stock_data['code'], stock_data['code_name']))
        
    # print("1 record inserted, ID: ", cur.lastrowid)
    cur.close()
    conn.close()
    
    
def get_stock_target_code_info():
    """ 
        당일 대상종목 (종목코드, 종가(현재가)) 가져오기
        - return
            - 종가(현재가)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql_eixist = " SELECT CODE, CODE_NAME, CURRENT_PRICE FROM today_target_stock WHERE success = 0 AND DATE(m_date) = DATE(NOW()) AND replace(CURRENT_PRICE, '-', '') > 0 LIMIT 5 "
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
      
    cur.close()
    conn.close()
    
    return resultlist
    
    
def get_point_sell_stock_code_info(code):
    """ 
        매수 종목 가져오기
        - return
            - 종가(현재가)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE, CODE_NAME, buy_price FROM today_target_stock WHERE code = %s AND success = 2 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT CODE, CODE_NAME, buy_price FROM today_target_stock WHERE code = %s AND success = 2 AND buy_price > 0 "
    
    val = (code)
    cur.execute(sql_eixist, val)
    resultlist = cur.fetchall()
    
    cur.close()
    conn.close()
          
    return resultlist
    
    
def get_real_time_stock_code_info():
    """ 
        실시간 보유 종목에 대한 특정정보 가져오기
        - return
            - 종가(현재가)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE FROM today_target_stock WHERE success = 2 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT CODE FROM today_target_stock WHERE success = 2 AND buy_price > 0 "
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
    
    cur.close()
    conn.close()
          
    return resultlist
    

        
def get_call_sell_sign_point_info():
    """ 
        매수 종목 가져오기
        - return
            - 종가(현재가)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND buy_price > 0 "
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
     
    cur.close()
    conn.close()
         
    return resultlist
        
def get_call_sell_count_info():
    """ 
        매수 종목 총건수 가져오기
        - return
            - 현재 매수한 종목 건수
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT COUNT(1) FROM today_target_stock WHERE success = 2 or success = 1 AND sell = 0 "
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
    
    cur.close()
    conn.close()
          
    return resultlist
        
def get_buy_unsuccess_order_count_info():
    """ 
        전 영업일 매수 주문 미체결 종목 리스트
        - return
            - 튜플형 ((종목코드, 종목수량, 종목주문번호),)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT code, quantity, order_no FROM today_target_stock WHERE success = 1  AND DATE(m_date) < DATE(NOW())"
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
    
    cur.close()
    conn.close()
          
    return resultlist
        
        
def get_buy_unsuccess_order_update(code, order_no):
    """ 
        전 영업일 미체결 상태의 매수 주문 종목 취소 처리 후 DB 업데이트   
        - param 
            - code     : 종목 코드
            - order_no : 종문 주문 번호
    """
    
    conn = get_db_connection()
    cur = conn.cursor()

    sql_eixist = " UPDATE today_target_stock SET success = 9 WHERE code = %s AND order_no = %s "
    
    val = (code, order_no)
        
    cur.execute(sql_eixist, val)
    conn.commit()

    cur.close()
    conn.close()
        
        
def get_balance_info_update_buy_stock_info(code, purchase_price):
    """ 
        인터넷이 끊어진 후 잔고조회시 보유 잔고를 기반으로 매수여부 DB 업데이트
        - param 
            - code     : 종목 코드
            - order_no : 종문 주문 번호
    """
    
    conn = get_db_connection()
    cur = conn.cursor()

    sql_eixist = " UPDATE today_target_stock SET success = 2, buy_price = %s WHERE code = %s AND success = 1 "
    
    val = (purchase_price, code)
        
    cur.execute(sql_eixist, val)
    conn.commit()

    cur.close()
    conn.close()


def get_search_number():
    """ 
       조건검색 식 번호 가져오기(사용자가 입력함)
        - return
            - 조건번호
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT no FROM SEARCH_NUM"
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
     
    cur.close()
    conn.close()
         
    return resultlist

def get_sell_rate():
    """ 
       조건검색 식 번호 가져오기(사용자가 입력함)
        - return
            - 조건번호
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # sql_eixist = " SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0 "
    sql_eixist = " SELECT win_rate, lose_rate FROM sell_rate"
        
    cur.execute(sql_eixist)
    resultlist = cur.fetchall()
     
    cur.close()
    conn.close()
         
    return resultlist



def get_sell_rate_update(win_rate, lose_rate):
    """ 
        매매 기준 손절 익절 퍼센트 업데이트 
        - param 
            - win_rate  : 익절
            - lose_rate : 손절
    """
    
    conn = get_db_connection()
    cur = conn.cursor()

    sql_eixist = " UPDATE sell_rate SET win_rate = %s, lose_rate = %s"
    
    val = (win_rate, lose_rate)
        
    cur.execute(sql_eixist, val)
    conn.commit()

    cur.close()
    conn.close()