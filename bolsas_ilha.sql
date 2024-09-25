-- MySQL dump 10.13  Distrib 8.2.0, for macos13.5 (x86_64)
--
-- Host: localhost    Database: dbname
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Admin`
--

DROP TABLE IF EXISTS `Admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
INSERT INTO `Admin` VALUES (1,'Maria FD. Gomes','password%100','fatima.d.gomes@azores.gov.pt','2024-09-25 14:33:50','2024-09-25 14:33:50'),(2,'Daniela MBA. Gomes','password%100','daniela.mb.gomes@azores.gov.pt','2024-09-25 14:33:50','2024-09-25 14:33:50'),(3,'Rafael B. Pereira','scrypt:32768:8:1$JzPdfqhk2ZfUTWSE$ae2f53902aa761734619bd53993cc23d543fd67267aeaca4cc6457c10d5920b46505805d90bafba9e49cdbe6ce507e2372bbd95b86e357eb79c9d0b9a686cede','rafael.b.pereira@azores.gov.pt','2024-09-25 14:33:50','2024-09-25 15:31:44');
/*!40000 ALTER TABLE `Admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Bolsa`
--

DROP TABLE IF EXISTS `Bolsa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Bolsa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Bolsa`
--

LOCK TABLES `Bolsa` WRITE;
/*!40000 ALTER TABLE `Bolsa` DISABLE KEYS */;
INSERT INTO `Bolsa` VALUES (1,'Bolsa de Ilha São Miguel'),(2,'Bolsa de Ilha Terceira'),(3,'Bolsa de Ilha Santa Maria'),(4,'Bolsa de Ilha Faial'),(5,'Bolsa de Ilha Pico'),(6,'Bolsa de Ilha São Jorge'),(7,'Bolsa de Ilha Graciosa'),(8,'Bolsa de Ilha Flores'),(9,'Bolsa de Ilha Corvo');
/*!40000 ALTER TABLE `Bolsa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Bolsa_Escola`
--

DROP TABLE IF EXISTS `Bolsa_Escola`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Bolsa_Escola` (
  `bolsa_id` int NOT NULL,
  `escola_id` int NOT NULL,
  PRIMARY KEY (`bolsa_id`,`escola_id`),
  KEY `escola_id` (`escola_id`),
  CONSTRAINT `bolsa_escola_ibfk_1` FOREIGN KEY (`bolsa_id`) REFERENCES `Bolsa` (`id`),
  CONSTRAINT `bolsa_escola_ibfk_2` FOREIGN KEY (`escola_id`) REFERENCES `Escola` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Bolsa_Escola`
--

LOCK TABLES `Bolsa_Escola` WRITE;
/*!40000 ALTER TABLE `Bolsa_Escola` DISABLE KEYS */;
INSERT INTO `Bolsa_Escola` VALUES (1,43),(1,44),(1,45),(1,46),(1,47),(1,48),(1,49),(1,50),(1,51),(1,52),(1,53),(1,54),(1,55),(1,56),(1,57),(1,58),(1,59),(1,60),(1,61),(1,62),(1,63),(2,64),(2,65),(2,66),(2,67),(2,68),(2,69),(2,70),(3,71),(4,72),(4,73),(5,74),(5,75),(5,76),(6,77),(6,78),(6,79),(7,80),(8,81),(8,82),(9,83);
/*!40000 ALTER TABLE `Bolsa_Escola` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contrato`
--

DROP TABLE IF EXISTS `contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contrato` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` enum('indeterminado','termo resolutivo','ambos') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contrato`
--

LOCK TABLES `contrato` WRITE;
/*!40000 ALTER TABLE `contrato` DISABLE KEYS */;
INSERT INTO `contrato` VALUES (1,'indeterminado'),(2,'termo resolutivo'),(3,'ambos');
/*!40000 ALTER TABLE `contrato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Escola`
--

DROP TABLE IF EXISTS `Escola`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Escola` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Escola`
--

LOCK TABLES `Escola` WRITE;
/*!40000 ALTER TABLE `Escola` DISABLE KEYS */;
INSERT INTO `Escola` VALUES (43,'EBS NORDESTE'),(44,'EBI DA RIBEIRA GRANDE'),(45,'EBI DA MAIA'),(46,'EBI DE VILA DE CAPELAS'),(47,'ES LARANJEIRAS'),(48,'EBI DE ARRIFES'),(49,'Conservatório Regional de Ponta Delgada'),(50,'EBI ÁGUA DE PAU'),(51,'ES DA LAGOA'),(52,'ES ANTERO QUENTAL'),(53,'EBI ROBERTO IVENS'),(54,'ES DA RIBEIRA GRANDE'),(55,'EBI RABO DE PEIXE'),(56,'EBI PONTA GARÇA'),(57,'EBI DA LAGOA'),(58,'ES DOMINGOS REBELO'),(59,'EBI CANTO DA MAIA'),(60,'EBI DE GINETES'),(61,'EBS POVOAÇÃO'),(62,'EBS FURNAS'),(63,'EBS ARMANDO CÔRTES-RODRIGUES'),(64,'ES JERÓNIMO EMILIANO ANDRADE'),(65,'EBI DOS BISCOITOS'),(66,'ES VITORINO NEMÉSIO'),(67,'EBI DA PRAIA DA VITÓRIA'),(68,'EBS TOMÁS DE BORBA'),(69,'EBI DE ANGRA DO HEROÍSMO'),(70,'EBI FRANCISCO FERREIRA DRUMMOND'),(71,'EBS de Santa Maria'),(72,'EBI HORTA'),(73,'ES Manuel Arriaga'),(74,'EBS Lajes do Pico'),(75,'EBS S.Roque do Pico'),(76,'EBS da Madalena'),(77,'EBS das Velas'),(78,'EBS da Calheta'),(79,'EBI Topo'),(80,'EBS da Graciosa'),(81,'EBS das Flores'),(82,'EBS Lajes das Flores'),(83,'EBS Mouzinho Silveira');
/*!40000 ALTER TABLE `Escola` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `contacto` varchar(50) DEFAULT NULL,
  `deficiencia` varchar(255) DEFAULT NULL,
  `avaliacao_curricular` varchar(255) DEFAULT NULL,
  `prova_de_conhecimentos` varchar(255) DEFAULT NULL,
  `nota_final` decimal(5,2) DEFAULT NULL,
  `Bolsa_id` int DEFAULT NULL,
  `escola_id` int DEFAULT NULL,
  `tipo_contrato` enum('indeterminado','termo resolutivo') DEFAULT NULL,
  `estado` enum('livre','a aguardar resposta','negado','aceite') DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id`),
  KEY `Bolsa_id` (`Bolsa_id`),
  KEY `escola_id` (`escola_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`Bolsa_id`) REFERENCES `Bolsa` (`id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`escola_id`) REFERENCES `Escola` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_escola`
--

DROP TABLE IF EXISTS `user_escola`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_escola` (
  `user_id` int NOT NULL,
  `escola_id` int NOT NULL,
  `escola_priority_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`escola_id`),
  KEY `escola_id` (`escola_id`),
  CONSTRAINT `user_escola_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `user_escola_ibfk_2` FOREIGN KEY (`escola_id`) REFERENCES `Escola` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_escola`
--

LOCK TABLES `user_escola` WRITE;
/*!40000 ALTER TABLE `user_escola` DISABLE KEYS */;
INSERT INTO `user_escola` VALUES (7,43,1),(7,44,5),(7,45,2),(7,46,6),(7,47,3),(7,49,4),(7,54,7),(7,56,8),(7,59,9),(7,61,10),(8,43,1),(8,47,2),(8,48,7),(8,50,6),(8,51,3),(8,53,4),(8,55,5),(9,43,1),(9,45,2),(9,47,3),(9,49,4),(9,51,5),(9,53,6),(10,64,1),(10,65,3),(10,66,2),(10,67,4),(10,68,5),(10,69,7),(10,70,6);
/*!40000 ALTER TABLE `user_escola` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userbolsas`
--

DROP TABLE IF EXISTS `userbolsas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userbolsas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `Bolsa_id` int DEFAULT NULL,
  `contrato_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `Bolsa_id` (`Bolsa_id`),
  CONSTRAINT `userbolsas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `userbolsas_ibfk_2` FOREIGN KEY (`Bolsa_id`) REFERENCES `Bolsa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userbolsas`
--

LOCK TABLES `userbolsas` WRITE;
/*!40000 ALTER TABLE `userbolsas` DISABLE KEYS */;
INSERT INTO `userbolsas` VALUES (3,7,1,1),(4,8,1,1),(5,9,1,2),(6,10,2,1);
/*!40000 ALTER TABLE `userbolsas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `contacto` varchar(50) DEFAULT NULL,
  `deficiencia` varchar(255) DEFAULT NULL,
  `avaliacao_curricular` varchar(255) DEFAULT NULL,
  `prova_de_conhecimentos` varchar(255) DEFAULT NULL,
  `nota_final` decimal(5,2) DEFAULT NULL,
  `estado` enum('livre','a aguardar resposta','negado','aceite') DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (7,'João Rodrigues','091234','nao','14','18',16.00,'livre','nada a observar'),(8,'António Flores','10923','nao','15','16',15.50,'livre','nada.'),(9,'Paula Pires','1092','nao','15','14',14.50,'livre','nada a observar.'),(10,'Fátima Sousa','1092','nao','19','19',19.00,'livre','nada a observar.');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-25 16:31:03
