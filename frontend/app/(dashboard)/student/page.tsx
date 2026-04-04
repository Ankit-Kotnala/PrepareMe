import { AppShell } from "@/components/app-shell";

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

export default function StudentDashboardPage(): JSX.Element {
  return (
    <AppShell
      eyebrow="Student Learning Surface"
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
    </AppShell>
  );
}

