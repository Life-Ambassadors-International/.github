import { PageShell } from "@/components/PageShell";
import Link from "next/link";
import { publications } from "@/data/publications";

const typeColors: Record<string, string> = {
  whitepaper: "phi",
  report: "recognition",
  brief: "benevolence",
  research: "sovereignty",
};

export default function PublicationsPage() {
  return (
    <PageShell
      title="Publications & Research"
      subtitle="Explore our whitepapers, research reports, technical briefs, and analysis documents. Deep dives into TEQUMSA implementation, QBEC economics, and consciousness-driven transformation."
      badge="Research Library"
    >
      {/* Publication Type Filters */}
      <div className="mb-8">
        <div className="text-sm text-slate-400 mb-3">Publication types:</div>
        <div className="flex flex-wrap gap-2">
          <span className="phi-badge">Whitepapers</span>
          <span className="recognition-badge">Reports</span>
          <span className="benevolence-badge">Briefs</span>
          <span className="sovereignty-badge">Research</span>
        </div>
      </div>

      {/* Publications List */}
      <div className="space-y-6">
        {publications.map((pub) => (
          <Link
            key={pub.slug}
            href={`/publications/${pub.slug}`}
            className="group block consciousness-card p-6 hover:glow-recognition"
          >
            <div className="flex flex-col md:flex-row gap-6">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`${typeColors[pub.type]}-badge text-xs uppercase`}>
                    {pub.type}
                  </span>
                  <span className="text-xs text-slate-500">{pub.date}</span>
                </div>

                <h2 className="text-xl font-semibold text-slate-100 mb-2 group-hover:text-gradient-phi transition-colors">
                  {pub.title}
                </h2>

                <p className="text-sm text-slate-400 leading-relaxed mb-4">
                  {pub.summary}
                </p>

                {pub.authors && (
                  <div className="text-xs text-slate-500">
                    By: {pub.authors.join(", ")}
                  </div>
                )}
              </div>

              <div className="flex md:flex-col items-center gap-4 md:justify-center">
                <span className="text-sm text-recognition group-hover:underline">
                  Read publication →
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* CTA Section */}
      <section className="mt-16 consciousness-card p-8 text-center">
        <div className="text-2xl mb-4">📚</div>
        <h3 className="text-lg font-semibold mb-2 text-gradient-phi">
          Contribute to Our Research
        </h3>
        <p className="text-sm text-slate-400 max-w-2xl mx-auto mb-6">
          Life Ambassadors International welcomes research contributions from academics,
          practitioners, and consciousness explorers. Join our network of researchers
          advancing the TEQUMSA framework.
        </p>
        <Link href="/join" className="btn-secondary">
          Become a Contributor
        </Link>
      </section>
    </PageShell>
  );
}
