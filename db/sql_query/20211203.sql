SELECT *
FROM opt10081
WHERE  CODE = '201490'
ORDER BY DATE_vAL DESC
LIMIT 1
;

SELECT current_price FROM opt20002 WHERE  CODE = '201490' 

SELECT DATE(NOW()) FROM DUAL;


SELECT *
FROM today_target_stock
;

DELETE FROM today_target_stock;
COMMIT;


SELECT CODE, CURRENT_PRICE, m_date FROM today_target_stock WHERE DATE(m_date) = DATE(NOW()) AND replace(CURRENT_PRICE, '-', '') > 0
;


 SELECT COUNT(1) FROM today_target_stock WHERE CODE = '001800' AND DATE(m_date) = DATE(NOW());
 
 UPDATE today_target_stock a SET sell = 0, SUCCESS = 2 WHERE CODE = '142280';
 COMMIT;
 
  SELECT CODE FROM today_target_stock WHERE success = 2 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0;
  
  SELECT CODE, CODE_NAME, CURRENT_PRICE FROM today_target_stock WHERE  replace(CURRENT_PRICE, '-', '') > 0  LIMIT 5;