-- ==============================
-- 		E-commerce DATABASE
-- ============================== 

-- STEP 1: Create Database
DROP DATABASE IF EXISTS ecommerce_db;
-- CREATE DATABASE IF NOT EXISTS ecommerce_db;

CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- STEP 2: Create Tables
-- Customers Table
DROP TABLE IF EXISTS customers;
CREATE TABLE customers ( 
customer_id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
email VARCHAR(100) UNIQUE,
country VARCHAR(50),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
category_id INT AUTO_INCREMENT PRIMARY KEY,
category_name VARCHAR(50) NOT NULL
);

-- Products table
DROP TABLE IF EXISTS products;
CREATE TABLE products (
product_id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(100) NOT NULL,
price DECIMAL(10,2) NOT NULL,
category_id INT,
FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Orders table
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
order_id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT,
order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
order_status ENUM('Pending','Shipped','Delivered','Cancelled') DEFAULT 'Pending',
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items table
DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
order_item_id INT AUTO_INCREMENT PRIMARY KEY,
order_id INT,
product_id INT,
quantity INT NOT NULL,
FOREIGN KEY (order_id) REFERENCES orders(order_id),
FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Payments table
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
payment_id INT AUTO_INCREMENT PRIMARY KEY,
order_id INT,
amount DECIMAL(10,2) NOT NULL,
payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
method ENUM('Credit Card','PayPal','Bank Transfer','Apple Pay'),
FOREIGN KEY (order_id) REFERENCES orders(order_id)
);


-- STEP 3: Insert Sample Data
-- ===================================================================
-- NOTE:
-- 1. Run this schema file first
-- 2. Then Import ecommerce_data.sql (generated via python script)
-- ===================================================================

