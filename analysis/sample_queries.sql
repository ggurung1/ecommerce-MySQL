-- ==============================================
-- SAMPLE SQL QUERIES: E-commerce Analytics
-- ==============================================
-- Purpose: MySQL joins, aggregations, and others
-- Database: ecommerce_db
-- ==============================================

-- Customers from USA
SELECT CONCAT(first_name,' ',last_name) AS name,email FROM customers WHERE country='USA';

-- Average order value
SELECT ROUND(AVG(amount),2) AS average_order_value FROM payments;

-- Product names and category names
SELECT ca.category_name,pr.product_name FROM products pr JOIN categories ca 
ON pr.category_id=ca.category_id;

-- Total revenue per payment method
SELECT pa.method,SUM(pa.amount) AS total_payment FROM payments pa GROUP BY pa.method
ORDER BY total_payment DESC;

-- Total number of orders per customer
SELECT cu.customer_id,COUNT(o.order_id) AS total_orders FROM customers cu JOIN orders o
ON cu.customer_id=o.customer_id GROUP BY cu.customer_id ORDER BY total_orders DESC;

-- Top 5 customers by total spending
SELECT CONCAT(cu.first_name,' ', cu.last_name) AS name,SUM(pa.amount) AS total_spending
FROM customers cu JOIN orders o ON cu.customer_id=o.customer_id
JOIN payments pa ON o.order_id=pa.order_id GROUP BY cu.customer_id
ORDER BY total_spending DESC LIMIT 5;

-- Top 5 best selling products by quantity
SELECT pr.product_name,SUM(oi.quantity) AS total_quantity FROM products pr 
JOIN order_items oi ON pr.product_id=oi.product_id GROUP BY pr.product_id ORDER BY total_quantity DESC LIMIT 5;

-- List product categories by revenue
SELECT ca.category_name,SUM(oi.quantity*pr.price) AS total_revenue FROM categories ca
JOIN products pr ON ca.category_id=pr.category_id
JOIN order_items oi ON oi.product_id=pr.product_id GROUP BY ca.category_id
ORDER BY total_revenue DESC LIMIT 3; 

-- customers who have never order
SELECT cu.customer_id,CONCAT(cu.first_name, ' ', cu.last_name) AS full_name,cu.email,cu.country FROM customers cu 
LEFT JOIN orders o ON cu.customer_id = o.customer_id WHERE o.order_id IS NULL ORDER BY cu.country, full_name;

-- Rank customers by total sepnding using a window function
SELECT cu.customer_id,CONCAT(cu.first_name, ' ', cu.last_name) AS full_name,SUM(pa.amount) AS total_spent,
RANK() OVER(ORDER BY SUM(pa.amount) DESC) AS spending_rank FROM customers cu JOIN orders o ON cu.customer_id=o.customer_id 
JOIN payments pa ON pa.order_id=o.order_id GROUP BY cu.customer_id ORDER BY spending_rank LIMIT 10;

-- Top 3 customers per country by Total Spending 
WITH customer_spending AS (
SELECT cu.country,cu.customer_id,CONCAT(cu.first_name,' ',cu.last_name) AS full_name, SUM(pa.amount) AS total_spent,
RANK() OVER(PARTITION BY cu.country ORDER BY SUM(pa.amount) DESC) AS spending_rank FROM customers cu 
JOIN orders o ON cu.customer_id=o.customer_id JOIN payments pa ON o.order_id=pa.order_id GROUP BY cu.country,cu.customer_id
)
SELECT country,customer_id,full_name,total_spent,spending_rank FROM customer_spending WHERE spending_rank<=3 ORDER BY country,spending_rank;
