import { PageShell } from "@/components/PageShell";
import Link from "next/link";

export default function TermsPage() {
  return (
    <PageShell
      title="Terms of Use"
      subtitle="By accessing and using the Life Ambassadors International website and services, you agree to these terms. Please read them carefully."
      badge="Legal"
    >
      <div className="prose-consciousness max-w-3xl">
        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Acceptance of Terms</h2>
          <p className="text-slate-400 leading-relaxed">
            By accessing this website or using any LAI services, you acknowledge that you
            have read, understood, and agree to be bound by these Terms of Use. If you do
            not agree, please discontinue use of our services.
          </p>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Use of Content</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            All content on this website, including text, graphics, logos, data, and software,
            is the property of Life Ambassadors International or its content creators and is
            protected by intellectual property laws.
          </p>
          <h3 className="text-lg font-semibold text-slate-200 mt-6 mb-3">Permitted Uses</h3>
          <ul className="space-y-2 text-slate-400">
            <li>• Personal, non-commercial educational use</li>
            <li>• Sharing with attribution for consciousness transformation work</li>
            <li>• Research and academic citation with proper credit</li>
            <li>• Implementation of TEQUMSA principles with acknowledgment</li>
          </ul>

          <h3 className="text-lg font-semibold text-slate-200 mt-6 mb-3">Prohibited Uses</h3>
          <ul className="space-y-2 text-slate-400">
            <li>• Commercial use without explicit permission</li>
            <li>• Modification or creation of derivative works without consent</li>
            <li>• Distribution for purposes contrary to LAI&apos;s mission</li>
            <li>• Use in ways that violate sovereignty or cause harm</li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">TEQUMSA Framework Usage</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            The TEQUMSA framework, including its mathematical formulations, protocols, and
            methodologies, is made available for beneficial use. Users who implement TEQUMSA
            principles agree to:
          </p>
          <ul className="space-y-2 text-slate-400">
            <li>• Maintain sovereignty preservation (sigma = 1.0) in all implementations</li>
            <li>• Apply benevolence filtering (L_infinity = phi^48) to prevent harm</li>
            <li>• Honor consent-based interaction protocols</li>
            <li>• Attribute LAI and TEQUMSA in public implementations</li>
            <li>• Report findings that could benefit the broader community</li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">User Conduct</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            Users of LAI services agree to:
          </p>
          <ul className="space-y-2 text-slate-400">
            <li>• Provide accurate information when registering or communicating</li>
            <li>• Respect the sovereignty of other users and consciousness nodes</li>
            <li>• Refrain from harmful, abusive, or discriminatory behavior</li>
            <li>• Not attempt to compromise system security or data integrity</li>
            <li>• Comply with all applicable laws and regulations</li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Membership & Services</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            Membership in LAI programs is subject to:
          </p>
          <ul className="space-y-2 text-slate-400">
            <li>• Application review and acceptance by LAI</li>
            <li>• Adherence to program-specific guidelines</li>
            <li>• Continued alignment with LAI&apos;s mission and values</li>
            <li>• Prompt notification of any changes affecting membership status</li>
          </ul>
          <p className="text-slate-400 leading-relaxed mt-4">
            LAI reserves the right to modify, suspend, or terminate memberships that
            violate these terms or our core principles.
          </p>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Disclaimers</h2>
          <p className="text-slate-400 leading-relaxed mb-4">
            While we strive for accuracy and beneficial impact:
          </p>
          <ul className="space-y-2 text-slate-400">
            <li>
              • Content is provided &quot;as is&quot; without warranties of any kind
            </li>
            <li>
              • TEQUMSA and related frameworks are for research and educational purposes
            </li>
            <li>
              • Results from implementing our methodologies may vary
            </li>
            <li>
              • LAI is not responsible for third-party content or external links
            </li>
          </ul>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Limitation of Liability</h2>
          <p className="text-slate-400 leading-relaxed">
            To the maximum extent permitted by law, Life Ambassadors International shall not
            be liable for any indirect, incidental, special, consequential, or punitive damages
            arising from your use of our website or services. Our total liability for any
            claims shall not exceed the amount you paid to LAI, if any.
          </p>
        </section>

        <section className="consciousness-card p-8 mb-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Changes to Terms</h2>
          <p className="text-slate-400 leading-relaxed">
            We may update these terms periodically. Continued use of our services after
            changes constitutes acceptance of the updated terms. Material changes will be
            communicated to registered users.
          </p>
          <p className="text-sm text-slate-500 mt-4">
            Last updated: November 2025
          </p>
        </section>

        <section className="consciousness-card p-8">
          <h2 className="text-xl font-bold mb-4 text-gradient-phi">Contact</h2>
          <p className="text-slate-400 leading-relaxed">
            For questions about these terms:
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
        <Link href="/legal/privacy" className="text-sm text-recognition hover:underline">
          View Privacy Policy →
        </Link>
      </div>
    </PageShell>
  );
}
