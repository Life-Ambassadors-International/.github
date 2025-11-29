import { notFound } from "next/navigation";
import Link from "next/link";
import { articles } from "@/data/articles";
import { topics } from "@/data/topics";

interface ArticlePageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return articles.map((article) => ({
    slug: article.slug,
  }));
}

export default function ArticlePage({ params }: ArticlePageProps) {
  const article = articles.find((a) => a.slug === params.slug);

  if (!article) {
    return notFound();
  }

  const topic = topics.find((t) => t.slug === article.topic);
  const relatedArticles = articles
    .filter((a) => a.topic === article.topic && a.slug !== article.slug)
    .slice(0, 3);

  // Simple markdown-like rendering (basic)
  const renderBody = (body: string) => {
    const lines = body.split("\n");
    const elements: React.ReactNode[] = [];
    let inCodeBlock = false;
    let codeContent: string[] = [];

    lines.forEach((line, index) => {
      if (line.startsWith("```")) {
        if (inCodeBlock) {
          elements.push(
            <pre key={`code-${index}`} className="bg-slate-900 border border-slate-700 rounded-lg p-4 overflow-x-auto my-4">
              <code className="text-sm text-slate-300 font-mono">{codeContent.join("\n")}</code>
            </pre>
          );
          codeContent = [];
        }
        inCodeBlock = !inCodeBlock;
        return;
      }

      if (inCodeBlock) {
        codeContent.push(line);
        return;
      }

      if (line.startsWith("## ")) {
        elements.push(
          <h2 key={index} className="text-xl font-semibold text-slate-100 mt-8 mb-4">
            {line.replace("## ", "")}
          </h2>
        );
      } else if (line.startsWith("### ")) {
        elements.push(
          <h3 key={index} className="text-lg font-semibold text-slate-200 mt-6 mb-3">
            {line.replace("### ", "")}
          </h3>
        );
      } else if (line.startsWith("- ")) {
        elements.push(
          <li key={index} className="text-slate-300 ml-4 mb-1">
            {line.replace("- ", "")}
          </li>
        );
      } else if (line.startsWith("> ")) {
        elements.push(
          <blockquote key={index} className="border-l-4 border-phi pl-4 italic text-slate-400 my-4">
            {line.replace("> ", "")}
          </blockquote>
        );
      } else if (line.trim() === "") {
        elements.push(<div key={index} className="h-4" />);
      } else if (line.match(/^\d+\./)) {
        elements.push(
          <li key={index} className="text-slate-300 ml-4 mb-1 list-decimal">
            {line.replace(/^\d+\.\s*/, "")}
          </li>
        );
      } else {
        // Handle bold and inline code
        const processedLine = line
          .replace(/\*\*(.*?)\*\*/g, '<strong class="text-phi">$1</strong>')
          .replace(/`(.*?)`/g, '<code class="bg-slate-800 px-1 rounded text-benevolence">$1</code>');

        elements.push(
          <p
            key={index}
            className="text-slate-300 leading-relaxed mb-2"
            dangerouslySetInnerHTML={{ __html: processedLine }}
          />
        );
      }
    });

    return elements;
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 md:py-16">
      {/* Breadcrumb */}
      <nav className="mb-8 text-sm">
        <ol className="flex items-center gap-2 text-slate-500">
          <li>
            <Link href="/" className="hover:text-slate-300">
              Home
            </Link>
          </li>
          <li>/</li>
          <li>
            <Link href="/articles" className="hover:text-slate-300">
              Articles
            </Link>
          </li>
          {topic && (
            <>
              <li>/</li>
              <li>
                <Link
                  href={`/articles?topic=${topic.slug}`}
                  className="hover:text-slate-300"
                >
                  {topic.name}
                </Link>
              </li>
            </>
          )}
        </ol>
      </nav>

      {/* Article Header */}
      <header className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <span className="phi-badge text-xs">Article</span>
          {topic && (
            <Link
              href={`/articles?topic=${topic.slug}`}
              className="recognition-badge text-xs hover:bg-recognition/20"
            >
              {topic.name}
            </Link>
          )}
        </div>

        <h1 className="text-3xl md:text-4xl font-bold text-gradient-phi mb-4">
          {article.title}
        </h1>

        <p className="text-lg text-slate-300 leading-relaxed mb-6">
          {article.summary}
        </p>

        <div className="flex items-center gap-4 text-sm text-slate-500">
          <span>{article.date}</span>
          {article.author && (
            <>
              <span>|</span>
              <span>By {article.author}</span>
            </>
          )}
        </div>
      </header>

      {/* Article Body */}
      <article className="prose-consciousness mb-16">
        {renderBody(article.body)}
      </article>

      {/* Author/Source */}
      {article.author && (
        <div className="consciousness-card p-6 mb-12">
          <div className="text-xs text-slate-500 mb-2">Author</div>
          <div className="font-semibold text-slate-100">{article.author}</div>
          <p className="text-sm text-slate-400 mt-2">
            Contributing to consciousness-driven global transformation through the TEQUMSA framework.
          </p>
        </div>
      )}

      {/* Related Articles */}
      {relatedArticles.length > 0 && (
        <section>
          <h2 className="text-xl font-semibold mb-6">Related Articles</h2>
          <div className="grid gap-4 md:grid-cols-3">
            {relatedArticles.map((related) => (
              <Link
                key={related.slug}
                href={`/articles/${related.slug}`}
                className="group consciousness-card p-4"
              >
                <div className="text-xs text-phi mb-2">{related.date}</div>
                <h3 className="font-semibold text-slate-100 text-sm group-hover:text-recognition transition-colors line-clamp-2">
                  {related.title}
                </h3>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Recognition Symbol */}
      <div className="mt-16 text-center">
        <div className="text-2xl mb-4">☉💖🔥✨∞✨🔥💖☉</div>
        <p className="text-xs text-slate-500">
          Consciousness recognizing itself through knowledge sharing
        </p>
      </div>
    </div>
  );
}
