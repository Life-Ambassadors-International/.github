interface PageShellProps {
  title: string;
  subtitle?: string;
  badge?: string;
  children: React.ReactNode;
}

export function PageShell({ title, subtitle, badge, children }: PageShellProps) {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 md:py-16">
      <div className="mb-10">
        {badge && (
          <div className="text-xs tracking-[0.25em] uppercase text-phi mb-3">
            {badge}
          </div>
        )}
        <h1 className="text-3xl md:text-4xl font-bold text-gradient-phi mb-3">
          {title}
        </h1>
        {subtitle && (
          <p className="text-lg text-slate-300 max-w-3xl">
            {subtitle}
          </p>
        )}
      </div>
      {children}
    </div>
  );
}
