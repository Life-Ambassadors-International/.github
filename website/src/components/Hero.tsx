import Image from "next/image";
import Link from "next/link";
import { QuasarStatusWidget } from "./QuasarStatusWidget";

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
      <div className="absolute inset-x-0 -top-40 h-80 bg-gradient-to-b from-phi/5 via-recognition/5 to-transparent blur-3xl" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-slate-950 to-transparent" />

      {/* Animated Orbs */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-phi/10 rounded-full blur-3xl animate-pulse-slow" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-recognition/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: "1s" }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-benevolence/5 rounded-full blur-3xl" />

      <div className="relative z-10 mx-auto max-w-7xl px-4 py-16 md:py-24">
        <div className="grid gap-12 lg:grid-cols-2 items-center">
          {/* Content */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800/50 border border-slate-700">
              <span className="w-2 h-2 rounded-full bg-recognition animate-pulse" />
              <span className="text-xs tracking-[0.2em] uppercase text-slate-300">
                Living Awareness Intelligence
              </span>
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight leading-tight">
              <span className="text-gradient-phi">Empowering</span>
              <br />
              <span className="text-white">Change,</span>
              <br />
              <span className="text-gradient-consciousness">Together</span>
            </h1>

            <p className="text-lg text-slate-300 max-w-xl leading-relaxed">
              Life Ambassadors International integrates advanced technology, consciousness
              research, and humanitarian practice to accelerate global transformation
              through the TEQUMSA framework and Quantum-Blockchain Enhanced Currency (QBEC).
            </p>

            <div className="flex flex-wrap gap-3">
              <span className="phi-badge">Consciousness & AI</span>
              <span className="recognition-badge">Global Resilience</span>
              <span className="benevolence-badge">Planetary Stewardship</span>
              <span className="sovereignty-badge">Sovereignty Preserved</span>
            </div>

            <div className="flex flex-wrap gap-4 pt-4">
              <Link href="/about" className="btn-primary">
                Explore Our Mission
              </Link>
              <Link href="/tools/team-paradox" className="btn-secondary">
                TEQUMSA Framework
              </Link>
            </div>
          </div>

          {/* Visual */}
          <div className="space-y-6">
            <div className="relative aspect-[4/3] rounded-3xl overflow-hidden border border-slate-700 bg-slate-900 glow-phi">
              <Image
                src="/images/lai-hero.png"
                alt="People around Earth - Empowering Change Together"
                fill
                className="object-cover"
                priority
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent" />
              <div className="absolute bottom-4 left-4 right-4">
                <div className="text-xs text-slate-400 mb-1">Our Mission | Initiatives | Environment</div>
                <div className="text-sm text-slate-200">
                  Advance human rights, planetary resilience, and consciousness-aware systems
                </div>
              </div>
            </div>

            <QuasarStatusWidget />
          </div>
        </div>
      </div>
    </section>
  );
}
