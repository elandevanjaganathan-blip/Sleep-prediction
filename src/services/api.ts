import { z } from 'zod';

export interface SleepFormData {
  gender: 'Male' | 'Female';
  age: number;
  occupation: string;
  bmi_category: 'Normal' | 'Overweight' | 'Obese' | 'Other';
  sleep_duration: number;
  quality_of_sleep: number;
  physical_activity_level: number;
  stress_level: number;
  blood_pressure: string;
  heart_rate: number;
  daily_steps: number;
}

export interface PredictionResponse {
  prediction: string;
  confidence: number;
}

// The Python endpoint should accept these snake_case JSON keys.
const inputSchema = z.object({
  gender: z.enum(['Male', 'Female']),
  age: z.number().int().min(1).max(120),
  occupation: z.string().trim().min(1).max(100),
  bmi_category: z.enum(['Normal', 'Overweight', 'Obese', 'Other']),
  sleep_duration: z.number().min(0).max(24),
  quality_of_sleep: z.number().int().min(1).max(10),
  physical_activity_level: z.number().int().min(0).max(1440),
  stress_level: z.number().int().min(1).max(10),
  blood_pressure: z.string().max(7).regex(/^\d{2,3}\/\d{2,3}$/).refine(value => {
    const [systolic = 0, diastolic = 0] = value.split('/').map(Number);
    return systolic >= 60 && systolic <= 250 && diastolic >= 30 && diastolic <= 150 && systolic > diastolic;
  }),
  heart_rate: z.number().int().min(20).max(250),
  daily_steps: z.number().int().min(0).max(100000),
});

const responseSchema = z.object({
  prediction: z.string().trim().min(1).max(200),
  confidence: z.number().finite().min(0).max(1),
});

export async function predictSleepDisorder(data: SleepFormData): Promise<PredictionResponse> {
  const validated = inputSchema.safeParse(data);
  if (!validated.success) throw new Error('Please check your assessment details before submitting.');
  const baseUrl = import.meta.env['VITE_API_BASE_URL']?.trim().replace(/\/+$/, '');
  if (!baseUrl) {
    throw new Error('The prediction service is not connected yet. Set VITE_API_BASE_URL to your Python API address to enable predictions.');
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);
  try {
    const response = await fetch(`${baseUrl}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(validated.data),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`The prediction service returned an error (${response.status}). Please try again later.`);
    }
    const result: unknown = await response.json();
    const parsed = responseSchema.safeParse(result);
    if (!parsed.success) {
      throw new Error('The prediction service returned an invalid result. Expected a prediction and confidence between 0 and 1.');
    }
    return parsed.data;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('The prediction service took too long to respond. Please try again.');
    }
    if (error instanceof TypeError) {
      throw new Error('Unable to reach the prediction service. Check that your Python API is running and allows requests from this website.');
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}