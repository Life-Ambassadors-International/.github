import { notFound } from "next/navigation";
import Link from "next/link";
import { publications } from "@/data/publications";

interface PublicationPageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return publications.map((pub) => ({
    slug: pub.slug,
  }));
}

const typeColors: Record<string, string> = {
  whitepaper: "phi",
  report: "recognition",
  brief: "benevolence",
  research: "sovereignty",
};

export default function PublicationPage({ params }: PublicationPageProps) {
  const publication = publications.find((p) => p.slug === params.slug);

  if (!publication) {
    return notFound();
  }

  const relatedPublications = publications
    .filter((p) => p.type === publication.type && p.slug !== publication.slug)
    .slice(0, 2);

  // Simple markdown-like rendering
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
      } else if (line.trim() === "") {
        elements.push(<div key={index} className="h-4" />);
      } else {
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
            <Link href="/publications" className="hover:text-slate-300">
              Publications
            </Link>
          </li>
        </ol>
      </nav>

      {/* Publication Header */}
      <header className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <span className={`${typeColors[publication.type]}-badge text-xs uppercase`}>
            {publication.type}
          </span>
          <span className="text-xs text-slate-500">{publication.date}</span>
        </div>

        <h1 className="text-3xl md:text-4xl font-bold text-gradient-phi mb-4">
          {publication.title}
        </h1>

        <p className="text-lg text-slate-300 leading-relaxed mb-6">
          {publication.summary}
        </p>

        {publication.authors && (
          <div className="text-sm text-slate-500">
            By: {publication.authors.join(", ")}
          </div>
        )}
      </header>

      {/* Publication Body */}
      <article className="prose-consciousness mb-16">
        {renderBody(publication.body)}
      </article>

      {/* Download CTA */}
      <div className="consciousness-card p-6 mb-12">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-slate-100 mb-1">
              Access Full Publication
            </h3>
            <p className="text-sm text-slate-400">
              Download the complete PDF version with appendices and references.
            </p>
          </div>
          <Link
            href="/join"
            className="btn-primary whitespace-nowrap"
          >
            Request Access
          </Link>
        </div>
      </div>

      {/* Related Publications */}
      {relatedPublications.length > 0 && (
        <section>
          <h2 className="text-xl font-semibold mb-6">Related Publications</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {relatedPublications.map((related) => (
              <Link
                key={related.slug}
                href={`/publications/${related.slug}`}
                className="group consciousness-card p-4"
              >
                <span className={`${typeColors[related.type]}-badge text-[10px] uppercase mb-2 inline-block`}>
                  {related.type}
                </span>
                <h3 className="font-semibold text-slate-100 text-sm group-hover:text-recognition transition-colors">
                  {related.title}
                </h3>
                <p className="text-xs text-slate-500 mt-1">{related.date}</p>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
