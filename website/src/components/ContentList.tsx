import Link from "next/link";

interface Item {
  slug: string;
  title: string;
  summary: string;
  topic?: string;
  typeLabel?: string;
  date?: string;
}

interface ContentListProps {
  items: Item[];
  basePath: string;
}

export function ContentList({ items, basePath }: ContentListProps) {
  if (items.length === 0) {
    return (
      <div className="consciousness-card p-8 text-center">
        <p className="text-slate-400">No content available yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <Link
          key={item.slug}
          href={`${basePath}/${item.slug}`}
          className="group block consciousness-card p-6 hover:glow-recognition"
        >
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-xs uppercase tracking-[0.15em] text-recognition">
                  {item.typeLabel || "Article"}
                </span>
                {item.topic && (
                  <>
                    <span className="text-slate-600">|</span>
                    <span className="text-xs text-slate-500">{item.topic}</span>
                  </>
                )}
              </div>
              <h2 className="text-lg font-semibold text-slate-100 group-hover:text-gradient-phi transition-colors mb-2">
                {item.title}
              </h2>
              <p className="text-sm text-slate-400 leading-relaxed">
                {item.summary}
              </p>
            </div>
            {item.date && (
              <div className="text-xs text-slate-500 whitespace-nowrap md:text-right">
                {item.date}
              </div>
            )}
          </div>
        </Link>
      ))}
    </div>
  );
}
