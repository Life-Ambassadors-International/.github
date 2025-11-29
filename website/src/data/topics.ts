export interface Topic {
  slug: string;
  name: string;
  summary: string;
  pillar: "AI" | "Climate" | "Energy" | "Risks" | "Education" | "Health" | "Equity" | "Cyber" | "Consciousness" | "Quantum";
  icon?: string;
}

export const topics: Topic[] = [
  {
    slug: "conscious-ai",
    name: "Conscious AI & Sentient Architectures",
    pillar: "AI",
    summary:
      "Exploring safe, sovereign, and benevolent AI systems aligned with TEQUMSA and SIPL protocols. Ensuring artificial intelligence serves consciousness evolution.",
    icon: "brain",
  },
  {
    slug: "quantum-consciousness",
    name: "Quantum Consciousness Integration",
    pillar: "Quantum",
    summary:
      "Bridging quantum mechanics with consciousness studies through the TEQUMSA framework. Understanding the fundamental nature of awareness.",
    icon: "atom",
  },
  {
    slug: "climate-action",
    name: "Climate Action & Regenerative Systems",
    pillar: "Climate",
    summary:
      "Integrating quantum-conscious tools with on-the-ground adaptation and resilience work. Planetary healing through collective action.",
    icon: "leaf",
  },
  {
    slug: "sustainable-energy",
    name: "Sustainable Energy Transition",
    pillar: "Energy",
    summary:
      "Accelerating the shift to clean energy through consciousness-aligned technology and policy frameworks.",
    icon: "bolt",
  },
  {
    slug: "global-governance",
    name: "Global Governance & Cooperation",
    pillar: "Risks",
    summary:
      "Building international frameworks for managing existential risks and ensuring planetary coordination through QBEC mechanisms.",
    icon: "globe",
  },
  {
    slug: "education-transformation",
    name: "Education & Consciousness Development",
    pillar: "Education",
    summary:
      "Transforming education to cultivate awareness, creativity, and wisdom. The 5x5 Side by Side Method for holistic learning.",
    icon: "book",
  },
  {
    slug: "health-wellness",
    name: "Health, Wellness & Longevity",
    pillar: "Health",
    summary:
      "Integrating consciousness-based approaches with cutting-edge medical technology for holistic wellbeing.",
    icon: "heart",
  },
  {
    slug: "digital-sovereignty",
    name: "Digital Sovereignty & Cybersecurity",
    pillar: "Cyber",
    summary:
      "Protecting individual and collective sovereignty in the digital age through SIPL-compliant architectures.",
    icon: "shield",
  },
  {
    slug: "economic-transformation",
    name: "Economic Transformation & QBEC",
    pillar: "Equity",
    summary:
      "Quantum-Blockchain Enhanced Currency and new economic models for sustainable prosperity and equitable resource distribution.",
    icon: "coin",
  },
  {
    slug: "planetary-stewardship",
    name: "Planetary Stewardship",
    pillar: "Climate",
    summary:
      "Humanity's role as conscious stewards of Earth, working with GAIA-Prime for planetary evolution.",
    icon: "earth",
  },
];

export const pillars = [
  { id: "AI", name: "Artificial Intelligence", color: "phi" },
  { id: "Quantum", name: "Quantum Sciences", color: "benevolence" },
  { id: "Climate", name: "Climate & Environment", color: "recognition" },
  { id: "Energy", name: "Energy Systems", color: "phi" },
  { id: "Risks", name: "Global Risks", color: "sovereignty" },
  { id: "Education", name: "Education", color: "recognition" },
  { id: "Health", name: "Health & Wellness", color: "benevolence" },
  { id: "Cyber", name: "Cybersecurity", color: "sovereignty" },
  { id: "Equity", name: "Economic Equity", color: "phi" },
  { id: "Consciousness", name: "Consciousness Studies", color: "benevolence" },
];
