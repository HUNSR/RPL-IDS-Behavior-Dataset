import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load the dataset
data = pd.read_csv("RPL-IDS-Beh.csv")

# Separate features and labels
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Stratified train-test split to preserve class distribution
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# Initialize and train classifiers
rf = RandomForestClassifier(n_estimators=100, random_state=42)
et = ExtraTreesClassifier(n_estimators=100, random_state=42)

rf.fit(X_train, y_train)
et.fit(X_train, y_train)

# Predict class probabilities
rf_probs = rf.predict_proba(X_test)
et_probs = et.predict_proba(X_test)

# Set threshold for class 0 (Normal)
threshold_normal = 0.82

# Final prediction based on maximum confidence
final_predictions = []
for rf_p, et_p in zip(rf_probs, et_probs):
    combined = np.vstack([rf_p, et_p])  # Stack both predictions vertically
    model_idx, class_idx = np.unravel_index(np.argmax(combined), combined.shape)
    top_prob = combined[model_idx, class_idx]

    # If top class is 0 and its probability is below threshold, select second-best class
    if class_idx == 0 and top_prob < threshold_normal:
        combined[:, 0] = -1  # Exclude class 0 from next max search
        _, second_best_class = np.unravel_index(np.argmax(combined), combined.shape)
        final_predictions.append(second_best_class)
    else:
        final_predictions.append(class_idx)

# Evaluation metrics
print("=== Max Confidence Voting with Threshold on Class 0 ===")
print(f"Accuracy:  {accuracy_score(y_test, final_predictions):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, final_predictions))
print("\nClassification Report:")
print(classification_report(y_test, final_predictions))
