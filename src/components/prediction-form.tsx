import { useState, type ReactNode } from 'react';
import { useForm, type UseFormRegister, type FieldErrors } from 'react-hook-form';
import { useNavigate } from '@tanstack/react-router';
import { AlertCircle, ArrowRight, HeartPulse, LoaderCircle, Moon, RotateCcw, ShieldCheck, UserRound } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { predictSleepDisorder, type SleepFormData } from '@/services/api';
import { usePrediction } from '@/components/prediction-context';

type FieldConfig = { name: keyof SleepFormData; label: string; placeholder?: string; unit?: string; hint?: string; min?: number; max?: number; step?: number; options?: string[]; text?: boolean };
const personal: FieldConfig[] = [
  { name: 'gender', label: 'Gender', options: ['Male', 'Female'] },
  { name: 'age', label: 'Age', min: 1, max: 120, step: 1, placeholder: 'e.g. 28', unit: 'years' },
  { name: 'occupation', label: 'Occupation', options: ['Student', 'Software Engineer', 'Doctor', 'Nurse', 'Teacher', 'Accountant', 'Engineer', 'Lawyer', 'Salesperson', 'Scientist', 'Manager', 'Other'] },
  { name: 'bmi_category', label: 'BMI Category', options: ['Normal', 'Overweight', 'Obese', 'Other'] },
];
const sleep: FieldConfig[] = [
  { name: 'sleep_duration', label: 'Sleep Duration', placeholder: 'e.g. 7.5', unit: 'hours', min: 0, max: 24, step: 0.1, hint: 'Average hours of sleep each night' },
  { name: 'quality_of_sleep', label: 'Quality of Sleep', placeholder: 'e.g. 7', unit: '/ 10', min: 1, max: 10, step: 1, hint: '1 = very poor · 10 = excellent' },
  { name: 'physical_activity_level', label: 'Physical Activity Level', placeholder: 'e.g. 45', unit: 'min / day', min: 0, max: 1440, step: 1, hint: 'Average daily active minutes' },
  { name: 'stress_level', label: 'Stress Level', placeholder: 'e.g. 4', unit: '/ 10', min: 1, max: 10, step: 1, hint: '1 = very low · 10 = very high' },
];
const health: FieldConfig[] = [
  { name: 'blood_pressure', label: 'Blood Pressure', placeholder: 'e.g. 120/80', unit: 'mmHg', text: true, hint: 'Systolic / diastolic' },
  { name: 'heart_rate', label: 'Heart Rate', placeholder: 'e.g. 72', unit: 'bpm', min: 20, max: 250, step: 1 },
  { name: 'daily_steps', label: 'Daily Steps', placeholder: 'e.g. 8000', unit: 'steps', min: 0, max: 100000, step: 1 },
];

function Field({ field, register, errors }: { field: FieldConfig; register: UseFormRegister<SleepFormData>; errors: FieldErrors<SleepFormData> }) {
  const error = errors[field.name]?.message;
  const rules = {
    required: `${field.label} is required.`,
    ...(field.options || field.text ? {} : {
      valueAsNumber: true,
      min: { value: field.min ?? 0, message: `${field.label} must be at least ${field.min}.` },
      max: { value: field.max ?? Infinity, message: `${field.label} must not exceed ${field.max}.` },
      validate: (value: string | number) => typeof value === 'number' && Number.isFinite(value) && (field.step !== 1 || Number.isInteger(value)) || 'Enter a valid number.',
    }),
    ...(field.name === 'blood_pressure' ? { validate: (value: string | number) => {
      const match = String(value).match(/^(\d{2,3})\/(\d{2,3})$/);
      if (!match) return 'Use systolic/diastolic format, e.g. 120/80.';
      const systolic = Number(match[1]); const diastolic = Number(match[2]);
      return (systolic >= 60 && systolic <= 250 && diastolic >= 30 && diastolic <= 150 && systolic > diastolic) || 'Enter a valid blood pressure reading.';
    } } : {}),
  };
  return <div><label htmlFor={field.name} className="mb-2 block text-sm font-medium">{field.label} <span className="text-muted-foreground">*</span></label><div className="relative">{field.options ? <select id={field.name} className="form-control pr-8" aria-invalid={Boolean(error)} aria-describedby={error ? `${field.name}-error` : undefined} {...register(field.name, rules)}><option value="">Select {field.label.toLowerCase()}</option>{field.options.map(option => <option key={option} value={option}>{option}</option>)}</select> : <><input id={field.name} className={`form-control ${field.unit ? 'pr-24' : ''}`} type={field.text ? 'text' : 'number'} placeholder={field.placeholder} min={field.min} max={field.max} step={field.step} aria-invalid={Boolean(error)} aria-describedby={error ? `${field.name}-error` : field.hint ? `${field.name}-hint` : undefined} {...register(field.name, rules)} />{field.unit && <span className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">{field.unit}</span>}</>}</div>{error ? <p id={`${field.name}-error`} className="mt-1.5 text-xs text-destructive">{error}</p> : field.hint ? <p id={`${field.name}-hint`} className="mt-1.5 text-xs text-muted-foreground">{field.hint}</p> : null}</div>;
}

function FormSection({ title, subtitle, icon, children }: { title: string; subtitle: string; icon: ReactNode; children: ReactNode }) {
  return <fieldset className="rounded-lg border border-border bg-card p-6 shadow-soft sm:p-7"><legend className="sr-only">{title}</legend><div className="mb-6 flex items-center gap-3"><span className="flex size-10 items-center justify-center rounded-lg bg-accent text-primary">{icon}</span><div><h2 className="text-base font-semibold">{title}</h2><p className="mt-0.5 text-xs text-muted-foreground">{subtitle}</p></div></div><div className="grid gap-x-6 gap-y-5 sm:grid-cols-2">{children}</div></fieldset>;
}

export function PredictionForm() {
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<SleepFormData>();
  const [apiError, setApiError] = useState('');
  const { setResult } = usePrediction();
  const navigate = useNavigate();
  async function submit(data: SleepFormData) {
    setApiError(''); setResult(null);
    try {
      const result = await predictSleepDisorder(data);
      setResult(result);
      await navigate({ to: '/result' });
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unable to process your prediction. Please try again.');
    }
  }
  return <form noValidate onSubmit={handleSubmit(submit)} className="space-y-5">
    <div className="flex items-center justify-between text-xs text-muted-foreground"><span>YOUR SLEEP HEALTH ASSESSMENT</span><span>* Required fields</span></div>
    <fieldset disabled={isSubmitting} className="space-y-5">
      <FormSection title="Personal Information" subtitle="A few details about you" icon={<UserRound className="size-5" />}>{personal.map(field => <Field key={field.name} field={field} register={register} errors={errors} />)}</FormSection>
      <FormSection title="Sleep & Lifestyle" subtitle="Your everyday sleep and activity patterns" icon={<Moon className="size-5" />}>{sleep.map(field => <Field key={field.name} field={field} register={register} errors={errors} />)}</FormSection>
      <FormSection title="Health Information" subtitle="Your recent health measurements" icon={<HeartPulse className="size-5" />}>{health.map(field => <Field key={field.name} field={field} register={register} errors={errors} />)}</FormSection>
    </fieldset>
    {Object.keys(errors).length > 0 && <div role="alert" className="flex gap-2 rounded-md border border-destructive/20 bg-destructive/5 p-4 text-sm text-destructive"><AlertCircle className="size-5 shrink-0" />Please check the highlighted fields before submitting.</div>}
    {apiError && <div role="alert" className="flex gap-3 rounded-md border border-destructive/20 bg-destructive/5 p-4 text-sm text-destructive"><AlertCircle className="mt-0.5 size-5 shrink-0" /><div><p className="font-semibold">Prediction unavailable</p><p className="mt-1 leading-6">{apiError}</p></div></div>}
    <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-between"><Button type="button" variant="outline" disabled={isSubmitting} className="h-12 px-5" onClick={() => { reset(); setApiError(''); setResult(null); }}><RotateCcw />Clear Form</Button><Button type="submit" disabled={isSubmitting} className="h-12 px-6">{isSubmitting ? <><LoaderCircle className="animate-spin" />Analyzing your details…</> : <>Predict Sleep Disorder <ArrowRight /></>}</Button></div>
    <p className="flex items-start justify-center gap-2 pt-2 text-center text-xs leading-5 text-muted-foreground"><ShieldCheck className="mt-0.5 size-4 shrink-0" />This prediction is for educational purposes only and is not a medical diagnosis.</p>
  </form>;
}