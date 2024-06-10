''' 
    상위 폴더 의 모듈 가져오기위함 ==================================
'''
import os
import sys

from util.made_price import *



sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import datetime
from numpy import mat




sid = int(1000000)
sid = int(int(sid) / 5)
print(sid)

order_q = int(sid / 81600)
print(f"order : {order_q} ")
    
now = datetime.datetime.today().isoweekday()
print(now)
result = "sdfg"
print(0 if "정상" == result else 1)


"""
    기하 평균 계산 코드
    
    ^ == **
    
"""
ret = str(0.6534 ** (1 / 6) - 1)[:8]
ret = float(ret) * 100



print(f"ret = {ret}")


str = "[RC4058] 모의투자 장종료"
print(str.find("장종료"))


a = -3.2799552071668533
if float(a) <= -3 :
    print("작다")
else :
    print("크다")
    

# price = 77400
# market_price = int(int(price) *  0.97)
# print(market_price)
# print(" made_buy_price : ", made_buy_price(market_price))

# fluctuation_rate = (int(market_price) / int(price)) * 100 - 100
# print(fluctuation_rate)