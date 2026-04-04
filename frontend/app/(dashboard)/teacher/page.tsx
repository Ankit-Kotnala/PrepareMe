import { AppShell } from "@/components/app-shell";

const teacherCards = [
  {
    title: "Upload and map content",
    copy: "Bring notes, slides, or past papers into a curriculum-aware review pipeline."
  },
  {
    title: "Review AI-generated drafts",
    copy: "Approve, reject, or edit quiz drafts before they ever reach students."
  },
  {
    title: "See weak-topic signals",
    copy: "Surface class-wide confusion patterns before exam results make them obvious."
  }
];

export default function TeacherDashboardPage(): JSX.Element {
  return (
    <AppShell
      eyebrow="Teacher Control Plane"
      title="Teachers stay in control while the platform does the heavy lifting."
      description="This surface will grow into the upload, review, approval, and publishing workflow that turns raw curriculum assets into governed learning experiences."
    >
      <div className="grid gap-5 md:grid-cols-3">
        {teacherCards.map((card) => (
          <article key={card.title} className="rounded-[24px] bg-mist/50 p-5">
            <h2 className="text-lg font-semibold text-ink">{card.title}</h2>
            <p className="mt-3 text-sm leading-6 text-ink/72">{card.copy}</p>
          </article>
        ))}
      </div>
    </AppShell>
  );
}

