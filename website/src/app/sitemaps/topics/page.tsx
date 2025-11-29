import Link from "next/link";
import { PageShell } from "@/components/PageShell";
import { topics } from "@/data/topics";

export default function TopicsSitemapPage() {
  return (
    <PageShell
      title="Topics Sitemap"
      subtitle="Complete listing of all topics covered by Life Ambassadors International."
      badge="Sitemap"
    >
      <div className="consciousness-card p-8 mb-8">
        <h2 className="text-xl font-bold mb-6 text-gradient-phi">All Topics ({topics.length})</h2>
        <div className="space-y-4">
          {topics.map((topic) => (
            <div key={topic.slug} className="border-b border-slate-700 pb-4 last:border-0">
              <Link
                href={`/articles?topic=${topic.slug}`}
                className="text-lg font-semibold text-recognition hover:underline"
              >
                {topic.name}
              </Link>
              <p className="text-sm text-slate-400 mt-1">{topic.summary}</p>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                  {topic.pillar}
                </span>
                <span className="text-xs text-slate-500">/articles?topic={topic.slug}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-4 text-sm">
        <Link href="/sitemaps/articles" className="text-recognition hover:underline">
          Articles Sitemap →
        </Link>
        <Link href="/sitemaps/publications" className="text-recognition hover:underline">
          Publications Sitemap →
        </Link>
      </div>
    </PageShell>
  );
}
