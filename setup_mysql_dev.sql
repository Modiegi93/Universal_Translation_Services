CREATE DATABASE IF NOT EXISTS ult_dev_db;
CREATE USER IF NOT EXISTS 'ult_dev'@'localhost' IDENTIFIED BY 'ult_dev_pwd';
GRANT SELECT ON performance_schema.* TO 'ult_dev'@'localhost';
GRANT ALL PRIVILEGES ON ult_dev_db.* TO 'ult_dev'@'localhost';
