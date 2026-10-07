import { createContext, useContext, useState, type ReactNode } from 'react';
import type { PredictionResponse } from '@/services/api';

const PredictionContext = createContext<{
  result: PredictionResponse | null;
  setResult: (result: PredictionResponse | null) => void;
} | null>(null);

export function PredictionProvider({ children }: { children: ReactNode }) {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  return <PredictionContext.Provider value={{ result, setResult }}>{children}</PredictionContext.Provider>;
}

export function usePrediction() {
  const context = useContext(PredictionContext);
  if (!context) throw new Error('PredictionProvider is required');
  return context;
}