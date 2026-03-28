import pandas as pd
import joblib

# Load dataset untuk lihat kolom
df = pd.read_csv('student_data_metabase_final.csv', sep=';')
print("=== DATASET COLUMNS ===")
print(f"Total columns: {len(df.columns)}")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# Load model dan cek feature_names
print("\n=== MODEL REQUIREMENTS ===")
try:
    model = joblib.load('model/student_status_model.joblib')
    # Get n_features_in_ dari model
    n_features = model.n_features_in_
    print(f"Model expects {n_features} features")
    
    # Check jika model punya feature_names
    if hasattr(model, 'feature_names_in_'):
        print(f"Model feature names: {model.feature_names_in_}")
    else:
        print("Model tidak menyimpan feature_names")
        
except Exception as e:
    print(f"Error loading model: {e}")

# Cek pickle file
print("\n=== FEATURE NAMES FROM FILE ===")
try:
    feature_names = joblib.load('model/feature_names.joblib')
    print(f"Total features in joblib: {len(feature_names)}")
    print(f"Feature names: {feature_names}")
except Exception as e:
    print(f"Error: {e}")
