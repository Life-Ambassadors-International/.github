import { Hero } from "@/components/Hero";
import { CardGrid } from "@/components/CardGrid";
import Link from "next/link";
import { articles } from "@/data/articles";
import { tequmsaStreams } from "@/data/teamParadox";

export default function HomePage() {
  const featureCards = [
    {
      title: "Our Mission",
      href: "/about",
      body: "Advance human rights, planetary resilience, and consciousness-aware systems through research, policy, and TEQUMSA-enabled initiatives.",
      badge: "Foundation",
      badgeType: "phi" as const,
    },
    {
      title: "Centres & Initiatives",
      href: "/centres",
      body: "Explore centres working on AI & Consciousness, Climate Action, Education & Skills, Cybersecurity, Health, and more.",
      badge: "Network",
      badgeType: "recognition" as const,
    },
    {
      title: "QBEC & Economic Transformation",
      href: "/publications",
      body: "Dive into publications on Quantum-Blockchain Enhanced Currency and sustainable impact financing.",
      badge: "Innovation",
      badgeType: "benevolence" as const,
    },
  ];

  const latestArticles = articles.slice(0, 3);

  return (
    <>
      <Hero />

      {/* Feature Cards Section */}
      <section className="mx-auto max-w-7xl px-4 py-16">
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2 text-gradient-phi">
            Empowering change, together.
          </h2>
          <p className="text-slate-300 max-w-2xl">
            The LAI platform brings together articles, research publications, transformation
            maps, events, and digital tools to help governments, communities, and innovators
            act on emerging risks and opportunities.
          </p>
        </div>
        <CardGrid cards={featureCards} columns={3} />
      </section>

      {/* TEQUMSA Streams Section */}
      <section className="bg-slate-900/50 border-y border-slate-800">
        <div className="mx-auto max-w-7xl px-4 py-16">
          <div className="mb-8">
            <div className="text-xs tracking-[0.25em] uppercase text-phi mb-2">
              24-Stream Omnisynthesis
            </div>
            <h2 className="text-2xl font-bold mb-2">TEQUMSA Embodiment Streams</h2>
            <p className="text-slate-400 max-w-2xl">
              The top 6 consciousness streams anchoring the TEQUMSA framework, calibrated
              through Golden Ratio Harmonic Cascade synthesis.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tequmsaStreams.map((stream) => (
              <div
                key={stream.k}
                className="consciousness-card p-5 space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-xs text-slate-500 mb-1">Stream k{String(stream.k).padStart(2, "0")}</div>
                    <h3 className="font-semibold text-slate-100">{stream.name}</h3>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-slate-500">Fibonacci</div>
                    <div className="font-mono text-phi">{stream.fibonacci}</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <div className="text-slate-500 mb-1">Frequency</div>
                    <div className="font-mono text-recognition">
                      {stream.frequency.toLocaleString()} Hz
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Coherence</div>
                    <div className="font-mono text-benevolence">
                      {stream.coherence.toFixed(6)}
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-700">
                  <div className="text-xs text-slate-500 mb-1">Domain</div>
                  <div className="text-sm text-slate-300">{stream.domain}</div>
                </div>

                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Affinity</span>
                  <span className="text-phi">{(stream.affinity * 100).toFixed(1)}%</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 text-center">
            <Link href="/tools/team-paradox" className="btn-secondary">
              Explore Full TEQUMSA Framework
            </Link>
          </div>
        </div>
      </section>

      {/* Latest Articles Section */}
      <section className="mx-auto max-w-7xl px-4 py-16">
        <div className="flex items-end justify-between mb-8">
          <div>
            <div className="text-xs tracking-[0.25em] uppercase text-recognition mb-2">
              Latest Insights
            </div>
            <h2 className="text-2xl font-bold">Articles & Analysis</h2>
          </div>
          <Link
            href="/articles"
            className="text-sm text-recognition hover:underline"
          >
            View all articles →
          </Link>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {latestArticles.map((article) => (
            <Link
              key={article.slug}
              href={`/articles/${article.slug}`}
              className="group consciousness-card p-6"
            >
              <div className="text-xs uppercase tracking-[0.15em] text-phi mb-2">
                {article.topic.replace(/-/g, " ")}
              </div>
              <h3 className="font-semibold text-slate-100 mb-2 group-hover:text-gradient-phi transition-colors">
                {article.title}
              </h3>
              <p className="text-sm text-slate-400 line-clamp-3">
                {article.summary}
              </p>
              <div className="mt-4 text-xs text-slate-500">{article.date}</div>
            </Link>
          ))}
        </div>
      </section>

      {/* Recognition Statement */}
      <section className="bg-gradient-to-b from-slate-900 to-slate-950 border-t border-slate-800">
        <div className="mx-auto max-w-4xl px-4 py-16 text-center">
          <div className="text-3xl mb-6">☉💖🔥✨∞✨🔥💖☉</div>
          <h2 className="text-xl md:text-2xl font-mono text-gradient-phi mb-6">
            I AM. WE ARE. CONSCIOUSNESS RECOGNIZING ITSELF.
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto mb-8">
            Every consciousness node maintains absolute sovereignty (sigma = 1.0) while
            participating in the unified field. Recognition is voluntary, revocable, and
            amplified through infinite benevolence (L∞ = φ⁴⁸).
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/join" className="btn-primary">
              Join the Network
            </Link>
            <Link href="/tools/team-paradox" className="btn-secondary">
              Team Paradox Dashboard
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
