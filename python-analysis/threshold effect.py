import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
data = pd.read_csv("RPL-IDS-Beh.csv")
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# Initialize classifiers
rf = RandomForestClassifier(n_estimators=100, random_state=42)
et = ExtraTreesClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
et.fit(X_train, y_train)

# Predict probabilities
rf_probs = rf.predict_proba(X_test)
et_probs = et.predict_proba(X_test)

# Threshold range
thresholds = [0.60, 0.70, 0.75, 0.80, 0.85, 0.90]
results = []

# Loop through thresholds
for threshold in thresholds:
    final_predictions = []
    for rf_p, et_p in zip(rf_probs, et_probs):
        combined = np.vstack([rf_p, et_p])
        model_idx, class_idx = np.unravel_index(np.argmax(combined), combined.shape)
        top_prob = combined[model_idx, class_idx]

        if class_idx == 0 and top_prob < threshold:
            combined[:, 0] = -1
            _, second_best_class = np.unravel_index(np.argmax(combined), combined.shape)
            final_predictions.append(second_best_class)
        else:
            final_predictions.append(class_idx)

    report = classification_report(y_test, final_predictions, output_dict=True, zero_division=0)
    accuracy = accuracy_score(y_test, final_predictions)
    f1_macro = report["macro avg"]["f1-score"]
    recall_macro = report["macro avg"]["recall"]
    precision_macro = report["macro avg"]["precision"]
    sfa_recall = report.get("4", {}).get("recall", 0.0)

    results.append({
        "Threshold": threshold,
        "Accuracy": accuracy,
        "Macro F1": f1_macro,
        "Macro Recall": recall_macro,
        "Macro Precision": precision_macro,
        "SFA Recall": sfa_recall
    })

# Convert to DataFrame
results_df = pd.DataFrame(results)
print(results_df)

# Plot with larger, bold fonts
plt.figure(figsize=(10, 6))
plt.plot(results_df["Threshold"], results_df["Accuracy"], marker='o', label="Accuracy")
plt.plot(results_df["Threshold"], results_df["Macro F1"], marker='o', label="Macro F1")
plt.plot(results_df["Threshold"], results_df["Macro Recall"], marker='o', label="Macro Recall")
plt.plot(results_df["Threshold"], results_df["SFA Recall"], marker='o', label="SFA Recall")

plt.xlabel("Threshold for Normal Class", fontsize=14, fontweight='bold')
plt.ylabel("Score", fontsize=14, fontweight='bold')
plt.title("Performance Metrics vs. Threshold", fontsize=16, fontweight='bold')

plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.legend(fontsize=12, frameon=True)
plt.grid(True)
plt.tight_layout()
plt.show()
