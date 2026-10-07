import { createFileRoute, Link } from '@tanstack/react-router';
import { ArrowRight, Home, Moon, RotateCcw, ShieldCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { usePrediction } from '@/components/prediction-context';

export const Route = createFileRoute('/result')({
  head: () => ({ meta: [
    { title: 'Prediction Result — Sleep Disorder Classification' },
    { name: 'description', content: 'Review your sleep disorder prediction and the model’s confidence score.' },
    { property: 'og:title', content: 'Prediction Result — Sleep Disorder Classification' },
    { property: 'og:description', content: 'Your educational sleep health prediction and confidence score.' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
  ] }),
  component: ResultPage,
});

function ResultPage() {
  const { result, setResult } = usePrediction();
  return <section className="bg-muted/35 px-6 py-16 sm:py-20"><div className="mx-auto max-w-2xl text-center"><p className="eyebrow">YOUR SLEEP HEALTH INSIGHTS</p><h1 className="mt-3 text-3xl font-semibold sm:text-4xl">Prediction Result</h1><p className="mt-4 text-sm text-muted-foreground">{result ? 'A clearer view of your sleep health, informed by your details.' : 'Your result will appear here after completing an assessment.'}</p>
    <div className="mt-9 rounded-lg border border-border bg-card p-8 shadow-soft sm:p-12"><span className="mx-auto mb-6 flex size-16 items-center justify-center rounded-full bg-accent text-primary"><Moon className="size-8" /></span>{result ? <><p className="text-xs font-medium uppercase tracking-[0.12em] text-muted-foreground">PREDICTED SLEEP DISORDER</p><h2 className="mt-3 break-words text-3xl font-semibold text-primary sm:text-4xl">{result.prediction}</h2><div className="mx-auto mt-6 flex w-fit items-baseline gap-2 rounded-md bg-accent px-5 py-3"><span className="text-2xl font-semibold text-primary">{Math.round(result.confidence * 100)}%</span><span className="text-xs text-muted-foreground">model confidence</span></div><p className="mt-7 text-sm leading-7 text-muted-foreground">{['none', 'normal', 'no disorder', 'no sleep disorder'].includes(result.prediction.toLowerCase()) ? 'The ML model predicts that you may have no sleep disorder based on the information provided.' : `The ML model predicts that you may have ${result.prediction} based on the information provided.`}</p></> : <><h2 className="text-xl font-semibold">No prediction yet</h2><p className="mt-3 text-sm leading-6 text-muted-foreground">Complete your sleep health assessment to receive a prediction from the connected ML model.</p><Button asChild className="mt-6"><Link to="/prediction">Start Prediction <ArrowRight /></Link></Button></>}</div>
    <div className="mt-6 flex items-start gap-3 rounded-md border border-border bg-background p-5 text-left"><ShieldCheck className="mt-0.5 size-5 shrink-0 text-primary" /><div><p className="text-sm font-medium">An insight, not a diagnosis</p><p className="mt-1 text-xs leading-6 text-muted-foreground">This prediction is for educational purposes only and is not a medical diagnosis.</p></div></div>
    <div className="mt-8 flex flex-wrap justify-center gap-3">{result && <Button asChild className="h-11 px-5" onClick={() => setResult(null)}><Link to="/prediction"><RotateCcw />Predict Again</Link></Button>}<Button asChild variant="outline" className="h-11 px-5"><Link to="/"><Home />Back to Home</Link></Button></div>
  </div></section>;
}