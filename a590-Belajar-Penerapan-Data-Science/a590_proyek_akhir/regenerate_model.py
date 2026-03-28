"""
Script untuk meregenerasi model artifacts dengan versi terbaru.
PENTING: Data training hanya menggunakan Dropout dan Graduate (bukan Enrolled)
karena Enrolled belum memiliki label akhir yang definitif.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import joblib

print("=" * 70)
print("Regenerating Model Artifacts - Data Science Project")
print("=" * 70)

# Load data
print("\n[1/6] Loading dataset...")
# Try multiple paths for dataset
possible_paths = [
    '../Dataset/data.csv',
    './Dataset/data.csv',
    '../../Dataset/data.csv',
]

df = None
for path in possible_paths:
    try:
        if os.path.exists(path):
            df = pd.read_csv(path, sep=';')
            print(f"Loaded dataset from: {path}")
            break
    except:
        continue

if df is None:
    print("ERROR: Dataset file not found. Please ensure data.csv exists in Dataset directory.")
    print("Available locations checked:", possible_paths)
    sys.exit(1)

print(f"Loaded {len(df):,} records with {len(df.columns)} columns")
print(f"Status distribution (BEFORE filtering):")
print(df['Status'].value_counts())

# Filter data - ONLY Dropout and Graduate
print("\n[2/6] Filtering data - ONLY Dropout & Graduate for training...")
print("""
IMPORTANT: Data Filtering Rationale:
  - Dropout: Student stopped studying (FINAL LABEL)
  - Graduate: Student completed studies (FINAL LABEL)
  - Enrolled: Student still active (NO FINAL LABEL) - EXCLUDED from training
  
Enrolled students will be used only for prediction/inference, not for model training.
""")

df_training = df[df['Status'].isin(['Dropout', 'Graduate'])].copy()
print(f"Filtered to {len(df_training):,} records (Dropout + Graduate only)")
print(f"Status distribution (AFTER filtering):")
print(df_training['Status'].value_counts())

# Prepare data
print("\n[3/6] Preparing and preprocessing data...")
X = df_training.drop('Status', axis=1)
y = df_training['Status']

# Encode categorical variables
label_encoders = {}
categorical_cols = X.select_dtypes(include=['object']).columns
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Handle missing values
X = X.fillna(X.mean(numeric_only=True))

# Encode target (Binary: Dropout vs Graduate)
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

print(f"Data prepared: {X.shape[0]:,} samples, {X.shape[1]} features")
print(f"Target classes (BINARY): {le_target.classes_}")
print(f"Class distribution: Dropout={sum(y_encoded==0)}, Graduate={sum(y_encoded==1)}")

# Split and scale
print("\n[4/6] Splitting and scaling data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"Train set: {X_train.shape[0]:,} samples")
print(f"Test set: {X_test.shape[0]:,} samples")

# Train multiple models
print("\n[5/6] Training machine learning models...")
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

trained_models = {}
best_model = None
best_accuracy = 0
best_model_name = None

for name, model in models.items():
    # Train with appropriate data
    if name == 'Logistic Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    
    print(f"\n{name}:")
    print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  F1-Score: {f1:.4f}")
    
    trained_models[name] = model
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

print(f"\nBest Model: {best_model_name} with accuracy {best_accuracy*100:.2f}%")

# Save artifacts
print("\n[6/6] Saving model artifacts...")
os.makedirs('./model', exist_ok=True)

joblib.dump(best_model, './model/student_status_model.joblib')
joblib.dump(scaler, './model/scaler.joblib')
joblib.dump(label_encoders, './model/label_encoders.joblib')
joblib.dump(le_target, './model/le_target.joblib')
joblib.dump(X.columns, './model/feature_names.joblib')

print("Artifacts saved successfully to ./model/")

# Print system information
print("\n" + "=" * 70)
print("Model Regeneration Complete")
print("=" * 70)
print(f"Best Model: {best_model_name}")
print(f"Training Accuracy: {best_accuracy*100:.2f}%")
print(f"\nPython version: {sys.version}")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
from sklearn import __version__ as sk_version
print(f"Scikit-learn version: {sk_version}")
print("\nReady to run Streamlit app!")
