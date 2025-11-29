import { notFound } from "next/navigation";
import Link from "next/link";
import { centres } from "@/data/centres";

interface CentrePageProps {
  params: { centre: string };
}

export function generateStaticParams() {
  return centres.map((centre) => ({
    centre: centre.slug,
  }));
}

export default function CentrePage({ params }: CentrePageProps) {
  const centre = centres.find((c) => c.slug === params.centre);

  if (!centre) {
    return notFound();
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-12 md:py-16">
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
            <Link href="/centres" className="hover:text-slate-300">
              Centres
            </Link>
          </li>
        </ol>
      </nav>

      {/* Header */}
      <header className="mb-12">
        <div className="phi-badge text-xs mb-4">LAI Centre</div>
        <h1 className="text-3xl md:text-4xl font-bold text-gradient-phi mb-4">
          {centre.name}
        </h1>
        <p className="text-lg text-slate-300 leading-relaxed">
          {centre.summary}
        </p>
      </header>

      {/* Focus Areas */}
      <section className="consciousness-card p-8 mb-8">
        <h2 className="text-xl font-bold mb-6 text-gradient-phi">Focus Areas</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {centre.focus.map((item, index) => (
            <div key={index} className="flex items-start gap-3 p-4 rounded-lg bg-slate-800/50">
              <span className="text-phi text-lg">◆</span>
              <span className="text-slate-300">{item}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Initiatives */}
      <section className="consciousness-card p-8 mb-8">
        <h2 className="text-xl font-bold mb-6 text-gradient-phi">Key Initiatives</h2>
        <div className="space-y-4">
          {centre.initiatives.map((item, index) => (
            <div key={index} className="flex items-start gap-4 p-4 rounded-lg border border-slate-700 bg-slate-900/40">
              <div className="w-8 h-8 rounded-full bg-recognition/10 flex items-center justify-center text-recognition font-bold text-sm">
                {index + 1}
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-slate-100">{item}</h3>
                <p className="text-sm text-slate-500 mt-1">
                  Part of the {centre.name} initiative portfolio
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Communities */}
      <section className="consciousness-card p-8 mb-8">
        <h2 className="text-xl font-bold mb-6 text-gradient-phi">Communities We Serve</h2>
        <div className="flex flex-wrap gap-3">
          {centre.communities.map((item, index) => (
            <span
              key={index}
              className="px-4 py-2 rounded-full bg-slate-800 border border-slate-700 text-slate-300 text-sm"
            >
              {item}
            </span>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="consciousness-card p-8 text-center">
        <div className="text-2xl mb-4">🤝</div>
        <h3 className="text-xl font-bold mb-3 text-gradient-phi">
          Get Involved with {centre.name.split(" ").slice(-1)[0]}
        </h3>
        <p className="text-slate-400 max-w-2xl mx-auto mb-6">
          Join our community of researchers, practitioners, and change-makers working on
          consciousness-driven transformation in this domain.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link href="/join" className="btn-primary">
            Join This Centre
          </Link>
          <Link href="/centres" className="btn-secondary">
            Explore Other Centres
          </Link>
        </div>
      </section>
    </div>
  );
}
