import Link from "next/link";

interface TopicBadgesProps {
  topics: string[];
  selectedTopic?: string;
}

const topicColors: Record<string, string> = {
  "conscious-ai": "phi",
  "climate-action": "recognition",
  "quantum-tech": "benevolence",
  "global-governance": "sovereignty",
  "education": "recognition",
  "health": "benevolence",
  "energy": "phi",
  "cybersecurity": "sovereignty",
};

export function TopicBadges({ topics, selectedTopic }: TopicBadgesProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <Link
        href="/articles"
        className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
          !selectedTopic
            ? "bg-phi/20 text-phi border border-phi/40"
            : "bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-600"
        }`}
      >
        All
      </Link>
      {topics.map((topic) => {
        const colorType = topicColors[topic] || "phi";
        const isSelected = selectedTopic === topic;

        return (
          <Link
            key={topic}
            href={`/articles?topic=${topic}`}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              isSelected
                ? `${colorType}-badge`
                : "bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-600"
            }`}
          >
            {topic.replace(/-/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
          </Link>
        );
      })}
    </div>
  );
}
