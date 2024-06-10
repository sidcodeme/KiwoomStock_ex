-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.6.3-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 테이블 my_stock_world.batch_history 구조 내보내기
DROP TABLE IF EXISTS `batch_history`;
CREATE TABLE IF NOT EXISTS `batch_history` (
  `SEQ_NO` int(11) NOT NULL AUTO_INCREMENT COMMENT '순번',
  `BATCH_NAME` varchar(50) NOT NULL DEFAULT '0' COMMENT '배치명',
  `SUCCESS` int(11) NOT NULL DEFAULT 0 COMMENT '배치완료여부',
  `START_DTM` datetime NOT NULL DEFAULT sysdate() COMMENT '시작시간',
  `END_DTM` datetime DEFAULT NULL COMMENT '종료시간',
  `ERROR_MSG` varchar(400) DEFAULT NULL COMMENT '오류메세지',
  PRIMARY KEY (`SEQ_NO`) USING BTREE,
  KEY `SUCCESS` (`SUCCESS`) USING BTREE,
  KEY `START_DTM` (`START_DTM`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='배치 실행 여부 와 배치 처리 관련 내용 ';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 my_stock_world.opt10081 구조 내보내기
DROP TABLE IF EXISTS `opt10081`;
CREATE TABLE IF NOT EXISTS `opt10081` (
  `SEQ_NO` int(11) NOT NULL AUTO_INCREMENT COMMENT '순번',
  `code` varchar(8) NOT NULL COMMENT '종목코드',
  `date_val` varchar(8) NOT NULL COMMENT '일자',
  `open_price` int(11) NOT NULL COMMENT '시가',
  `high_price` int(11) NOT NULL COMMENT '고가',
  `low_price` int(11) NOT NULL COMMENT '저가',
  `close_price` int(11) NOT NULL COMMENT '현재가',
  `volume` int(11) NOT NULL COMMENT '거래량',
  `volume_price` int(11) NOT NULL COMMENT '거래대금',
  `INS_DTM` datetime NOT NULL DEFAULT sysdate() COMMENT '등록일시',
  `UPD_DTM` datetime DEFAULT NULL COMMENT '업데이트일시',
  PRIMARY KEY (`SEQ_NO`) USING BTREE,
  KEY `code_code_name` (`date_val`,`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT=' [ opt10081 : 주식일봉차트조회요청 ]';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 my_stock_world.opt20002 구조 내보내기
DROP TABLE IF EXISTS `opt20002`;
CREATE TABLE IF NOT EXISTS `opt20002` (
  `SEQ_NO` int(11) NOT NULL AUTO_INCREMENT COMMENT '순번',
  `code` varchar(8) NOT NULL COMMENT '종목코드',
  `code_name` varchar(50) NOT NULL COMMENT '종목명',
  `current_price` int(11) NOT NULL COMMENT '현재가',
  `pre_sign` int(11) NOT NULL COMMENT '전일대비기호',
  `pre_av` int(11) NOT NULL COMMENT '전일대비',
  `fluctuation_rate` float NOT NULL DEFAULT 0 COMMENT '등락률',
  `current_trading_volume` int(11) NOT NULL COMMENT '현재거래량',
  `sell_ask_price` int(11) NOT NULL COMMENT '매도호가',
  `bid_price` int(11) NOT NULL COMMENT '매수호가',
  `market_price` int(11) NOT NULL DEFAULT 0 COMMENT '시가',
  `high_price` int(11) NOT NULL COMMENT '고가',
  `low_price` int(11) NOT NULL COMMENT '저가',
  `total_vol_price` int(11) DEFAULT 0 COMMENT '시가총액',
  `DEL_STOCK` int(1) DEFAULT 0 COMMENT '시가총액500억이하(1:여, 0:뿌)',
  `supervising` int(1) DEFAULT 1 COMMENT '감리결과(0:정상, 1:{ 투자주의, 투자경고, 투자위험, 투자주의환기종목})',
  `INS_DTM` datetime NOT NULL DEFAULT sysdate() COMMENT '등록일시',
  `UPD_DTM` datetime DEFAULT NULL COMMENT '업데이트일시',
  PRIMARY KEY (`SEQ_NO`) USING BTREE,
  KEY `code_code_name` (`code`,`code_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT=' [ opt20002 : 업종별주가요청 ]';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 my_stock_world.per_info 구조 내보내기
DROP TABLE IF EXISTS `per_info`;
CREATE TABLE IF NOT EXISTS `per_info` (
  `seq_no` int(11) NOT NULL AUTO_INCREMENT COMMENT '시퀀스',
  `code` varchar(7) NOT NULL COMMENT '종목코드',
  `code_name` varchar(100) NOT NULL COMMENT '종목명',
  `per` float NOT NULL COMMENT 'PER',
  `current_price` varchar(25) NOT NULL COMMENT '현재가',
  `pre_sign` int(11) NOT NULL COMMENT '전일대비기호',
  `pre_av` varchar(10) NOT NULL COMMENT '전일대비',
  `fluctuation_rate` varchar(10) NOT NULL COMMENT '등락률',
  `current_trading_volume` int(11) NOT NULL COMMENT '현재거래량',
  `sell_ask_price` varchar(25) NOT NULL COMMENT '매도호가',
  `m_date` datetime NOT NULL DEFAULT sysdate() COMMENT '생성일시',
  `u_date` datetime DEFAULT NULL COMMENT '업데이트일시',
  `per_val` int(11) DEFAULT NULL COMMENT 'per요청코드',
  PRIMARY KEY (`seq_no`) USING BTREE,
  KEY `code` (`code`) USING BTREE,
  KEY `code_name` (`code_name`) USING BTREE,
  KEY `per` (`per`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='각 종목별\r\nPER구분 = 1:저PER, 2:고PER, 3:저PBR, 4:고PBR, 5:저ROE, 6:고ROE';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 my_stock_world.today_target_stock 구조 내보내기
DROP TABLE IF EXISTS `today_target_stock`;
CREATE TABLE `today_target_stock` (
	`seq_no` INT(11) NOT NULL AUTO_INCREMENT COMMENT '시퀀스',
	`code` VARCHAR(7) NOT NULL COMMENT '종목코드' COLLATE 'utf8mb3_general_ci',
	`code_name` VARCHAR(100) NOT NULL COMMENT '종목명' COLLATE 'utf8mb3_general_ci',
	`current_price` VARCHAR(25) NOT NULL COMMENT '현재가(종가)' COLLATE 'utf8mb3_general_ci',
	`buy_price` VARCHAR(25) NULL DEFAULT NULL COMMENT '매수가격' COLLATE 'utf8mb3_general_ci',
	`sell_price` VARCHAR(25) NULL DEFAULT NULL COMMENT '매도가격' COLLATE 'utf8mb3_general_ci',
	`m_date` DATETIME NOT NULL DEFAULT sysdate() COMMENT '생성일시',
	`success` INT(1) NULL DEFAULT '0' COMMENT '거래여부(0:대기, 1:매수, 2:매수성공, 3:매도, 4:매도성공)',
	`sell` INT(1) NULL DEFAULT '0' COMMENT '매도포인트(0: 대기, 1:매도)',
	`quantity` INT(5) NULL DEFAULT '0' COMMENT '주문수량',
	`order_no` VARCHAR(10) NULL DEFAULT NULL COMMENT '주문번호' COLLATE 'utf8mb3_general_ci',
  `sell_order_no` VARCHAR(50) NULL DEFAULT NULL COMMENT '매도 주문번호',
	PRIMARY KEY (`seq_no`) USING BTREE,
	INDEX `code` (`code`) USING BTREE,
	INDEX `code_name` (`code_name`) USING BTREE,
	INDEX `success` (`success`) USING BTREE,
	INDEX `buy_price` (`buy_price`) USING BTREE,
	INDEX `sell_price` (`sell_price`) USING BTREE
)
COMMENT='당일 거래 대상 종목'
COLLATE='utf8mb3_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

;


-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
