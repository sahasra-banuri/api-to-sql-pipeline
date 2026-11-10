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