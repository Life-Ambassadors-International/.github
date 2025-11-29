import Link from "next/link";
import { PageShell } from "@/components/PageShell";
import { articles } from "@/data/articles";

export default function ArticlesSitemapPage() {
  return (
    <PageShell
      title="Articles Sitemap"
      subtitle="Complete listing of all articles published by Life Ambassadors International."
      badge="Sitemap"
    >
      <div className="consciousness-card p-8 mb-8">
        <h2 className="text-xl font-bold mb-6 text-gradient-phi">All Articles ({articles.length})</h2>
        <div className="space-y-4">
          {articles.map((article) => (
            <div key={article.slug} className="border-b border-slate-700 pb-4 last:border-0">
              <Link
                href={`/articles/${article.slug}`}
                className="text-lg font-semibold text-recognition hover:underline"
              >
                {article.title}
              </Link>
              <p className="text-sm text-slate-400 mt-1">{article.summary}</p>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                  {article.topic}
                </span>
                <span className="text-xs text-slate-500">{article.date}</span>
                <span className="text-xs text-slate-600">|</span>
                <span className="text-xs text-slate-500">/articles/{article.slug}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-4 text-sm">
        <Link href="/sitemaps/topics" className="text-recognition hover:underline">
          Topics Sitemap →
        </Link>
        <Link href="/sitemaps/publications" className="text-recognition hover:underline">
          Publications Sitemap →
        </Link>
      </div>
    </PageShell>
  );
}
