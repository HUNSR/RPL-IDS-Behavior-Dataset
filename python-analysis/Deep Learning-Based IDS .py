import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Conv1D, Flatten, LSTM, Dropout, LayerNormalization, MultiHeadAttention, GlobalAveragePooling1D, Add
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

# Load and preprocess
data = pd.read_csv("RPL-IDS-Beh.csv")
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y_encoded = to_categorical(y)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.3, random_state=42)
X_train_seq = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test_seq = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
num_classes = y_encoded.shape[1]
input_shape = (X_train_seq.shape[1], 1)
label_names = ["Normal", "VNA", "DRA", "DISA", "SFA"]

# CNN
def build_cnn():
    model = Sequential([
        Input(shape=input_shape),
        Conv1D(64, 3, activation='relu'),
        Conv1D(64, 3, activation='relu'),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    return model

# LSTM
def build_lstm():
    model = Sequential([
        Input(shape=input_shape),
        LSTM(64),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    return model

# Transformer
def build_transformer():
    inputs = Input(shape=input_shape)
    x = LayerNormalization()(inputs)
    attn = MultiHeadAttention(num_heads=2, key_dim=1)(x, x)
    x = Add()([x, attn])
    x = GlobalAveragePooling1D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    return Model(inputs, outputs)

# Evaluation
def evaluate_model(name, model):
    y_pred_probs = model.predict(X_test_seq)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = np.argmax(y_test, axis=1)
    print(f"\n=== {name} Model Evaluation ===")
    print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred, average='weighted'):.4f}")
    print(f"Recall:    {recall_score(y_true, y_pred, average='weighted'):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred, average='weighted'):.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("Classification Report:")
    print(classification_report(y_true, y_pred, target_names=label_names))

# Train and Evaluate CNN
cnn = build_cnn()
cnn.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
cnn.fit(X_train_seq, y_train, epochs=10, batch_size=64, validation_split=0.1, verbose=0)
evaluate_model("CNN", cnn)

# Train and Evaluate LSTM
lstm = build_lstm()
lstm.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
lstm.fit(X_train_seq, y_train, epochs=10, batch_size=64, validation_split=0.1, verbose=0)
evaluate_model("LSTM", lstm)

# Train and Evaluate Transformer
transformer = build_transformer()
transformer.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
transformer.fit(X_train_seq, y_train, epochs=10, batch_size=64, validation_split=0.1, verbose=0)
evaluate_model("Transformer", transformer)
