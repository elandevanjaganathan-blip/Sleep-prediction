# Sleep Disorder Classification

A lightweight, full-stack Machine Learning application designed to predict sleep disorders (**None**, **Insomnia**, or **Sleep Apnea**) based on personal, lifestyle, and biometric factors.

Built with **HTML, CSS, Vanilla JavaScript** on the frontend, a **Python FastAPI** serverless backend, and **scikit-learn** for machine learning inference, deployed seamlessly on **Vercel**.

---

## 📌 Project Overview

Sleep health plays a critical role in overall physical and mental wellbeing. This project trains and benchmarks multiple classification algorithms on clinical sleep and lifestyle parameters, packaging the best-performing model into an interactive, beginner-friendly web application.

- **Frontend**: Clean Vanilla HTML5, CSS3, and JavaScript (Zero external framework dependencies).
- **Backend**: Python FastAPI serverless functions optimized for Vercel.
- **Machine Learning**: End-to-end scikit-learn Pipeline (preprocessing + Support Vector Machine).
- **Accuracy**: **97.33%** test accuracy with real model-derived probability estimates.

---

## 🎯 Features

- **End-to-End ML Pipeline**: Automated feature scaling, one-hot encoding, and classification wrapped in a reusable `Pipeline`.
- **Three Models Evaluated**: Logistic Regression, Random Forest, and Support Vector Machine (SVM).
- **Interactive UI**: Responsive assessment form, accessible inputs, instant validation, dynamic result badges, and confidence bars.
- **Vercel Serverless Ready**: Designed specifically for Vercel's Python serverless runtime with zero always-on server overhead.
- **Clean Architecture**: Clear separation of frontend, serverless API, and ML pipeline without bloated node frameworks.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JS | Lightweight, responsive interface |
| **Backend** | Python 3, FastAPI, Pydantic | RESTful API & Serverless Function |
| **Machine Learning** | scikit-learn, pandas, numpy, joblib | Data preparation & model inference |
| **Deployment** | Vercel | Static frontend CDN + Python Serverless API |

---

## 📊 Dataset & Features

The model is trained on the **Sleep Health and Lifestyle Dataset** (`ml/data/sleep_health_lifestyle_dataset.csv`):
- **Total Samples**: 374
- **Target Feature**: `Sleep Disorder` (`None`, `Insomnia`, `Sleep Apnea`)

### Evaluated Features
1. **Gender**: Male, Female
2. **Age**: Age in years (1 – 120)
3. **Occupation**: Software Engineer, Doctor, Nurse, Teacher, Engineer, Lawyer, etc.
4. **Sleep Duration**: Hours of sleep per night
5. **Quality of Sleep**: Rating on a scale of 1 to 10
6. **Physical Activity Level**: Active minutes per day
7. **Stress Level**: Rating on a scale of 1 to 10
8. **BMI Category**: Normal, Overweight, Obese
9. **Blood Pressure**: Systolic / Diastolic readings (e.g. `120/80`)
10. **Heart Rate**: Resting heart rate in bpm
11. **Daily Steps**: Total steps walked per day

---

## 🤖 Model Comparison & Evaluation

All three classification models were trained and evaluated on an 80/20 stratified split:

| Model | Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 94.67% | 95.09% | 94.67% | 94.64% | Evaluated |
| **Random Forest** | 94.67% | 94.82% | 94.67% | 94.72% | Evaluated |
| **Support Vector Machine (SVM)** | **97.33%** | **97.63%** | **97.33%** | **97.32%** | **Selected Best** |

The **Support Vector Machine** with an RBF kernel was selected and persisted as an end-to-end scikit-learn Pipeline at `ml/model/sleep_disorder_model.pkl`.

---

## 📁 Project Structure

```
Sleep-prediction/
│
├── index.html                   # Semantic HTML5 frontend
├── style.css                    # Modern responsive stylesheet
├── script.js                    # Vanilla JS validation & API interaction
│
├── api/
│   ├── predict.py               # FastAPI serverless prediction function
│   └── health.py                # Health check endpoint
│
├── ml/
│   ├── train.py                 # Training script & model comparison
│   ├── model/
│   │   ├── sleep_disorder_model.pkl  # Trained Pipeline artifact
│   │   └── metadata.json        # Evaluation metrics and class labels
│   └── data/
│       └── sleep_health_lifestyle_dataset.csv # Dataset
│
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel routing rules
├── .gitignore                   # Git ignore configurations
└── README.md                    # Project documentation
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/elandevanjaganathan-blip/Sleep-prediction.git
cd Sleep-prediction
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Re-train the Model
```bash
python ml/train.py
```

### 4. Run the Backend API
```bash
uvicorn api.predict:app --reload --port 8000
```

### 5. Launch the Frontend
You can open `index.html` directly in any web browser, or serve it using Python's built-in HTTP server:
```bash
python -m http.server 3000
```
Open `http://localhost:3000` to interact with the application.

---

## ☁️ Deployment to Vercel

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Deploy sleep disorder prediction project"
   git push origin main
   ```
2. Import the repository in [Vercel](https://vercel.com).
3. Vercel automatically detects the static HTML/CSS/JS frontend and sets up Python serverless functions from the `api/` directory.
4. No environment variables or custom build commands are needed.

---

## 📡 API Endpoints

### 1. Health Status
- **Method**: `GET /api/health`
- **Response**:
```json
{
  "status": "healthy"
}
```

### 2. Predict Sleep Disorder
- **Method**: `POST /api/predict`
- **Request Body**:
```json
{
  "gender": "Male",
  "age": 28,
  "occupation": "Doctor",
  "sleep_duration": 7.8,
  "quality_of_sleep": 7,
  "physical_activity_level": 75,
  "stress_level": 6,
  "bmi_category": "Normal",
  "blood_pressure": "120/80",
  "heart_rate": 70,
  "daily_steps": 8000
}
```
- **Response**:
```json
{
  "prediction": "None",
  "confidence": 0.92
}
```

---

## ⚠️ Disclaimer

This application is developed strictly for **educational and academic research purposes** and does not constitute medical advice or a clinical diagnosis. Always seek the advice of a qualified healthcare provider for sleep or health-related concerns.
