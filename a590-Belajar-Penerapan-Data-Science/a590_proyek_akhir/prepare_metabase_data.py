"""
================================================================================
PREPARE DATASET UNTUK METABASE & STREAMLIT
Script untuk mengubah label numerik menjadi kategorikal dan export dataset
================================================================================
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

print("="*80)
print("📊 PREPARE DATASET FOR METABASE")
print("="*80)

# STEP 1: Load Dataset
print("\n[STEP 1] Loading Dataset...")
dataset_paths = [
    '../Dataset/student_data_metabase_categorical.csv',
    'dataset_with_predictions.csv'
]

df_final = None
for path in dataset_paths:
    if os.path.exists(path):
        print(f"  ✓ Found: {path}")
        df_final = pd.read_csv(path, sep=';', encoding='utf-8')
        break

if df_final is None:
    print("  ⚠️ Dataset tidak ditemukan!")
    print("  Pastikan sudah menjalankan notebook cell sebelumnya")
    exit(1)

print(f"  ✓ Dataset loaded: {df_final.shape[0]:,} records × {df_final.shape[1]} columns")

# STEP 2: Nama Column Legacy (jika belum ada Label columns)
print("\n[STEP 2] Checking Categorical Columns...")
label_columns_exist = [col for col in df_final.columns if 'Label' in col]
if len(label_columns_exist) == 0:
    print("  ⚠️ Label columns tidak ditemukan!")
    print("  Membuat mapping kategorikal...")
    
    # Gender
    gender_map = {0: "👩 Perempuan", 1: "👨 Laki-laki"}
    df_final['Gender_Label'] = df_final['Gender'].map(gender_map)
    
    # Scholarship
    scholarship_map = {0: "❌ Tanpa Beasiswa", 1: "✅ Dengan Beasiswa"}
    df_final['Scholarship_Label'] = df_final['Scholarship_holder'].map(scholarship_map)
    
    # Tuition
    tuition_map = {0: "⚠️ Belum/Menunggak", 1: "✅ Bayar Tepat Waktu"}
    df_final['Tuition_Label'] = df_final['Tuition_fees_up_to_date'].map(tuition_map)
    
    # Debtor
    debtor_map = {0: "✅ Non-Debtor", 1: "⚠️ Debtor"}
    df_final['Debtor_Label'] = df_final['Debtor'].map(debtor_map)
    
    # Attendance
    attendance_map = {0: "🌙 Evening", 1: "☀️ Daytime"}
    df_final['Attendance_Label'] = df_final['Daytime_evening_attendance'].map(attendance_map)
    
    # Displaced
    displaced_map = {0: "🏠 Tidak Pindah", 1: "📍 Pindah"}
    df_final['Displaced_Label'] = df_final['Displaced'].map(displaced_map)
    
    # International
    international_map = {0: "🇵🇹 Domestik", 1: "🌍 Internasional"}
    df_final['International_Label'] = df_final['International'].map(international_map)
    
    # Special Needs
    special_needs_map = {0: "✓ Tidak", 1: "⚠️ Ya"}
    df_final['Special_Needs_Label'] = df_final['Educational_special_needs'].map(special_needs_map)
    
    print("  ✓ Kategorikal columns ditambahkan")
else:
    print(f"  ✓ {len(label_columns_exist)} label columns sudah ada")

# STEP 3: Pilih Kolom untuk Export
print("\n[STEP 3] Selecting Columns for Metabase...")

final_columns = [
    # Status & Predictions
    'Status',
    'Model_Prediction',
    'Prediction_Confidence',
    'Prediction_Correct',
    
    # Demographics
    'Gender', 'Gender_Label',
    'Age_at_enrollment',
    'Marital_status',
    'International', 'International_Label',
    'Displaced', 'Displaced_Label',
    
    # Academic Performance
    'Course',
    'Admission_grade',
    'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade',
    'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade',
    'Educational_special_needs', 'Special_Needs_Label',
    
    # Financial
    'Scholarship_holder', 'Scholarship_Label',
    'Tuition_fees_up_to_date', 'Tuition_Label',
    'Debtor', 'Debtor_Label',
    
    # Attendance
    'Daytime_evening_attendance', 'Attendance_Label',
    
    # Probabilities
]

# Add probability columns jika ada
prob_cols = [col for col in df_final.columns if col.startswith('Probability_')]
final_columns.extend(prob_cols)

# Filter columns yang ada
available_cols = [col for col in final_columns if col in df_final.columns]
df_export = df_final[available_cols].copy()

print(f"  ✓ {len(available_cols)} columns dipilih untuk export")

# STEP 4: Export untuk Metabase
print("\n[STEP 4] Exporting Data...")

# Buat directory jika belum ada
os.makedirs('../Dataset', exist_ok=True)

# Export ke CSV
output_file = '../Dataset/student_data_metabase_final.csv'
df_export.to_csv(output_file, index=False, sep=';', encoding='utf-8')
print(f"  ✓ CSV exported: {output_file}")
print(f"    Size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")

# Export ke Excel (jika diperlukan)
try:
    output_excel = '../Dataset/student_data_metabase_final.xlsx'
    df_export.to_excel(output_excel, index=False, sheet_name='Student Data')
    print(f"  ✓ Excel exported: {output_excel}")
except Exception as e:
    print(f"  ⚠️ Excel export failed: {e}")

# STEP 5: Summary Statistics
print("\n[STEP 5] Dataset Summary...")
print(f"""
📊 Dataset Information:
   • Total Records: {len(df_export):,}
   • Total Columns: {len(available_cols)}
   • File Format: CSV (semicolon-delimited, UTF-8 encoding)
   • Size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB

📈 Status Distribution (Actual):
""")

for status, count in df_export['Status'].value_counts().items():
    pct = count / len(df_export) * 100
    bar = "█" * int(pct / 5)
    print(f"   {status:12} │ {bar:<20} {pct:5.1f}% ({count:,})")

print(f"""
🤖 Model Predictions Distribution:
""")

for status, count in df_export['Model_Prediction'].value_counts().items():
    pct = count / len(df_export) * 100
    bar = "█" * int(pct / 5)
    print(f"   {status:12} │ {bar:<20} {pct:5.1f}% ({count:,})")

print(f"""
📌 Gender Distribution (with Labels):
""")

for gender, count in df_export['Gender_Label'].value_counts().items():
    pct = count / len(df_export) * 100
    bar = "█" * int(pct / 5)
    print(f"   {gender:25} │ {bar:<20} {pct:5.1f}%")

print(f"""
💰 Financial Status Distribution:
""")

print("   Scholarship:")
for label, count in df_export['Scholarship_Label'].value_counts().items():
    pct = count / len(df_export) * 100
    print(f"     {label:25} {pct:5.1f}%")

print("   Tuition Payment:")
for label, count in df_export['Tuition_Label'].value_counts().items():
    pct = count / len(df_export) * 100
    print(f"     {label:25} {pct:5.1f}%")

print("   Debtor Status:")
for label, count in df_export['Debtor_Label'].value_counts().items():
    pct = count / len(df_export) * 100
    print(f"     {label:25} {pct:5.1f}%")

# Model Performance
if 'Prediction_Correct' in df_export.columns:
    accuracy = (df_export['Prediction_Correct'] == 1).mean() * 100
    print(f"""
🎯 Model Performance:
   • Accuracy: {accuracy:.2f}%
   • Average Confidence: {df_export['Prediction_Confidence'].mean():.2f}%
   • Min Confidence: {df_export['Prediction_Confidence'].min():.2f}%
   • Max Confidence: {df_export['Prediction_Confidence'].max():.2f}%
""")

# STEP 6: Column Information
print(f"""
📋 Column Categories:
   • Status & Predictions: 4 columns (Status, Model_Prediction, Confidence, Correct)
   • Demographics: 7 columns (Gender, Age, Marital, International, Displaced)
   • Academic: 9 columns (Course, Admission Grade, Curricular Units, Grades)
   • Financial: 6 columns (Scholarship, Tuition, Debtor)
   • Attendance: 2 columns (Daytime/Evening Attendance)
   • Probabilities: {len(prob_cols)} columns (Class probabilities)
   • Labels: 8 columns (Kategorikal labels untuk readability)

🎨 Emoji Labels untuk Metabase Visualization:
   • Gender: 👩 Perempuan / 👨 Laki-laki
   • Scholarship: ❌ Tanpa / ✅ Dengan
   • Tuition: ⚠️ Menunggak / ✅ Tepat Waktu
   • Debtor: ⚠️ Debtor / ✅ Non-Debtor
   • Attendance: 🌙 Evening / ☀️ Daytime
   • Displaced: 🏠 Tidak Pindah / 📍 Pindah
   • International: 🇵🇹 Domestik / 🌍 Internasional

📁 Output Files:
   ✓ {output_file} (PRIMARY - untuk Metabase import)
""")

if os.path.exists('../Dataset/student_data_metabase_final.xlsx'):
    print(f"   ✓ ../Dataset/student_data_metabase_final.xlsx (Excel format)")

print(f"""
🚀 NEXT STEPS:
   1. Download file: {output_file}
   2. Upload ke METABASE:
      - Settings > Admin > Databases > Create new connection
      - Pilih PostgreSQL atau MySQL
      - Import CSV file ke database
   3. Create visualizations:
      - Status Distribution (pie chart)
      - Gender vs Status (bar chart)
      - Financial factors vs Dropout (scatter)
      - Model Predictions accuracy (gauge)
   
   4. Streamlit integration:
      - Script akan menggunakan model artifacts dari ./model/
      - Load dataset untuk reference predictions
      - Display student profiles & recommendations

✅ Dataset Ready for:
   ✓ Metabase Dashboard
   ✓ Streamlit Web Application
   ✓ Business Intelligence & Analytics
   ✓ Decision Making & Student Support Programs

📧 Contact: ipengi794@gmail.com
""")

print("="*80)
print("✨ Dataset preparation completed!")
print("="*80)
