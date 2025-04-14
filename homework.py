import sqlite3

DATABASE = "./test_db.db"

conn = sqlite3.connect(DATABASE)
print(f"DB {DATABASE} created ok!")


query_create = """

CREATE TABLE restaurants (
id INT PRIMARY KEY,
name VARCHAR(55),
address VARCHAR(255),
rating FLOAT,
Culinary tradition VARCHAR(255)
"""

query_insert1 = """
INSERT INTO users (id, name, address, rating, Culinary tradition)
VALUES (1, 'Vino e Cucina', 'вул. Січових Стрільців', 4.2, 'італійска');"""

conn.execute(query_create)
conn.commit()
conn.close()