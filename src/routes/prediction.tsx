import { createFileRoute, Link } from '@tanstack/react-router';
import { ArrowLeft, BrainCircuit, Check, Info } from 'lucide-react';
import { PredictionForm } from '@/components/prediction-form';

export const Route = createFileRoute('/prediction')({
  head: () => ({ meta: [
    { title: 'Sleep Assessment — Sleep Disorder Classification' },
    { name: 'description', content: 'Enter your personal, sleep, lifestyle, and health information for a sleep disorder prediction.' },
    { property: 'og:title', content: 'Sleep Assessment — Sleep Disorder Classification' },
    { property: 'og:description', content: 'Complete your sleep health assessment for machine learning based analysis.' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
  ] }),
  component: PredictionPage,
});

function PredictionPage() {
  return <div className="bg-muted/35"><div className="mx-auto max-w-6xl px-6 py-10 lg:px-10 lg:py-12">
    <Link to="/" className="mb-7 inline-flex items-center gap-2 text-xs font-medium text-muted-foreground hover:text-primary"><ArrowLeft className="size-3.5" />Back to Home</Link>
    <p className="eyebrow">UNDERSTAND YOUR SLEEP</p><h1 className="mt-3 text-3xl font-semibold sm:text-4xl">Sleep Health Prediction</h1><p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground">Every detail brings us closer to a clearer picture. Tell us about your health and daily habits to begin your assessment.</p>
    <div className="mt-10 grid items-start gap-10 lg:grid-cols-[1fr_260px]">
      <PredictionForm />
      <aside className="hidden space-y-8 pt-9 lg:block"><div><span className="mb-4 flex size-11 items-center justify-center rounded-lg bg-accent text-primary"><BrainCircuit className="size-6" /></span><h2 className="text-base font-semibold">A more complete picture</h2><p className="mt-3 text-sm leading-6 text-muted-foreground">Your information helps the model identify patterns that may be associated with sleep disorders.</p><ul className="mt-5 space-y-3 text-xs text-muted-foreground">{['Personal health factors', 'Sleep quality and duration', 'Lifestyle and activity patterns'].map(text => <li key={text} className="flex items-center gap-2"><Check className="size-4 text-primary" />{text}</li>)}</ul></div><div className="border-t border-border pt-6"><h3 className="flex items-center gap-2 text-sm font-semibold"><Info className="size-4 text-primary" />A quick reminder</h3><p className="mt-3 text-xs leading-6 text-muted-foreground">Use your most recent measurements and typical daily averages. Results are educational insights, not a substitute for professional medical advice.</p></div></aside>
    </div>
  </div></div>;
}