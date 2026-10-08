"""
Vercel Serverless Function - Sleep Disorder Classification API
Endpoints:
- POST /api/predict (also /predict) : Model inference
- GET  /api/health  (also /health)  : Health check status
"""

import re
from pathlib import Path
from typing import Literal, Optional
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# App Initialization & CORS
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sleep Disorder Classification API",
    description="Machine Learning API for predicting sleep disorders (None, Insomnia, Sleep Apnea).",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Model Loader (Cached Singleton)
# ---------------------------------------------------------------------------
_model_pipeline = None


def get_model():
    global _model_pipeline
    if _model_pipeline is None:
        # Resolve path relative to repository root
        current_file = Path(__file__).resolve()
        candidate_paths = [
            current_file.parent.parent / "ml" / "model" / "sleep_disorder_model.pkl",
            Path.cwd() / "ml" / "model" / "sleep_disorder_model.pkl",
            current_file.parent / "model" / "sleep_disorder_model.pkl"
        ]

        model_path = None
        for p in candidate_paths:
            if p.exists():
                model_path = p
                break

        if model_path is None:
            raise FileNotFoundError(
                f"Model artifact 'sleep_disorder_model.pkl' not found in candidate paths: {candidate_paths}. "
                "Please run 'python ml/train.py' first."
            )

        _model_pipeline = joblib.load(model_path)
    return _model_pipeline


# ---------------------------------------------------------------------------
# Request & Response Schemas
# ---------------------------------------------------------------------------
class PredictionInput(BaseModel):
    gender: Literal["Male", "Female"]
    age: int = Field(..., ge=1, le=120, description="Age in years")
    occupation: str = Field(..., min_length=1, max_length=100, description="Occupation")
    sleep_duration: float = Field(..., ge=0.0, le=24.0, description="Sleep duration in hours")
    quality_of_sleep: int = Field(..., ge=1, le=10, description="Quality of sleep from 1 to 10")
    physical_activity_level: int = Field(..., ge=0, le=1440, description="Physical activity in minutes/day")
    stress_level: int = Field(..., ge=1, le=10, description="Stress level from 1 to 10")
    bmi_category: str = Field(..., min_length=1, max_length=50, description="BMI Category")
    blood_pressure: str = Field(..., min_length=3, max_length=7, description="Blood pressure e.g. 120/80")
    heart_rate: int = Field(..., ge=20, le=250, description="Resting heart rate in bpm")
    daily_steps: int = Field(..., ge=0, le=100000, description="Daily steps count")

    @field_validator("blood_pressure")
    @classmethod
    def validate_blood_pressure(cls, v: str) -> str:
        pattern = r"^\d{2,3}/\d{2,3}$"
        if not re.match(pattern, v.strip()):
            raise ValueError("Blood pressure must be in format 'systolic/diastolic', e.g. '120/80'")
        systolic, diastolic = [int(p) for p in v.split("/")]
        if not (60 <= systolic <= 250 and 30 <= diastolic <= 150 and systolic > diastolic):
            raise ValueError("Please provide realistic blood pressure values (e.g. 120/80)")
        return v.strip()


class PredictionOutput(BaseModel):
    prediction: str
    confidence: float


class HealthOutput(BaseModel):
    status: str


# ---------------------------------------------------------------------------
# Core Prediction Logic
# ---------------------------------------------------------------------------
def execute_prediction(data: PredictionInput) -> PredictionOutput:
    pipeline = get_model()

    # Feature transformation
    bp_parts = data.blood_pressure.split("/")
    systolic_bp = float(bp_parts[0])
    diastolic_bp = float(bp_parts[1])

    # Normalize BMI category
    bmi = data.bmi_category.strip()
    if bmi.lower() in ["normal weight", "normal"]:
        bmi = "Normal"

    # Construct feature DataFrame matching trained pipeline columns
    input_df = pd.DataFrame([{
        "gender": data.gender,
        "age": float(data.age),
        "occupation": data.occupation.strip(),
        "sleep_duration": float(data.sleep_duration),
        "quality_of_sleep": float(data.quality_of_sleep),
        "physical_activity_level": float(data.physical_activity_level),
        "stress_level": float(data.stress_level),
        "bmi_category": bmi,
        "heart_rate": float(data.heart_rate),
        "daily_steps": float(data.daily_steps),
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp
    }])

    # Predict class
    prediction = str(pipeline.predict(input_df)[0])

    # Compute model-derived probability/confidence
    if hasattr(pipeline, "predict_proba"):
        probs = pipeline.predict_proba(input_df)[0]
        confidence = float(np.max(probs))
    else:
        confidence = 1.0

    confidence = round(max(0.0, min(1.0, confidence)), 2)

    return PredictionOutput(
        prediction=prediction,
        confidence=confidence
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.post("/api/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
@app.post("/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
@app.post("/", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
def predict_endpoint(payload: PredictionInput):
    try:
        return execute_prediction(payload)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/api/health", response_model=HealthOutput, status_code=status.HTTP_200_OK)
@app.get("/health", response_model=HealthOutput, status_code=status.HTTP_200_OK)
def health_endpoint():
    return HealthOutput(status="healthy")


@app.get("/api", status_code=status.HTTP_200_OK)
@app.get("/", status_code=status.HTTP_200_OK)
def root_endpoint():
    return {"message": "Sleep Disorder Classification API is running", "status": "healthy"}
