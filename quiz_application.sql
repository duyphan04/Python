CREATE DATABASE  IF NOT EXISTS `quiz_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `quiz_app`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: quiz_app
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;



-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `name` varchar(50) NULL,
  `college` varchar(100) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NULL,
  `role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('nguyen',NULL,'12@gmail.com','123','USER'),('khanh',NULL,'1@gmail.com','123','USER'),('dang','HCMUTE','22110295@student.hcmute.edu.vn','123','USER'),('hoa',NULL,'2@gmail.com','123','USER'),('vy',NULL,'3@gmail.com','123','USER'),('duy','HCMUTE','duyprovn987@gmail.com','123','ADMIN');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;


--
-- Table structure for table `quiz`
--

DROP TABLE IF EXISTS `quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz` (
  `id` int NOT NULL AUTO_INCREMENT,
  `eid` VARCHAR(255) NULL,
  `title` varchar(100) NULL,
  `total` int NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

ALTER TABLE `quiz` ADD INDEX `idx_eid` (`eid`);


--
-- Dumping data for table `quiz`
--

LOCK TABLES `quiz` WRITE;
/*!40000 ALTER TABLE `quiz` DISABLE KEYS */;
INSERT INTO `quiz` VALUES (1,'5b141b8009cf0','Php & Mysql',10,'2024-04-18 02:38:41'),(2,'5b141f1e8399e','Ip Networking',11,'2024-04-22 07:38:07');
/*!40000 ALTER TABLE `quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `eid` VARCHAR(255) NULL,
  `qid` VARCHAR(255) NULL,
  `qns` varchar(50) NOT NULL,
  `choice` int DEFAULT NULL,
  `sn` int DEFAULT NULL,
  PRIMARY KEY (`qns`),
  FOREIGN KEY (eid) REFERENCES quiz (eid) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

ALTER TABLE `questions` ADD INDEX `idx_qid` (`qid`);


--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES ('5b141b8009cf0','5b141d72d7a1c','A function in PHP which starts with __ (double und',4,7),('5b141f1e8399e','5b1422651fdde','How long is an IPv6 address?',4,1),('5b141f1e8399e','5b14226663cf4','If you use either Telnet or FTP, which is the high',4,5),('5b141b8009cf0','5b141d71ddb46','PHP files have a default file extension of.',4,3),('5b141f1e8399e','5byc00rji2n5s','superman',4,11),('5b141f1e8399e','5b1422677371f','To test the IP stack on your local host, which IP ',4,10),('5b141b8009cf0','5b141d712647f','What does PHP stand for?',4,1),('5b141f1e8399e','5b142266c525c','What is the maximum number of IP addresses that ca',4,7),('5b141f1e8399e','5b142265b5d08','Where is a hub specified in the OSI model?',4,3),('5b141f1e8399e','5b1422669481b','Which of the following is a layer 2 protocol used ',4,6),('5b141f1e8399e','5b1422661d93f','Which of the following is private IP address?',4,4),('5b141b8009cf0','5b141d7260b7d','Which of the following PHP statements will output ',4,5),('5b141b8009cf0','5b141d721a738','Which of the looping statements is/are supported b',4,4),('5b141b8009cf0','5b141d7345176','Which of the methods are used to manage result set',4,9),('5b141b8009cf0','5b141d72a6fa1','Which one of the following function is capable of ',4,6),('5b141b8009cf0','5b141d737ddfc','Which one of the following functions can be used t',4,10),('5b141b8009cf0','5b141d731429b','Which one of the following statements is used to c',4,8),('5b141f1e8399e','5b14226574ed5','Which protocol does DHCP use at the Transport laye',4,2),('5b141b8009cf0','5b141d718f873','Who is the father of PHP?',4,2),('5b141f1e8399e','5b1422674286d','You have an interface on a router with the IP addr',4,9),('5b141f1e8399e','5b14226711d91','You need to subnet a network that has 5 subnets, e',4,8);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `options`
--

DROP TABLE IF EXISTS `options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `options` (
  `id` int NOT NULL AUTO_INCREMENT,
  `qid` varchar(50) NULL,
  `option` varchar(5000) NULL,
  `optionid` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (qid) REFERENCES questions (qid) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

ALTER TABLE `options` ADD INDEX `idx_optionid` (`optionid`);

--
-- Dumping data for table `options`
--

LOCK TABLES `options` WRITE;
/*!40000 ALTER TABLE `options` DISABLE KEYS */;
INSERT INTO `options` VALUES (9,'5b141d712647f','Personal Home Page','5b141d71485b9'),(10,'5b141d712647f','Private Home Page','5b141d71485dc'),(11,'5b141d712647f','PreVARCHAR(255) HyperVARCHAR(255) Processor','5b141d71485e0'),(12,'5b141d712647f','Preprocessor Home Page','5b141d71485e4'),(13,'5b141d718f873','Rasmus Lerdorf','5b141d71978be'),(14,'5b141d718f873','Willam Makepiece','5b141d71978cc'),(15,'5b141d718f873','Drek Kolkevi','5b141d71978d1'),(16,'5b141d718f873','List Barely','5b141d71978d4'),(17,'5b141d71ddb46','.html','5b141d71e5f2b'),(18,'5b141d71ddb46','.ph','5b141d71e5f3c'),(19,'5b141d71ddb46','.php','5b141d71e5f43'),(20,'5b141d71ddb46','.xml','5b141d71e5f48'),(21,'5b141d721a738','for loop','5b141d7222820'),(22,'5b141d721a738','do-while loop','5b141d722282f'),(23,'5b141d721a738','foreach loop','5b141d7222880'),(24,'5b141d721a738','All of the above','5b141d7222884'),(25,'5b141d7260b7d','echo (â€œHello Worldâ€);','5b141d7268b8a'),(26,'5b141d7260b7d','print (â€œHello Worldâ€);','5b141d7268b95'),(27,'5b141d7260b7d','printf (â€œHello Worldâ€);','5b141d7268b98'),(28,'5b141d7260b7d','All of the above','5b141d7268b9a'),(29,'5b141d72a6fa1','file()','5b141d72aefcb'),(30,'5b141d72a6fa1','arr_file()','5b141d72aefd8'),(31,'5b141d72a6fa1','arrfile()','5b141d72aefdc'),(32,'5b141d72a6fa1','file_arr()','5b141d72aefe0'),(33,'5b141d72d7a1c','Magic Function','5b141d72dfa7b'),(34,'5b141d72d7a1c','Inbuilt Function','5b141d72dfa85'),(35,'5b141d72d7a1c','Default Function','5b141d72dfa88'),(36,'5b141d72d7a1c','User Defined Function','5b141d72dfa8b'),(37,'5b141d731429b','CREATE TABLE table_name (column_name column_type);','5b141d731c234'),(38,'5b141d731429b','CREATE table_name (column_type column_name);','5b141d731c242'),(39,'5b141d731429b','CREATE table_name (column_name column_type);','5b141d731c248'),(40,'5b141d731429b','CREATE TABLE table_name (column_type column_name);','5b141d731c24b'),(41,'5b141d7345176','get_array() and get_row()','5b141d734cd10'),(42,'5b141d7345176','fetch_array() and fetch_row()','5b141d734cd1b'),(43,'5b141d7345176','get_array() and get_column()','5b141d734cd1d'),(44,'5b141d7345176','fetch_array() and fetch_column()','5b141d734cd20'),(45,'5b141d737ddfc','explode()','5b141d73858d0'),(46,'5b141d737ddfc','implode()','5b141d73858df'),(47,'5b141d737ddfc','concat()','5b141d73858e3'),(48,'5b141d737ddfc','concatenate()','5b141d73858e8'),(49,'5b1422651fdde','32 bits','5b1422654ab3a'),(50,'5b1422651fdde','128 bytes','5b1422654ab48'),(51,'5b1422651fdde','64 bits','5b1422654ab4d'),(52,'5b1422651fdde','16 bytes','5b1422654ab51'),(53,'5b14226574ed5','IP','5b1422657d052'),(54,'5b14226574ed5','TCP','5b1422657d05f'),(55,'5b14226574ed5','UDP','5b1422657d064'),(56,'5b14226574ed5','ARP','5b1422657d069'),(57,'5b142265b5d08','Session layer','5b142265c09e3'),(58,'5b142265b5d08','Physical layer','5b142265c09f5'),(59,'5b142265b5d08','Data Link layer','5b142265c09fa'),(60,'5b142265b5d08','Application layer','5b142265c09ff'),(61,'5b1422661d93f','12.0.0.1','5b14226635df5'),(62,'5b1422661d93f','168.172.19.39','5b14226635e04'),(63,'5b1422661d93f','172.15.14.36','5b14226635e09'),(64,'5b1422661d93f','192.168.24.43','5b14226635e0d'),(65,'5b14226663cf4','Application','5b1422666bf2b'),(66,'5b14226663cf4','Presentation','5b1422666bf39'),(67,'5b14226663cf4','Session','5b1422666bf3e'),(68,'5b14226663cf4','Transport','5b1422666bf42'),(69,'5b1422669481b','VTP','5b1422669c8dc'),(70,'5b1422669481b','STP','5b1422669c8ea'),(71,'5b1422669481b','RIP','5b1422669c8ef'),(72,'5b1422669481b','CDP','5b1422669c8f3'),(73,'5b142266c525c','14','5b142266cd353'),(74,'5b142266c525c','15','5b142266cd361'),(75,'5b142266c525c','16','5b142266cd365'),(76,'5b142266c525c','30','5b142266cd369'),(77,'5b14226711d91','255.255.255.192','5b14226719fa0'),(78,'5b14226711d91','255.255.255.224','5b14226719fb1'),(79,'5b14226711d91','255.255.255.240','5b14226719fb7'),(80,'5b14226711d91','255.255.255.248','5b14226719fbb'),(81,'5b1422674286d','6','5b1422674a9ee'),(82,'5b1422674286d','8','5b1422674aa01'),(83,'5b1422674286d','30','5b1422674aa06'),(84,'5b1422674286d','32','5b1422674aa0b'),(85,'5b1422677371f','127.0.0.0','5b1422677b3e9'),(86,'5b1422677371f','1.0.0.127','5b1422677b3f7'),(87,'5b1422677371f','127.0.0.1','5b1422677b3fc'),(88,'5b1422677371f','127.0.0.255','5b1422677b400'),(102,'5byc00rji2n5s','1','5bmwdm3kszigr'),(103,'5byc00rji2n5s','2','5btwprn0d3dks'),(104,'5byc00rji2n5s','3','5b7ihs2jkfa7u'),(105,'5byc00rji2n5s','4','5b7a96vkybgz7');
/*!40000 ALTER TABLE `options` ENABLE KEYS */;
UNLOCK TABLES;



--
--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer` (
  `qid` VARCHAR(255) NULL,
  `ansid` VARCHAR(255) NULL,
  FOREIGN KEY (`qid`) REFERENCES `questions` (`qid`) ON DELETE CASCADE,
  FOREIGN KEY (`ansid`) REFERENCES `options` (`optionid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES ('5b13ed3a6e006','5b13ed3a9436a'),('5b13ed72489d8','5b13ed7263d70'),('5b141d712647f','5b141d71485b9'),('5b141d718f873','5b141d71978be'),('5b141d71ddb46','5b141d71e5f43'),('5b141d721a738','5b141d7222884'),('5b141d7260b7d','5b141d7268b9a'),('5b141d72a6fa1','5b141d72aefcb'),('5b141d72d7a1c','5b141d72dfa7b'),('5b141d731429b','5b141d731c234'),('5b141d7345176','5b141d734cd1b'),('5b141d737ddfc','5b141d73858df'),('5b1422651fdde','5b1422654ab51'),('5b14226574ed5','5b1422657d064'),('5b142265b5d08','5b142265c09f5'),('5b1422661d93f','5b14226635e0d'),('5b14226663cf4','5b1422666bf2b'),('5b1422669481b','5b1422669c8ea'),('5b142266c525c','5b142266cd369'),('5b14226711d91','5b14226719fb1'),('5b1422674286d','5b1422674a9ee'),('5b1422677371f','5b1422677b3fc'),('5b9ksc9xtdo2z','5b7begf0453l8'),('5bs9ezlgxyigh','5b4vgkt8lmrt5'),('5bl6sxvwtnarr','5b6675c7f0umf'),('5b7j5g1i4i7fc','5bep6ejuntqcs'),('5byc00rji2n5s','5btwprn0d3dks');
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaderboard`
--

DROP TABLE IF EXISTS `leaderboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaderboard` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `score` int DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`email`) REFERENCES `user`(`email`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Dumping data for table `leaderboard`
--

LOCK TABLES `leaderboard` WRITE;
/*!40000 ALTER TABLE `leaderboard` DISABLE KEYS */;
INSERT INTO `leaderboard` VALUES (1,'22110295@student.hcmute.edu.vn',2,'2024-04-15 15:15:53'),(5,'1@gmail.com',3,'2024-04-17 20:58:25'),(6,'2@gmail.com',4,'2024-04-17 20:58:25'),(7,'3@gmail.com',6,'2024-04-17 20:58:25'),(8,'22110295@student.hcmute.edu.vn',2,'2024-04-17 21:34:10'),(9,'duyprovn987@gmail.com',8,'2024-04-17 20:58:25'),(10,'duyprovn987@gmail.com',4,'2024-04-17 20:58:25'),(11,'duyprovn987@gmail.com',0,'2024-04-18 10:59:34'),(12,'22110295@student.hcmute.edu.vn',4,'2024-04-18 11:14:37'),(13,'duyprovn987@gmail.com',1,'2024-04-18 11:32:29'),(14,'duyprovn987@gmail.com',4,'2024-04-21 14:08:27'),(15,'duyprovn987@gmail.com',11,'2024-04-21 15:03:56'),(16,'duyprovn987@gmail.com',9,'2024-04-21 15:07:13'),(17,'duyprovn987@gmail.com',4,'2024-04-21 15:28:05'),(18,'3@gmail.com',15,'2024-04-22 14:06:34'),(19,'3@gmail.com',5,'2024-04-22 14:31:34'),(20,'duyprovn987@gmail.com',10,'2024-04-22 14:33:22');
/*!40000 ALTER TABLE `leaderboard` ENABLE KEYS */;
UNLOCK TABLES;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-25 19:29:04
