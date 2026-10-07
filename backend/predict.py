"""
Sleep Disorder Classification - Prediction Service

Loads pre-trained model artifacts and produces predictions and confidence scores
for user health and lifestyle input data.
"""

import os
import joblib
import numpy as np
import pandas as pd


class SleepPredictor:
    def __init__(self, model_dir: str = None):
        if model_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(base_dir, 'model')

        self.model_path = os.path.join(model_dir, 'sleep_disorder_model.pkl')
        self.preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
        self.metadata_path = os.path.join(model_dir, 'metadata.pkl')

        if not (os.path.exists(self.model_path) and os.path.exists(self.preprocessor_path)):
            raise FileNotFoundError(
                f"Model artifacts not found in {model_dir}. Please run 'python train.py' first."
            )

        self.model = joblib.load(self.model_path)
        self.preprocessor = joblib.load(self.preprocessor_path)
        self.metadata = joblib.load(self.metadata_path) if os.path.exists(self.metadata_path) else {}
        self.classes = self.metadata.get("classes", getattr(self.model, "classes_", ["Insomnia", "None", "Sleep Apnea"]))

    def preprocess_input(self, data: dict) -> pd.DataFrame:
        """
        Converts raw input dictionary into structured DataFrame with split blood pressure and normalized BMI.
        """
        bp_raw = str(data.get('blood_pressure', '120/80')).strip()
        if '/' in bp_raw:
            parts = bp_raw.split('/')
            systolic = float(parts[0]) if parts[0].isdigit() else 120.0
            diastolic = float(parts[1]) if parts[1].isdigit() else 80.0
        else:
            systolic, diastolic = 120.0, 80.0

        bmi = str(data.get('bmi_category', 'Normal')).strip()
        if bmi.lower() in ['normal weight', 'normal']:
            bmi = 'Normal'

        row = {
            'gender': str(data.get('gender', 'Male')).strip(),
            'age': float(data.get('age', 30)),
            'occupation': str(data.get('occupation', 'Other')).strip(),
            'bmi_category': bmi,
            'sleep_duration': float(data.get('sleep_duration', 7.0)),
            'quality_of_sleep': float(data.get('quality_of_sleep', 7)),
            'physical_activity_level': float(data.get('physical_activity_level', 45)),
            'stress_level': float(data.get('stress_level', 5)),
            'heart_rate': float(data.get('heart_rate', 70)),
            'daily_steps': float(data.get('daily_steps', 7000)),
            'systolic_bp': systolic,
            'diastolic_bp': diastolic
        }

        return pd.DataFrame([row])

    def predict(self, data: dict) -> dict:
        """
        Runs ML prediction and returns disorder class and confidence decimal (0.0 - 1.0).
        """
        df_input = self.preprocess_input(data)
        X_trans = self.preprocessor.transform(df_input)

        # Class prediction
        predicted_class = str(self.model.predict(X_trans)[0])

        # Confidence calculation
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(X_trans)[0]
            confidence = float(np.max(probabilities))
        elif hasattr(self.model, "decision_function"):
            decision = self.model.decision_function(X_trans)[0]
            exp_d = np.exp(decision - np.max(decision))
            probabilities = exp_d / np.sum(exp_d)
            confidence = float(np.max(probabilities))
        else:
            confidence = 1.0

        # Bound confidence strictly between 0 and 1
        confidence = max(0.0, min(1.0, round(confidence, 2)))

        return {
            "prediction": predicted_class,
            "confidence": confidence
        }


# Lazy loaded singleton instance for reuse
_predictor_instance = None


def get_predictor() -> SleepPredictor:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = SleepPredictor()
    return _predictor_instance
