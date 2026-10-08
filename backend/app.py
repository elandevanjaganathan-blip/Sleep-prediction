"""
FastAPI Backend Application for Sleep Disorder Classification

Endpoints:
- GET  /         : Service status message
- GET  /health   : Health check
- POST /predict  : ML model inference for sleep disorder classification
"""

import sys
import os

# Ensure backend directory is in sys.path so modules import correctly regardless of CWD
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from typing import Literal
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from predict import get_predictor

app = FastAPI(
    title="Sleep Disorder Classification API",
    description="ML backend predicting sleep disorders (Insomnia, Sleep Apnea, None) based on lifestyle and biometric metrics.",
    version="1.0.0"
)

# CORS Configuration
# Supports frontend running on Vercel, common local ports, or custom origins
raw_origins = os.getenv(
    "CORS_ORIGINS",
    "*"
)
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in allowed_origins or not allowed_origins else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SleepInput(BaseModel):
    gender: Literal["Male", "Female"]
    age: int = Field(..., ge=1, le=120, description="Age in years")
    occupation: str = Field(..., min_length=1, max_length=100, description="Occupation title")
    bmi_category: Literal["Normal", "Overweight", "Obese", "Other"]
    sleep_duration: float = Field(..., ge=0.0, le=24.0, description="Sleep duration in hours")
    quality_of_sleep: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")
    physical_activity_level: int = Field(..., ge=0, le=1440, description="Daily physical activity in minutes")
    stress_level: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")
    blood_pressure: str = Field(..., max_length=7, pattern=r"^\d{2,3}/\d{2,3}$", description="Systolic/diastolic e.g. 120/80")
    heart_rate: int = Field(..., ge=20, le=250, description="Resting heart rate in bpm")
    daily_steps: int = Field(..., ge=0, le=100000, description="Daily steps count")

    @field_validator("blood_pressure")
    @classmethod
    def validate_blood_pressure(cls, v: str) -> str:
        parts = v.split("/")
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            raise ValueError("Blood pressure must be in systolic/diastolic format (e.g. 120/80)")
        systolic = int(parts[0])
        diastolic = int(parts[1])
        if not (60 <= systolic <= 250 and 30 <= diastolic <= 150 and systolic > diastolic):
            raise ValueError("Enter a valid blood pressure reading (e.g. 120/80)")
        return v


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Sleep Disorder Classification API is running"}


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict(input_data: SleepInput):
    try:
        predictor = get_predictor()
        result = predictor.predict(input_data.model_dump())
        return result
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model artifacts not ready: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating prediction: {str(e)}"
        )
