CREATE DATABASE IF NOT EXISTS accountability_db;
USE accountability_db;

CREATE TABLE IF NOT EXISTS cik_ticker_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cik_str varchar(128),
    ticker varchar(128),
    title varchar(128)
);
