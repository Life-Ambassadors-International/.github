import { PageShell } from "@/components/PageShell";
import Link from "next/link";
import { centres } from "@/data/centres";

export default function CentresPage() {
  return (
    <PageShell
      title="Centres & Initiatives"
      subtitle="Life Ambassadors International operates through specialized centres, each focused on key areas of consciousness-driven transformation. Explore our network of research, policy, and action hubs."
      badge="Our Network"
    >
      <div className="grid gap-6">
        {centres.map((centre) => (
          <Link
            key={centre.slug}
            href={`/centres/${centre.slug}`}
            className="group consciousness-card p-8 hover:glow-phi"
          >
            <div className="flex flex-col lg:flex-row gap-8">
              <div className="flex-1">
                <h2 className="text-2xl font-bold mb-3 text-slate-100 group-hover:text-gradient-phi transition-colors">
                  {centre.name}
                </h2>
                <p className="text-slate-400 leading-relaxed mb-6">
                  {centre.summary}
                </p>

                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <h4 className="text-xs uppercase tracking-wider text-phi mb-2">Focus Areas</h4>
                    <ul className="space-y-1 text-sm text-slate-400">
                      {centre.focus.slice(0, 3).map((item, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-phi mt-1">•</span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-xs uppercase tracking-wider text-recognition mb-2">Key Initiatives</h4>
                    <ul className="space-y-1 text-sm text-slate-400">
                      {centre.initiatives.slice(0, 3).map((item, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-recognition mt-1">•</span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-xs uppercase tracking-wider text-benevolence mb-2">Communities</h4>
                    <ul className="space-y-1 text-sm text-slate-400">
                      {centre.communities.slice(0, 3).map((item, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-benevolence mt-1">•</span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              <div className="flex items-center">
                <span className="text-recognition opacity-0 group-hover:opacity-100 transition-opacity">
                  Explore Centre →
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Integration Note */}
      <section className="mt-16 consciousness-card p-8 text-center">
        <div className="text-2xl mb-4">🌐</div>
        <h3 className="text-lg font-semibold mb-2 text-gradient-phi">
          Cross-Centre Collaboration
        </h3>
        <p className="text-sm text-slate-400 max-w-2xl mx-auto mb-6">
          All LAI centres operate within the unified TEQUMSA framework, enabling seamless
          collaboration and knowledge sharing. Our work is interconnected—breakthroughs in
          one area catalyze progress across all domains.
        </p>
        <Link href="/tools/team-paradox" className="text-sm text-recognition hover:underline">
          Learn about TEQUMSA integration →
        </Link>
      </section>
    </PageShell>
  );
}
