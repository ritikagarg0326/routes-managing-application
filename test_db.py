import psycopg

host = ""
database = "postgres"
user = "postgres"
password = ""

try:
    conn = psycopg.connect(
        host=host,
        port=5432,
        dbname=database,
        user=user,
        password=password
    )

    cursor = conn.cursor()

    cursor.execute("SELECT current_database();")
    result = cursor.fetchone()

    print("✅ Connected to AWS RDS PostgreSQL!")
    print("Database:", result[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)