"""
Backend Unit and API Test Suite

Tests:
1. Root and Health endpoints
2. Valid prediction payloads (None, Insomnia, Sleep Apnea cases)
3. Validation on missing fields and invalid inputs
4. Output format and types
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sleep Disorder Classification API is running"}
    print("[PASS] GET / endpoint test passed")


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    print("[PASS] GET /health endpoint test passed")


def test_predict_teacher():
    payload = {
        "gender": "Female",
        "age": 28,
        "occupation": "Teacher",
        "bmi_category": "Normal",
        "sleep_duration": 7.5,
        "quality_of_sleep": 7,
        "physical_activity_level": 45,
        "stress_level": 4,
        "blood_pressure": "120/80",
        "heart_rate": 72,
        "daily_steps": 8000
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert isinstance(data["prediction"], str)
    assert isinstance(data["confidence"], (float, int))
    assert 0.0 <= data["confidence"] <= 1.0
    print(f"[PASS] POST /predict teacher response: {data}")


def test_predict_insomnia():
    payload = {
        "gender": "Male",
        "age": 45,
        "occupation": "Salesperson",
        "bmi_category": "Overweight",
        "sleep_duration": 5.2,
        "quality_of_sleep": 4,
        "physical_activity_level": 30,
        "stress_level": 8,
        "blood_pressure": "130/85",
        "heart_rate": 80,
        "daily_steps": 5000
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in ["Insomnia", "Sleep Apnea", "None"]
    assert 0.0 <= data["confidence"] <= 1.0
    print(f"[PASS] POST /predict high-stress profile response: {data}")


def test_invalid_blood_pressure():
    payload = {
        "gender": "Male",
        "age": 30,
        "occupation": "Doctor",
        "bmi_category": "Normal",
        "sleep_duration": 7.0,
        "quality_of_sleep": 8,
        "physical_activity_level": 60,
        "stress_level": 3,
        "blood_pressure": "invalid_bp",
        "heart_rate": 65,
        "daily_steps": 9000
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    print("[PASS] POST /predict invalid blood pressure validation passed")


def test_missing_fields():
    payload = {
        "gender": "Male",
        "age": 30
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    print("[PASS] POST /predict missing fields validation passed")


if __name__ == "__main__":
    print("Running backend test suite...")
    test_root()
    test_health()
    test_predict_teacher()
    test_predict_insomnia()
    test_invalid_blood_pressure()
    test_missing_fields()
    print("\nALL BACKEND TESTS PASSED SUCCESSFULLY! [OK]")
