CREATE DATABASE IF NOT EXISTS accountability_db;
USE accountability_db;

CREATE TABLE IF NOT EXISTS cik_ticker_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cik_str varchar(128),
    ticker varchar(128),
    title varchar(128)
);

CREATE TABLE IF NOT EXISTS recent_filing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cik_str varchar(128),
    accessionNumber varchar(128),
    filingDate DATETIME,
    reportDate DATETIME,
    acceptanceDateTime DATETIME,
    act varchar(128),
    form varchar(128),
    fileNumber varchar(128),
    filmNumber varchar(128),
    items varchar(128),
    size varchar(128),
    isXBRL int,
    isInlineXBRL int,
    primaryDocument varchar(128),
    primaryDocDescription varchar(128)
);
