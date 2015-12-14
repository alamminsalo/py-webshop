
DROP DATABASE IF EXISTS webshop;
CREATE DATABASE webshop;


CREATE USER 'shop'@'localhost' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON webshop.* TO 'shop'@'localhost';


USE webshop;

CREATE TABLE products (
	product_id SERIAL PRIMARY KEY,
	code VARCHAR(20) NOT NULL UNIQUE,
	name VARCHAR(80) NOT NULL,
	price DECIMAL(10, 2) UNSIGNED,
	in_stock INT NOT NULL
);

CREATE TABLE shopcarts (
	user_id BIGINT UNSIGNED NOT NULL,
	/*CONSTRAINT fk_cart_user FOREIGN KEY (user_id) REFERENCES user_accounts(user_id) ON DELETE CASCADE,*/
	product_id BIGINT UNSIGNED NOT NULL,
	CONSTRAINT fk_cart_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	count INT UNSIGNED NOT NULL
);


/*Triggers for updating in_stock values of products table*/
/*On insert minus values, on delete add values back*/
CREATE TRIGGER stock_insert_trigger BEFORE INSERT ON shopcarts FOR EACH ROW
	UPDATE products SET in_stock = in_stock - cast(NEW.count as signed) WHERE product_id = NEW.product_id;

CREATE TRIGGER stock_delete_trigger BEFORE DELETE ON shopcarts FOR EACH ROW
	UPDATE products SET in_stock = in_stock + cast(OLD.count as signed) WHERE product_id = OLD.product_id;


/*Insert 10000 units of coffee to products*/
INSERT INTO products(code,name,price,in_stock) VALUES("FAIRTRADECOF","Coffee, Fairtrade", 5.20, 10000);
/*Insert 1500 units of t-shirts to products*/
INSERT INTO products(code,name,price,in_stock) VALUES("TSHIRTBL","Cool T-Shirt, blue", 29.90, 1500);
/*Insert 777 units of footballs to products*/
INSERT INTO products(code,name,price,in_stock) VALUES("FOOTBALLWHITE","Football, white", 12.50, 500);

/*Insert a few shopcarts*/
INSERT INTO shopcarts(user_id, product_id, count) VALUES (49, 1, 9);
INSERT INTO shopcarts(user_id, product_id, count) VALUES (33, 2, 19);
INSERT INTO shopcarts(user_id, product_id, count) VALUES (33, 3, 99);

