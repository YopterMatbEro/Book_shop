INSERT INTO publisher (name)
VALUES('Пушкин')

INSERT INTO book (title, id_publisher)
VALUES ('Няне', 1)

INSERT INTO shop (name)
VALUES ('Книжный город')

INSERT INTO stock (id_book, id_shop, count)
VALUES (1, 1, 15)

INSERT INTO sale (price, date_sale, id_stock, count)
VALUES (139, '2023-05-26', 1, 3)

SELECT title, s2.name, price, date_sale FROM book b
JOIN publisher p ON p.id = b.id_publisher 
JOIN stock s ON s.id_book = b.id
JOIN shop s2 ON s2.id = s.id_shop 
JOIN sale s3 ON s3.id_stock = s.id 
WHERE p.name = 'Пушкин'
