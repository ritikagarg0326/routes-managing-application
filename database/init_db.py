import os
import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable is not set")


# psycopg expects postgresql://
DATABASE_URL = DATABASE_URL.replace(
    "postgresql+psycopg://",
    "postgresql://"
)


def run_sql_file(cursor, filename):
    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    cursor.execute(sql)


conn = psycopg.connect(DATABASE_URL)

try:
    cursor = conn.cursor()

    print("Creating database tables...")
    run_sql_file(cursor, "database/schema.sql")

    print("Inserting initial data...")
    run_sql_file(cursor, "database/seed.sql")

    conn.commit()

    print("✅ Database setup completed successfully!")

except Exception as e:
    conn.rollback()
    print("❌ Database setup failed:")
    print(e)

finally:
    cursor.close()
    conn.close()