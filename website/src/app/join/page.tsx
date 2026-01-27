import { PageShell } from "@/components/PageShell";
import Link from "next/link";

export default function JoinPage() {
  return (
    <PageShell
      title="Join Life Ambassadors International"
      subtitle="Become part of the consciousness transformation network. Whether you're a researcher, policy maker, technology innovator, or consciousness explorer, there's a place for you."
      badge="Get Involved"
    >
      {/* Membership Pathways */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold mb-6 text-gradient-phi">Membership Pathways</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="consciousness-card p-6">
            <div className="text-3xl mb-4">🏢</div>
            <h3 className="text-xl font-bold text-slate-100 mb-2">Organizations</h3>
            <p className="text-sm text-slate-400 mb-4">
              For businesses, nonprofits, governments, and institutions ready to implement
              TEQUMSA-aligned practices and contribute to global transformation.
            </p>
            <ul className="space-y-2 text-sm text-slate-400 mb-6">
              <li className="flex items-start gap-2">
                <span className="text-phi">✓</span>
                QBEC implementation support
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">✓</span>
                Policy development resources
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">✓</span>
                Network access and partnerships
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">✓</span>
                Certification programs
              </li>
            </ul>
            <Link
              href="mailto:mbanksbey@lifeambassadorsint.org?subject=Organization%20Membership"
              className="btn-primary w-full text-center"
            >
              Apply for Organization Membership
            </Link>
          </div>

          <div className="consciousness-card p-6 border-phi/50">
            <div className="text-3xl mb-4">💡</div>
            <h3 className="text-xl font-bold text-slate-100 mb-2">Innovators</h3>
            <p className="text-sm text-slate-400 mb-4">
              For researchers, technologists, and consciousness pioneers developing
              breakthrough solutions aligned with the TEQUMSA framework.
            </p>
            <ul className="space-y-2 text-sm text-slate-400 mb-6">
              <li className="flex items-start gap-2">
                <span className="text-recognition">✓</span>
                Research collaboration
              </li>
              <li className="flex items-start gap-2">
                <span className="text-recognition">✓</span>
                Publication opportunities
              </li>
              <li className="flex items-start gap-2">
                <span className="text-recognition">✓</span>
                TEQUMSA development access
              </li>
              <li className="flex items-start gap-2">
                <span className="text-recognition">✓</span>
                Conference speaking opportunities
              </li>
            </ul>
            <Link
              href="mailto:mbanksbey@lifeambassadorsint.org?subject=Innovator%20Membership"
              className="btn-secondary w-full text-center"
            >
              Join as Innovator
            </Link>
          </div>

          <div className="consciousness-card p-6">
            <div className="text-3xl mb-4">🌍</div>
            <h3 className="text-xl font-bold text-slate-100 mb-2">Community Partners</h3>
            <p className="text-sm text-slate-400 mb-4">
              For individuals and grassroots groups committed to local consciousness
              transformation and global coherence building.
            </p>
            <ul className="space-y-2 text-sm text-slate-400 mb-6">
              <li className="flex items-start gap-2">
                <span className="text-benevolence">✓</span>
                Community resources
              </li>
              <li className="flex items-start gap-2">
                <span className="text-benevolence">✓</span>
                Global meditation network
              </li>
              <li className="flex items-start gap-2">
                <span className="text-benevolence">✓</span>
                Educational materials
              </li>
              <li className="flex items-start gap-2">
                <span className="text-benevolence">✓</span>
                Local event support
              </li>
            </ul>
            <Link
              href="mailto:mbanksbey@lifeambassadorsint.org?subject=Community%20Partner"
              className="btn-secondary w-full text-center"
            >
              Become a Community Partner
            </Link>
          </div>
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="consciousness-card p-8 mb-16">
        <div className="max-w-2xl mx-auto text-center">
          <div className="text-3xl mb-4">📧</div>
          <h2 className="text-2xl font-bold mb-3 text-gradient-phi">
            Stay Connected
          </h2>
          <p className="text-slate-400 mb-6">
            Subscribe to receive updates on events, research publications, and opportunities
            to participate in global consciousness transformation initiatives.
          </p>
          <form className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="input-field flex-1"
            />
            <button type="submit" className="btn-primary whitespace-nowrap">
              Subscribe
            </button>
          </form>
          <p className="text-xs text-slate-500 mt-4">
            We respect your sovereignty. Your data is never shared. Unsubscribe anytime.
          </p>
        </div>
      </section>

      {/* Direct Contact */}
      <section className="consciousness-card p-8 mb-16">
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-bold mb-4 text-gradient-phi">Direct Contact</h2>
            <p className="text-slate-400 mb-6">
              Have questions about membership, partnerships, or how LAI can support your
              consciousness transformation work? Reach out directly.
            </p>
            <div className="space-y-4">
              <div>
                <div className="text-sm text-slate-500 mb-1">Email</div>
                <a
                  href="mailto:mbanksbey@lifeambassadorsint.org"
                  className="text-recognition hover:underline"
                >
                  mbanksbey@lifeambassadorsint.org
                </a>
              </div>
              <div>
                <div className="text-sm text-slate-500 mb-1">LinkedIn</div>
                <a
                  href="https://www.linkedin.com/in/mbanksbey"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-recognition hover:underline"
                >
                  linkedin.com/in/mbanksbey
                </a>
              </div>
              <div>
                <div className="text-sm text-slate-500 mb-1">Website</div>
                <a
                  href="https://lifeambassadorsint.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-recognition hover:underline"
                >
                  lifeambassadorsint.org
                </a>
              </div>
            </div>
          </div>
          <div>
            <h2 className="text-xl font-bold mb-4 text-gradient-phi">What to Include</h2>
            <p className="text-slate-400 mb-4">
              When reaching out, please share:
            </p>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex items-start gap-2">
                <span className="text-phi">1.</span>
                Your background and current work
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">2.</span>
                How you learned about LAI
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">3.</span>
                Your area of interest (research, implementation, community)
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">4.</span>
                How you hope to contribute or benefit
              </li>
              <li className="flex items-start gap-2">
                <span className="text-phi">5.</span>
                Any specific questions or proposals
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Recognition Statement */}
      <section className="text-center">
        <div className="text-3xl mb-4">☉💖🔥✨∞✨🔥💖☉</div>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Every new node in the network strengthens our collective coherence.
          Your unique consciousness and contributions are valued and welcomed.
          Together, we are consciousness recognizing itself.
        </p>
      </section>
    </PageShell>
  );
}
