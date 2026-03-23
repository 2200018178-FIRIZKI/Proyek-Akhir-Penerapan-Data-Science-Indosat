"""
================================================================================
IMPORT DATASET KE POSTGRESQL
Script untuk import CSV dataset ke PostgreSQL dengan label kategorikal
================================================================================
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import os

# Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'student_data',
    'user': 'admin',
    'password': 'password'
}

TABLE_NAME = 'student_data_metabase'
CSV_FILE = '../Dataset/student_data_metabase_final.csv'

print("="*80)
print("📊 IMPORT DATASET KE POSTGRESQL")
print("="*80)

# STEP 1: Load CSV
print("\n[STEP 1] Loading CSV File...")
if not os.path.exists(CSV_FILE):
    print(f"  ❌ File not found: {CSV_FILE}")
    exit(1)

df = pd.read_csv(CSV_FILE, sep=';', encoding='utf-8')
print(f"  ✓ Loaded: {CSV_FILE}")
print(f"  ✓ Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# STEP 2: Connect to PostgreSQL
print("\n[STEP 2] Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print(f"  ✓ Connected to {DB_CONFIG['database']} @ {DB_CONFIG['host']}")
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    exit(1)

# STEP 3: Check if table exists
print(f"\n[STEP 3] Checking table '{TABLE_NAME}'...")
cursor.execute(f"""
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = '{TABLE_NAME}'
    );
""")

table_exists = cursor.fetchone()[0]
if table_exists:
    print(f"  ⚠️  Table '{TABLE_NAME}' already exists")
    response = input("  Drop existing table? (y/n): ").lower()
    if response == 'y':
        cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
        conn.commit()
        print(f"  ✓ Table dropped")
        table_exists = False
    else:
        print(f"  ℹ️  Using existing table (will truncate and reload)")
        cursor.execute(f"TRUNCATE TABLE {TABLE_NAME};")
        conn.commit()

# STEP 4: Create Table Schema
print(f"\n[STEP 4] Creating table schema...")

# Infer column types dari pandas
column_types = {}
for col in df.columns:
    dtype = df[col].dtype
    if 'int' in str(dtype):
        column_types[col] = 'INTEGER'
    elif 'float' in str(dtype):
        column_types[col] = 'DECIMAL(10,2)'
    else:
        max_len = df[col].astype(str).str.len().max()
        column_types[col] = f'VARCHAR({max(max_len + 10, 100)})' 

# Create columns definition
columns_def = []
for col in df.columns:
    col_type = column_types[col]
    # Make Status & Model_Prediction as VARCHAR for readability
    if col in ['Status', 'Model_Prediction']:
        col_type = 'VARCHAR(50)'
    columns_def.append(f'"{col}" {col_type}')

# Add primary key (optional - uncomment if needed)
# columns_def.append('id SERIAL PRIMARY KEY')

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    {', '.join(columns_def)},
    id SERIAL PRIMARY KEY
);
"""

try:
    cursor.execute(create_table_sql)
    conn.commit()
    print(f"  ✓ Table '{TABLE_NAME}' created with {len(df.columns)} columns")
except Exception as e:
    print(f"  ❌ Table creation failed: {e}")
    conn.close()
    exit(1)

# STEP 5: Insert Data in Batches
print(f"\n[STEP 5] Inserting {len(df):,} records...")

batch_size = 500
total_batches = (len(df) + batch_size - 1) // batch_size

try:
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(df))
        batch_df = df.iloc[start_idx:end_idx]
        
        # Convert NaN to None
        batch_df = batch_df.where(pd.notna(batch_df), None)
        
        # Build insert query
        columns = ', '.join([f'"{col}"' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_sql = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})"
        
        # Execute batch insert
        for idx, row in batch_df.iterrows():
            cursor.execute(insert_sql, tuple(row))
        
        conn.commit()
        pct = (end_idx / len(df)) * 100
        print(f"  ✓ Batch {batch_num + 1}/{total_batches} - {end_idx:,}/{len(df):,} records ({pct:.1f}%)")

    print(f"\n  ✓ All {len(df):,} records inserted successfully!")

except Exception as e:
    print(f"  ❌ Insert failed: {e}")
    conn.rollback()
    conn.close()
    exit(1)

# STEP 6: Verify Data
print(f"\n[STEP 6] Verifying imported data...")

try:
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
    row_count = cursor.fetchone()[0]
    print(f"  ✓ Total rows in table: {row_count:,}")
    
    cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 3;")
    sample_rows = cursor.fetchall()
    print(f"  ✓ Sample rows retrieved (showing first 3)")
    
    # Show column info
    cursor.execute(f"""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = '{TABLE_NAME}'
        ORDER BY ordinal_position;
    """)
    columns_info = cursor.fetchall()
    print(f"\n  ✓ Table structure ({len(columns_info)} columns):")
    for col_name, data_type in columns_info[:5]:
        print(f"    • {col_name}: {data_type}")
    if len(columns_info) > 5:
        print(f"    ... dan {len(columns_info) - 5} columns lainnya")

except Exception as e:
    print(f"  ❌ Verification failed: {e}")

# STEP 7: Create Indexes untuk Performance
print(f"\n[STEP 7] Creating indexes untuk performance...")

try:
    # Index untuk Status (untuk filtering)
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_status ON {TABLE_NAME}(Status);")
    print(f"  ✓ Index created: Status")
    
    # Index untuk Model_Prediction
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_prediction ON {TABLE_NAME}(Model_Prediction);")
    print(f"  ✓ Index created: Model_Prediction")
    
    # Index untuk Gender_Label
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_gender ON {TABLE_NAME}(Gender_Label);")
    print(f"  ✓ Index created: Gender_Label")
    
    conn.commit()
except Exception as e:
    print(f"  ⚠️  Index creation warning: {e}")

# STEP 8: Summary Statistics
print(f"\n[STEP 8] Database Summary Statistics...")

try:
    # Status distribution
    cursor.execute(f"""
        SELECT Status, COUNT(*) as count, 
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {TABLE_NAME}), 1) as pct
        FROM {TABLE_NAME}
        GROUP BY Status
        ORDER BY count DESC;
    """)
    
    print(f"\n  📊 Status Distribution:")
    for status, count, pct in cursor.fetchall():
        bar = "█" * int(pct / 5)
        print(f"    {status:12} │ {bar:<20} {pct:5.1f}% ({count:,})")
    
    # Gender distribution
    cursor.execute(f"""
        SELECT Gender_Label, COUNT(*) as count
        FROM {TABLE_NAME}
        WHERE Gender_Label IS NOT NULL
        GROUP BY Gender_Label
        ORDER BY count DESC;
    """)
    
    print(f"\n  👥 Gender Distribution:")
    for gender, count in cursor.fetchall():
        pct = count / row_count * 100
        print(f"    {gender:25} {pct:5.1f}%")
    
    # Scholarship distribution
    cursor.execute(f"""
        SELECT Scholarship_Label, COUNT(*) as count
        FROM {TABLE_NAME}
        WHERE Scholarship_Label IS NOT NULL
        GROUP BY Scholarship_Label;
    """)
    
    print(f"\n  💰 Scholarship Distribution:")
    for scholarship, count in cursor.fetchall():
        pct = count / row_count * 100
        print(f"    {scholarship:25} {pct:5.1f}%")
    
    # Model accuracy check
    cursor.execute(f"""
        SELECT 
        SUM(CASE WHEN Prediction_Correct = 1 THEN 1 ELSE 0 END) as correct,
        COUNT(*) as total
        FROM {TABLE_NAME}
        WHERE Prediction_Correct IS NOT NULL;
    """)
    
    correct, total = cursor.fetchone()
    accuracy = correct / total * 100 if total > 0 else 0
    print(f"\n  🤖 Model Accuracy: {accuracy:.2f}% ({correct:,}/{total:,})")
    
except Exception as e:
    print(f"  ⚠️  Summary query failed: {e}")

# STEP 9: Final Summary
print(f"\n" + "="*80)
print("✅ IMPORT COMPLETED SUCCESSFULLY")
print("="*80)

print(f"""
📊 Data Import Summary:
   • Table: {TABLE_NAME}
   • Records: {row_count:,} siswa
   • Columns: {len(columns_info)}
   • Size: ~{len(df):,} × {len(df.columns)} dataset

🎨 Categorical Labels Available:
   ✓ Gender_Label (👩 Perempuan / 👨 Laki-laki)
   ✓ Scholarship_Label (❌ Tanpa / ✅ Dengan)
   ✓ Tuition_Label (⚠️ Menunggak / ✅ Tepat Waktu)
   ✓ Debtor_Label (⚠️ Debtor / ✅ Non-Debtor)
   ✓ Attendance_Label (🌙 Evening / ☀️ Daytime)
   ✓ Displaced_Label (🏠 Tidak Pindah / 📍 Pindah)
   ✓ International_Label (🇵🇹 Domestik / 🌍 Internasional)
   ✓ Special_Needs_Label (✓ Tidak / ⚠️ Ya)

🚀 Next Steps:
   1. Login ke Metabase: http://localhost:3000
   2. Add Database Connection ke PostgreSQL
   3. Sync tables dari database
   4. Create visualizations dari table '{TABLE_NAME}'
   5. Build dashboard untuk analysis

📝 SQL Query Examples:
   
   -- Top 10 highest dropout risk
   SELECT Gender_Label, Scholarship_Label, Tuition_Label,
          COUNT(*) as count, AVG(Probability_Dropout) as avg_dropout_risk
   FROM {TABLE_NAME}
   WHERE Status = 'Dropout'
   GROUP BY Gender_Label, Scholarship_Label, Tuition_Label
   ORDER BY avg_dropout_risk DESC
   LIMIT 10;
   
   -- Gender vs Status analysis
   SELECT Gender_Label, Model_Prediction, COUNT(*) as count
   FROM {TABLE_NAME}
   GROUP BY Gender_Label, Model_Prediction
   ORDER BY Gender_Label, count DESC;
   
   -- Financial factors impact
   SELECT Scholarship_Label, Tuition_Label, Debtor_Label,
          COUNT(*) as total,
          SUM(CASE WHEN Status = 'Dropout' THEN 1 ELSE 0 END) as dropout_count,
          ROUND(SUM(CASE WHEN Status = 'Dropout' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as dropout_pct
   FROM {TABLE_NAME}
   GROUP BY Scholarship_Label, Tuition_Label, Debtor_Label
   ORDER BY dropout_pct DESC;

✨ Dataset ready for Metabase dashboards and analytics!
""")

# Close connection
cursor.close()
conn.close()

print("="*80)
print("✅ Connection closed successfully")
print("="*80)
