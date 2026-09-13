import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="logistics",
    user="postgres",
    password="postgres"
)

print("Connected to PostgreSQL! local")

conn.close()