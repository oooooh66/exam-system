-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        12.3.2-MariaDB - MariaDB Server
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 导出  表 exam_system.tb_biz_index 结构
CREATE TABLE IF NOT EXISTS `tb_biz_index` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `org_id` varchar(20) NOT NULL COMMENT '机构号',
  `org_nm` varchar(100) NOT NULL COMMENT '机构名',
  `area_name` varchar(100) DEFAULT NULL COMMENT '地区名称',
  `org_lvl` varchar(10) DEFAULT NULL COMMENT '机构级别：1-村行，2-网点',
  `sheet_nm` varchar(100) DEFAULT NULL COMMENT 'sheet标签名',
  `sheet_sort` int(11) DEFAULT NULL COMMENT 'sheet标签顺序',
  `table_name` varchar(100) DEFAULT NULL COMMENT '业务表名',
  `table_sort` int(11) DEFAULT NULL COMMENT '业务表顺序',
  `label_type` varchar(100) DEFAULT NULL COMMENT '指标类别：户数类/余额类/占比类',
  `label_sort` int(11) DEFAULT NULL COMMENT '指标类别顺序',
  `busi_type` varchar(100) DEFAULT NULL COMMENT '业务类别：liability-负债，asset-资产/信贷',
  `busi_sort` int(11) DEFAULT NULL COMMENT '业务类别顺序',
  `col_nm` varchar(200) NOT NULL COMMENT '列名（指标名称）',
  `col_sort` int(11) DEFAULT NULL COMMENT '列名顺序',
  `num_fmt` varchar(10) DEFAULT '2' COMMENT '数值展示格式：1-百分比，2-普通数值，3-万元',
  `curr_num` decimal(38,4) DEFAULT NULL COMMENT '当前值',
  `data_dt` date NOT NULL COMMENT '数据日期（月份）',
  `exam_flag` tinyint(4) NOT NULL DEFAULT 0 COMMENT '抽题标签：1-可抽题，0-不抽题',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_org` (`org_id`),
  KEY `idx_busi_type` (`busi_type`),
  KEY `idx_data_dt` (`data_dt`),
  KEY `idx_exam_flag` (`exam_flag`),
  KEY `idx_org_busi_dt` (`org_id`,`busi_type`,`data_dt`),
  KEY `idx_col_nm` (`col_nm`)
) ENGINE=InnoDB AUTO_INCREMENT=559 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='业务指标题库表（含抽题标签exam_flag）';

-- 正在导出表  exam_system.tb_biz_index 的数据：~558 rows (大约)
DELETE FROM `tb_biz_index`;
INSERT INTO `tb_biz_index` (`id`, `org_id`, `org_nm`, `area_name`, `org_lvl`, `sheet_nm`, `sheet_sort`, `table_name`, `table_sort`, `label_type`, `label_sort`, `busi_type`, `busi_sort`, `col_nm`, `col_sort`, `num_fmt`, `curr_num`, `data_dt`, `exam_flag`, `created_at`, `updated_at`) VALUES
	(1, '659000', '六枝', '贵州地区', '1', '2.2.2贷款业务-首拓期限结构', 8, '机构首拓期限结构', 1, '余额', 1, '余额', 1, '余额', 1, '3', 197559764.2732, '2026-05-31', 0, '2026-07-02 17:05:56', '2026-07-02 17:05:56'),
	(2, '659000', '六枝', '贵州地区', '1', '2.2.2贷款业务-首拓期限结构', 8, '机构首拓期限结构', 1, '户数', 2, '户数', 2, '户数', 2, '2', 3246.7600, '2026-05-31', 0, '2026-07-02 17:05:56', '2026-07-02 17:05:56'),
	(3, '659000', '六枝', '贵州地区', '1', '2.2.2贷款业务-首拓期限结构', 8, '机构首拓期限结构', 1, '短期', 3, '余额', 1, '当前', 1, '3', 80267789.7304, '2026-05-31', 0, '2026-07-02 17:05:56', '2026-07-02 17:05:56'),
	(4, '659000', '六枝', '贵州地区', '1', '2.2.2贷款业务-首拓期限结构', 8, '机构首拓期限结构', 1, '短期', 3, '余额', 1, '同比', 2, '3', 35276362.5304, '2026-05-31', 0, '2026-07-02 17:05:56', '2026-07-02 17:05:56'),
	(5, '659000', '六枝', '贵州地区', '1', '2.2.2贷款业务-首拓期限结构', 8, '机构首拓期限结构', 1, '短期', 3, '余额', 1, '占比', 3, '1', 1.2758, '2026-05-31', 0, '2026-07-02 17:05:56', '2026-07-02 17:05:56');