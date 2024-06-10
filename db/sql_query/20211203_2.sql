-- UPDATE today_target_stock SET success = 1, sell_price = 1 WHERE CODE = '123';

SELECT *
FROM today_target_stock
WHERE SUCCESS > 0 
	AND SUCCESS NOT IN(9, 4, 9)
--   AND SUCCESS <2 4
ORDER BY success, m_date desc
;


SELECT *
FROM today_target_stock
-- WHERE SUCCESS > 0 
--   AND SUCCESS < 4
ORDER BY SUCCESS
;

SELECT *
FROM SEARCH_NUM
;

-- 조건검색
-- UPDATE SEARCH_NUM SET NO = '5';
-- COMMIT;


-- SELECT code, quantity, order_no FROM today_target_stock WHERE success = 1  AND DATE(m_date) < DATE(NOW());
-- SELECT COUNT(1) FROM today_target_stock WHERE success = 2 or success = 1 AND sell = 0;
-- 
-- SELECT CODE, QUANTITY FROM today_target_stock WHERE success = 2 AND sell = 1 AND DATE(m_date) = DATE(NOW()) AND buy_price > 0;

SELECT CODE, CODE_NAME, CURRENT_PRICE FROM today_target_stock WHERE success = 0 AND DATE(m_date) = DATE(NOW()) AND replace(CURRENT_PRICE, '-', '') > 0 LIMIT 5;

-- COMMIT;
-- 
-- 
-- DELETE FROM today_target_stock;
-- COMMIT;
-- UPDATE today_target_stock SET SUCCESS = 4, sell =1, sell_price = '7210' WHERE CODE = '201490';
-- COMMIT;

-- UPDATE today_target_stock SET success = 9 WHERE CODE = 065450 AND order_no =0145499;
-- COMMIT;


-- SELECT COUNT(1) FROM today_target_stock WHERE success = 2;
-- SELECT CODE, CODE_NAME, CURRENT_PRICE FROM today_target_stock WHERE success = 0 AND DATE(m_date) = DATE(NOW()) AND replace(CURRENT_PRICE, '-', '') > 0 LIMIT 5
-- ;
-- 
-- SELECT *
-- FROM today_target_stock
-- WHERE success = 0 
--   AND DATE(m_date) < DATE(NOW())
-- ;
-- 
-- -- update today_target_stock set success = '4' WHERE success = 2  AND DATE(m_date) < DATE(NOW());
-- -- COMMIT;
-- -- 
-- 
-- SELECT *
-- FROM today_target_stock
-- ;
-- 



