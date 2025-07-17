import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

FILE_PATH = "RPL-IDS-Beh.csv"

df = pd.read_csv(FILE_PATH, low_memory=False)
df.columns = df.columns.str.strip()  # إزالة الفراغات والفواصل الزائدة

if "label" not in df.columns:
    print("[ERROR] 'label' column not found. Found columns:")
    print(df.columns)
    exit()

label_col = "label"

nan_count = df[label_col].isna().sum()
if nan_count == len(df):
    print("[ERROR] All rows contain NaN in the label column.")
    exit()
else:
    df = df.dropna(subset=[label_col])
    print(f"[INFO] Removed {nan_count} rows with NaN in label column.")
print(f"\nOriginal shape: {df.shape}")

bias_cols = [
    'from', 'to', 'node_id', 'ID', 'source', 'Source', 'No.', 'Time', 'Interval',
    'destination','Destination', 'info', 'category', 'length', 'time'
]
bias_cols_present = [col for col in bias_cols if col in df.columns]

X_raw = df.drop(columns=[label_col]).copy()
y_raw = df[label_col].copy()
le = LabelEncoder()

for col in X_raw.columns:
    if X_raw[col].dtype == 'object':
        try:
            X_raw[col] = le.fit_transform(X_raw[col].astype(str))
        except:
            pass

if y_raw.dtype == 'object':
    y_raw = le.fit_transform(y_raw)

X_train_raw, X_test_raw, y_train_raw, y_test_raw = train_test_split(
    X_raw, y_raw, stratify=y_raw, test_size=0.3, random_state=42)

rf_raw = RandomForestClassifier(random_state=42)
rf_raw.fit(X_train_raw, y_train_raw)
y_pred_raw = rf_raw.predict(X_test_raw)

print("\n=== Evaluation Before Cleaning ===")
print(f"Accuracy               : {accuracy_score(y_test_raw, y_pred_raw):.4f}")
print(f"Precision (weighted)   : {precision_score(y_test_raw, y_pred_raw, average='weighted'):.4f}")
print(f"Precision (macro)      : {precision_score(y_test_raw, y_pred_raw, average='macro'):.4f}")
print(f"Recall (weighted)      : {recall_score(y_test_raw, y_pred_raw, average='weighted'):.4f}")
print(f"Recall (macro)         : {recall_score(y_test_raw, y_pred_raw, average='macro'):.4f}")
print(f"F1 Score (weighted)    : {f1_score(y_test_raw, y_pred_raw, average='weighted'):.4f}")
print(f"F1 Score (macro)       : {f1_score(y_test_raw, y_pred_raw, average='macro'):.4f}")

feat_imp_before = pd.Series(rf_raw.feature_importances_, index=X_raw.columns)
print("\n=== Importance of top 5 feature Before cleaning ===")
print(feat_imp_before.sort_values(ascending=False).head(5))

df = df.drop(columns=bias_cols_present)  # حذف الأعمدة المنحازة
df = df.drop_duplicates()

print(f"\nShape After cleaning: {df.shape}")

X = df.drop(columns=[label_col]).copy()
y = df[label_col].copy()
removed_cols = []

for col in X.columns:
    if X[col].dtype == 'object':
        try:
            X[col] = X[col].astype(float)
        except:
            try:
                X[col] = le.fit_transform(X[col].astype(str))
            except:
                removed_cols.append(col)
                X.drop(columns=[col], inplace=True)

if y.dtype == 'object':
    y = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.3, random_state=42)

rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print("\n=== Evaluation After Cleaning ===")
print(f"Accuracy               : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision (weighted)   : {precision_score(y_test, y_pred, average='weighted'):.4f}")
print(f"Precision (macro)      : {precision_score(y_test, y_pred, average='macro'):.4f}")
print(f"Recall (weighted)      : {recall_score(y_test, y_pred, average='weighted'):.4f}")
print(f"Recall (macro)         : {recall_score(y_test, y_pred, average='macro'):.4f}")
print(f"F1 Score (weighted)    : {f1_score(y_test, y_pred, average='weighted'):.4f}")
print(f"F1 Score (macro)       : {f1_score(y_test, y_pred, average='macro'):.4f}")

# === أهمية الميزات بعد التنظيف ===
feat_imp_after = pd.Series(rf.feature_importances_, index=X.columns)
print("\n=== Importance of top 5 feature After cleaning ===")
print(feat_imp_after.sort_values(ascending=False).head(5))

# === طباعة الأعمدة التي تم حذفها ===
if bias_cols_present:
    print("\n[INFO] Removed biased columns:")
    for col in bias_cols_present:
        print(f" - {col}")
else:
    print("\n[INFO] No biased columns found for removal.")

if removed_cols:
    print("\n[INFO] Removed non-numeric columns (unable to convert):")
    for col in removed_cols:
        print(f" - {col}")
else:
    print("\n[INFO] No additional non-numeric columns were removed.")
