-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 21, 2022 at 10:01 PM
-- Server version: 8.0.30-0ubuntu0.20.04.2
-- PHP Version: 8.0.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jtv`
--

-- --------------------------------------------------------

--
-- Table structure for table `channel`
--

CREATE TABLE `channel` (
  `CHID` bigint NOT NULL,
  `name` varchar(120) NOT NULL DEFAULT '',
  `descrip` text NOT NULL,
  `type` varchar(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `channel`
--

INSERT INTO `channel` (`CHID`, `name`, `descrip`, `type`) VALUES
(2, 'channels.live', 'channels.des-live', 'channel'),
(3, 'channels.music', 'channels.des-music', 'channel'),
(4, 'channels.instruct', 'channels.des-instruct', 'channel'),
(14, 'channels.clubs', 'channels.des-clubs', 'prop'),
(5, 'channels.festival', 'channels.des-festivals', 'channel'),
(6, 'channels.comedy', 'channels.des-comedy', 'channel'),
(7, 'channels.promo', 'channels.des-promo', 'channel'),
(8, 'channels.history', 'channels.des-history', 'channel'),
(9, 'channels.passing', 'channels.des-passing', 'channel'),
(10, 'channels.tv', 'channels.des-tv', 'channel'),
(11, 'channels.single', 'channels.des-single', 'channel'),
(12, 'channels.numbers', 'channels.des-numbers', 'channel'),
(13, 'channels.jtv', 'channels.des-jtv', 'channel'),
(16, 'channels.balls', 'channels.des-balls', 'prop'),
(17, 'channels.rings', 'channels.des-rings', 'prop'),
(18, 'channels.diabolo', 'channels.des-diabolo', 'prop'),
(19, 'channels.contact', 'channels.des-contact', 'prop'),
(20, 'channels.sticks', 'channels.des-sticks', 'prop'),
(21, 'channels.bricks', 'channels.des-bricks', 'prop'),
(22, 'channels.hats', 'channels.des-hats', 'prop'),
(23, 'channels.uni', 'channels.des-uni', 'prop'),
(24, 'channels.spin', 'channels.des-spin', 'prop'),
(25, 'channels.yoyo', 'channels.des-yoyo', 'prop'),
(26, 'channels.kendama', 'channels.des-kendama', 'prop'),
(27, 'channels.fire', 'channels.des-fire', 'prop'),
(28, 'channels.hoops', 'channels.des-hoops', 'prop'),
(29, 'channels.feet', 'channels.des-feet', 'prop'),
(30, 'channels.bounce', 'channels.des-bounce', 'prop'),
(31, 'channels.other', 'channels.des-other', 'prop'),
(32, 'channels.mixed', 'channels.des-mixed', 'prop');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `channel`
--
ALTER TABLE `channel`
  ADD PRIMARY KEY (`CHID`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `channel`
--
ALTER TABLE `channel`
  MODIFY `CHID` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
