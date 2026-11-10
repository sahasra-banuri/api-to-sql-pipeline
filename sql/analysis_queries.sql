USE ecommerce_pipeline;

SHOW TABLES;

DESCRIBE carts;

DESCRIBE cart_products;

SELECT COUNT(*)
FROM carts;

SELECT COUNT(*)
FROM cart_products;

SELECT * FROM carts LIMIT 5;

SELECT * FROM cart_products LIMIT 5;

SELECT 
c.cart_id,
c.user_id,
p.product_id,
p.title,
p.price,
p.quantity
FROM carts c
INNER JOIN cart_products p
ON c.cart_id = p.cart_id;

-- GROUP BY 
SELECT 
cart_id,
COUNT(product_id) AS product_count 
FROM cart_products
GROUP BY cart_id;

SELECT 
cart_id, user_id,
COUNT(product_id) AS product_count
FROM cart_products
GROUP BY cart_id, user_id; -- you should use joins in order to execute this

SELECT 
user_id,
SUM(total) AS total_value
FROM carts
GROUP BY user_id
HAVING SUM(total) > 1000;

SELECT COUNT(*) AS total_carts
FROM carts;

SELECT COUNT(*) AS total_products
FROM cart_products;

SELECT
    c.user_id,
    COUNT(p.product_id) AS total_products,
    SUM(p.total) AS total_cart_value
FROM carts c
INNER JOIN cart_products p
    ON c.cart_id = p.cart_id
GROUP BY c.user_id
ORDER BY total_cart_value DESC;

SELECT COUNT(*) AS total_carts
FROM carts;

SELECT COUNT(*) AS total_products
FROM cart_products;
