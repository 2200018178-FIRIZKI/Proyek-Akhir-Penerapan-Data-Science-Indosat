import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Student Status Prediction",
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
    model = joblib.load('./model/student_status_model.joblib')
    scaler = joblib.load('./model/scaler.joblib')
    label_encoders = joblib.load('./model/label_encoders.joblib')
    le_target = joblib.load('./model/le_target.joblib')
    feature_names = joblib.load('./model/feature_names.joblib')
    return model, scaler, label_encoders, le_target, feature_names

model, scaler, label_encoders, le_target, feature_names = load_model_artifacts()

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    page = st.radio("Select Page:", ["🏠 Home", "📊 Prediction", "📈 Analytics", "ℹ️ About"])

# Home Page
if page == "🏠 Home":
    st.title("🎓 Student Status Prediction System")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### About This System
        
        This machine learning system helps **Jaya Jaya Institut** predict student outcomes:
        - 🎓 **Graduate**: Successfully completed studies
        - 📚 **Enrolled**: Currently pursuing studies
        - ⛔ **Dropout**: Left the program
        
        ### Key Features
        - Real-time student status prediction
        - Data-driven insights for student support
        - Evidence-based intervention strategies
        
        ### How to Use
        1. Navigate to **Prediction** page
        2. Enter student information
        3. Get instant prediction results
        """)
    
    with col2:
        st.markdown("""
        ### Model Performance
        
        **Accuracy**: 76.84%
        
        **Top Predictive Factors**:
        1. 2nd Semester Performance
        2. 1st Semester Performance
        3. Admission Grade
        4. Age at Enrollment
        5. Tuition Payment Status
        
        ### Dataset Info
        - **Total Records**: 4,424 students
        - **Features**: 36 input variables
        - **Target Classes**: 3 (Dropout, Enrolled, Graduate)
        """)
    
    st.markdown("---")
    st.info("👉 Use the sidebar to navigate to different sections")

# Prediction Page
elif page == "📊 Prediction":
    st.title("📊 Student Status Prediction")
    st.markdown("---")
    
    # Create input form
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Personal Information")
            age = st.number_input("Age at Enrollment", min_value=15, max_value=80, value=20)
            gender = st.selectbox("Gender", [1, 2])
            marital_status = st.selectbox("Marital Status", [1, 2, 3, 4, 5, 6])
        
        with col2:
            st.subheader("Academic Information")
            application_mode = st.number_input("Application Mode", min_value=1, max_value=60, value=1)
            admission_grade = st.number_input("Admission Grade", min_value=0.0, max_value=200.0, value=120.0)
            previous_qual = st.number_input("Previous Qualification Grade", min_value=0.0, max_value=200.0, value=122.0)
        
        with col3:
            st.subheader("Financial Information")
            tuition_fees_updated = st.selectbox("Tuition Fees Up to Date", [0, 1])
            scholarship = st.selectbox("Scholarship Holder", [0, 1])
            debtor = st.selectbox("Is Debtor", [0, 1])
        
        st.subheader("1st Semester Performance")
        col_sem1_1, col_sem1_2, col_sem1_3, col_sem1_4 = st.columns(4)
        
        with col_sem1_1:
            sem1_credited = st.number_input("1st Sem - Credited Units", min_value=0, max_value=30, value=0)
        with col_sem1_2:
            sem1_enrolled = st.number_input("1st Sem - Enrolled Units", min_value=0, max_value=30, value=0)
        with col_sem1_3:
            sem1_approved = st.number_input("1st Sem - Approved Units", min_value=0, max_value=30, value=0)
        with col_sem1_4:
            sem1_grade = st.number_input("1st Sem - Grade", min_value=0.0, max_value=20.0, value=0.0)
        
        st.subheader("2nd Semester Performance")
        col_sem2_1, col_sem2_2, col_sem2_3, col_sem2_4 = st.columns(4)
        
        with col_sem2_1:
            sem2_credited = st.number_input("2nd Sem - Credited Units", min_value=0, max_value=30, value=0)
        with col_sem2_2:
            sem2_enrolled = st.number_input("2nd Sem - Enrolled Units", min_value=0, max_value=30, value=0)
        with col_sem2_3:
            sem2_approved = st.number_input("2nd Sem - Approved Units", min_value=0, max_value=30, value=0)
        with col_sem2_4:
            sem2_grade = st.number_input("2nd Sem - Grade", min_value=0.0, max_value=20.0, value=0.0)
        
        # More fields (with default values for simplicity)
        col_other_1, col_other_2, col_other_3 = st.columns(3)
        with col_other_1:
            course = st.number_input("Course", min_value=1, max_value=17000, value=9147)
        with col_other_2:
            displaced = st.selectbox("Displaced", [0, 1])
        with col_other_3:
            international = st.selectbox("International", [0, 1])
        
        col_econ_1, col_econ_2, col_econ_3 = st.columns(3)
        with col_econ_1:
            unemployment_rate = st.number_input("Unemployment Rate (%)", min_value=0.0, max_value=30.0, value=12.7)
        with col_econ_2:
            inflation_rate = st.number_input("Inflation Rate (%)", min_value=-10.0, max_value=10.0, value=3.7)
        with col_econ_3:
            gdp = st.number_input("GDP", min_value=-10.0, max_value=10.0, value=-1.7)
        
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
        
        submit_button = st.form_submit_button("🔮 Predict Student Status", use_container_width=True)
    
    if submit_button:
        # Create DataFrame with all features in correct order
        input_data = pd.DataFrame({
            'Marital_status': [marital_status],
            'Application_mode': [application_mode],
            'Application_order': [application_order],
            'Course': [course],
            'Daytime_evening_attenda': [daytime_evening],
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
            st.subheader("🎯 Prediction Results")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                predicted_class = le_target.classes_[prediction]
                
                if predicted_class == 'Graduate':
                    st.success(f"## 🎓 Predicted Status: **{predicted_class}**")
                elif predicted_class == 'Enrolled':
                    st.info(f"## 📚 Predicted Status: **{predicted_class}**")
                else:
                    st.warning(f"## ⛔ Predicted Status: **{predicted_class}**")
            
            with col2:
                st.metric("Confidence", f"{max(probabilities)*100:.1f}%")
            
            # Probability distribution
            st.subheader("Probability Distribution")
            prob_df = pd.DataFrame({
                'Status': le_target.classes_,
                'Probability': probabilities
            }).sort_values('Probability', ascending=True)
            
            st.bar_chart(prob_df.set_index('Status')['Probability'])
            
            # Recommendations
            st.subheader("💡 Recommendations")
            
            if predicted_class == 'Dropout':
                st.warning("""
                **High-Risk Student Detected**
                
                Recommended Actions:
                - 📞 Schedule immediate counseling session
                - 📋 Review academic performance and identify challenges
                - 🤝 Assign academic mentor/advisor
                - 💰 Assess financial support needs
                - 📚 Provide additional tutoring or support programs
                """)
            elif predicted_class == 'Enrolled':
                st.info("""
                **Student on Track**
                
                Recommended Actions:
                - ✅ Continue monitoring academic progress
                - 🎯 Provide career guidance and mentorship
                - 📊 Track semester performance consistently
                - 🌟 Encourage participation in academic activities
                """)
            else:
                st.success("""
                **High Probability of Graduation**
                
                Recommended Actions:
                - 🎯 Focus on graduation preparation
                - 💼 Facilitate career placement services
                - 📜 Alumni network engagement
                - ⭐ Recognition and celebration of achievement
                """)
        
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

# Analytics Page
elif page == "📈 Analytics":
    st.title("📈 Analytics & Insights")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Accuracy", "76.84%")
    with col2:
        st.metric("Total Students Analyzed", "4,424")
    with col3:
        st.metric("Model Type", "Logistic Regression")
    
    st.markdown("---")
    st.subheader("Top 5 Most Important Features")
    
    features_importance = {
        '2nd Semester Approved Units': 0.142283,
        '2nd Semester Grade': 0.109008,
        '1st Semester Approved Units': 0.091937,
        '1st Semester Grade': 0.059588,
        'Admission Grade': 0.043575
    }
    
    import_df = pd.DataFrame(list(features_importance.items()), columns=['Feature', 'Importance'])
    import_df = import_df.sort_values('Importance', ascending=True)
    
    st.bar_chart(import_df.set_index('Feature')['Importance'])
    
    st.markdown("---")
    st.subheader("Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Academic Performance Impact
        - **Semester grades** are the strongest predictor (25.17%)
        - **Unit completion rate** crucial for success
        - **Early identification**: Monitor 1st semester performance
        """)
    
    with col2:
        st.markdown("""
        ### Student Success Factors
        - **Prior academic qualification** matters
        - **Age at enrollment** affects outcomes
        - **Financial stability** impacts retention
        - **Course selection** influences completion
        """)

# About Page
elif page == "ℹ️ About":
    st.title("ℹ️ About This Project")
    st.markdown("---")
    
    st.markdown("""
    ### Project Overview
    
    This is a **Final Project** for the Data Science Learning Path at Dicoding Academy, 
    focused on solving real-world problems for **Jaya Jaya Institut**.
    
    **Problem Statement:**
    Jaya Jaya Institut wants to identify at-risk students to implement early intervention 
    strategies and improve retention and graduation rates.
    
    ### Solution Approach
    
    **1. Data Collection & Analysis**
    - Analyzed 4,424 student records
    - 36 input features covering academic, demographic, and economic factors
    - Identified key patterns in student success/dropout
    
    **2. Machine Learning Model**
    - Algorithm: Logistic Regression
    - Accuracy: 76.84%
    - Classes: Dropout, Enrolled, Graduate
    
    **3. Key Findings**
    - Academic performance in semesters is the strongest predictor
    - Early intervention based on semester 1 performance is critical
    - Multiple factors (financial, demographic, academic) collectively influence outcomes
    
    ### Technologies Used
    - **Python 3.9+**
    - **Scikit-learn**: Machine Learning
    - **Pandas**: Data Processing
    - **Streamlit**: Web Application
    - **Matplotlib/Seaborn**: Visualization
    
    ### Action Items for Jaya Jaya Institut
    
    1. **Early Warning System**
       - Implement automated alerts for at-risk students
       - Monitor semester 1 performance closely
    
    2. **Intervention Programs**
       - Tutoring and academic support
       - Counseling services
       - Financial aid programs
    
    3. **Student Support Resources**
       - Mentorship program
       - Career guidance
       - Mental health support
    
    4. **Data-Driven Decisions**
       - Regular model updates with new data
       - Track intervention effectiveness
       - Continuous improvement of support programs
    
    ### Project Artifacts
    - 📓 Jupyter Notebook with full analysis
    - 🤖 Trained ML model (Logistic Regression)
    - 🎨 Interactive Streamlit Application
    - 📊 Feature importance analysis
    - 📈 Dashboard visualizations
    
    ### Author
    **SHAH FIRIZKI AZMI**
    - Email: ipengi794@gmail.com
    - Dicoding ID: shah-firizki-azmi
    
    ### Last Updated
    """ + datetime.now().strftime("%B %d, %Y")
    )
    
    st.markdown("---")
    st.info("For more information, visit the GitHub repository or contact the author.")
