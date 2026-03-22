"""
Script untuk membuat categorical labels dari numeric values di PostgreSQL
Dijalankan SETELAH import_data.py selesai
"""

import psycopg2
import pandas as pd

# Database connection
conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    database="student_data",
    user="admin",
    password="password"
)

cursor = conn.cursor()

# Query untuk menambah kolom kategorikal jika belum ada
alter_queries = [
    # Gender
    """
    ALTER TABLE student_data ADD COLUMN IF NOT EXISTS Gender_Label VARCHAR(50);
    """,
    # Scholarship holder
    """
    ALTER TABLE student_data ADD COLUMN IF NOT EXISTS Scholarship_Label VARCHAR(50);
    """,
    # Tuition fees
    """
    ALTER TABLE student_data ADD COLUMN IF NOT EXISTS Tuition_Label VARCHAR(50);
    """,
    # Debtor
    """
    ALTER TABLE student_data ADD COLUMN IF NOT EXISTS Debtor_Label VARCHAR(50);
    """,
    # Marital Status
    """
    ALTER TABLE student_data ADD COLUMN IF NOT EXISTS Marital_Status_Label VARCHAR(50);
    """,
]

# Jalankan ALTER TABLE
for query in alter_queries:
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"Warning: {e}")

# Update categorical labels dengan CASE statements
update_queries = [
    # Gender mapping
    """
    UPDATE student_data 
    SET Gender_Label = CASE
        WHEN Gender = '1' THEN 'Laki-laki (M)'
        WHEN Gender = '0' THEN 'Perempuan (F)'
        ELSE Gender
    END
    WHERE Gender_Label IS NULL OR Gender_Label = '';
    """,
    
    # Scholarship holder mapping
    """
    UPDATE student_data 
    SET Scholarship_Label = CASE
        WHEN Scholarship_holder = '1' THEN 'Dengan Beasiswa'
        WHEN Scholarship_holder = '0' THEN 'Tanpa Beasiswa'
        ELSE Scholarship_holder
    END
    WHERE Scholarship_Label IS NULL OR Scholarship_Label = '';
    """,
    
    # Tuition fees mapping
    """
    UPDATE student_data 
    SET Tuition_Label = CASE
        WHEN Tuition_fees_up_to_date = '1' THEN 'Bayar Tepat Waktu ✅'
        WHEN Tuition_fees_up_to_date = '0' THEN 'Belum/Menunggak ❌'
        ELSE Tuition_fees_up_to_date
    END
    WHERE Tuition_Label IS NULL OR Tuition_Label = '';
    """,
    
    # Debtor mapping
    """
    UPDATE student_data 
    SET Debtor_Label = CASE
        WHEN Debtor = '1' THEN 'Debtor (Memiliki Piutang) ⚠️'
        WHEN Debtor = '0' THEN 'Non-Debtor (Tidak Ada Piutang) ✅'
        ELSE Debtor
    END
    WHERE Debtor_Label IS NULL OR Debtor_Label = '';
    """,
    
    # Marital status mapping
    """
    UPDATE student_data 
    SET Marital_Status_Label = CASE
        WHEN Marital_status = '1' THEN 'Menikah'
        WHEN Marital_status = '2' THEN 'Bercerai'
        WHEN Marital_status = '3' THEN 'De Facto Union'
        WHEN Marital_status = '4' THEN 'Divorced'
        WHEN Marital_status = '5' THEN 'Legally Separated'
        WHEN Marital_status = '6' THEN 'Widowed'
        ELSE 'Lajang/Single'
    END
    WHERE Marital_Status_Label IS NULL OR Marital_Status_Label = '';
    """,
]

print("="*70)
print("🔄 MEMBUAT CATEGORICAL LABELS UNTUK DASHBOARD METABASE")
print("="*70)

for i, query in enumerate(update_queries, 1):
    try:
        cursor.execute(query)
        rows_affected = cursor.rowcount
        conn.commit()
        print(f"✅ Step {i}: Berhasil update ({rows_affected} rows)")
    except Exception as e:
        print(f"❌ Error pada Step {i}: {e}")
        conn.rollback()

# Verifikasi hasil
verify_query = """
SELECT 
    COUNT(*) as Total,
    SUM(CASE WHEN Gender_Label IS NOT NULL THEN 1 ELSE 0 END) as Gender_Done,
    SUM(CASE WHEN Scholarship_Label IS NOT NULL THEN 1 ELSE 0 END) as Scholarship_Done,
    SUM(CASE WHEN Tuition_Label IS NOT NULL THEN 1 ELSE 0 END) as Tuition_Done,
    SUM(CASE WHEN Debtor_Label IS NOT NULL THEN 1 ELSE 0 END) as Debtor_Done,
    SUM(CASE WHEN Marital_Status_Label IS NOT NULL THEN 1 ELSE 0 END) as Marital_Done
FROM student_data;
"""

cursor.execute(verify_query)
result = cursor.fetchone()

print("\n" + "="*70)
print("📊 HASIL VERIFIKASI")
print("="*70)
print(f"Total Records: {result[0]}")
print(f"Gender Labels: {result[1]}/{result[0]} ✅" if result[1] == result[0] else f"Gender Labels: {result[1]}/{result[0]} ⚠️")
print(f"Scholarship Labels: {result[2]}/{result[0]} ✅" if result[2] == result[0] else f"Scholarship Labels: {result[2]}/{result[0]} ⚠️")
print(f"Tuition Labels: {result[3]}/{result[0]} ✅" if result[3] == result[0] else f"Tuition Labels: {result[3]}/{result[0]} ⚠️")
print(f"Debtor Labels: {result[4]}/{result[0]} ✅" if result[4] == result[0] else f"Debtor Labels: {result[4]}/{result[0]} ⚠️")
print(f"Marital Status Labels: {result[5]}/{result[0]} ✅" if result[5] == result[0] else f"Marital Status Labels: {result[5]}/{result[0]} ⚠️")

# Tampilkan sample data
print("\n" + "="*70)
print("📋 SAMPLE DATA DENGAN CATEGORICAL LABELS")
print("="*70)

sample_query = """
SELECT 
    ID, 
    Gender, Gender_Label, 
    Scholarship_holder, Scholarship_Label,
    Tuition_fees_up_to_date, Tuition_Label,
    Debtor, Debtor_Label,
    Status
FROM student_data
LIMIT 5;
"""

df_sample = pd.read_sql(sample_query, conn)
print(df_sample.to_string())

conn.close()

print("\n✅ Selesai! Categorical labels sudah diupdate di PostgreSQL")
print("💡 Gunakan kolom baru ini di Metabase untuk visualisasi yang lebih clear")
print("   Contoh: Gender_Label, Scholarship_Label, Tuition_Label, Debtor_Label")
