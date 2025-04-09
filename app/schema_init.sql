-- MySQL database schema initialization for Azulu CRM

-- Drop tables if they exist
DROP TABLE IF EXISTS mailing_list;
DROP TABLE IF EXISTS contents;
DROP TABLE IF EXISTS events;

-- Events table
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    venue_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    start_date DATETIME NOT NULL,
    start_time VARCHAR(10) NOT NULL,  -- Format: "HH:MM"
    end_time VARCHAR(10) NOT NULL,    -- Format: "HH:MM"
    time_zone VARCHAR(50) NOT NULL,   -- IANA time zone name
    ticket_status VARCHAR(50) NOT NULL,
    ticket_link VARCHAR(255),
    lineup JSON,                      -- Store as JSON array
    genres JSON,                      -- Store as JSON array
    description TEXT NOT NULL,
    poster_url VARCHAR(255),
    price DECIMAL(10, 2),
    currency VARCHAR(3) NOT NULL,
    INDEX idx_events_name (name),
    INDEX idx_events_start_date (start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contents table for static content
CREATE TABLE contents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(255) NOT NULL,
    string_collection JSON,           -- Store as JSON array
    big_string TEXT,
    UNIQUE KEY idx_contents_key (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Mailing list table
CREATE TABLE mailing_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subscribed BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE KEY idx_mailing_list_email (email),
    INDEX idx_mailing_list_subscribed (subscribed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Helpful comments about column types:
-- VARCHAR(255): String fields with a maximum length
-- TEXT: For longer text content like descriptions
-- DATETIME: For date and time fields stored in UTC
-- JSON: For arrays and nested structures (lineup, genres, string_collection)
-- DECIMAL(10,2): For price with 2 decimal places
-- BOOLEAN: For true/false values (subscribed)
