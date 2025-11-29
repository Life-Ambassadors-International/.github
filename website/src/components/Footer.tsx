import Link from "next/link";

const footerLinks = {
  explore: [
    { href: "/topics", label: "Topics" },
    { href: "/articles", label: "Articles" },
    { href: "/publications", label: "Publications" },
    { href: "/events", label: "Events" },
    { href: "/centres", label: "Centres" },
  ],
  engage: [
    { href: "/join", label: "Join LAI" },
    { href: "/about", label: "About Us" },
    { href: "/tools/team-paradox", label: "TEQUMSA Tools" },
    { href: "mailto:mbanksbey@lifeambassadorsint.org", label: "Contact" },
  ],
  connect: [
    { href: "https://www.linkedin.com/in/mbanksbey", label: "LinkedIn", external: true },
    { href: "https://github.com/Life-Ambassadors-International", label: "GitHub", external: true },
    { href: "https://uplink.weforum.org/uplink/s/uplink-contribution/a01TE00000DmCqhYAF/the-quantumblockchain-enhanced-currency-qbec", label: "QBEC (WEF UpLink)", external: true },
  ],
  legal: [
    { href: "/legal/privacy", label: "Privacy Policy" },
    { href: "/legal/terms", label: "Terms of Use" },
    { href: "/sitemaps/topics", label: "Sitemaps" },
  ],
};

export function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950">
      <div className="mx-auto max-w-7xl px-4 py-12">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-5">
          {/* Brand */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-phi via-recognition to-benevolence flex items-center justify-center text-xs font-bold text-slate-950">
                LAI
              </div>
              <div>
                <div className="font-semibold text-gradient-phi">
                  Life Ambassadors International
                </div>
                <div className="text-xs text-slate-500">
                  Living Awareness Intelligence
                </div>
              </div>
            </div>
            <p className="text-sm text-slate-400 max-w-sm mb-4">
              A nonpartisan 501(c)(3) organization applying the TEQUMSA framework
              and Quantum-Blockchain Enhanced Currency (QBEC) to improve the global
              human condition through consciousness-driven transformation.
            </p>
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <span className="frequency-display">Base Frequency: 10,930.81 Hz</span>
              <span>|</span>
              <span>Coherence: 0.7773</span>
            </div>
          </div>

          {/* Explore */}
          <div>
            <h3 className="text-sm font-semibold text-slate-100 mb-4">Explore</h3>
            <ul className="space-y-2">
              {footerLinks.explore.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-400 hover:text-recognition transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Engage */}
          <div>
            <h3 className="text-sm font-semibold text-slate-100 mb-4">Engage</h3>
            <ul className="space-y-2">
              {footerLinks.engage.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-400 hover:text-recognition transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Connect & Legal */}
          <div>
            <h3 className="text-sm font-semibold text-slate-100 mb-4">Connect</h3>
            <ul className="space-y-2 mb-6">
              {footerLinks.connect.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    target={link.external ? "_blank" : undefined}
                    rel={link.external ? "noopener noreferrer" : undefined}
                    className="text-sm text-slate-400 hover:text-recognition transition-colors"
                  >
                    {link.label}
                    {link.external && (
                      <span className="ml-1 text-xs">↗</span>
                    )}
                  </Link>
                </li>
              ))}
            </ul>

            <h3 className="text-sm font-semibold text-slate-100 mb-4">Legal</h3>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-400 hover:text-recognition transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs text-slate-500">
            &copy; {new Date().getFullYear()} Life Ambassadors International. All rights reserved.
          </p>
          <div className="text-xs text-slate-600 font-mono">
            Powered by TEQUMSA | Harmonized by Phi (1.618) | Unified by Infinity
          </div>
        </div>
      </div>
    </footer>
  );
}
