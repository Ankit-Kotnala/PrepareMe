import { DashboardFrame } from "@/components/dashboard-frame";
import { requireServerSession } from "@/lib/auth";

const adminCards = [
  {
    title: "Policy strictness",
    copy: "Control confidence thresholds, refusal behavior, and explanation depth across the institution."
  },
  {
    title: "Institution analytics",
    copy: "See cohort weakness, exam readiness distribution, and content effectiveness signals."
  },
  {
    title: "Governance and access",
    copy: "Manage role-bound surfaces, audit visibility, and review workflow expectations."
  }
];

export default async function AdminDashboardPage(): Promise<JSX.Element> {
  const session = await requireServerSession(["institution_admin", "platform_admin"]);

  return (
    <DashboardFrame
      session={session}
      title="Admins shape the policy, trust, and operating rules of the platform."
      description="This dashboard is where institutional governance lives: policy controls, role visibility, analytics access, and the operating guardrails that make PrepareMe safe to deploy."
    >
      <div className="grid gap-5 md:grid-cols-3">
        {adminCards.map((card) => (
          <article key={card.title} className="rounded-[24px] bg-mist/50 p-5">
            <h2 className="text-lg font-semibold text-ink">{card.title}</h2>
            <p className="mt-3 text-sm leading-6 text-ink/72">{card.copy}</p>
          </article>
        ))}
      </div>

      <div className="mt-6 grid gap-5 lg:grid-cols-[1.15fr_0.85fr]">
        <section className="rounded-[24px] border border-black/5 bg-white/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-ember">
            Immediate Controls
          </p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/72">
            <li>Raise minimum confidence threshold for chemistry explanations</li>
            <li>Keep student-facing assessments under manual approval</li>
            <li>Review flagged AI responses from the last 24 hours</li>
          </ul>
        </section>
        <section className="rounded-[24px] border border-black/5 bg-white/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-ember">
            Institution Snapshot
          </p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-ink/72">
            <li>3 teacher workspaces active today</li>
            <li>1 review queue at risk of delay</li>
            <li>Top confusion cluster: electrochemistry vs galvanic cell setup</li>
          </ul>
        </section>
      </div>
    </DashboardFrame>
  );
}
