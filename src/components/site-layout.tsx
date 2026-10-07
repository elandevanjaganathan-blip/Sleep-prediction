import { Link } from '@tanstack/react-router';
import { Activity, ArrowUpRight, Moon, ShieldCheck } from 'lucide-react';
import type { ReactNode } from 'react';
import { Button } from '@/components/ui/button';

export function SiteLayout({ children }: { children: ReactNode }) {
  return <div className="flex min-h-screen flex-col">
    <header className="border-b border-border bg-background">
      <div className="mx-auto flex min-h-24 max-w-7xl items-center justify-between gap-4 px-6 lg:px-10">
        <Link to="/" className="flex items-center gap-3" aria-label="Sleep Disorder Classification home">
          <span className="flex size-11 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground"><Moon className="size-6" /></span>
          <span><span className="block text-[15px] font-bold sm:text-lg">Sleep Disorder Classification</span><span className="mt-0.5 block text-[10px] font-medium uppercase tracking-[0.12em] text-muted-foreground sm:text-xs">Sleep health, understood.</span></span>
        </Link>
        <nav aria-label="Main navigation" className="flex items-center gap-2 sm:gap-6">
          <Link to="/" activeOptions={{ exact: true }} activeProps={{ className: 'text-primary' }} inactiveProps={{ className: 'text-muted-foreground' }} className="nav-link text-sm font-medium">Home</Link>
          <Link to="/prediction" activeProps={{ className: 'text-primary' }} inactiveProps={{ className: 'text-muted-foreground' }} className="nav-link text-sm font-medium">Prediction</Link>
          <Button asChild className="ml-3 hidden h-10 gap-2 px-4 lg:inline-flex"><Link to="/prediction">Start Prediction <ArrowUpRight /></Link></Button>
        </nav>
      </div>
    </header>
    <main className="flex-1">{children}</main>
    <footer className="border-t border-border bg-background">
      <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-5 px-6 py-7 text-xs text-muted-foreground sm:flex-row sm:items-center lg:px-10">
        <div className="flex items-center gap-2"><Activity className="size-4 text-primary" /><span>Sleep Disorder Classification <span className="mx-2 text-border">|</span> An educational ML project</span></div>
        <span className="flex items-center gap-2"><ShieldCheck className="size-4" />For educational purposes. Not a medical diagnosis.</span>
      </div>
    </footer>
  </div>;
}