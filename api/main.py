"""
FastAPI Backend Entrypoint for Sleep Disorder Classification
Single Vercel Serverless Function entrypoint containing /api/health and /api/predict.
"""

import re
from pathlib import Path
from typing import Literal
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 1. FastAPI App Initialization & CORS
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sleep Disorder Classification API",
    description="Machine Learning API predicting sleep disorders (None, Insomnia, Sleep Apnea).",
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
# 2. Model Pipeline Loader (Singleton using Pathlib)
# ---------------------------------------------------------------------------
_model_pipeline = None


def get_model():
    global _model_pipeline
    if _model_pipeline is None:
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
                f"Model file 'sleep_disorder_model.pkl' not found in candidate paths: {candidate_paths}. "
                "Ensure 'python ml/train.py' has been run."
            )

        _model_pipeline = joblib.load(model_path)
    return _model_pipeline


# ---------------------------------------------------------------------------
# 3. Pydantic Schemas & Field Validations
# ---------------------------------------------------------------------------
VALID_OCCUPATIONS = [
    "Accountant", "Doctor", "Engineer", "Lawyer", "Manager", "Nurse",
    "Sales Representative", "Salesperson", "Scientist", "Software Engineer", "Teacher"
]

VALID_BMI_CATEGORIES = ["Normal", "Normal Weight", "Overweight", "Obese"]


class PredictionInput(BaseModel):
    gender: Literal["Male", "Female"]
    age: int = Field(..., ge=1, le=120, description="Age in years")
    occupation: str = Field(..., min_length=1, max_length=100, description="Occupation")
    sleep_duration: float = Field(..., ge=1.0, le=24.0, description="Sleep duration in hours")
    quality_of_sleep: int = Field(..., ge=1, le=10, description="Quality of sleep from 1 to 10")
    physical_activity_level: int = Field(..., ge=0, le=720, description="Daily physical activity in minutes")
    stress_level: int = Field(..., ge=1, le=10, description="Stress level from 1 to 10")
    bmi_category: str = Field(..., min_length=1, max_length=50, description="BMI Category")
    blood_pressure: str = Field(..., min_length=3, max_length=7, description="Blood pressure e.g. 120/80")
    heart_rate: int = Field(..., ge=30, le=220, description="Resting heart rate in bpm")
    daily_steps: int = Field(..., ge=0, le=50000, description="Daily steps count")

    @field_validator("blood_pressure")
    @classmethod
    def validate_blood_pressure(cls, v: str) -> str:
        v_clean = v.strip()
        pattern = r"^\d{2,3}/\d{2,3}$"
        if not re.match(pattern, v_clean):
            raise ValueError("Blood pressure must be in systolic/diastolic format (e.g. 120/80)")
        parts = [int(p) for p in v_clean.split("/")]
        systolic, diastolic = parts[0], parts[1]
        if not (60 <= systolic <= 250 and 30 <= diastolic <= 150 and systolic > diastolic):
            raise ValueError("Enter realistic blood pressure values (e.g. 120/80)")
        return v_clean


class PredictionOutput(BaseModel):
    prediction: str
    confidence: float


class HealthOutput(BaseModel):
    message: str = "Sleep Disorder Classification API is running"
    status: str = "healthy"


# ---------------------------------------------------------------------------
# 4. Inference Logic
# ---------------------------------------------------------------------------
def run_inference(data: PredictionInput) -> PredictionOutput:
    pipeline = get_model()

    # Parse Blood Pressure into numeric systolic and diastolic
    sys_bp, dia_bp = [float(p) for p in data.blood_pressure.split("/")]

    # Normalize BMI category to match training set ('Normal Weight' -> 'Normal')
    bmi = data.bmi_category.strip()
    if bmi.lower() in ["normal weight", "normal"]:
        bmi = "Normal"

    # Construct DataFrame with exact column names expected by ColumnTransformer
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
        "systolic_bp": sys_bp,
        "diastolic_bp": dia_bp
    }])

    # Predict class using trained pipeline
    prediction = str(pipeline.predict(input_df)[0])

    # Model probability confidence
    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba(input_df)[0]
        confidence = float(np.max(probabilities))
    else:
        confidence = 1.0

    confidence = round(max(0.0, min(1.0, confidence)), 2)

    return PredictionOutput(
        prediction=prediction,
        confidence=confidence
    )


# ---------------------------------------------------------------------------
# 5. REST Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health", response_model=HealthOutput, status_code=status.HTTP_200_OK)
@app.get("/health", response_model=HealthOutput, status_code=status.HTTP_200_OK)
@app.get("/api", response_model=HealthOutput, status_code=status.HTTP_200_OK)
def health_check():
    return {
        "message": "Sleep Disorder Classification API is running",
        "status": "healthy"
    }


@app.post("/api/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
@app.post("/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
def predict_disorder(payload: PredictionInput):
    try:
        return run_inference(payload)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )


def find_frontend_file(filename: str) -> Path:
    candidates = [
        BASE_DIR / filename,
        Path.cwd() / filename,
        Path(__file__).resolve().parent / filename,
        Path("/var/task") / filename
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"{filename} not found in candidate paths: {candidates}")


@app.get("/", response_class=HTMLResponse)
def serve_index():
    try:
        path = find_frontend_file("index.html")
        return HTMLResponse(content=path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"index.html error: {str(e)}")


@app.get("/style.css")
def serve_css():
    try:
        path = find_frontend_file("style.css")
        return Response(content=path.read_text(encoding="utf-8"), media_type="text/css")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"style.css error: {str(e)}")


@app.get("/script.js")
def serve_js():
    try:
        path = find_frontend_file("script.js")
        return Response(content=path.read_text(encoding="utf-8"), media_type="application/javascript")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"script.js error: {str(e)}")
