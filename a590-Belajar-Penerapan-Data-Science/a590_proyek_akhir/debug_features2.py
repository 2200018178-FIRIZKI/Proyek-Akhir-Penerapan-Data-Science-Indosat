import pandas as pd
import joblib

# Load dataset
df = pd.read_csv('student_data_metabase_final.csv', sep=';')

# Remove Status column seperti di notebook
df_training = df[df['Status'].isin(['Dropout', 'Graduate'])].copy()

# Drop Status column untuk get X
X = df_training.drop('Status', axis=1)
y = df_training['Status']

print("=== ACTUAL FEATURES USED IN MODEL ===")
print(f"X shape: {X.shape}")
print(f"\nFeature columns ({len(X.columns)}):")
for i, col in enumerate(X.columns, 1):
    print(f"{i}. {col}")

# Compare dengan feature_names dari joblib
feature_names = joblib.load('model/feature_names.joblib')
print(f"\n=== FEATURES IN JOBLIB FILE ===")
print(f"Total: {len(feature_names)}")
print(feature_names)

print("\n=== COMPARISON ===")
X_cols_set = set(X.columns)
joblib_set = set(feature_names)

print(f"In X but not in joblib: {X_cols_set - joblib_set}")
print(f"In joblib but not in X: {joblib_set - X_cols_set}")

# Test if we can use X as features
print(f"\n=== CAN WE USE X DIRECTLY? ===")
print(f"X columns match feature_names? {list(X.columns) == feature_names}")
print(f"X columns set match? {X_cols_set == joblib_set}")
