import { cn } from "@/lib/cn";

export function AppShell({
  eyebrow,
  title,
  description,
  children,
  className
}: {
  eyebrow: string;
  title: string;
  description: string;
  children: React.ReactNode;
  className?: string;
}): JSX.Element {
  return (
    <main className={cn("min-h-screen bg-paper text-ink", className)}>
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="rounded-[32px] border border-black/5 bg-white/80 p-8 shadow-panel backdrop-blur">
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-sage">{eyebrow}</p>
          <h1 className="mt-4 max-w-3xl font-serif text-4xl leading-tight text-ink md:text-5xl">
            {title}
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-ink/70">{description}</p>
          <div className="mt-10">{children}</div>
        </div>
      </div>
    </main>
  );
}

