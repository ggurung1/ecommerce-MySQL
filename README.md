# e-commerce (MySQL)
This project demonstrates MySQL and database design by building a **fully functional e-commerce database** using MySQL. It includes schema creation, relationships, constraints, and a Python script to generate and populate realistic sample data.

## Overview
The database models an online store system with entities for customers, products, orders, and payments. It is designed to demonstrate my understanding of:
- Normalized database schema design (3NF)
- Use of primary and foreign keys for relationships
- ENUM constraints for categorical fields
- SQL DDL (Data Definition Language) and DML (Data Manipulation Language)
- Automated data generation using Python

---

Database Schema

**Database name:** `ecommerce_data`

### Tables
| Table | Description |
|--------|-------------|
| `customers` | Stores customer information including name, email, and country |
| `categories` | Contains product category details |
| `products` | Holds product names, prices, and links to categories |
| `orders` | Represents customer orders and their statuses |
| `order_items` | Details the products and quantities in each order |
| `payments` | Stores payment details for each order |
Each table is linked through **foreign keys**, ensuring referential integrity and a logical relational structure.


---

## Entity Relationship Diagram

CUSTOMERS (customer_id PK)
│
└──< ORDERS (order_id PK, customer_id FK)
     │
     ├──< ORDER_ITEMS (order_item_id PK, order_id FK, product_id FK)
     │        │
     │        └── PRODUCTS (product_id PK, category_id FK)
     │                    │
     │                    └── CATEGORIES (category_id PK)
     │
     └── PAYMENTS (payment_id PK, order_id FK)

PK = Primary Key  
FK = Foreign Key


PK(Primary Key) FK(Foreign Key)


The sample script includes ready-to-run queries with MySQL;
1. List customers from USA
2. calculate average_order_value
3. List out product_names and category_names
4. Find the total revenue per payment methode
5. FInd the total number of orders per customer
6. Top 5 customers by total spending
7. Top 5 best selling products by quantity
8. List product categories by revenue
9. Identify customers who have never placed an order
10. Rank customers by total spending using a window function
11. Top 3 customers per country by total spending
