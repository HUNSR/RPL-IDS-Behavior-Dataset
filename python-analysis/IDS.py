import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    classification_report
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# Load the dataset
data = pd.read_csv("processed_data.csv")  # Replace with your actual CSV path

# Separate features and labels
X = data.iloc[:, :-1]  # All columns except the last one
y = data.iloc[:, -1]  # Last column (label)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Apply SMOTE on the training set only
# smote = SMOTE(random_state=42)
# X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
# X_train = X_train_balanced
# y_train = y_train_balanced

# Initialize classifiers
classifiers = {
    "Random Forest": RandomForestClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    # "SVM": SVC(),
    # "Naive Bayes": GaussianNB(),

}

# Train each classifier and evaluate
results = {}
labels = ["Normal", "VNA", "DRA", "DISA", "SFA"]
# labels = ["Normal",   "SFA"]

for name, clf in classifiers.items():
    # Train the classifier on the balanced training set
    # clf.fit(X_train_balanced, y_train_balanced)
    clf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = clf.predict(X_test)

    # Evaluate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")
    conf_matrix = confusion_matrix(y_test, y_pred, labels=range(len(labels)))

    # Extended classification report
    report = classification_report(y_test, y_pred, target_names=labels, output_dict=True)

    # Format the report for display
    formatted_report = classification_report(y_test, y_pred, target_names=labels)

    # Save the results
    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "Confusion Matrix": conf_matrix,
        "Classification Report": formatted_report
    }

    print(f"--- {name} ---")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1 Score: {f1:.3f}")
    print("Confusion Matrix:\n", conf_matrix)
    print("Classification Report:\n", formatted_report)
    print("\n")
