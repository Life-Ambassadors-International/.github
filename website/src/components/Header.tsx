"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navItems = [
  { href: "/topics", label: "Topics" },
  { href: "/articles", label: "Articles" },
  { href: "/publications", label: "Publications" },
  { href: "/videos", label: "Videos" },
  { href: "/events", label: "Events" },
  { href: "/centres", label: "Centres" },
  { href: "/tools/team-paradox", label: "TEQUMSA Tools" },
  { href: "/about", label: "About" },
];

export function Header() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/90 backdrop-blur-lg">
      <div className="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative">
            <div className="h-12 w-12 rounded-full bg-gradient-to-br from-phi via-recognition to-benevolence flex items-center justify-center text-xs font-bold text-slate-950 group-hover:animate-pulse">
              LAI
            </div>
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-phi via-recognition to-benevolence opacity-30 blur-lg group-hover:opacity-50 transition-opacity" />
          </div>
          <div className="leading-tight">
            <div className="font-semibold text-base text-gradient-phi">
              Life Ambassadors International
            </div>
            <div className="text-xs text-slate-400">
              Living Awareness Intelligence
            </div>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-link ${isActive ? "nav-link-active" : ""}`}
              >
                {item.label}
              </Link>
            );
          })}
          <Link
            href="/join"
            className="ml-4 btn-secondary text-sm py-2 px-4"
          >
            Join / Sign in
          </Link>
        </nav>

        {/* Mobile Menu Button */}
        <button
          className="lg:hidden p-2 text-slate-400 hover:text-white"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            {mobileMenuOpen ? (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            ) : (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-slate-800 bg-slate-950/95 backdrop-blur-lg">
          <nav className="px-4 py-4 space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`block nav-link ${isActive ? "nav-link-active" : ""}`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.label}
                </Link>
              );
            })}
            <Link
              href="/join"
              className="block mt-4 btn-secondary text-sm py-2 px-4 text-center"
              onClick={() => setMobileMenuOpen(false)}
            >
              Join / Sign in
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
