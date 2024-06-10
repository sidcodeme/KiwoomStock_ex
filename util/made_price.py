
# price = 130871
# print("0 ==> ", (price * 0.03))
# price = price - (price * 0.03)
# print("1 ==> ", int(price))
# print("2 ==> ", int(price / 10) * 10 + 10)
# price = int(price / 10) * 10 + 10
# print("3 ==> ", int(price))

def get_fluctuation_rate(market_price, price):
    """
        수익률(%) = (오르거나 떨어진 현재 주식 가격 / 내가 매수한 주식 가격) * 100 - 100
    """
    fluctuation_rate = (int(market_price) / int(price)) * 100 - 100
    
    return fluctuation_rate


def get_quantity(order_sid, buy_price):
    """ 
        주문수량 

    Args:
        order_sid ([type]): [시드머니]]
        buy_price ([type]): [-3% 된 매수금액]

    Returns:
        [int]: [수량]
    """
    quantity = int(int(order_sid) / int(buy_price))

    return quantity
 

def made_buy_price(price) : 
    """ 
        매수주문 호가 
        주식 가격 기준가 와 호가 단위 처리
        - 1,000원                  미만    1원
        - 1,000원   이상 5,000원   미만    5원
        - 5,000원   이상 10,000원  미만	  10원
        - 10,000원  이상 50,000원  미만	  50원
        - 50,000원  이상 100,000원 미만	 100원
        - 100,000원 이상 500,000원 미만	 500원
        - 500,000원 이상                1000원
    """
    
    price = int(int(price) *  0.99) # -1% 에 주문 하기위함
    
    if price < 1000 :
        price_detect = int(price / 10) * 10 + 1
        
    elif price >= 1000 and price < 5000 :
        price_detect = int(price / 10) * 10 + 5
        price_detect -= 5
        
    elif price >= 5000 and price < 10000 :
        price_detect = int(price / 10) * 10
        
    elif price >= 10000 and price < 50000 :
        price_detect = int(price / 100) * 100 + 50
        price_detect -= 50
        
    elif price >= 50000 and price < 100000 :
        price_detect = int(price / 100) * 100
        
    elif price >= 100000 and price < 500000 :
        price_detect = int(price / 1000) * 1000 + 500
        
    elif price <= 500000 :
        price_detect = int(price / 1000) * 1000
        
        
    # print("price = ", price_detect)
    return price_detect






def made_sell_price(price) : 
    """ 
        매도주문 호가 
        주식 가격 기준가 와 호가 단위 처리
        - 1,000원                  미만    1원
        - 1,000원   이상 5,000원   미만    5원
        - 5,000원   이상 10,000원  미만	  10원
        - 10,000원  이상 50,000원  미만	  50원
        - 50,000원  이상 100,000원 미만	 100원
        - 100,000원 이상 500,000원 미만	 500원
        - 500,000원 이상                1000원
    """
    
    if price < 1000 :
        price_detect = int(price / 10) * 10 + 1
        
    elif price >= 1000 and price < 5000 :
        price_detect = int(price / 10) * 10 + 5
        price_detect += 5
        
    elif price >= 5000 and price < 10000 :
        price_detect = int(price / 10) * 10
        
    elif price >= 10000 and price < 50000 :
        price_detect = int(price / 100) * 100 + 50
        price_detect += 50
        
    elif price >= 50000 and price < 100000 :
        price_detect = int(price / 100) * 100
        
    elif price >= 100000 and price < 500000 :
        price_detect = int(price / 1000) * 1000 + 500
        
    elif price <= 500000 :
        price_detect = int(price / 1000) * 1000
        
        
    # print("price = ", price_detect)
    return price_detect


def made_sell_low_price(price) : 
    """ 
        매수주문 호가 
        주식 가격 기준가 와 호가 단위 처리
        - 1,000원                  미만    1원
        - 1,000원   이상 5,000원   미만    5원
        - 5,000원   이상 10,000원  미만	  10원
        - 10,000원  이상 50,000원  미만	  50원
        - 50,000원  이상 100,000원 미만	 100원
        - 100,000원 이상 500,000원 미만	 500원
        - 500,000원 이상                1000원
    """

    if price < 1000 :
        price_detect = int(price / 10) * 10 + 1
        
    elif price >= 1000 and price < 5000 :
        price_detect = int(price / 10) * 10 + 5
        price_detect -= 5
        
    elif price >= 5000 and price < 10000 :
        price_detect = int(price / 10) * 10
        
    elif price >= 10000 and price < 50000 :
        price_detect = int(price / 100) * 100 + 50
        price_detect -= 50
        
    elif price >= 50000 and price < 100000 :
        price_detect = int(price / 100) * 100
        
    elif price >= 100000 and price < 500000 :
        price_detect = int(price / 1000) * 1000 + 500
        
    elif price <= 500000 :
        price_detect = int(price / 1000) * 1000
        
        
    # print("price = ", price_detect)
    return price_detect



# made_sell_price(74900)

def get_order_quantity(codes_data) :
    order = {}
    for code, code_name, price in codes_data :
         buy_price = made_buy_price(price)
         
         order ={
             'code'   : code
             ,'price' : buy_price
         }

    return order