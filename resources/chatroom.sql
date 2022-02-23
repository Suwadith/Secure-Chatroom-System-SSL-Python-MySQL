-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 24, 2022 at 12:09 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chatroom`
--

-- --------------------------------------------------------

--
-- Table structure for table `ban_list`
--

CREATE TABLE `ban_list` (
  `ban_list_id` int(10) NOT NULL,
  `username` varchar(10) NOT NULL,
  `ip_address` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `chat_history`
--

CREATE TABLE `chat_history` (
  `message_id` int(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `username` varchar(10) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chat_history`
--


CREATE TABLE `users` (
  `user_id` int(10) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `user_type`) VALUES
(1, 'admin', '55EyX+w=*Xf8oCqDgP1BzT6hym+LPBQ==*ASBofMpJmKkKnLIoyTzvyg==*u+x1MIQxqWYpy0lYdyTy3Q==', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ban_list`
--
ALTER TABLE `ban_list`
  ADD PRIMARY KEY (`ban_list_id`);

--
-- Indexes for table `chat_history`
--
ALTER TABLE `chat_history`
  ADD PRIMARY KEY (`message_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ban_list`
--
ALTER TABLE `ban_list`
  MODIFY `ban_list_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `chat_history`
--
ALTER TABLE `chat_history`
  MODIFY `message_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
