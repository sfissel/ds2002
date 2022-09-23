#Question 0: How many rows are in the Products Table?
SELECT COUNT(*)
FROM products;
#Question 1: Product Name and Unit/Quantity
SELECT product_name, quantity_per_unit
FROM products;
#Question 2: Product ID and Name of Current Products
SELECT id, product_name
FROM products
WHERE discontinued = 0;
#Question 3: Product ID and Name of Discontinued Products
SELECT id, product_name
FROM products
WHERE discontinued = 1;
#Question 4: Name & List Price of Most & Least Expensive Products
SELECT * FROM (
SELECT product_name, list_price
FROM products
ORDER BY list_price DESC LIMIT 1) z
UNION ALL
SELECT * FROM (
SELECT product_name, list_price
FROM products
ORDER BY list_price ASC LIMIT 1) z;
#Question 5: Product ID, Name & List Price Costing Less Than $20
SELECT id, product_name, list_price
FROM products
WHERE list_price < 20;
#Question 6: Product ID, Name & List Price Costing Between $15 and $20
SELECT id, product_name, list_price
FROM products
WHERE list_price BETWEEN 15 AND 20;
#Question 7: Product Name & List Price Costing Above Average List Price
SELECT product_name, list_price 
FROM products 
WHERE list_price > (SELECT AVG(list_price) FROM products);
#Question 8: Product Name & List Price of 10 Most Expensive Products
SELECT product_name, list_price
FROM products
ORDER BY list_price DESC LIMIT 10;
#Question 9: Count of Current and Discontinued Products
SELECT COUNT(discontinued = 1 + discontinued = 0)
FROM products;
#Extra Credit:
#Question 11: Products with Supplier Company & Address Info
SELECT products.product_name, suppliers.company, suppliers.address
FROM products
INNER JOIN suppliers ON products.supplier_ids = suppliers.id;
