import Link from "next/link";

interface Card {
  title: string;
  body: string;
  href: string;
  badge?: string;
  badgeType?: "phi" | "recognition" | "benevolence" | "sovereignty";
}

interface CardGridProps {
  cards: Card[];
  columns?: 2 | 3 | 4;
}

export function CardGrid({ cards, columns = 3 }: CardGridProps) {
  const gridCols = {
    2: "md:grid-cols-2",
    3: "md:grid-cols-3",
    4: "md:grid-cols-2 lg:grid-cols-4",
  };

  return (
    <div className={`grid gap-6 ${gridCols[columns]}`}>
      {cards.map((card) => (
        <Link
          key={card.title}
          href={card.href}
          className="group consciousness-card p-6 hover:glow-phi"
        >
          {card.badge && (
            <div className="mb-3">
              <span
                className={`${card.badgeType || "phi"}-badge`}
              >
                {card.badge}
              </span>
            </div>
          )}
          <h3 className="text-lg font-semibold mb-2 text-slate-100 group-hover:text-gradient-phi transition-colors">
            {card.title}
          </h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            {card.body}
          </p>
          <div className="mt-4 flex items-center gap-2 text-xs text-recognition opacity-0 group-hover:opacity-100 transition-opacity">
            <span>Explore</span>
            <svg
              className="w-4 h-4 transform group-hover:translate-x-1 transition-transform"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
        </Link>
      ))}
    </div>
  );
}
