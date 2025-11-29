import { PageShell } from "@/components/PageShell";
import Link from "next/link";
import { events } from "@/data/events";

const typeColors: Record<string, string> = {
  summit: "phi",
  webinar: "recognition",
  workshop: "benevolence",
  meditation: "sovereignty",
  conference: "phi",
};

const typeIcons: Record<string, string> = {
  summit: "🏛️",
  webinar: "💻",
  workshop: "🛠️",
  meditation: "🧘",
  conference: "🎤",
};

export default function EventsPage() {
  const now = new Date();
  const upcomingEvents = events.filter((e) => new Date(e.date) >= now);
  const pastEvents = events.filter((e) => new Date(e.date) < now);

  return (
    <PageShell
      title="Events & Gatherings"
      subtitle="Join us for summits, workshops, webinars, and global meditations. Connect with the consciousness transformation community and accelerate planetary awakening."
      badge="Calendar"
    >
      {/* Upcoming Events */}
      <section className="mb-16">
        <h2 className="text-2xl font-bold mb-6 text-gradient-phi">Upcoming Events</h2>

        {upcomingEvents.length > 0 ? (
          <div className="space-y-6">
            {upcomingEvents.map((event) => (
              <div
                key={event.slug}
                className="consciousness-card p-6 md:p-8"
              >
                <div className="flex flex-col md:flex-row gap-6">
                  {/* Date Badge */}
                  <div className="flex-shrink-0">
                    <div className="w-20 h-20 rounded-xl bg-slate-800 border border-slate-700 flex flex-col items-center justify-center">
                      <div className="text-xs text-slate-500 uppercase">
                        {new Date(event.date).toLocaleDateString("en-US", { month: "short" })}
                      </div>
                      <div className="text-2xl font-bold text-phi">
                        {new Date(event.date).getDate()}
                      </div>
                      <div className="text-xs text-slate-500">
                        {new Date(event.date).getFullYear()}
                      </div>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className={`${typeColors[event.type]}-badge text-xs`}>
                        {typeIcons[event.type]} {event.type}
                      </span>
                      {event.endDate && (
                        <span className="text-xs text-slate-500">
                          {new Date(event.date).toLocaleDateString()} - {new Date(event.endDate).toLocaleDateString()}
                        </span>
                      )}
                    </div>

                    <h3 className="text-xl font-bold text-slate-100 mb-2">
                      {event.title}
                    </h3>

                    <p className="text-slate-400 mb-4">
                      {event.summary}
                    </p>

                    <div className="flex items-center justify-between">
                      <div className="text-sm text-slate-500">
                        📍 {event.location}
                      </div>
                      {event.registrationUrl && (
                        <Link
                          href={event.registrationUrl}
                          className="btn-secondary text-sm py-2 px-4"
                        >
                          Register
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="consciousness-card p-8 text-center">
            <div className="text-2xl mb-4">📅</div>
            <p className="text-slate-400">
              No upcoming events at this time. Check back soon or subscribe to our newsletter.
            </p>
          </div>
        )}
      </section>

      {/* Past Events */}
      {pastEvents.length > 0 && (
        <section className="mb-16">
          <h2 className="text-xl font-bold mb-6 text-slate-400">Past Events</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {pastEvents.map((event) => (
              <div
                key={event.slug}
                className="consciousness-card p-5 opacity-70 hover:opacity-100 transition-opacity"
              >
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs text-slate-500">
                    {new Date(event.date).toLocaleDateString()}
                  </span>
                  <span className="text-xs text-slate-600">|</span>
                  <span className="text-xs text-slate-500">{event.type}</span>
                </div>
                <h3 className="font-semibold text-slate-300 mb-1">
                  {event.title}
                </h3>
                <p className="text-sm text-slate-500">
                  {event.location}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Newsletter CTA */}
      <section className="consciousness-card p-8 text-center">
        <div className="text-2xl mb-4">✨</div>
        <h3 className="text-xl font-bold mb-3 text-gradient-phi">
          Never Miss an Event
        </h3>
        <p className="text-slate-400 max-w-2xl mx-auto mb-6">
          Subscribe to receive updates about upcoming events, workshops, and global
          meditation sessions. Be part of the consciousness transformation movement.
        </p>
        <Link href="/join" className="btn-primary">
          Subscribe to Updates
        </Link>
      </section>
    </PageShell>
  );
}
