/**
 * Sleep Disorder Classification - Client Application
 * Handles assessment form validation, API communication, and result rendering.
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('sleepForm');
  const submitBtn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnLoader = document.getElementById('btnLoader');
  const resetBtn = document.getElementById('resetBtn');
  
  const resultCard = document.getElementById('resultCard');
  const resultDisorder = document.getElementById('resultDisorder');
  const resultConfidence = document.getElementById('resultConfidence');
  const confidenceBar = document.getElementById('confidenceBar');
  const resultExplanation = document.getElementById('resultExplanation');
  const predictAgainBtn = document.getElementById('predictAgainBtn');
  
  const errorAlert = document.getElementById('errorAlert');
  const errorMessage = document.getElementById('errorMessage');

  // Input Field References
  const fields = [
    'gender',
    'age',
    'occupation',
    'sleep_duration',
    'quality_of_sleep',
    'physical_activity_level',
    'stress_level',
    'bmi_category',
    'blood_pressure',
    'heart_rate',
    'daily_steps'
  ];

  // -------------------------------------------------------------------------
  // Validation Logic
  // -------------------------------------------------------------------------
  function validateField(name, value) {
    switch (name) {
      case 'gender':
        return value ? '' : 'Please select your gender.';
      case 'age': {
        const val = parseInt(value, 10);
        if (isNaN(val) || val < 1 || val > 120) {
          return 'Please enter a valid age between 1 and 120.';
        }
        return '';
      }
      case 'occupation':
        return value ? '' : 'Please select your occupation.';
      case 'sleep_duration': {
        const val = parseFloat(value);
        if (isNaN(val) || val < 1.0 || val > 24.0) {
          return 'Please enter sleep duration between 1 and 24 hours.';
        }
        return '';
      }
      case 'quality_of_sleep': {
        const val = parseInt(value, 10);
        if (isNaN(val) || val < 1 || val > 10) {
          return 'Please rate sleep quality from 1 to 10.';
        }
        return '';
      }
      case 'physical_activity_level': {
        const val = parseInt(value, 10);
        if (isNaN(val) || val < 0 || val > 720) {
          return 'Please enter active minutes between 0 and 720.';
        }
        return '';
      }
      case 'stress_level': {
        const val = parseInt(value, 10);
        if (isNaN(val) || val < 1 || val > 10) {
          return 'Please rate stress level from 1 to 10.';
        }
        return '';
      }
      case 'bmi_category':
        return value ? '' : 'Please select your BMI category.';
      case 'blood_pressure': {
        const bpPattern = /^\d{2,3}\/\d{2,3}$/;
        if (!bpPattern.test(value.trim())) {
          return 'Format must be systolic/diastolic (e.g. 120/80).';
        }
        const [sys, dia] = value.split('/').map(Number);
        if (sys < 60 || sys > 250 || dia < 30 || dia > 150 || sys <= dia) {
          return 'Please enter realistic values (e.g. 120/80).';
        }
        return '';
      }
      case 'heart_rate': {
        const val = parseInt(value, 10);
        if (isNaN(val) || val < 30 || val > 220) {
          return 'Please enter heart rate between 30 and 220 bpm.';
        }
        return '';
      }
      case 'daily_steps': {
        const val = parseInt(value, 10);
        if (isNaN(val) || val < 0 || val > 50000) {
          return 'Please enter daily steps between 0 and 50,000.';
        }
        return '';
      }
      default:
        return '';
    }
  }

  function validateAll() {
    let isValid = true;
    fields.forEach((fieldId) => {
      const el = document.getElementById(fieldId);
      const errEl = document.getElementById(`${fieldId}Error`);
      const error = validateField(fieldId, el.value);

      if (error) {
        isValid = false;
        el.classList.add('is-invalid');
        if (errEl) errEl.textContent = error;
      } else {
        el.classList.remove('is-invalid');
        if (errEl) errEl.textContent = '';
      }
    });
    return isValid;
  }

  // Clear errors on input
  fields.forEach((fieldId) => {
    const el = document.getElementById(fieldId);
    if (!el) return;
    el.addEventListener('input', () => {
      el.classList.remove('is-invalid');
      const errEl = document.getElementById(`${fieldId}Error`);
      if (errEl) errEl.textContent = '';
      hideError();
    });
  });

  // -------------------------------------------------------------------------
  // UI State Helpers
  // -------------------------------------------------------------------------
  function setLoading(loading) {
    if (loading) {
      submitBtn.disabled = true;
      btnText.textContent = 'Analyzing your sleep profile...';
      btnLoader.classList.remove('hidden');
    } else {
      submitBtn.disabled = false;
      btnText.textContent = 'Predict Sleep Disorder';
      btnLoader.classList.add('hidden');
    }
  }

  function showError(msg) {
    errorMessage.textContent = msg || 'Unable to connect to the prediction service. Please try again.';
    errorAlert.classList.remove('hidden');
  }

  function hideError() {
    errorAlert.classList.add('hidden');
  }

  function renderResult(data) {
    const prediction = data.prediction || 'None';
    const confidencePercent = Math.round((data.confidence || 0) * 100);

    resultDisorder.textContent = prediction;
    resultConfidence.textContent = `${confidencePercent}%`;

    // Reset badge classes
    resultDisorder.className = 'result-value disorder-badge';
    if (prediction.toLowerCase() === 'none') {
      resultDisorder.classList.add('disorder-none');
      resultExplanation.textContent = 'Your metrics indicate healthy sleep patterns with no significant markers of common sleep disorders.';
    } else if (prediction.toLowerCase() === 'insomnia') {
      resultDisorder.classList.add('disorder-insomnia');
      resultExplanation.textContent = 'Patterns associated with insomnia were detected (e.g., lower sleep duration, elevated stress, or disrupted sleep quality).';
    } else if (prediction.toLowerCase() === 'sleep apnea') {
      resultDisorder.classList.add('disorder-apnea');
      resultExplanation.textContent = 'Characteristics correlating with sleep apnea were identified (such as blood pressure, BMI, and biometric markers).';
    } else {
      resultExplanation.textContent = 'Assessment completed based on provided lifestyle and sleep variables.';
    }

    // Progress bar animation
    confidenceBar.style.width = '0%';
    resultCard.classList.remove('hidden');
    
    // Smooth scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    setTimeout(() => {
      confidenceBar.style.width = `${confidencePercent}%`;
    }, 100);
  }

  // -------------------------------------------------------------------------
  // Form Submission
  // -------------------------------------------------------------------------
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideError();

    if (!validateAll()) {
      const firstInvalid = form.querySelector('.is-invalid');
      if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstInvalid.focus();
      }
      return;
    }

    const payload = {
      gender: document.getElementById('gender').value,
      age: parseInt(document.getElementById('age').value, 10),
      occupation: document.getElementById('occupation').value,
      sleep_duration: parseFloat(document.getElementById('sleep_duration').value),
      quality_of_sleep: parseInt(document.getElementById('quality_of_sleep').value, 10),
      physical_activity_level: parseInt(document.getElementById('physical_activity_level').value, 10),
      stress_level: parseInt(document.getElementById('stress_level').value, 10),
      bmi_category: document.getElementById('bmi_category').value,
      blood_pressure: document.getElementById('blood_pressure').value.trim(),
      heart_rate: parseInt(document.getElementById('heart_rate').value, 10),
      daily_steps: parseInt(document.getElementById('daily_steps').value, 10)
    };

    setLoading(true);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const result = await response.json();
      renderResult(result);
    } catch (err) {
      console.error('Prediction request failed:', err);
      showError('Unable to connect to the prediction service. Please try again.');
    } finally {
      setLoading(false);
    }
  });

  // -------------------------------------------------------------------------
  // Reset & Predict Again
  // -------------------------------------------------------------------------
  function resetAll() {
    form.reset();
    resultCard.classList.add('hidden');
    hideError();
    fields.forEach((fieldId) => {
      const el = document.getElementById(fieldId);
      if (el) el.classList.remove('is-invalid');
      const errEl = document.getElementById(`${fieldId}Error`);
      if (errEl) errEl.textContent = '';
    });
  }

  resetBtn.addEventListener('click', resetAll);

  predictAgainBtn.addEventListener('click', () => {
    resultCard.classList.add('hidden');
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    const firstInput = document.getElementById('gender');
    if (firstInput) firstInput.focus();
  });
});
