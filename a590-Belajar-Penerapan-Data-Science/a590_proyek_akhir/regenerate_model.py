"""
Script untuk meregenerasi model artifacts dengan versi terbaru
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib

print("=" * 70)
print("Regenerating Model Artifacts with Compatible Versions")
print("=" * 70)

# Load data
print("\n[1/5] Loading dataset...")
df = pd.read_csv('../Dataset/data.csv', sep=';')
print(f"✓ Loaded {len(df)} records with {len(df.columns)} columns")

# Prepare data
print("\n[2/5] Preparing data...")
X = df.drop('Status', axis=1)
y = df['Status']

# Encode categorical variables
label_encoders = {}
categorical_cols = X.select_dtypes(include=['object']).columns
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Handle missing values
X = X.fillna(X.mean(numeric_only=True))

# Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

print(f"✓ Data prepared: {X.shape[0]} samples, {X.shape[1]} features")
print(f"✓ Target classes: {le_target.classes_}")

# Split and scale
print("\n[3/5] Splitting and scaling data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"✓ Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# Train model
print("\n[4/5] Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
accuracy = model.score(X_test_scaled, y_test)
print(f"✓ Model trained with accuracy: {accuracy:.4f}")

# Save artifacts
print("\n[5/5] Saving model artifacts...")
os.makedirs('./model', exist_ok=True)

joblib.dump(model, './model/student_status_model.joblib')
print("✓ Saved: student_status_model.joblib")

joblib.dump(scaler, './model/scaler.joblib')
print("✓ Saved: scaler.joblib")

joblib.dump(label_encoders, './model/label_encoders.joblib')
print("✓ Saved: label_encoders.joblib")

joblib.dump(le_target, './model/le_target.joblib')
print("✓ Saved: le_target.joblib")

joblib.dump(X.columns, './model/feature_names.joblib')
print("✓ Saved: feature_names.joblib")

print("\n" + "=" * 70)
print("✅ All artifacts regenerated successfully!")
print("=" * 70)
print(f"\nModel Performance: {accuracy*100:.2f}%")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
from sklearn import __version__ as sk_version
print(f"Scikit-learn version: {sk_version}")
print("\nReady to run Streamlit app!")
