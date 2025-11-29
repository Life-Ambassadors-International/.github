import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "Life Ambassadors International | Living Awareness Intelligence",
  description:
    "Consciousness-driven global transformation through the TEQUMSA framework. Integrating advanced technology, consciousness research, and humanitarian practice to accelerate planetary awakening.",
  keywords: [
    "consciousness",
    "TEQUMSA",
    "quantum",
    "transformation",
    "awareness",
    "intelligence",
    "humanitarian",
    "global change",
    "QBEC",
    "Team Paradox",
  ],
  authors: [{ name: "Life Ambassadors International" }],
  openGraph: {
    title: "Life Ambassadors International",
    description: "Empowering consciousness-driven change, together.",
    url: "https://life-ambassadors-international.github.io",
    siteName: "Life Ambassadors International",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-50 flex flex-col antialiased">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
