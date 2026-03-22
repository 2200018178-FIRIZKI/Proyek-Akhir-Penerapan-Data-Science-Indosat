# 📊 PANDUAN MENGGUNAKAN DATASET UNTUK METABASE

## 📁 File Dataset yang Telah Dipersiapkan

| File | Ukuran | Format | Tujuan |
|------|--------|--------|--------|
| `student_data_metabase_final.csv` | 1.04 MB | CSV (UTF-8) | **PRIMARY** - Import ke Metabase |
| `student_data_metabase_final.xlsx` | 2.12 MB | Excel | Alternative - Untuk analisis Excel |
| `dataset_with_predictions.csv` | 1.5 MB | CSV | Backup - Data dengan predictions |

**Lokasi:** `../Dataset/`

---

## 📋 Struktur Dataset (31 Columns)

### 1️⃣ Status & Model Predictions (4 columns)
```
- Status                    : Actual status (Dropout/Enrolled/Graduate)
- Model_Prediction         : Predicted status dari ML model
- Prediction_Confidence    : Confidence score (%) dari prediksi
- Prediction_Correct       : 1 if correct, 0 if incorrect
```

### 2️⃣ Demographics (7 columns)
```
- Gender                   : 0/1 (Original numeric)
- Gender_Label            : 👩 Perempuan / 👨 Laki-laki (CATEGORICAL)
- Age_at_enrollment       : Numeric - Age saat enrollment
- Marital_status          : Numeric - Marital status code
- International           : 0/1 (Original)
- International_Label     : 🇵🇹 Domestik / 🌍 Internasional (CATEGORICAL)
- Displaced               : 0/1 (Original)
- Displaced_Label         : 🏠 Tidak Pindah / 📍 Pindah (CATEGORICAL)
```

### 3️⃣ Academic Performance (9 columns)
```
- Course                              : Course ID/Code
- Admission_grade                     : Numeric - Grade saat admission
- Curricular_units_1st_sem_enrolled   : Jumlah unit untuk semester 1
- Curricular_units_1st_sem_approved   : Jumlah unit LULUS semester 1 ✓
- Curricular_units_1st_sem_grade      : Grade rata-rata semester 1
- Curricular_units_2nd_sem_enrolled   : Jumlah unit untuk semester 2
- Curricular_units_2nd_sem_approved   : Jumlah unit LULUS semester 2 ✓
- Curricular_units_2nd_sem_grade      : Grade rata-rata semester 2
- Educational_special_needs           : 0/1 (Original)
- Special_Needs_Label                 : ✓ Tidak / ⚠️ Ya (CATEGORICAL)
```

### 4️⃣ Financial Status (6 columns)
```
- Scholarship_holder                  : 0/1 (Original)
- Scholarship_Label                   : ❌ Tanpa / ✅ Dengan (CATEGORICAL)
- Tuition_fees_up_to_date            : 0/1 (Original)
- Tuition_Label                       : ⚠️ Menunggak / ✅ Tepat Waktu (CATEGORICAL)
- Debtor                              : 0/1 (Original)
- Debtor_Label                        : ⚠️ Debtor / ✅ Non-Debtor (CATEGORICAL)
```

### 5️⃣ Attendance (2 columns)
```
- Daytime_evening_attendance          : 0/1 (Original)
- Attendance_Label                    : 🌙 Evening / ☀️ Daytime (CATEGORICAL)
```

### 6️⃣ Probabilities (3 columns)
```
- Probability_Dropout                 : Likelihood siswa akan dropout (%)
- Probability_Enrolled                : Likelihood siswa akan enrolled (%)
- Probability_Graduate                : Likelihood siswa akan graduate (%)
```

---

## 📊 Dataset Statistics

```
Total Records          : 4,424 siswa
Total Columns          : 31 features
File Size              : 1.04 MB
Encoding               : UTF-8
Delimiter              : Semicolon (;)

Status Distribution:
  • Graduate:          49.9% (2,209)
  • Dropout:           32.1% (1,421)
  • Enrolled:          17.9% (794)

Model Accuracy:        77.19%
Average Confidence:    77.17%

Gender Distribution:
  • Perempuan (👩):   64.8% (2,868)
  • Laki-laki (👨):   35.2% (1,556)

Financial Status:
  • Tanpa Beasiswa:    75.2%
  • Dengan Beasiswa:   24.8%
  • Bayar Tepat Waktu: 88.1%
  • Menunggak:         11.9%
  • Non-Debtor:        88.6%
  • Debtor:            11.4%
```

---

## 🎨 Emoji Labels untuk Visualisasi

Semua label menggunakan emoji untuk memudahkan identifikasi visual di Metabase:

| Field | Labels |
|-------|--------|
| **Gender** | 👩 Perempuan / 👨 Laki-laki |
| **Scholarship** | ❌ Tanpa Beasiswa / ✅ Dengan Beasiswa |
| **Tuition** | ⚠️ Belum/Menunggak / ✅ Bayar Tepat Waktu |
| **Debtor** | ⚠️ Debtor / ✅ Non-Debtor |
| **Attendance** | 🌙 Evening / ☀️ Daytime |
| **Displaced** | 🏠 Tidak Pindah / 📍 Pindah |
| **International** | 🇵🇹 Domestik / 🌍 Internasional |
| **Special Needs** | ✓ Tidak / ⚠️ Ya - Kebutuhan Khusus |

---

## 🚀 Cara Import ke Metabase

### Prerequisites:
- Metabase running di `localhost:3000`
- PostgreSQL database running
- Credentials: `ipengi794@gmail.com` / `Madinah017#`

### Step-by-Step Import:

#### **Option 1: Upload CSV File**

1. **Buka Metabase** → `localhost:3000`
2. **Login** dengan credentials yang tersedia
3. **Navigate to:** Admin Panel > Databases
4. **Click:** "New Database" button
5. **Select:** PostgreSQL
6. Isi connection details:
   ```
   Host: host.docker.internal
   Port: 5432
   Database: student_data
   Username: admin
   Password: password
   ```
7. **Test Connection** & **Create**
8. **Sync Database** untuk load tables

#### **Option 2: Import CSV ke Database (Recommended)**

```sql
-- Dari terminal/SQL client:
-- 1. Create table dengan struktur
CREATE TABLE student_data_metabase (
    Status VARCHAR(50),
    Model_Prediction VARCHAR(50),
    Prediction_Confidence DECIMAL(5,2),
    Prediction_Correct INT,
    Gender INT,
    Gender_Label VARCHAR(50),
    Age_at_enrollment INT,
    Marital_status INT,
    International INT,
    International_Label VARCHAR(50),
    ...
);

-- 2. Import CSV:
COPY student_data_metabase FROM '/path/to/student_data_metabase_final.csv' 
DELIMITER ';' CSV HEADER ENCODING 'UTF8';
```

#### **Option 3: Manual Data Entry (Not Recommended)**
- Terlalu banyak kolom (31)
- Tidak efisien untuk 4,424 records
- Gunakan Option 1 atau 2

---

## 📈 Visualization Ideas untuk Metabase

### Dashboard 1: Overview
```
1. Status Distribution Pie Chart
   - Graduate: 49.9%
   - Dropout: 32.1%
   - Enrolled: 17.9%

2. Gender Distribution Bar Chart
   - 👩 Perempuan: 64.8%
   - 👨 Laki-laki: 35.2%

3. Model Accuracy Gauge
   - 77.19% accuracy

4. Sample Data Table
   - Top 20 High-Risk Dropouts
```

### Dashboard 2: Risk Analysis
```
1. Dropout Risk by Gender
   - Cross-tabulation chart
   
2. Financial Impact
   - Scholarship vs Status
   - Tuition Payment vs Status
   - Debtor Status vs Status

3. Academic Performance
   - Curricular units approved vs Status
   - Grade average vs Status

4. Risk Heatmap
   - Multiple factors vs Dropout rate
```

### Dashboard 3: Model Predictions
```
1. Prediction Accuracy Table
   - Status vs Model_Prediction confusion matrix

2. Confidence Distribution
   - Histogram of prediction confidence scores

3. Probability Distribution
   - Box plot for each class probability

4. High-Risk Student List
   - Filter by Probability_Dropout > 60%
```

---

## 💡 Actionable Insights dari Data

### 🔴 High-Risk Factors untuk Dropout:
```
1. Tidak lulus units di semester 1 (Key predictor: 0.63 correlation)
2. Grade rendah di semester 1 (0.49 correlation)
3. Age at enrollment tinggi (-0.24 correlation)
4. Adalah seorang Debtor (-0.24 correlation)
5. Jenis kelamin Laki-laki (-0.23 correlation)
6. Menggunakan application mode tertentu (-0.22 correlation)
```

### 🟢 Protective Factors untuk Graduate:
```
1. Lulus banyak units di semester 2 (0.62 correlation) ✓
2. Grade tinggi di semester 2 (0.57 correlation) ✓
3. Bayar tuition tepat waktu (0.41 correlation) ✓
4. Memiliki beasiswa (0.30 correlation) ✓
5. Adalah Perempuan (0.23 correlation) ✓
6. Non-Debtor status (0.24 correlation) ✓
```

### 💼 Business Recommendations:
```
1. Early Intervention Program
   - Target siswa dengan 0 approved units di semester 1
   - Provide academic support & tutoring

2. Financial Support
   - Expand scholarship program (saat ini hanya 24.8%)
   - Create payment plan untuk tuition

3. Mentorship Program
   - Assign mentor untuk high-risk students
   - Focus on semester 1 performance

4. Gender-Specific Support
   - Investigate why male students have higher dropout
   - Consider gender-specific programs

5. Debtor Management
   - Create payment assistance program
   - Track correlation between debtor status & dropout

6. Attendance Optimization
   - Monitor attendance patterns
   - Correlation analysis: day vs evening classes
```

---

## 📱 Streaming Data untuk Metabase

Jika ingin real-time update dari predictions:

```python
# Script untuk generate predictions on new students
from joblib import load

# Load model artifacts
model = load('./model/student_status_model.joblib')
scaler = load('./model/scaler.joblib')
encoders = load('./model/label_encoders.joblib')

# Process new data
# 1. Encode categorical
# 2. Scale features
# 3. Predict with model
# 4. Save to database/CSV

# Export ke CSV → Upload ke Metabase
# Atau stream directly ke database table
```

---

## 🔐 Data Privacy & Security

```
⚠️ IMPORTANT NOTES:

1. Dataset contains PII (Personal Identifiable Info)?
   - Recommendation: Anonymize student IDs jika diperlukan

2. Export untuk production environment?
   - Ensure proper access controls
   - Encrypt sensitive columns
   - Audit logs untuk data access

3. GDPR Compliance?
   - Assess individual rights (right to be forgotten)
   - Implement data retention policies
```

---

## 📞 Support & Next Steps

**Dataset Preparation:** ✅ COMPLETE
**Metabase Integration:** 🔄 READY (Follow steps above)
**Streamlit App:** 🔄 Integration pending
**Documentation:** ✅ COMPLETE

**Questions?** Contact: `ipengi794@gmail.com`

---

## 📋 Checklist untuk Metabase Setup

- [ ] Download file `student_data_metabase_final.csv`
- [ ] Buka Metabase di `localhost:3000`
- [ ] Connect ke PostgreSQL database
- [ ] Import/Upload CSV file
- [ ] Create first dashboard dengan status distribution
- [ ] Add drill-down untuk demographics
- [ ] Create risk analysis dashboard
- [ ] Setup alerts untuk high-risk students
- [ ] Share dashboard dengan team

---

**Version:** 1.0  
**Last Updated:** March 2026  
**Status:** ✅ Ready for Production
