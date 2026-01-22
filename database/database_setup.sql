-- Create database
CREATE DATABASE IF NOT EXISTS momo_db;
USE momo_db;

-- Table 1: users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for each user',
    phone_number VARCHAR(15) NOT NULL COMMENT 'User phone number in international format',
    full_name VARCHAR(100) NOT NULL COMMENT 'Full name of the user'
);

-- Table 2: categories
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for each category',
    category_name VARCHAR(50) NOT NULL COMMENT 'Name of the transaction category',
    category_type  ENUM('Income', 'Expense') NOT NULL COMMENT 'Type of category: Income/Expense'
);

-- Table 3: transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for each transaction',
    txn_code VARCHAR(50) NOT NULL COMMENT 'Transaction code',
    category_id INT COMMENT 'References category of the transaction',
    amount DECIMAL(10,2) NOT NULL COMMENT 'Transaction amount',
    transaction_date DATETIME NOT NULL COMMENT 'Date and time of transaction',
    message TEXT COMMENT 'Optional transaction message',
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT chk_amount_positive CHECK (amount >= 0)
);

-- Table 4: user_transactions
CREATE TABLE user_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for user-transaction mapping',
    user_id INT COMMENT 'References user',
    transaction_id INT COMMENT 'References transaction',
    role ENUM('sender', 'receiver') NOT NULL COMMENT 'Role in transaction: sender/receiver',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- Table 5: system_logs
CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for system log',
    log_type VARCHAR(50) COMMENT 'Type of log',
    message TEXT COMMENT 'Log message',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log creation timestamp'
);

CREATE TABLE fee_types (
    fee_type_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for fee type',
    fee_name VARCHAR(50) NOT NULL COMMENT 'Name of the fee',
    fee_code VARCHAR(20) NOT NULL UNIQUE COMMENT 'Short code for fee type',
    calculation_method ENUM('fixed', 'percentage', 'tiered') DEFAULT 'fixed' COMMENT 'How fee is calculated',
    fee_value DECIMAL(10,2) NOT NULL COMMENT 'Base fee value or percentage',
    min_fee DECIMAL(10,2) NULL COMMENT 'Minimum fee amount',
    max_fee DECIMAL(10,2) NULL COMMENT 'Maximum fee amount',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Whether fee type is active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation time',

     CONSTRAINT chk_fee_value_positive CHECK (fee_value >= 0),
    CONSTRAINT chk_min_max_fee CHECK (
        min_fee IS NULL OR 
        max_fee IS NULL OR 
        min_fee <= max_fee
    )
);

CREATE TABLE transaction_fees (
    transaction_fee_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID for transaction-fee record',
    transaction_id INT NOT NULL COMMENT 'References transaction',
    fee_type_id INT NOT NULL COMMENT 'References fee type',
    fee_amount DECIMAL(10,2) NOT NULL COMMENT 'Actual fee amount charged',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When fee was applied',
    
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (fee_type_id) REFERENCES fee_types(fee_type_id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    CONSTRAINT chk_fee_amount_positive CHECK (fee_amount >= 0),
    UNIQUE KEY uk_transaction_fee_type (transaction_id, fee_type_id),
);

-- Add sample users 
INSERT INTO users (user_id, phone_number, full_name) VALUES
(1, '+250788123456', 'KAMANZI Ghod'),
(2, '+250789654321', 'UWARIYA Jane'),
(3, '+250788112233', 'UWINEZA Alice'),
(4, '+250789445566', 'MUGISHA Bob'),
(5, '+250788998877', 'NSABIMANA Williams');

-- Add sample data 
INSERT INTO categories (category_id, category_name, category_type) VALUES
(1, 'Received Money', 'Income'),
(2, 'Sent Money', 'Expense'),
(3, 'Airtime', 'Expense'),
(4, 'Bill Payment', 'Expense'),
(5, 'Cashback', 'Income');

-- Add sample transactions
INSERT INTO transactions (transaction_id, txn_code, category_id, amount, transaction_date, message) VALUES
(1, 'TXN001', 1, 5000, '2024-01-15 10:00:00', 'Received money'),
(2, 'TXN002', 2, 2000, '2024-01-16 11:00:00', 'Sent money'),
(3, 'TXN003', 3, 1500, '2024-01-17 09:30:00', 'Bought airtime'),
(4, 'TXN004', 4, 10000, '2024-01-18 14:45:00', 'Paid electricity bill'),
(5, 'TXN005', 5, 300, '2024-01-19 12:15:00', 'Cashback reward');

INSERT INTO user_transactions (id, user_id, transaction_id, role) VALUES
(1, 1, 1, 'receiver'),
(2, 2, 2, 'sender'),
(3, 3, 3, 'sender'),
(4, 4, 4, 'sender'),
(5, 5, 5, 'receiver');

INSERT INTO system_logs (log_id, log_type, message) VALUES
(1, 'INFO', 'System initialized'),
(2, 'ERROR', 'Transaction failed for TXN002'),
(3, 'INFO', 'User John Doe created'),
(4, 'WARNING', 'Transaction TXN003 took longer than expected'),
(5, 'INFO', 'Database backup completed');
