import { afterEach, describe, expect, it, vi } from 'vitest';
import { predictSleepDisorder, type SleepFormData } from './api';

const data: SleepFormData = { gender: 'Female', age: 28, occupation: 'Teacher', bmi_category: 'Normal', sleep_duration: 7.5, quality_of_sleep: 7, physical_activity_level: 45, stress_level: 4, blood_pressure: '120/80', heart_rate: 72, daily_steps: 8000 };
afterEach(() => { vi.unstubAllEnvs(); vi.unstubAllGlobals(); });
describe('Prediction API', () => {
  it('reports an unconfigured service', async () => {
    vi.stubEnv('VITE_API_BASE_URL', '');
    await expect(predictSleepDisorder(data)).rejects.toThrow('not connected yet');
  });
  it('posts the inputs and returns the actual result', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'https://sleep-api.example/');
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ prediction: 'Insomnia', confidence: 0.87 })));
    vi.stubGlobal('fetch', fetchMock);
    await expect(predictSleepDisorder(data)).resolves.toEqual({ prediction: 'Insomnia', confidence: 0.87 });
    expect(fetchMock).toHaveBeenCalledWith('https://sleep-api.example/predict', expect.objectContaining({ method: 'POST', body: JSON.stringify(data) }));
  });
  it('rejects invalid model responses', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'https://sleep-api.example');
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ prediction: 'Insomnia', confidence: 87 }))));
    await expect(predictSleepDisorder(data)).rejects.toThrow('invalid result');
  });
  it('handles unavailable services without crashing', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'https://sleep-api.example');
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    await expect(predictSleepDisorder(data)).rejects.toThrow('Unable to reach');
  });
});