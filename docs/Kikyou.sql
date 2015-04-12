-- MySQL dump 10.13  Distrib 5.5.30, for Linux (x86_64)
--
-- Host: localhost    Database: Kikyou
-- ------------------------------------------------------
-- Server version	5.5.30-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Kikyou`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Kikyou` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `Kikyou`;

--
-- Table structure for table `grpInfo`
--

DROP TABLE IF EXISTS `grpInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grpInfo` (
  `grp_id` int(11) NOT NULL AUTO_INCREMENT,
  `grp_name` varchar(30) NOT NULL,
  `grp_status` tinyint(4) NOT NULL,
  `app_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`grp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `srvInfo`
--

DROP TABLE IF EXISTS `srvInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `srvInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `grp_id` int(11) NOT NULL,
  `srv_name` varchar(20) NOT NULL,
  `ip_vlan` varchar(15) NOT NULL,
  `ip_wlan` varchar(15) DEFAULT NULL,
  `core_num` tinyint(4) NOT NULL,
  `mem_size` float DEFAULT NULL,
  `disk_size` int(11) NOT NULL,
  `os_version` varchar(100) DEFAULT NULL,
  `prize` float DEFAULT NULL,
  `purchase_date` datetime DEFAULT NULL,
  `refund_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `srvStatus`
--

DROP TABLE IF EXISTS `srvStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `srvStatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipaddr` varchar(15) DEFAULT NULL,
  `cpu_load5` float DEFAULT NULL,
  `cpu_load10` float DEFAULT NULL,
  `cpu_load15` float DEFAULT NULL,
  `mem_used` float DEFAULT NULL,
  `tcp_estab` mediumint(9) NOT NULL,
  `eth_in` smallint(6) NOT NULL,
  `eth_out` smallint(6) NOT NULL,
  `disk_used_root` tinyint(4) NOT NULL,
  `disk_used_data` tinyint(4) NOT NULL,
  `inode_used_root` tinyint(4) NOT NULL,
  `inode_used_data` tinyint(4) NOT NULL,
  `ts` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger tgr_status_insert
after insert on srvStatus for each row
begin
replace into tmpStatus
values (new.ipaddr,new.cpu_load5,new.cpu_load10,new.cpu_load15,new.mem_used,new.tcp_estab,new.eth_in,new.eth_out,new.disk_used_root,new.disk_used_data,new.inode_used_root,new.inode_used_data,new.ts);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `tmpStatus`
--

DROP TABLE IF EXISTS `tmpStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmpStatus` (
  `ipaddr` varchar(15) NOT NULL DEFAULT '',
  `cpu_load5` float DEFAULT NULL,
  `cpu_load10` float DEFAULT NULL,
  `cpu_load15` float DEFAULT NULL,
  `mem_used` float DEFAULT NULL,
  `tcp_estab` mediumint(9) DEFAULT NULL,
  `eth_in` smallint(6) NOT NULL,
  `eth_out` smallint(6) NOT NULL,
  `disk_used_root` tinyint(4) NOT NULL,
  `disk_used_data` tinyint(4) NOT NULL,
  `inode_used_root` tinyint(4) NOT NULL,
  `inode_used_data` tinyint(4) NOT NULL,
  `ts` datetime DEFAULT NULL,
  PRIMARY KEY (`ipaddr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-24 10:50:50
