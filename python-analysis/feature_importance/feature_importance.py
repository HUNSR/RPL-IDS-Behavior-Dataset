import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

input_file = "SFA.csv" # should be with format attack_name.csv
attack = input_file.split('.')[0]

# Load the dataset
data = pd.read_csv(input_file)

# Specify feature columns and target column
feature_columns = data.columns[:-1]  # Assuming last column is the target
target_column = data.columns[-1]

X = data[feature_columns]
y = data[target_column]

# Train a Random Forest model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(random_state=42, n_estimators=100)
rf_model.fit(X_train, y_train)

# Calculate feature importance
feature_importances = rf_model.feature_importances_

# Create a DataFrame for visualization
importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# Select the top 10 features
top_10_features = importance_df.head(10)

# Visualize the top 10 feature importance
plt.figure(figsize=(12, 8))
plt.barh(top_10_features['Feature'], top_10_features['Importance'], color='skyblue')
plt.gca().invert_yaxis()
plt.xlabel('Feature Importance', fontsize=14)
plt.ylabel('Feature', fontsize=14)
plt.title('Top 10 Feature Importance Rankings for Detecting '+attack+' Using Random Forest', fontsize=16)

# Adjust y-axis tick labels for better readability
plt.yticks(fontsize=12)
plt.xticks(fontsize=12)
plt.tight_layout()

# Save and display the image
plt.savefig(attack, dpi=300, bbox_inches='tight')
plt.show()

