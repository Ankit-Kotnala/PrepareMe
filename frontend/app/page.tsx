import Link from "next/link";

export default function HomePage(): JSX.Element {
  return (
    <main className="min-h-screen bg-paper text-ink">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-16">
        <section className="rounded-[36px] border border-black/5 bg-white/80 p-8 shadow-panel backdrop-blur md:p-12">
          <p className="text-xs font-semibold uppercase tracking-[0.38em] text-sage">
            Institutional AI Learning OS
          </p>
          <h1 className="mt-5 max-w-4xl font-serif text-5xl leading-tight md:text-7xl">
            Build trust first. Let the intelligence compound second.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-ink/72">
            PrepareMe converts institutional curriculum into an executable learning graph,
            protects responses with a hallucination firewall, and compounds value through
            persistent mastery memory.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              className="rounded-full bg-ink px-6 py-3 text-sm font-semibold text-paper transition hover:bg-ink/90"
              href="/teacher"
            >
              Open Teacher Surface
            </Link>
            <Link
              className="rounded-full border border-ink/15 px-6 py-3 text-sm font-semibold text-ink transition hover:border-ink/40"
              href="/student"
            >
              Open Student Surface
            </Link>
          </div>
        </section>

        <section className="grid gap-5 md:grid-cols-3">
          {[
            {
              title: "Curriculum Graph",
              copy: "Institutional academic DNA captured as a structured, versioned graph."
            },
            {
              title: "Hallucination Firewall",
              copy: "Grounded retrieval, confidence scoring, refusal logic, and auditability."
            },
            {
              title: "Mastery Memory",
              copy: "Per-student learning state that compounds with every interaction."
            }
          ].map((item) => (
            <article
              key={item.title}
              className="rounded-[28px] border border-black/5 bg-white/70 p-6 shadow-panel"
            >
              <p className="text-sm font-semibold uppercase tracking-[0.18em] text-ember">
                {item.title}
              </p>
              <p className="mt-4 text-base leading-7 text-ink/72">{item.copy}</p>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}

