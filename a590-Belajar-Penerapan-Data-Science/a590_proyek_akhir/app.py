import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="Prediksi Status Siswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and preprocessing objects
@st.cache_resource
def load_model_artifacts():
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    model = joblib.load(os.path.join(model_dir, 'student_status_model.joblib'))
    scaler = joblib.load(os.path.join(model_dir, 'scaler.joblib'))
    label_encoders = joblib.load(os.path.join(model_dir, 'label_encoders.joblib'))
    le_target = joblib.load(os.path.join(model_dir, 'le_target.joblib'))
    feature_names = joblib.load(os.path.join(model_dir, 'feature_names.joblib'))
    return model, scaler, label_encoders, le_target, feature_names

# Mapping untuk dropdown options (user-friendly)
GENDER_OPTIONS = {"Laki-laki": 1, "Perempuan": 2}
MARITAL_STATUS_OPTIONS = {
    "Belum Menikah": 1,
    "Menikah": 2,
    "Janda/Duda": 3,
    "Cerai Hidup": 4,
    "Cerai Mati": 5,
    "Tidak Diketahui": 6
}
PAYMENT_STATUS_OPTIONS = {"Belum Dibayar": 0, "Sudah Dibayar": 1}
YES_NO_OPTIONS = {"Tidak": 0, "Ya": 1}

model, scaler, label_encoders, le_target, feature_names = load_model_artifacts()

# Load final dataset dengan categorical labels
@st.cache_data
def load_dataset():
    try:
        dataset_path = os.path.join(os.path.dirname(__file__), '..', 'Dataset', 'student_data_metabase_final.csv')
        df = pd.read_csv(dataset_path, sep=';', encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Tidak dapat memuat dataset: {str(e)}")
        return None

df_dataset = load_dataset()

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Konfigurasi")
    page = st.radio("Pilih Halaman:", ["🏠 Beranda", "📊 Prediksi", "📈 Analitik", "🔍 Dataset & Eksplorasi", "ℹ️ Tentang"])

# Home Page
if page == "🏠 Beranda":
    st.title("🎓 Sistem Prediksi Status Siswa")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Tentang Sistem Ini
        
        Sistem machine learning ini membantu **Jaya Jaya Institut** memprediksi hasil siswa:
        - 🎓 **Lulus**: Menyelesaikan studi dengan sukses
        - 📚 **Aktif Studi**: Sedang melanjutkan studi
        - ⛔ **Dropout**: Meninggalkan program
        
        ### Fitur Utama
        - Prediksi status siswa secara real-time
        - Wawasan berbasis data untuk dukungan siswa
        - Strategi intervensi berbasis bukti
        
        ### Cara Penggunaan
        1. Navigasi ke halaman **Prediksi**
        2. Masukkan informasi siswa
        3. Dapatkan hasil prediksi secara instan
        """)
    
    with col2:
        st.markdown("""
        ### Performa Model
        
        **Akurasi**: 76.84%
        
        **Faktor Prediktif Utama**:
        1. Performa Semester 2
        2. Performa Semester 1
        3. Nilai Penerimaan
        4. Usia saat Pendaftaran
        5. Status Pembayaran Kuliah
        
        ### Informasi Dataset
        - **Total Catatan**: 4.424 siswa
        - **Fitur**: 36 variabel input
        - **Kelas Target**: 3 (Dropout, Aktif Studi, Lulus)
        """)
    
    st.markdown("---")
    st.info("👉 Gunakan sidebar untuk menavigasi ke berbagai bagian")

# Prediction Page
elif page == "📊 Prediksi":
    st.title("📊 Prediksi Status Siswa")
    st.markdown("---")
    
    # Create input form
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👤 Informasi Pribadi")
            age = st.number_input("Usia saat Pendaftaran (tahun)", min_value=15, max_value=80, value=20, help="Contoh: 20 tahun")
            gender_label = st.selectbox("Jenis Kelamin", list(GENDER_OPTIONS.keys()))
            gender = GENDER_OPTIONS[gender_label]
            marital_label = st.selectbox("Status Pernikahan", list(MARITAL_STATUS_OPTIONS.keys()))
            marital_status = MARITAL_STATUS_OPTIONS[marital_label]
        
        with col2:
            st.subheader("📚 Informasi Akademik")
            application_mode = st.number_input("Mode Aplikasi", min_value=1, max_value=60, value=1, help="Lihat tabel mode aplikasi yang tersedia")
            admission_grade = st.number_input("Nilai Penerimaan (0-200)", min_value=0.0, max_value=200.0, value=120.0)
            previous_qual = st.number_input("Nilai Kualifikasi Sebelumnya (0-200)", min_value=0.0, max_value=200.0, value=122.0)
        
        with col3:
            st.subheader("💰 Informasi Keuangan")
            payment_label = st.selectbox("Status Pembayaran Kuliah", list(PAYMENT_STATUS_OPTIONS.keys()))
            tuition_fees_updated = PAYMENT_STATUS_OPTIONS[payment_label]
            scholarship_label = st.selectbox("Penerima Beasiswa", list(YES_NO_OPTIONS.keys()))
            scholarship = YES_NO_OPTIONS[scholarship_label]
            debtor_label = st.selectbox("Memiliki Utang", list(YES_NO_OPTIONS.keys()))
            debtor = YES_NO_OPTIONS[debtor_label]
        
        st.markdown("---")
        st.subheader("📊 Performa Semester 1")
        col_sem1_1, col_sem1_2, col_sem1_3, col_sem1_4 = st.columns(4)
        
        with col_sem1_1:
            sem1_credited = st.number_input("Sem 1 - Unit Kredit", min_value=0, max_value=30, value=0, help="Jumlah unit yang dikreditkan")
        with col_sem1_2:
            sem1_enrolled = st.number_input("Sem 1 - Unit Terdaftar", min_value=0, max_value=30, value=0, help="Jumlah unit terdaftar")
        with col_sem1_3:
            sem1_approved = st.number_input("Sem 1 - Unit Lulus", min_value=0, max_value=30, value=0, help="Jumlah unit yang lulus")
        with col_sem1_4:
            sem1_grade = st.number_input("Sem 1 - IPK/Nilai Rata-rata (0-4.0)", min_value=0.0, max_value=20.0, value=0.0)
        
        st.markdown("---")
        st.subheader("📊 Performa Semester 2")
        col_sem2_1, col_sem2_2, col_sem2_3, col_sem2_4 = st.columns(4)
        
        with col_sem2_1:
            sem2_credited = st.number_input("Sem 2 - Unit Kredit", min_value=0, max_value=30, value=0)
        with col_sem2_2:
            sem2_enrolled = st.number_input("Sem 2 - Unit Terdaftar", min_value=0, max_value=30, value=0)
        with col_sem2_3:
            sem2_approved = st.number_input("Sem 2 - Unit Lulus", min_value=0, max_value=30, value=0)
        with col_sem2_4:
            sem2_grade = st.number_input("Sem 2 - IPK/Nilai Rata-rata (0-4.0)", min_value=0.0, max_value=20.0, value=0.0)
        
        st.markdown("---")
        st.subheader("🌍 Informasi Tambahan")
        col_other_1, col_other_2, col_other_3 = st.columns(3)
        
        with col_other_1:
            course = st.number_input("Kode Program Studi", min_value=1, max_value=17000, value=9147, help="Lihat kode program studi yang tersedia")
        with col_other_2:
            displaced_label = st.selectbox("Status Terlantar", list(YES_NO_OPTIONS.keys()))
            displaced = YES_NO_OPTIONS[displaced_label]
        with col_other_3:
            international_label = st.selectbox("Siswa Internasional", list(YES_NO_OPTIONS.keys()))
            international = YES_NO_OPTIONS[international_label]
        
        st.markdown("---")
        st.subheader("📈 Faktor Ekonomi (opsional)")
        col_econ_1, col_econ_2, col_econ_3 = st.columns(3)
        with col_econ_1:
            unemployment_rate = st.number_input("Tingkat Pengangguran (%)", min_value=0.0, max_value=30.0, value=12.7)
        with col_econ_2:
            inflation_rate = st.number_input("Tingkat Inflasi (%)", min_value=-10.0, max_value=10.0, value=3.7)
        with col_econ_3:
            gdp = st.number_input("PDB Pertumbuhan (%)", min_value=-10.0, max_value=10.0, value=-1.7)
        
        # Default values for other features
        application_order = 1
        daytime_evening = 1
        previous_qualification = 1
        nacionality = 1
        mothers_qualification = 19
        fathers_qualification = 37
        mothers_occupation = 5
        fathers_occupation = 9
        educational_special_needs = 0
        sem1_evaluations = sem1_enrolled if sem1_enrolled > 0 else 0
        sem1_without_eval = 0
        sem2_evaluations = sem2_enrolled if sem2_enrolled > 0 else 0
        sem2_without_eval = 0
        
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            submit_button = st.form_submit_button("🔮 Prediksi Sekarang", use_container_width=True)
        with col_btn3:
            st.caption("💡 Tip: Isi semua field untuk mendapatkan prediksi yang akurat")
    
    if submit_button:
        # Create DataFrame with all features in correct order
        input_data = pd.DataFrame({
            'Marital_status': [marital_status],
            'Application_mode': [application_mode],
            'Application_order': [application_order],
            'Course': [course],
            'Daytime_evening_attendance': [daytime_evening],
            'Previous_qualification': [previous_qualification],
            'Previous_qualification_grade': [previous_qual],
            'Nacionality': [nacionality],
            'Mothers_qualification': [mothers_qualification],
            'Fathers_qualification': [fathers_qualification],
            'Mothers_occupation': [mothers_occupation],
            'Fathers_occupation': [fathers_occupation],
            'Admission_grade': [admission_grade],
            'Displaced': [displaced],
            'Educational_special_needs': [educational_special_needs],
            'Debtor': [debtor],
            'Tuition_fees_up_to_date': [tuition_fees_updated],
            'Gender': [gender],
            'Scholarship_holder': [scholarship],
            'Age_at_enrollment': [age],
            'International': [international],
            'Curricular_units_1st_sem_credited': [sem1_credited],
            'Curricular_units_1st_sem_enrolled': [sem1_enrolled],
            'Curricular_units_1st_sem_evaluations': [sem1_evaluations],
            'Curricular_units_1st_sem_approved': [sem1_approved],
            'Curricular_units_1st_sem_grade': [sem1_grade],
            'Curricular_units_1st_sem_without_evaluations': [sem1_without_eval],
            'Curricular_units_2nd_sem_credited': [sem2_credited],
            'Curricular_units_2nd_sem_enrolled': [sem2_enrolled],
            'Curricular_units_2nd_sem_evaluations': [sem2_evaluations],
            'Curricular_units_2nd_sem_approved': [sem2_approved],
            'Curricular_units_2nd_sem_grade': [sem2_grade],
            'Curricular_units_2nd_sem_without_evaluations': [sem2_without_eval],
            'Unemployment_rate': [unemployment_rate],
            'Inflation_rate': [inflation_rate],
            'GDP': [gdp]
        })
        
        # Make prediction
        try:
            X_pred_scaled = scaler.transform(input_data)
            prediction = model.predict(X_pred_scaled)[0]
            probabilities = model.predict_proba(X_pred_scaled)[0]
            
            # Display results
            st.markdown("---")
            st.subheader("🎯 Hasil Prediksi")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                predicted_class = le_target.classes_[prediction]
                
                if predicted_class == 'Graduate':
                    status_text = '✅ LULUS'
                    st.success(f"## {status_text}")
                    st.markdown("**Status:** Siswa diproyeksikan akan berhasil menyelesaikan program studi")
                elif predicted_class == 'Enrolled':
                    status_text = '📚 AKTIF STUDI'
                    st.info(f"## {status_text}")
                    st.markdown("**Status:** Siswa diproyeksikan akan melanjutkan studi")
                else:
                    status_text = '⚠️ RISIKO DROPOUT'
                    st.warning(f"## {status_text}")
                    st.markdown("**Status:** Siswa memiliki risiko tinggi untuk dropout kemudian")
            
            with col2:
                st.metric("Tingkat Kepercayaan", f"{max(probabilities)*100:.1f}%", delta=None)
            
            with col3:
                top_prob_class = le_target.classes_[np.argmax(probabilities)]
                if top_prob_class == 'Graduate':
                    st.metric("Kemungkinan", "TINGGI ✅")
                elif top_prob_class == 'Enrolled':
                    st.metric("Kemungkinan", "SEDANG 📊")
                else:
                    st.metric("Kemungkinan", "BERGEJALA ⚠️")
            
            st.markdown("---")
            st.subheader("📊 Distribusi Probabilitas")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                prob_df = pd.DataFrame({
                    'Status': ['Lulus ✅' if x == 'Graduate' else 'Aktif Studi 📚' if x == 'Enrolled' else 'Dropout ⚠️' for x in le_target.classes_],
                    'Probabilitas (%)': probabilities * 100
                }).sort_values('Probabilitas (%)', ascending=True)
                
                st.bar_chart(prob_df.set_index('Status')['Probabilitas (%)'])
            
            with col2:
                st.markdown("""
                **Interpretasi:**
                - Probabilitas tertinggi menunjukkan hasil yang paling mungkin
                - Nilai > 50% menunjukkan kepercayaan tinggi
                - Nilai 30-50% menunjukkan hasil yang perlu diperhatikan
                """)
            
            # Recommendations
            st.subheader("💡 Rekomendasi")
            
            if predicted_class == 'Dropout':
                st.warning("""
                **Siswa Berisiko Tinggi Terdeteksi**
                
                Tindakan yang Direkomendasikan:
                - 📞 Jadwalkan sesi konseling segera
                - 📋 Tinjau performa akademik dan identifikasi tantangan
                - 🤝 Tetapkan mentor/penasihat akademik
                - 💰 Nilai kebutuhan dukungan keuangan
                - 📚 Sediakan program tutoring atau dukungan tambahan
                """)
            elif predicted_class == 'Enrolled':
                st.info("""
                **Siswa dalam Jalur yang Tepat**
                
                Tindakan yang Direkomendasikan:
                - ✅ Terus pantau progres akademik
                - 🎯 Sediakan bimbingan karir dan mentoring
                - 📊 Lacak performa semester secara konsisten
                - 🌟 Dorong partisipasi dalam kegiatan akademik
                """)
            else:
                st.success("""
                **Probabilitas Tinggi untuk Lulus**
                
                Tindakan yang Direkomendasikan:
                - 🎯 Fokus pada persiapan kelulusan
                - 💼 Fasilitasi layanan penempatan karir
                - 📜 Keterlibatan jaringan alumni
                - ⭐ Pengakuan dan perayaan pencapaian
                """)
        
        except Exception as e:
            st.error(f"Kesalahan dalam prediksi: {str(e)}")

# Analytics Page
elif page == "📈 Analitik":
    st.title("📈 Analitik & Wawasan")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Akurasi Model", "76.84%")
    with col2:
        st.metric("Total Siswa Dianalisis", "4.424")
    with col3:
        st.metric("Tipe Model", "Logistic Regression")
    
    st.markdown("---")
    st.subheader("5 Fitur Paling Penting")
    
    features_importance = {
        'Unit Lulus Semester 2': 0.142283,
        'Nilai Semester 2': 0.109008,
        'Unit Lulus Semester 1': 0.091937,
        'Nilai Semester 1': 0.059588,
        'Nilai Penerimaan': 0.043575
    }
    
    import_df = pd.DataFrame(list(features_importance.items()), columns=['Fitur', 'Kepentingan'])
    import_df = import_df.sort_values('Kepentingan', ascending=True)
    
    st.bar_chart(import_df.set_index('Fitur')['Kepentingan'])
    
    st.markdown("---")
    st.subheader("Wawasan Kunci")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Dampak Performa Akademik
        - **Nilai semester** adalah prediktor terkuat (25.17%)
        - **Tingkat penyelesaian unit** krusial untuk kesuksesan
        - **Identifikasi awal**: Monitor performa semester 1
        """)
    
    with col2:
        st.markdown("""
        ### Faktor Kesuksesan Siswa
        - **Kualifikasi akademik sebelumnya** penting
        - **Usia saat pendaftaran** mempengaruhi hasil
        - **Stabilitas keuangan** berdampak pada retensi
        - **Pilihan program** mempengaruhi penyelesaian
        """)

# Dataset & Exploration Page
elif page == "🔍 Dataset & Eksplorasi":
    st.title("🔍 Dataset & Eksplorasi Data")
    st.markdown("---")
    
    if df_dataset is not None:
        # Dataset Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Siswa", len(df_dataset))
        with col2:
            st.metric("Total Fitur", len(df_dataset.columns))
        with col3:
            graduates = len(df_dataset[df_dataset['Status'] == 'Graduate'])
            st.metric("Lulus ✅", f"{graduates:,}")
        with col4:
            dropouts = len(df_dataset[df_dataset['Status'] == 'Dropout'])
            st.metric("Dropout ⚠️", f"{dropouts:,}")
        
        st.markdown("---")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Tabel Data", "📊 Statistik", "🎯 Distribusi Status", "👥 Demografi", "💰 Finansial"])
        
        with tab1:
            st.subheader("Tabel Data Lengkap")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                search_term = st.text_input("🔍 Cari (nama kolom):", help="Cari berdasarkan nama field")
            with col2:
                rows_to_show = st.slider("Jumlah baris:", min_value=5, max_value=100, value=20)
            
            # Filter columns based on search
            if search_term:
                filtered_cols = [col for col in df_dataset.columns if search_term.lower() in col.lower()]
                if filtered_cols:
                    st.dataframe(df_dataset[filtered_cols].head(rows_to_show), use_container_width=True)
                else:
                    st.warning(f"Tidak ada kolom yang sesuai dengan '{search_term}'")
            else:
                # Show important columns by default
                important_cols = ['Status', 'Model_Prediction', 'Prediction_Confidence',
                                 'Gender_Label', 'Scholarship_Label', 'Tuition_Label', 'Debtor_Label',
                                 'Attendance_Label', 'Displaced_Label', 'International_Label',
                                 'Special_Needs_Label', 'Age_at_enrollment']
                available_cols = [col for col in important_cols if col in df_dataset.columns]
                st.dataframe(df_dataset[available_cols].head(rows_to_show), use_container_width=True)
            
            st.info(f"💡 Menampilkan {min(rows_to_show, len(df_dataset))} dari {len(df_dataset):,} baris")
        
        with tab2:
            st.subheader("Statistik Deskriptif")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                stat_type = st.radio("Pilih Tipe:", ["Numerik", "Kategorikal"])
            
            if stat_type == "Numerik":
                numeric_cols = df_dataset.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    st.dataframe(df_dataset[numeric_cols].describe(), use_container_width=True)
                else:
                    st.warning("Tidak ada kolom numerik")
            else:
                categorical_cols = [col for col in df_dataset.columns if '_Label' in col or col == 'Status']
                if categorical_cols:
                    st.subheader("Distribusi Kategorikal")
                    for col in categorical_cols[:6]:  # Show first 6
                        st.write(f"**{col}**")
                        st.dataframe(df_dataset[col].value_counts(), use_container_width=True)
        
        with tab3:
            st.subheader("Distribusi Status Siswa")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Status actual distribution
                status_counts = df_dataset['Status'].value_counts()
                status_data = pd.DataFrame({
                    'Status': ['Graduate ✅', 'Dropout ⚠️', 'Enrolled 📚'],
                    'Jumlah': [status_counts.get('Graduate', 0), status_counts.get('Dropout', 0), status_counts.get('Enrolled', 0)]
                })
                
                st.markdown("**Status Aktual**")
                st.bar_chart(status_data.set_index('Status')['Jumlah'])
            
            with col2:
                # Prediction distribution
                pred_counts = df_dataset['Model_Prediction'].value_counts()
                pred_data = pd.DataFrame({
                    'Model Prediction': ['Graduate ✅', 'Dropout ⚠️', 'Enrolled 📚'],
                    'Jumlah': [pred_counts.get('Graduate', 0), pred_counts.get('Dropout', 0), pred_counts.get('Enrolled', 0)]
                })
                
                st.markdown("**Prediksi Model**")
                st.bar_chart(pred_data.set_index('Model Prediction')['Jumlah'])
            
            st.markdown("---")
            # Prediction accuracy
            accuracy = len(df_dataset[df_dataset['Prediction_Correct'] == 1]) / len(df_dataset) * 100
            st.metric("Akurasi Prediksi Model", f"{accuracy:.2f}%")
            
            st.subheader("Tingkat Kepercayaan Prediksi")
            conf_col = [col for col in df_dataset.columns if 'Prediction_Confidence' in col or 'confidence' in col.lower()]
            if conf_col:
                confidence_data = df_dataset[conf_col[0]]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Min Confidence", f"{confidence_data.min():.2f}%")
                with col2:
                    st.metric("Rata-rata", f"{confidence_data.mean():.2f}%")
                with col3:
                    st.metric("Median", f"{confidence_data.median():.2f}%")
                with col4:
                    st.metric("Max Confidence", f"{confidence_data.max():.2f}%")
                
                st.markdown("**Distribusi Tingkat Kepercayaan**")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.hist(confidence_data, bins=30, color='#3498db', edgecolor='black', alpha=0.7)
                ax.set_xlabel("Confidence Score (%)")
                ax.set_ylabel("Jumlah Prediksi")
                ax.set_title("Distribusi Tingkat Kepercayaan Model")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
        
        with tab4:
            st.subheader("Analisis Demografi Siswa")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gender distribution
                if 'Gender_Label' in df_dataset.columns:
                    st.markdown("**Distribusi Jenis Kelamin**")
                    gender_counts = df_dataset['Gender_Label'].value_counts()
                    st.bar_chart(gender_counts)
            
            with col2:
                # Age distribution
                if 'Age_at_enrollment' in df_dataset.columns:
                    st.markdown("**Distribusi Usia saat Pendaftaran**")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.hist(df_dataset['Age_at_enrollment'], bins=20, color='#2ecc71', edgecolor='black', alpha=0.7)
                    ax.set_xlabel("Usia (tahun)")
                    ax.set_ylabel("Jumlah Siswa")
                    ax.set_title("Distribusi Usia saat Pendaftaran")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # International status
                if 'International_Label' in df_dataset.columns:
                    st.markdown("**Status Internasional**")
                    intl_counts = df_dataset['International_Label'].value_counts()
                    st.pie(intl_counts.values, labels=intl_counts.index, use_container_width=True)
            
            with col2:
                # Special needs
                if 'Special_Needs_Label' in df_dataset.columns:
                    st.markdown("**Kebutuhan Khusus**")
                    needs_counts = df_dataset['Special_Needs_Label'].value_counts()
                    st.pie(needs_counts.values, labels=needs_counts.index, use_container_width=True)
        
        with tab5:
            st.subheader("Analisis Finansial Siswa")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Scholarship
                if 'Scholarship_Label' in df_dataset.columns:
                    st.markdown("**Penerima Beasiswa**")
                    scholarship_counts = df_dataset['Scholarship_Label'].value_counts()
                    st.bar_chart(scholarship_counts)
            
            with col2:
                # Tuition payment
                if 'Tuition_Label' in df_dataset.columns:
                    st.markdown("**Status Pembayaran Kuliah**")
                    tuition_counts = df_dataset['Tuition_Label'].value_counts()
                    st.bar_chart(tuition_counts)
            
            with col3:
                # Debtor status
                if 'Debtor_Label' in df_dataset.columns:
                    st.markdown("**Status Debtor**")
                    debtor_counts = df_dataset['Debtor_Label'].value_counts()
                    st.bar_chart(debtor_counts)
            
            st.markdown("---")
            
            # Financial summary
            st.subheader("Ringkasan Finansial")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                scholarship_pct = (df_dataset['Scholarship_Label'].str.contains('✅', na=False).sum() / len(df_dataset) * 100)
                st.metric("Penerima Beasiswa", f"{scholarship_pct:.1f}%")
            
            with col2:
                tuition_pct = (df_dataset['Tuition_Label'].str.contains('✅', na=False).sum() / len(df_dataset) * 100)
                st.metric("Pembayaran Tepat Waktu", f"{tuition_pct:.1f}%")
            
            with col3:
                non_debtor_pct = (df_dataset['Debtor_Label'].str.contains('Non-Debtor', na=False).sum() / len(df_dataset) * 100)
                st.metric("Non-Debtor", f"{non_debtor_pct:.1f}%")

# About Page
elif page == "ℹ️ Tentang":
    st.title("ℹ️ Tentang Proyek Ini")
    st.markdown("---")
    
    st.markdown("""
    ### Ringkasan Proyek
    
    Ini adalah **Proyek Akhir** untuk Data Science Learning Path di Dicoding Academy, 
    berfokus pada penyelesaian masalah dunia nyata untuk **Jaya Jaya Institut**.
    
    **Pernyataan Masalah:**
    Jaya Jaya Institut ingin mengidentifikasi siswa berisiko untuk menerapkan 
    strategi intervensi awal dan meningkatkan tingkat retensi dan kelulusan.
    
    ### Pendekatan Solusi
    
    **1. Pengumpulan & Analisis Data**
    - Menganalisis 4.424 catatan siswa
    - 36 fitur input yang mencakup faktor akademik, demografis, dan ekonomi
    - Mengidentifikasi pola kunci dalam kesuksesan/dropout siswa
    
    **2. Model Machine Learning**
    - Algoritma: Logistic Regression
    - Akurasi: 76.84%
    - Kelas: Dropout, Aktif Studi, Lulus
    
    **3. Temuan Utama**
    - Performa akademik di semester adalah prediktor terkuat
    - Intervensi awal berdasarkan performa semester 1 sangat penting
    - Beberapa faktor (keuangan, demografis, akademik) secara kolektif mempengaruhi hasil
    
    ### Teknologi yang Digunakan
    - **Python 3.9+**
    - **Scikit-learn**: Machine Learning
    - **Pandas**: Pemrosesan Data
    - **Streamlit**: Aplikasi Web
    - **Matplotlib/Seaborn**: Visualisasi
    
    ### Item Tindakan untuk Jaya Jaya Institut
    
    1. **Sistem Peringatan Dini**
       - Implementasi pemberitahuan otomatis untuk siswa berisiko
       - Pantau performa semester 1 dengan cermat
    
    2. **Program Intervensi**
       - Tutoring dan dukungan akademik
       - Layanan konseling
       - Program bantuan keuangan
    
    3. **Sumber Daya Dukungan Siswa**
       - Program mentoring
       - Bimbingan karir
       - Dukungan kesehatan mental
    
    4. **Keputusan Berbasis Data**
       - Update model reguler dengan data baru
       - Lacak efektivitas intervensi
       - Perbaikan berkelanjutan program dukungan
    
    ### Artefak Proyek
    - 📓 Jupyter Notebook dengan analisis lengkap
    - 🤖 Model ML terlatih (Logistic Regression)
    - 🎨 Aplikasi Streamlit Interaktif
    - 📊 Analisis kepentingan fitur
    - 📈 Visualisasi dashboard
    
    ### Penulis
    **SHAH FIRIZKI AZMI**
    - Email: ipengi794@gmail.com
    - Dicoding ID: shah-firizki-azmi
    
    ### Terakhir Diperbarui
    """ + datetime.now().strftime("%d %B, %Y")
    )
    
    st.markdown("---")
    st.info("Untuk informasi lebih lanjut, kunjungi repositori GitHub atau hubungi penulis.")
