# Sleep Disorder Classification - Backend API & ML Pipeline

A Python FastAPI backend serving machine learning predictions for sleep disorder classification (None, Insomnia, and Sleep Apnea) based on biometric and lifestyle parameters.

## Project Structure

```
backend/
│
├── app.py                      # FastAPI application with REST endpoints & CORS
├── train.py                    # Complete ML training & evaluation pipeline
├── predict.py                  # Inference predictor with preprocessor & model loading
├── test_backend.py             # Test suite for backend endpoints & validation
├── requirements.txt            # Python package dependencies
│
├── data/
│   └── sleep_health_lifestyle_dataset.csv   # Sleep Health and Lifestyle Dataset
│
└── model/
    ├── sleep_disorder_model.pkl             # Trained best ML model (SVM / Random Forest)
    ├── preprocessor.pkl                     # Saved ColumnTransformer (Scaler + OneHotEncoder)
    ├── metadata.pkl                         # Model metrics & target classes metadata
    └── metadata.json                        # Human-readable metrics and evaluation results
```

---

## Dataset Details

- **Dataset Name**: Sleep Health and Lifestyle Dataset
- **Location**: `backend/data/sleep_health_lifestyle_dataset.csv`
- **Rows**: 374
- **Features**:
  - `Gender`: Male / Female
  - `Age`: Age in years (1 - 120)
  - `Occupation`: Profession (Teacher, Engineer, Doctor, Nurse, etc.)
  - `Sleep Duration`: Average sleep in hours/night
  - `Quality of Sleep`: Rating from 1 (poor) to 10 (excellent)
  - `Physical Activity Level`: Daily active minutes
  - `Stress Level`: Rating from 1 (low) to 10 (high)
  - `BMI Category`: Normal, Overweight, Obese, Other
  - `Blood Pressure`: Systolic/diastolic format (e.g. `120/80`)
  - `Heart Rate`: Resting heart rate in bpm
  - `Daily Steps`: Daily step count
- **Target**: `Sleep Disorder` (Classes: `None`, `Insomnia`, `Sleep Apnea`)

---

## Machine Learning Pipeline

The pipeline (`train.py`) performs:
1. **Data Cleaning**: Strips identifiers, normalizes categorical aliases (e.g. `'Normal Weight'` $\rightarrow$ `'Normal'`), and fills missing target values with `'None'`.
2. **Feature Engineering**: Decomposes `Blood Pressure` into `systolic_bp` and `diastolic_bp` numeric features.
3. **Preprocessing Pipeline**: 
   - `StandardScaler` for numeric columns.
   - `OneHotEncoder(handle_unknown='ignore')` for categorical columns.
   - Composed in a scikit-learn `ColumnTransformer`.
4. **Model Training & Comparison**:
   - Logistic Regression
   - Random Forest Classifier
   - Support Vector Machine (SVM)
5. **Evaluation Metrics**:
   - Accuracy
   - Precision (Weighted)
   - Recall (Weighted)
   - F1-Score (Weighted)
   - Confusion Matrix
6. **Persistence**: Saves best model and preprocessor to `backend/model/`.

---

## Installation & Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the ML Model

```bash
python train.py
```

### 3. Run the Backend API

```bash
uvicorn app:app --reload --port 8000
```

The server will start at `http://localhost:8000`.

---

## API Endpoints

### 1. Root Status
- **Method**: `GET /`
- **Response**:
```json
{
  "message": "Sleep Disorder Classification API is running"
}
```

### 2. Health Check
- **Method**: `GET /health`
- **Response**:
```json
{
  "status": "healthy"
}
```

### 3. Predict Sleep Disorder
- **Method**: `POST /predict`
- **Request Body**:
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
- **Response**:
```json
{
  "prediction": "None",
  "confidence": 0.98
}
```

---

## Deploying Backend to Render

1. Create a new **Web Service** on [Render](https://dashboard.render.com).
2. Connect your GitHub repository (`Sleep-prediction`).
3. Set the following build and runtime settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
4. Once deployed, copy your Render web service URL (e.g. `https://sleep-prediction-backend.onrender.com`).
5. Set `VITE_API_BASE_URL` in your Vercel project Environment Variables pointing to your Render backend URL.

