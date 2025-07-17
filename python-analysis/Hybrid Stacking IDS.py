import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, StackingClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Load the dataset
data = pd.read_csv("RPL-IDS-Beh.csv")  # Ensure the file is in the same directory or provide the full path

# Separate features and labels
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define base classifiers
base_models = [
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
    ('xgb', XGBClassifier(eval_metric='mlogloss', random_state=42))
]

# Optional alternative base models (commented out)
# base_models = [
#     ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
#     ('Ext', ExtraTreesClassifier(random_state=42))
# ]

# Define the meta-classifier with class balancing
meta_model = LogisticRegression(max_iter=1000, class_weight='balanced')

# Create the stacking ensemble model
stacked_model = StackingClassifier(
    estimators=base_models,
    final_estimator=meta_model,
    passthrough=False,  # Pass only base model predictions to the meta-classifier
    cv=5,
    n_jobs=-1
)

# Train the stacked model
stacked_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = stacked_model.predict(X_test)

# Evaluate performance
print("=== Hybrid Stacking Model (Proposed Configuration) ===")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred, average='weighted'):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred, average='weighted'):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
