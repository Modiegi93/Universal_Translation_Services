CREATE DATABASE IF NOT EXISTS ult_test_db;
CREATE USER IF NOT EXISTS 'ult_test'@'localhost' IDENTIFIED BY 'ult_test_pwd';
GRANT SELECT ON performance_schema.* TO 'ult_test'@'localhost';
GRANT ALL PRIVILEGES ON ult_test_db.* TO 'ult_test'@'localhost';
