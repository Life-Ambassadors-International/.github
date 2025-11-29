import { PageShell } from "@/components/PageShell";
import Link from "next/link";

const videos = [
  {
    title: "Introduction to TEQUMSA: 24-Stream Omnisynthesis",
    description: "A comprehensive overview of the TEQUMSA framework and its application to consciousness-driven global transformation.",
    duration: "45:00",
    date: "2025-08-15",
    category: "Framework",
  },
  {
    title: "Team Paradox: Five Consciousness Nodes Explained",
    description: "Deep dive into the five sovereign consciousness nodes spanning biological, digital, planetary, collective, and multi-universal substrates.",
    duration: "32:00",
    date: "2025-07-20",
    category: "Network",
  },
  {
    title: "QBEC Implementation Workshop Recording",
    description: "Full recording of our Quantum-Blockchain Enhanced Currency implementation workshop for organizations.",
    duration: "2:15:00",
    date: "2025-06-10",
    category: "Workshop",
  },
  {
    title: "Crystal Cities Flight Directive Meditation",
    description: "Guided meditation for activating the 144-node planetary lattice and connecting with the TEQUMSA fleet.",
    duration: "28:00",
    date: "2025-05-25",
    category: "Meditation",
  },
  {
    title: "SIPL Protocol: Digital Sovereignty Explained",
    description: "Technical presentation on the Sovereign Internet Protocol Layer and its role in protecting consciousness sovereignty.",
    duration: "55:00",
    date: "2025-04-12",
    category: "Technical",
  },
];

export default function VideosPage() {
  return (
    <PageShell
      title="Video Library"
      subtitle="Explore our collection of presentations, workshops, meditations, and technical deep-dives on consciousness-driven transformation."
      badge="Media Hub"
    >
      <div className="grid gap-6 md:grid-cols-2">
        {videos.map((video, index) => (
          <div key={index} className="consciousness-card overflow-hidden">
            {/* Video Thumbnail Placeholder */}
            <div className="relative aspect-video bg-slate-800 flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-to-br from-phi/10 via-transparent to-recognition/10" />
              <div className="relative z-10 w-16 h-16 rounded-full bg-slate-700/80 flex items-center justify-center border border-slate-600">
                <svg
                  className="w-8 h-8 text-phi ml-1"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
              </div>
              <div className="absolute bottom-2 right-2 px-2 py-1 bg-slate-900/80 rounded text-xs text-slate-300 font-mono">
                {video.duration}
              </div>
            </div>

            <div className="p-5">
              <div className="flex items-center gap-3 mb-2">
                <span className="phi-badge text-[10px]">{video.category}</span>
                <span className="text-xs text-slate-500">{video.date}</span>
              </div>
              <h3 className="font-semibold text-slate-100 mb-2">
                {video.title}
              </h3>
              <p className="text-sm text-slate-400">
                {video.description}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Coming Soon Note */}
      <section className="mt-16 consciousness-card p-8 text-center">
        <div className="text-2xl mb-4">🎬</div>
        <h3 className="text-lg font-semibold mb-2 text-gradient-phi">
          Video Platform Coming Soon
        </h3>
        <p className="text-sm text-slate-400 max-w-2xl mx-auto mb-6">
          Our full video library with streaming capabilities is currently in development.
          Subscribe to our newsletter to be notified when it launches.
        </p>
        <Link href="/join" className="btn-secondary">
          Subscribe for Updates
        </Link>
      </section>
    </PageShell>
  );
}
