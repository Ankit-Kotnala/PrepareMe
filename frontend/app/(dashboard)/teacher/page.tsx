import { DashboardFrame } from "@/components/dashboard-frame";
import { requireServerSession } from "@/lib/auth";

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

export default async function TeacherDashboardPage(): Promise<JSX.Element> {
  const session = await requireServerSession(["teacher", "course_admin"]);

  return (
    <DashboardFrame
      session={session}
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
      <div className="mt-6 grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
        <section className="rounded-[24px] border border-black/5 bg-white/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-ember">
            Review Queue
          </p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/72">
            <li>7 draft quizzes waiting for review</li>
            <li>2 low-confidence uploads need curriculum remapping</li>
            <li>1 assessment is approved but not yet published</li>
          </ul>
        </section>
        <section className="rounded-[24px] border border-black/5 bg-white/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-ember">
            Today&apos;s Leverage
          </p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/72">
            <li>Re-run biology chapter mapping after latest upload</li>
            <li>Approve practice set for Unit 3 before 5 PM</li>
            <li>Review confusion cluster on alternating current</li>
          </ul>
        </section>
      </div>
    </DashboardFrame>
  );
}

