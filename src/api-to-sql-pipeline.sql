CREATE DATABASE ecommerce_pipeline;
USE ecommerce_pipeline;
CREATE TABLE carts (
    cart_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    total DECIMAL(10,2),
    discounted_total DECIMAL(10,2),
    total_products INT,
    total_quantity INT
);

CREATE TABLE cart_products (
    cart_product_id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10,2),
    quantity INT,
    total DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    discounted_total DECIMAL(10,2),

    CONSTRAINT fk_cart
        FOREIGN KEY (cart_id)
        REFERENCES carts(cart_id),

    CONSTRAINT unique_cart_product
        UNIQUE (cart_id, product_id)
);

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


