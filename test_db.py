import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="logistics",
    user="postgres",
    password="postgre@#$$s"
)

print("Connected to PostgreSQL! local in desktop")

conn.close()