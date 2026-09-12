import psycopg
import os


conn = psycopg.connect(
    os.getenv("DATABASE_URL").replace("postgresql+psycopg://", "postgresql://")
)

cursor = conn.cursor()

cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cursor.fetchall()

print("\nTables in AWS RDS:")
for table in tables:
    print("-", table[0])

cursor.close()
conn.close()