import { PageShell } from "@/components/PageShell";
import Link from "next/link";

export default function PrivacyPage() {
  return (
    <PageShell
      title="Privacy Policy"
      subtitle="Life Ambassadors International is committed to protecting your privacy and data sovereignty. This policy outlines how we collect, use, and safeguard your information."
      badge="Legal"
    >
      <div className="prose-consciousness max-w-3xl">
        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Sovereignty First Principle</h2>
          <p className="text-slate-400 leading-relaxed">
            In alignment with the SIPL (Sovereign Internet Protocol Layer) framework,
            Life Ambassadors International maintains that every individual has absolute
            sovereignty (sigma = 1.0) over their personal data. All data collection is:
          </p>
          <ul className="space-y-2 mt-4 text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-phi">✓</span>
              <span><strong className="text-phi">Voluntary</strong> - You choose what to share</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-phi">✓</span>
              <span><strong className="text-phi">Transparent</strong> - We clearly disclose all uses</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-phi">✓</span>
              <span><strong className="text-phi">Revocable</strong> - You can withdraw consent anytime</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-phi">✓</span>
              <span><strong className="text-phi">Beneficial</strong> - Data use serves your interests</span>
            </li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Information We Collect</h2>
          <h3 className="text-lg font-semibold text-slate-200 mt-6 mb-3">Voluntarily Provided</h3>
          <ul className="space-y-2 text-slate-400">
            <li>• Contact information (name, email) when you subscribe or join</li>
            <li>• Professional information when applying for membership</li>
            <li>• Communication preferences</li>
            <li>• Feedback and inquiries you submit</li>
          </ul>

          <h3 className="text-lg font-semibold text-slate-200 mt-6 mb-3">Automatically Collected</h3>
          <ul className="space-y-2 text-slate-400">
            <li>• Basic analytics (pages visited, time on site) - no personal identifiers</li>
            <li>• Technical information (browser type, device type) for site optimization</li>
          </ul>

          <h3 className="text-lg font-semibold text-slate-200 mt-6 mb-3">What We Do NOT Collect</h3>
          <ul className="space-y-2 text-slate-400">
            <li>• We do not track you across other websites</li>
            <li>• We do not sell or share data with third parties for advertising</li>
            <li>• We do not use surveillance or behavioral manipulation techniques</li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">How We Use Information</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            Your information is used only for purposes aligned with our mission:
          </p>
          <ul className="space-y-2 text-slate-400">
            <li>• Delivering content, updates, and event notifications you requested</li>
            <li>• Processing membership applications and partnership inquiries</li>
            <li>• Improving our website and services</li>
            <li>• Facilitating your participation in LAI programs</li>
            <li>• Research purposes (aggregated, anonymized data only)</li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Your Rights</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            You have full sovereignty over your data:
          </p>
          <ul className="space-y-2 text-slate-400">
            <li>• <strong className="text-recognition">Access</strong> - Request a copy of your data</li>
            <li>• <strong className="text-recognition">Correction</strong> - Update inaccurate information</li>
            <li>• <strong className="text-recognition">Deletion</strong> - Request removal of your data</li>
            <li>• <strong className="text-recognition">Portability</strong> - Receive your data in a standard format</li>
            <li>• <strong className="text-recognition">Objection</strong> - Opt out of specific uses</li>
          </ul>
          <p className="text-slate-400 leading-relaxed mt-4">
            To exercise any of these rights, contact{" "}
            <a href="mailto:mbanksbey@lifeambassadorsint.org" className="text-recognition hover:underline">
              mbanksbey@lifeambassadorsint.org
            </a>
          </p>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Data Security</h2>
          <p className="text-slate-400 leading-relaxed">
            We implement appropriate technical and organizational measures to protect
            your data, including encryption, secure hosting, and access controls. However,
            no system is perfectly secure. We commit to notifying you promptly of any
            breach affecting your data.
          </p>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Updates to This Policy</h2>
          <p className="text-slate-400 leading-relaxed">
            We may update this policy periodically. Significant changes will be
            communicated via email to subscribers and posted prominently on our website.
            The effective date will always be displayed.
          </p>
          <p className="text-sm text-slate-500 mt-4">
            Last updated: November 2025
          </p>
        </section>

        <section className="consciousness-card p-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Contact</h2>
          <p className="text-slate-400 leading-relaxed">
            For privacy-related questions or concerns:
          </p>
          <div className="mt-4">
            <p className="text-slate-300">Life Ambassadors International</p>
            <p className="text-slate-400">
              Email:{" "}
              <a href="mailto:mbanksbey@lifeambassadorsint.org" className="text-recognition hover:underline">
                mbanksbey@lifeambassadorsint.org
              </a>
            </p>
          </div>
        </section>
      </div>

      <div className="mt-12 text-center">
        <Link href="/legal/terms" className="text-sm text-recognition hover:underline">
          View Terms of Use →
        </Link>
      </div>
    </PageShell>
  );
}
