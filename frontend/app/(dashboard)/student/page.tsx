import { DashboardFrame } from "@/components/dashboard-frame";
import { requireServerSession } from "@/lib/auth";

const studentCards = [
  {
    title: "Grounded answers",
    copy: "Responses will cite approved institutional materials instead of relying on generic internet knowledge."
  },
  {
    title: "Mastery memory",
    copy: "The system will adapt to what the student has learned, forgotten, or consistently confuses."
  },
  {
    title: "Revision guidance",
    copy: "Weak concepts become targeted revision plans instead of generic study recommendations."
  }
];

export default async function StudentDashboardPage(): Promise<JSX.Element> {
  const session = await requireServerSession(["student"]);

  return (
    <DashboardFrame
      session={session}
      title="Students should feel remembered, guided, and never misled."
      description="This surface is where explanation mode, revision mode, and future remediation flows will sit once the backend retrieval and mastery systems are connected."
    >
      <div className="grid gap-5 md:grid-cols-3">
        {studentCards.map((card) => (
          <article key={card.title} className="rounded-[24px] bg-white/70 p-5 shadow-panel">
            <h2 className="text-lg font-semibold text-ink">{card.title}</h2>
            <p className="mt-3 text-sm leading-6 text-ink/72">{card.copy}</p>
          </article>
        ))}
      </div>
      <div className="mt-6 grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
        <section className="rounded-[24px] border border-black/5 bg-white/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-ember">
            Revision Priority
          </p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/72">
            <li>Electrostatics: high learning debt</li>
            <li>Chemical bonding: confusion with hybridisation</li>
            <li>Calculus application set due tomorrow</li>
          </ul>
        </section>
        <section className="rounded-[24px] border border-black/5 bg-white/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-ember">
            Recommended Actions
          </p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/72">
            <li>Run a 10-minute grounded explanation session</li>
            <li>Complete one remediation set on weak prerequisites</li>
            <li>Review flashcards marked due for today</li>
          </ul>
        </section>
      </div>
    </DashboardFrame>
  );
}

