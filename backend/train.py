"""
Sleep Disorder Classification - ML Training Pipeline

This script:
1. Loads the Sleep Health and Lifestyle dataset from backend/data/
2. Cleans and preprocesses features (splits blood pressure, normalizes categories)
3. Builds scikit-learn ColumnTransformer for scaling and encoding
4. Trains 3 classification algorithms:
   - Logistic Regression
   - Random Forest Classifier
   - Support Vector Machine (SVM)
5. Evaluates and compares all models using Accuracy, Precision, Recall, F1-Score, and Confusion Matrix
6. Selects the best performing model and saves the trained artifacts into backend/model/
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report


def clean_and_prepare_data(df: pd.DataFrame):
    """
    Standardizes column names, handles missing values, and extracts blood pressure components.
    """
    df_clean = df.copy()

    # Standardize column names to lowercase snake_case
    rename_dict = {
        'Person ID': 'person_id',
        'Gender': 'gender',
        'Age': 'age',
        'Occupation': 'occupation',
        'Sleep Duration': 'sleep_duration',
        'Quality of Sleep': 'quality_of_sleep',
        'Physical Activity Level': 'physical_activity_level',
        'Stress Level': 'stress_level',
        'BMI Category': 'bmi_category',
        'Blood Pressure': 'blood_pressure',
        'Heart Rate': 'heart_rate',
        'Daily Steps': 'daily_steps',
        'Sleep Disorder': 'sleep_disorder'
    }
    df_clean.rename(columns=rename_dict, inplace=True)

    # Drop person_id if present
    if 'person_id' in df_clean.columns:
        df_clean.drop(columns=['person_id'], inplace=True)

    # Target handling: In the dataset, NaN indicates No Sleep Disorder ("None")
    df_clean['sleep_disorder'] = df_clean['sleep_disorder'].fillna('None').astype(str).str.strip()

    # Normalize BMI Category: 'Normal Weight' -> 'Normal'
    df_clean['bmi_category'] = df_clean['bmi_category'].replace({'Normal Weight': 'Normal'})

    # Extract Systolic and Diastolic Blood Pressure
    bp_split = df_clean['blood_pressure'].astype(str).str.split('/', expand=True)
    df_clean['systolic_bp'] = pd.to_numeric(bp_split[0], errors='coerce')
    df_clean['diastolic_bp'] = pd.to_numeric(bp_split[1], errors='coerce')

    # Drop raw blood_pressure string column
    df_clean.drop(columns=['blood_pressure'], inplace=True)

    # Separate features and target
    X = df_clean.drop(columns=['sleep_disorder'])
    y = df_clean['sleep_disorder']

    return X, y


def build_preprocessor():
    """
    Creates ColumnTransformer with OneHotEncoder for categoricals and StandardScaler for numericals.
    """
    categorical_features = ['gender', 'occupation', 'bmi_category']
    numerical_features = [
        'age',
        'sleep_duration',
        'quality_of_sleep',
        'physical_activity_level',
        'stress_level',
        'heart_rate',
        'daily_steps',
        'systolic_bp',
        'diastolic_bp'
    ]

    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    numerical_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop'
    )

    return preprocessor, categorical_features, numerical_features


def train_and_evaluate(dataset_path: str = None, model_dir: str = None):
    # Set default paths relative to script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if dataset_path is None:
        dataset_path = os.path.join(base_dir, 'data', 'sleep_health_lifestyle_dataset.csv')
    if model_dir is None:
        model_dir = os.path.join(base_dir, 'model')

    os.makedirs(model_dir, exist_ok=True)

    print("==================================================")
    print("SLEEP DISORDER CLASSIFICATION - ML TRAINING")
    print("==================================================")
    print(f"Loading dataset from: {dataset_path}")

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please place sleep_health_lifestyle_dataset.csv in backend/data/.")

    df = pd.read_csv(dataset_path)
    print(f"Raw dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

    X, y = clean_and_prepare_data(df)
    classes = sorted(y.unique())
    print(f"Target classes found: {classes}")
    print(f"Class distribution:\n{y.value_counts()}")

    # Stratified Train/Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTraining set: {len(X_train)} samples, Test set: {len(X_test)} samples")

    # Fit preprocessor on training data
    preprocessor, cat_cols, num_cols = build_preprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # Initialize 3 candidate classification models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "Support Vector Machine": SVC(kernel='rbf', probability=True, random_state=42)
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None

    print("\n--------------------------------------------------")
    print("MODEL EVALUATION RESULTS")
    print("--------------------------------------------------")

    for name, model in models.items():
        # Train model
        model.fit(X_train_transformed, y_train)
        y_pred = model.predict(X_test_transformed)

        # Compute metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=classes)

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm.tolist()
        }

        print(f"\nModel: {name}")
        print(f"  Accuracy  : {acc:.4f} ({acc*100:.2f}%)")
        print(f"  Precision : {prec:.4f}")
        print(f"  Recall    : {rec:.4f}")
        print(f"  F1-Score  : {f1:.4f}")
        print(f"  Confusion Matrix (classes: {classes}):\n{cm}")
        print("\n  Classification Report:")
        print(classification_report(y_test, y_pred, target_names=classes, zero_division=0))

        # Model selection prioritizing F1-score and Accuracy
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model

    print("==================================================")
    print(f"BEST MODEL SELECTED: {best_model_name} (Weighted F1: {best_f1:.4f})")
    print("==================================================")

    # Save artifacts
    model_path = os.path.join(model_dir, "sleep_disorder_model.pkl")
    preprocessor_path = os.path.join(model_dir, "preprocessor.pkl")
    metadata_path = os.path.join(model_dir, "metadata.pkl")

    joblib.dump(best_model_obj, model_path)
    joblib.dump(preprocessor, preprocessor_path)

    metadata = {
        "best_model_name": best_model_name,
        "classes": classes,
        "metrics": results[best_model_name],
        "all_model_results": results,
        "feature_names": {
            "numerical": num_cols,
            "categorical": cat_cols
        }
    }
    joblib.dump(metadata, metadata_path)

    # Also save a human-readable metadata.json
    metadata_json_path = os.path.join(model_dir, "metadata.json")
    with open(metadata_json_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved best model to: {model_path}")
    print(f"Saved preprocessor to: {preprocessor_path}")
    print(f"Saved metadata to: {metadata_path} & {metadata_json_path}")
    print("Training pipeline completed successfully!\n")

    return best_model_name, results


if __name__ == "__main__":
    train_and_evaluate()
