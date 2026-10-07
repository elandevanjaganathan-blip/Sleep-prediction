# Sleep Disorder Classification

An end-to-end Machine Learning web application designed to assess sleep health and predict the likelihood of sleep disorders (**None**, **Insomnia**, or **Sleep Apnea**) using clinical and lifestyle factors.

---

## Project Overview

This project pairs an interactive, accessible React + TypeScript frontend with a high-performance Python FastAPI backend. The machine learning pipeline trains, evaluates, and compares multiple classification models (**Logistic Regression**, **Random Forest**, and **Support Vector Machine**) on the **Sleep Health and Lifestyle Dataset**, deploying the highest-accuracy model with full preprocessing preservation.

---

## Project Architecture

```
+-------------------------------------------------------------+
|                      React Frontend                         |
|  - Assessment Form (biometrics, sleep habits, lifestyle)    |
|  - Real-time client-side validation (Zod + React Hook Form) |
|  - Displays Predicted Disorder & Model Confidence Score     |
+-------------------------------------------------------------+
                              │
                    HTTP POST │ /predict
                    (JSON)    ▼
+-------------------------------------------------------------+
|                     FastAPI Backend                         |
|  - Request schema validation (Pydantic)                     |
|  - CORS middleware support                                  |
|  - REST endpoints: GET /, GET /health, POST /predict        |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                  ML Preprocessing & Inference               |
|  - Feature transformation (ColumnTransformer)               |
|    * Categorical: One-Hot Encoding (gender, occupation, BMI)|
|    * Numerical: Standard Scaling (BP split, steps, HR, etc.)|
|  - Best Trained Classifier (SVM / Random Forest)            |
|  - Outputs: Predicted Class & Confidence Probability        |
+-------------------------------------------------------------+
```

---

## Technology Stack

- **Frontend**: React 19, TypeScript, TanStack Router, Tailwind CSS, Lucide Icons, Zod, React Hook Form
- **Backend**: Python 3.12, FastAPI, Uvicorn, Pydantic
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib

---

## Folder Structure

```
Sleep-prediction/
├── backend/
│   ├── app.py                      # FastAPI application
│   ├── train.py                    # ML model training and evaluation script
│   ├── predict.py                  # Prediction inference service
│   ├── test_backend.py             # Test suite for backend endpoints & validation
│   ├── requirements.txt            # Python dependencies
│   ├── data/
│   │   └── sleep_health_lifestyle_dataset.csv  # Dataset
│   ├── model/
│   │   ├── sleep_disorder_model.pkl            # Best trained ML model
│   │   ├── preprocessor.pkl                    # Feature scaler & encoder
│   │   ├── metadata.pkl                        # Model metrics & metadata
│   │   └── metadata.json                       # Readable evaluation results
│   └── README.md
│
├── src/                            # React application source code
│   ├── components/                 # UI & Form components
│   ├── routes/                     # TanStack Router pages
│   └── services/                   # Frontend API client
├── .env.example                    # Environment variable template
├── package.json                    # Frontend dependencies and scripts
└── README.md                       # Project documentation
```

---

## Getting Started

### 1. Backend Setup

Open a terminal and navigate to the `backend` directory:

```bash
cd backend
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Train and evaluate the machine learning models:

```bash
python train.py
```

Start the FastAPI development server:

```bash
uvicorn app:app --reload --port 8000
```

The backend will be available at:
- **API URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

---

### 2. Frontend Setup

In a new terminal window at the project root:

Create your local environment file (optional if default is `http://localhost:8000`):

```bash
cp .env.example .env.local
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend development server:

```bash
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## API Reference

### `POST /predict`

**Request Body (`application/json`):**
```json
{
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
```

**Response (`application/json`):**
```json
{
  "prediction": "None",
  "confidence": 0.91
}
```

---

## Model Evaluation Summary

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| **Support Vector Machine (SVM)** | **97.33%** | **0.9763** | **0.9733** | **0.9732** |
| Random Forest Classifier | 96.00% | 0.9606 | 0.9600 | 0.9599 |
| Logistic Regression | 94.67% | 0.9509 | 0.9467 | 0.9464 |

*Best performing model (SVM) is automatically exported and served by the API.*
