-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 27, 2025 at 10:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `booking_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bills`
--

CREATE TABLE `bills` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `bill_date` date DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact_no` varchar(20) NOT NULL,
  `service` int(11) NOT NULL,
  `service_date` date NOT NULL,
  `special_request` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `name`, `contact_no`, `service`, `service_date`, `special_request`, `created_at`) VALUES
(2, 'Amar', '9137534732', 3, '2025-03-29', 'new printer', '2025-03-27 20:22:18'),
(5, 'Hrishikesh gaonkar', '9860596919', 1, '2025-03-29', 'new', '2025-03-27 20:25:42'),
(6, 'asha', '8087077816', 2, '2025-03-28', 'repair', '2025-03-27 20:34:14'),
(7, 'sid', 'sid@gmail.com', 2, '2025-03-28', 'dhhc', '2025-03-27 20:39:01'),
(10, 'lee', '956143990', 2, '2025-03-28', 'repair', '2025-03-27 20:42:35'),
(12, 'sid', 'sid@gmail.com', 2, '2025-03-28', 'dhhc', '2025-03-27 20:44:27'),
(16, 'abhi', '8830504884', 1, '2025-03-28', 'hey', '2025-03-27 20:50:52'),
(17, 'Amar', '956143990', 1, '2025-03-29', 'help', '2025-03-27 20:52:50'),
(18, 'Amar', '956143990', 2, '2025-03-29', 'hello', '2025-03-27 20:55:18'),
(20, 'sam', '9992255522', 1, '2025-03-29', 'hwuch', '2025-03-27 21:00:09'),
(21, 'admin', '8979788888', 1, '2025-03-29', 'admin', '2025-03-27 21:06:57'),
(22, 'Amar', '7879878787', 2, '2025-04-05', 'suggest', '2025-03-27 21:10:05');

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

CREATE TABLE `stock` (
  `id` int(11) NOT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock`
--

INSERT INTO `stock` (`id`, `product_name`, `quantity`) VALUES
(1, 'PC', 25),
(2, 'Laptop', 21),
(3, 'Printer', 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bills`
--
ALTER TABLE `bills`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_id` (`booking_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stock`
--
ALTER TABLE `stock`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bills`
--
ALTER TABLE `bills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `stock`
--
ALTER TABLE `stock`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bills`
--
ALTER TABLE `bills`
  ADD CONSTRAINT `bills_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
