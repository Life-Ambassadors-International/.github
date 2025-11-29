import { PageShell } from "@/components/PageShell";
import { ContentList } from "@/components/ContentList";
import { TopicBadges } from "@/components/TopicBadges";
import { articles } from "@/data/articles";
import { topics } from "@/data/topics";

interface ArticlesPageProps {
  searchParams: { topic?: string };
}

export default function ArticlesPage({ searchParams }: ArticlesPageProps) {
  const selectedTopic = searchParams.topic;
  const topicSlugs = topics.map((t) => t.slug);

  const filteredArticles = selectedTopic
    ? articles.filter((a) => a.topic === selectedTopic)
    : articles;

  const selectedTopicData = selectedTopic
    ? topics.find((t) => t.slug === selectedTopic)
    : null;

  return (
    <PageShell
      title={selectedTopicData ? selectedTopicData.name : "Articles & Analysis"}
      subtitle={
        selectedTopicData
          ? selectedTopicData.summary
          : "News, explainers, opinion, and analysis across LAI focus areas. Discover insights on consciousness-driven transformation, TEQUMSA implementation, and global change."
      }
      badge="Knowledge Hub"
    >
      {/* Topic Filters */}
      <div className="mb-8">
        <div className="text-sm text-slate-400 mb-3">Filter by topic:</div>
        <TopicBadges topics={topicSlugs} selectedTopic={selectedTopic} />
      </div>

      {/* Results Count */}
      <div className="mb-6 text-sm text-slate-500">
        Showing {filteredArticles.length} article{filteredArticles.length !== 1 ? "s" : ""}
        {selectedTopic && (
          <span>
            {" "}in <span className="text-phi">{selectedTopic.replace(/-/g, " ")}</span>
          </span>
        )}
      </div>

      {/* Articles List */}
      <ContentList
        items={filteredArticles.map((a) => ({
          slug: a.slug,
          title: a.title,
          summary: a.summary,
          topic: a.topic.replace(/-/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
          typeLabel: "Article",
          date: a.date,
        }))}
        basePath="/articles"
      />

      {/* Empty State */}
      {filteredArticles.length === 0 && (
        <div className="consciousness-card p-8 text-center">
          <div className="text-2xl mb-4">📚</div>
          <h3 className="text-lg font-semibold mb-2">No articles found</h3>
          <p className="text-sm text-slate-400">
            No articles match the selected topic. Try selecting a different topic or view all articles.
          </p>
        </div>
      )}
    </PageShell>
  );
}
