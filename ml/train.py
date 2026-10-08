"""
Sleep Disorder Classification - Model Training Pipeline
Trains Logistic Regression, Random Forest, and Support Vector Machine.
Evaluates using Accuracy, Precision, Recall, F1-score, and Confusion Matrix.
Saves the best end-to-end Pipeline to ml/model/sleep_disorder_model.pkl.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def load_and_clean_data(csv_path: str):
    print("=" * 60)
    print("STEP 1: LOADING AND INSPECTING DATASET")
    print("=" * 60)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nInitial Missing Values:")
    print(df.isnull().sum())

    # Target column cleaning: NaN represents 'None' (healthy / no sleep disorder)
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None').str.strip()
    print("\nTarget Class Distribution:")
    print(df['Sleep Disorder'].value_counts())

    # Standardize column names to lowercase snake_case
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    # Clean BMI Category ('Normal Weight' -> 'Normal')
    df['bmi_category'] = df['bmi_category'].replace({'Normal Weight': 'Normal'}).str.strip()

    # Split Blood Pressure into systolic and diastolic numeric features
    bp_split = df['blood_pressure'].str.split('/', expand=True)
    df['systolic_bp'] = bp_split[0].astype(float)
    df['diastolic_bp'] = bp_split[1].astype(float)

    # Drop identifier and original blood_pressure string column
    df = df.drop(columns=['person_id', 'blood_pressure'])

    return df


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'sleep_health_lifestyle_dataset.csv')
    model_dir = os.path.join(base_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)

    df = load_and_clean_data(data_path)

    # Separate Features and Target
    target_col = 'sleep_disorder'
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Identify Feature Columns
    categorical_cols = ['gender', 'occupation', 'bmi_category']
    numerical_cols = [
        'age', 'sleep_duration', 'quality_of_sleep',
        'physical_activity_level', 'stress_level', 'heart_rate',
        'daily_steps', 'systolic_bp', 'diastolic_bp'
    ]

    print(f"\nNumerical Features ({len(numerical_cols)}): {numerical_cols}")
    print(f"Categorical Features ({len(categorical_cols)}): {categorical_cols}")

    # Train / Test Split (Stratified to maintain class proportions)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTraining set size: {X_train.shape[0]} samples")
    print(f"Test set size: {X_test.shape[0]} samples")

    # Define Preprocessing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ]
    )

    # Define Models to Train
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Support Vector Machine": SVC(probability=True, kernel='rbf', C=1.0, random_state=42)
    }

    print("\n" + "=" * 60)
    print("STEP 2: TRAINING AND EVALUATING MODELS")
    print("=" * 60)

    results = []
    trained_pipelines = {}
    classes = sorted(y.unique().tolist())

    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=classes)

        results.append({
            "model": name,
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "confusion_matrix": cm.tolist()
        })
        trained_pipelines[name] = pipeline

        print(f"\n--- {name} ---")
        print(f"Accuracy  : {acc * 100:.2f}%")
        print(f"Precision : {prec * 100:.2f}%")
        print(f"Recall    : {rec * 100:.2f}%")
        print(f"F1-Score  : {f1 * 100:.2f}%")
        print("Confusion Matrix:")
        print(f"Classes: {classes}")
        print(cm)

    # Comparison Table
    print("\n" + "=" * 60)
    print("MODEL COMPARISON TABLE")
    print("=" * 60)
    print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 65)
    for r in results:
        print(f"{r['model']:<25} {r['accuracy']:<12.4f} {r['precision']:<12.4f} {r['recall']:<12.4f} {r['f1']:<12.4f}")

    # Select Best Model based on F1-Score
    best_result = max(results, key=lambda x: (x['f1'], x['accuracy']))
    best_name = best_result['model']
    best_pipeline = trained_pipelines[best_name]

    print("\n" + "=" * 60)
    print(f"BEST MODEL SELECTED: {best_name}")
    print(f"Accuracy: {best_result['accuracy'] * 100:.2f}%, F1-Score: {best_result['f1'] * 100:.2f}%")
    print("=" * 60)

    # Save Best Model Pipeline
    model_save_path = os.path.join(model_dir, 'sleep_disorder_model.pkl')
    joblib.dump(best_pipeline, model_save_path)
    print(f"\n[OK] Model pipeline saved to: {model_save_path}")

    # Save Metadata
    metadata = {
        "best_model": best_name,
        "classes": classes,
        "features": {
            "numerical": numerical_cols,
            "categorical": categorical_cols
        },
        "metrics": best_result,
        "all_results": results
    }
    meta_path = os.path.join(model_dir, 'metadata.json')
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"[OK] Metadata saved to: {meta_path}")


if __name__ == "__main__":
    main()
