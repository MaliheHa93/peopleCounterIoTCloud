-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3308
-- Generation Time: Feb 23, 2023 at 03:31 PM
-- Server version: 8.0.18
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartcity`
--

-- --------------------------------------------------------

--
-- Table structure for table `operators`
--

DROP TABLE IF EXISTS `operators`;
CREATE TABLE IF NOT EXISTS `operators` (
  `opID` int(250) NOT NULL AUTO_INCREMENT,
  `vehicleId` int(250) NOT NULL,
  `number_passengers` int(250) NOT NULL,
  PRIMARY KEY (`opID`),
  KEY `vehicleId` (`vehicleId`),
  KEY `opID` (`opID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
CREATE TABLE IF NOT EXISTS `vehicles` (
  `ID` int(100) NOT NULL AUTO_INCREMENT,
  `Round` varchar(250) COLLATE utf8mb4_bin NOT NULL,
  `camId` int(250) NOT NULL,
  `Direction` varchar(250) COLLATE utf8mb4_bin NOT NULL,
  `num_passengers` int(250) NOT NULL,
  `opID` int(250) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `opID` (`opID`),
  KEY `ID` (`ID`),
  KEY `opID_2` (`opID`,`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`ID`, `Round`, `camId`, `Direction`, `num_passengers`, `opID`) VALUES
(1, '', 0, '', 0, 0),
(2, '', 0, '', 0, 0),
(3, '', 0, '', 0, 0),
(4, '', 0, '', 0, 0),
(5, '', 0, '', 0, 0),
(6, '', 0, '', 0, 0),
(7, '', 0, '', 0, 0),
(8, '', 0, '', 0, 0),
(9, '', 0, '', 0, 0),
(10, '', 0, '', 0, 0),
(11, '', 0, '', 0, 0),
(12, '', 0, '', 0, 0),
(13, '', 0, '', 0, 0),
(14, '', 0, '', 0, 0),
(15, '', 0, '', 0, 0);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`opID`,`ID`) REFERENCES `vehicles` (`opID`, `ID`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
