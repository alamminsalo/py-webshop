
DROP DATABASE IF EXISTS webshop;
CREATE DATABASE webshop;


CREATE USER 'shop'@'localhost' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON webshop.* TO 'shop'@'localhost';


USE webshop;


CREATE TABLE user_accounts (
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR(80) NOT NULL,
	last_name VARCHAR(80) NOT NULL,
	email VARCHAR(120) NOT NULL,
	address VARCHAR(100) NOT NULL,
	post_code VARCHAR(10) NOT NULL,
	town VARCHAR(40) NOT NULL,
	country VARCHAR(20) NOT NULL
);

CREATE TABLE credentials (
	user_id BIGINT UNSIGNED NOT NULL,
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE,
	name VARCHAR(80) NOT NULL UNIQUE,
	password CHAR(64) NOT NULL,
	role ENUM("admin","customer") NOT NULL
);

/*
Played it simple here by just assuming the products are all inside one, shop-specific warehouse.
One could gain scalability by implementing warehouses, which hold counts of each product available
Prices in €
*/
CREATE TABLE products (
	product_id SERIAL PRIMARY KEY,
	code VARCHAR(20) NOT NULL UNIQUE,
	name VARCHAR(80) NOT NULL,
	price DECIMAL(10, 2) UNSIGNED,
	in_stock INT NOT NULL
);

/*
Customer has many-to-many relation witch products, so we simply use dedicated table with two foreign keys for this,
which we can query on product stock availability, products on customer's shopping cart etc.
*/
CREATE TABLE shopcart (
	user_id BIGINT UNSIGNED NOT NULL,
	CONSTRAINT fk_cart_user FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE,
	product_id BIGINT UNSIGNED NOT NULL,
	CONSTRAINT fk_cart_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);


/*Insert 10000 units of coffee to products*/
INSERT INTO products(code,name,price,in_stock) VALUES("FAIRTRADECOF","Coffee, Fairtrade", 5.20, 10000);

/*Insert 1500 units of t-shirts to products*/
INSERT INTO products(code,name,price,in_stock) VALUES("TSHIRTBL","Cool T-Shirt, blue", 29.90, 1500);

/*Insert 777 units of footballs to products*/
INSERT INTO products(code,name,price,in_stock) VALUES("FOOTBALLWHITE","Football, white", 12.50, 500);


