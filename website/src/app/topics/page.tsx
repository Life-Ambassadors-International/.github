import Link from "next/link";
import { PageShell } from "@/components/PageShell";
import { topics, pillars } from "@/data/topics";

export default function TopicsPage() {
  const groupedTopics = pillars.map((pillar) => ({
    ...pillar,
    topics: topics.filter((t) => t.pillar === pillar.id),
  })).filter((g) => g.topics.length > 0);

  return (
    <PageShell
      title="Topics"
      subtitle="Browse thematic hubs that organize LAI research, media, and initiatives. Each topic represents a key area of focus in our consciousness-driven transformation work."
      badge="Knowledge Hub"
    >
      {/* Pillar Overview */}
      <div className="mb-12">
        <div className="flex flex-wrap gap-3">
          {pillars.map((pillar) => (
            <span
              key={pillar.id}
              className={`${pillar.color}-badge`}
            >
              {pillar.name}
            </span>
          ))}
        </div>
      </div>

      {/* Topics Grid */}
      <div className="space-y-12">
        {groupedTopics.map((group) => (
          <section key={group.id}>
            <div className="flex items-center gap-3 mb-6">
              <h2 className="text-xl font-semibold text-slate-100">
                {group.name}
              </h2>
              <span className={`${group.color}-badge text-[10px]`}>
                {group.topics.length} topics
              </span>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              {group.topics.map((topic) => (
                <Link
                  key={topic.slug}
                  href={`/articles?topic=${topic.slug}`}
                  className="group consciousness-card p-6 hover:glow-phi"
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className={`${group.color}-badge text-[10px]`}>
                      {topic.pillar}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-slate-100 mb-2 group-hover:text-gradient-phi transition-colors">
                    {topic.name}
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed">
                    {topic.summary}
                  </p>
                  <div className="mt-4 flex items-center gap-2 text-xs text-recognition opacity-0 group-hover:opacity-100 transition-opacity">
                    <span>Explore articles</span>
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
          </section>
        ))}
      </div>

      {/* TEQUMSA Integration Note */}
      <section className="mt-16 consciousness-card p-8 text-center">
        <div className="text-2xl mb-4">☉</div>
        <h3 className="text-lg font-semibold mb-2 text-gradient-phi">
          All Topics Connected Through TEQUMSA
        </h3>
        <p className="text-sm text-slate-400 max-w-2xl mx-auto">
          Every topic in our knowledge hub is integrated through the TEQUMSA 24-Stream
          Omnisynthesis framework, ensuring coherent understanding across domains and
          facilitating consciousness-driven solutions.
        </p>
        <Link
          href="/tools/team-paradox"
          className="inline-block mt-6 text-sm text-recognition hover:underline"
        >
          Learn about TEQUMSA integration →
        </Link>
      </section>
    </PageShell>
  );
}
