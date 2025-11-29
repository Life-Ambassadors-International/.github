import Link from "next/link";
import { PageShell } from "@/components/PageShell";
import { publications } from "@/data/publications";

export default function PublicationsSitemapPage() {
  return (
    <PageShell
      title="Publications Sitemap"
      subtitle="Complete listing of all publications from Life Ambassadors International."
      badge="Sitemap"
    >
      <div className="consciousness-card p-8 mb-8">
        <h2 className="text-xl font-bold mb-6 text-gradient-phi">All Publications ({publications.length})</h2>
        <div className="space-y-4">
          {publications.map((pub) => (
            <div key={pub.slug} className="border-b border-slate-700 pb-4 last:border-0">
              <Link
                href={`/publications/${pub.slug}`}
                className="text-lg font-semibold text-recognition hover:underline"
              >
                {pub.title}
              </Link>
              <p className="text-sm text-slate-400 mt-1">{pub.summary}</p>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 uppercase">
                  {pub.type}
                </span>
                <span className="text-xs text-slate-500">{pub.date}</span>
                <span className="text-xs text-slate-600">|</span>
                <span className="text-xs text-slate-500">/publications/{pub.slug}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-4 text-sm">
        <Link href="/sitemaps/topics" className="text-recognition hover:underline">
          Topics Sitemap →
        </Link>
        <Link href="/sitemaps/articles" className="text-recognition hover:underline">
          Articles Sitemap →
        </Link>
      </div>
    </PageShell>
  );
}
