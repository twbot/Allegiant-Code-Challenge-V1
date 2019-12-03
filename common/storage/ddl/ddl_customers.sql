----------------------------------------------------------
--
-- Drop table 'customers' if exists
----------------------------------------------------------
DROP TABLE IF EXISTS customers;

----------------------------------------------------------
--
-- Table definition for table 'customers'
----------------------------------------------------------
CREATE TABLE customers (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL DEFAULT '',
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `latitude` float(10,6) DEFAULT NULL,
  `longitude` float(10,6) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE_EMAIL` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;