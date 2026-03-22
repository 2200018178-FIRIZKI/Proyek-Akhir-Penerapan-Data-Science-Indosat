import pandas as pd
import psycopg2
from psycopg2 import sql

# Read CSV
df = pd.read_csv(r"c:\Users\ACER\Downloads\Proyek Akhir Penerapan Data Scienctist\a590-Belajar-Penerapan-Data-Science\Dataset\data.csv", sep=';')

print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Column names: {list(df.columns)}")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="host.docker.internal",
    port=5432,
    database="student_data",
    user="admin",
    password="password"
)
cursor = conn.cursor()

# Drop old table
cursor.execute("DROP TABLE IF EXISTS student_data;")

# Create new table with all columns
columns_def = ", ".join([f'"{col}" TEXT' for col in df.columns])
create_table_sql = f"CREATE TABLE student_data ({columns_def});"
cursor.execute(create_table_sql)
print("✓ Table created")

# Insert data
for idx, row in df.iterrows():
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_sql = f"INSERT INTO student_data VALUES ({placeholders});"
    cursor.execute(insert_sql, tuple(row))
    if (idx + 1) % 500 == 0:
        print(f"  Imported {idx + 1} records...")

conn.commit()
cursor.close()
conn.close()

# Verify
print(f"✓ All {len(df)} records imported successfully!")
