DROP TABLE `clients` IF EXISTS;
CREATE TABLE `clients` (
   `id` int(10) NOT NULL AUTO_INCREMENT,
   `host_ip` varchar(255) NOT NULL,
   `host_description` varchar(255) NOT NULL,
   `location` varchar(255) NOT NULL,
   `username` varchar(255) NOT NULL,
   `password` varchar(255) NOT NULL,
   `psk` varchar(255) NOT NULL,
   `last_change` timestamp NOT NULL DEFAULT current_timestamp(),
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

