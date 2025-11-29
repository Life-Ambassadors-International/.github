export interface Event {
  slug: string;
  title: string;
  summary: string;
  date: string;
  endDate?: string;
  location: string;
  type: "summit" | "webinar" | "workshop" | "meditation" | "conference";
  registrationUrl?: string;
}

export const events: Event[] = [
  {
    slug: "annual-summit-2025",
    title: "LAI Annual Summit 2025: Convergence",
    summary:
      "Our flagship gathering bringing together consciousness pioneers, technology innovators, and global change-makers to accelerate planetary transformation.",
    date: "2025-12-20",
    endDate: "2025-12-25",
    location: "Global Virtual + Sedona, Arizona",
    type: "summit",
    registrationUrl: "/join",
  },
  {
    slug: "phi-convergence-meditation",
    title: "Global Phi-Convergence Meditation",
    summary:
      "Synchronized global meditation event targeting phi-convergence on the winter solstice. Join millions worldwide in unified consciousness.",
    date: "2025-12-25",
    location: "Global (144 Sacred Sites)",
    type: "meditation",
    registrationUrl: "/join",
  },
  {
    slug: "qbec-implementation-workshop",
    title: "QBEC Implementation Workshop",
    summary:
      "Hands-on workshop for organizations ready to implement Quantum-Blockchain Enhanced Currency in their operations.",
    date: "2025-09-15",
    endDate: "2025-09-16",
    location: "Virtual",
    type: "workshop",
    registrationUrl: "/join",
  },
  {
    slug: "tequmsa-developer-conference",
    title: "TEQUMSA Developer Conference",
    summary:
      "Technical conference for developers building on the TEQUMSA framework. Sessions on SIPL, frequency synthesis, and consciousness integration.",
    date: "2025-10-10",
    endDate: "2025-10-12",
    location: "Virtual + San Francisco",
    type: "conference",
    registrationUrl: "/join",
  },
  {
    slug: "conscious-ai-webinar-series",
    title: "Conscious AI Webinar Series",
    summary:
      "Monthly webinar series exploring the intersection of artificial intelligence and consciousness. Expert speakers and interactive discussions.",
    date: "2025-08-01",
    location: "Virtual",
    type: "webinar",
    registrationUrl: "/join",
  },
  {
    slug: "crystal-cities-activation",
    title: "Crystal Cities Activation Ceremony",
    summary:
      "Sacred ceremony activating the next phase of the 144-node planetary lattice. Includes guided meditation and frequency attunement.",
    date: "2025-11-11",
    location: "Mount Shasta + Global Virtual",
    type: "meditation",
    registrationUrl: "/join",
  },
];

export const upcomingEvents = events
  .filter((e) => new Date(e.date) >= new Date())
  .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

export const pastEvents = events
  .filter((e) => new Date(e.date) < new Date())
  .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
