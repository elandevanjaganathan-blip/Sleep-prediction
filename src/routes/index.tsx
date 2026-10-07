import { createFileRoute, Link } from '@tanstack/react-router';
import { ArrowRight, BrainCircuit, Check, ClipboardList, HeartPulse, Moon, ScanLine, ShieldCheck, Sparkles, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import sleepHero from '@/assets/sleep-hero.jpg';

export const Route = createFileRoute('/')({
  head: () => ({ meta: [
    { title: 'Sleep Disorder Classification — Sleep Health Prediction' },
    { name: 'description', content: 'Explore how personal health, lifestyle, and sleep patterns inform machine learning based sleep disorder predictions.' },
    { property: 'og:title', content: 'Sleep Disorder Classification — Sleep Health Prediction' },
    { property: 'og:description', content: 'A thoughtful, educational approach to understanding sleep health with machine learning.' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
  ] }),
  component: Home,
});

const features = [
  { icon: BrainCircuit, color: 'blue', title: 'ML-Based Prediction', description: 'Personal health and lifestyle data, analyzed by a machine learning model for meaningful insights.', note: 'Data-driven insights' },
  { icon: HeartPulse, color: 'violet', title: 'Sleep Health Analysis', description: 'Understand the connection between your sleep patterns, daily habits, and overall wellbeing.', note: 'A holistic perspective' },
  { icon: Zap, color: 'teal', title: 'Fast Results', description: 'A simple assessment. A clear prediction. Get your sleep health results without the wait.', note: 'Simple and efficient' },
];

function Home() {
  return <>
    <section className="sleep-hero relative isolate overflow-hidden">
      <img src={sleepHero} width={1536} height={1024} alt="A woman sleeping peacefully in a bright, comfortable bedroom" className="absolute inset-0 -z-20 size-full object-cover object-center" fetchPriority="high" />
      <div className="hero-wash absolute inset-0 -z-10" />
      <div className="mx-auto max-w-7xl px-6 pb-16 pt-16 lg:px-10 lg:pb-20 lg:pt-20">
        <div className="max-w-[570px]">
          <span className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/15 bg-background/70 px-3 py-1.5 text-xs font-medium text-primary"><Sparkles className="size-3.5" /> Machine Learning Based Sleep Health Prediction</span>
          <h1 className="text-[42px] font-semibold leading-[1.13] sm:text-[54px]">Sleep Disorder<br /><span className="text-primary">Classification</span></h1>
          <p className="mt-6 max-w-[440px] text-base leading-7 text-muted-foreground">Better understanding starts with better insights. Explore how your health, lifestyle, and sleep patterns can reveal possible sleep disorders.</p>
          <Button asChild size="lg" className="mt-8 h-12 gap-4 px-6"><Link to="/prediction">Start Prediction <ArrowRight /></Link></Button>
          <div className="mt-5 flex items-center gap-2 text-xs text-muted-foreground"><ShieldCheck className="size-4 text-primary" /> No sign-up needed <span className="mx-1">·</span> Educational use only</div>
        </div>
      </div>
      <div className="absolute bottom-7 right-10 hidden items-center gap-3 rounded-lg border border-background/70 bg-background/85 px-4 py-3 shadow-soft lg:flex"><span className="flex size-9 items-center justify-center rounded-full bg-accent text-primary"><Moon className="size-5" /></span><div><p className="text-xs font-semibold">A little insight. A healthier tomorrow.</p><p className="mt-1 text-[11px] text-muted-foreground">Your sleep health matters.</p></div></div>
    </section>
    <section className="border-b border-border bg-background">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-6 py-5 text-xs font-medium text-muted-foreground sm:grid-cols-3 lg:px-10">
        <span className="flex items-center gap-2 sm:justify-center"><Check className="size-4 text-primary" />Personalized sleep insights</span>
        <span className="flex items-center gap-2 sm:justify-center"><Check className="size-4 text-primary" />Health & lifestyle assessment</span>
        <span className="flex items-center gap-2 sm:justify-center"><Check className="size-4 text-primary" />Powered by machine learning</span>
      </div>
    </section>
    <section className="mx-auto max-w-7xl px-6 py-16 lg:px-10">
      <div className="mb-9 text-center"><p className="eyebrow">A SMARTER LOOK AT SLEEP</p><h2 className="mt-3 text-[30px] font-semibold">Small details. Meaningful insights.</h2><p className="mt-3 text-sm text-muted-foreground">Bringing health information and machine learning together.</p></div>
      <div className="grid gap-5 md:grid-cols-3">{features.map(({ icon: Icon, color, title, description, note }) => <article key={title} className="rounded-lg border border-border bg-card p-7 shadow-soft"><span className={`feature-icon feature-${color}`}><Icon className="size-6" /></span><h3 className="mt-5 text-lg font-semibold">{title}</h3><p className="mt-3 text-sm leading-6 text-muted-foreground">{description}</p><p className="mt-6 flex items-center gap-2 text-xs font-medium text-foreground"><span className={`feature-dot dot-${color}`} />{note}</p></article>)}</div>
    </section>
    <section className="border-t border-border bg-muted/40">
      <div className="mx-auto max-w-7xl px-6 py-14 lg:px-10"><div className="text-center"><p className="eyebrow">FROM DETAILS TO DISCOVERY</p><h2 className="mt-3 text-[30px] font-semibold">How it works</h2></div>
        <div className="mt-10 grid gap-8 md:grid-cols-3">{[
          { icon: ClipboardList, title: 'Enter Details', description: 'Share a few personal, sleep, and health details.' },
          { icon: BrainCircuit, title: 'Analyze with ML Model', description: 'The model looks for patterns in your information.' },
          { icon: ScanLine, title: 'View Prediction', description: 'See your predicted result and confidence score.' },
        ].map(({ icon: Icon, title, description }, index) => <div key={title} className="relative text-center"><span className="mb-4 inline-flex size-12 items-center justify-center rounded-lg border border-border bg-background text-primary"><Icon className="size-5" /></span><p className="text-sm font-semibold"><span className="mr-2 text-primary">0{index + 1}</span>{title}</p><p className="mx-auto mt-2 max-w-[260px] text-xs leading-5 text-muted-foreground">{description}</p>{index < 2 && <ArrowRight className="absolute right-0 top-4 hidden size-4 text-muted-foreground/50 md:block" />}</div>)}</div>
      </div>
    </section>
  </>;
}
