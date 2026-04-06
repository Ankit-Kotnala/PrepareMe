import { redirect } from "next/navigation";

import { LoginForm } from "@/components/login-form";
import { dashboardPathForRole, getServerSession } from "@/lib/auth";

const surfaceCards = [
  {
    label: "Teacher Surface",
    title: "Review drafts. Approve content. Publish with intent.",
    copy: "The control plane for mapping material, curating outputs, and protecting what reaches students."
  },
  {
    label: "Student Surface",
    title: "Revision that remembers where understanding actually breaks.",
    copy: "Mastery-aware explanations, targeted practice, and grounded support anchored to approved curriculum."
  },
  {
    label: "Admin Surface",
    title: "Policy, analytics, and institutional visibility in one place.",
    copy: "Adjust strictness, inspect readiness trends, and keep the tenant boundary non-negotiable."
  }
] as const;

const signalCards = [
  { metric: "RLS", label: "Database isolation active" },
  { metric: "LOG", label: "Audit-first AI interactions" },
  { metric: "MAP", label: "Curriculum-scoped routing" }
] as const;

export default async function HomePage(): Promise<JSX.Element> {
  const session = await getServerSession();
  if (session) {
    redirect(dashboardPathForRole(session.role));
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#040814] text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(114,225,255,0.18),transparent_28%),radial-gradient(circle_at_80%_18%,rgba(123,241,168,0.14),transparent_24%),linear-gradient(180deg,rgba(255,255,255,0.04),transparent_36%)]" />
      <div className="absolute inset-0 opacity-35 [background-image:linear-gradient(rgba(151,169,199,0.12)_1px,transparent_1px),linear-gradient(90deg,rgba(151,169,199,0.12)_1px,transparent_1px)] [background-size:72px_72px]" />
      <div className="auth-orb-drift absolute -left-20 top-24 h-72 w-72 rounded-full bg-[#72e1ff]/18 blur-3xl" />
      <div className="auth-orb-drift absolute right-[-4rem] top-[18rem] h-80 w-80 rounded-full bg-[#7bf1a8]/15 blur-3xl" />

      <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-6 lg:px-10">
        <header className="flex items-center justify-between">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-[0.34em] text-[#72e1ff]">
              PrepareMe
            </p>
            <p className="mt-2 max-w-xl text-sm text-white/52">
              Curriculum-aware learning infrastructure for institutions that need trust,
              policy, and persistent mastery to coexist in one system.
            </p>
          </div>

          <div className="hidden items-center gap-3 lg:flex">
            {["Tenant secure", "Grounded only", "Role aware"].map((item) => (
              <div
                key={item}
                className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 font-mono text-[11px] uppercase tracking-[0.22em] text-white/56"
              >
                {item}
              </div>
            ))}
          </div>
        </header>

        <section className="grid flex-1 gap-8 pb-10 pt-8 lg:grid-cols-[1.12fr_0.88fr]">
          <div className="relative overflow-hidden rounded-[34px] border border-white/10 bg-white/[0.05] p-8 shadow-[0_40px_120px_rgba(0,0,0,0.35)] backdrop-blur-2xl md:p-10">
            <div className="absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent via-[#72e1ff] to-transparent opacity-80" />

            <div className="grid gap-10 xl:grid-cols-[1.1fr_0.9fr]">
              <div>
                <div className="inline-flex items-center gap-3 rounded-full border border-white/10 bg-black/20 px-4 py-2">
                  <span className="h-2.5 w-2.5 rounded-full bg-[#7bf1a8]" />
                  <p className="font-mono text-[11px] uppercase tracking-[0.3em] text-white/62">
                    Identity-routed institutional access
                  </p>
                </div>

                <h1 className="mt-6 max-w-4xl font-serif text-5xl leading-[0.95] md:text-7xl">
                  Every sign-in should feel like entering the right operating layer.
                </h1>

                <p className="mt-6 max-w-2xl text-base leading-8 text-white/72 md:text-lg">
                  PrepareMe is not a chatbot wrapper. Teachers enter a publishing and
                  review surface. Students enter a mastery and revision surface. Admins
                  enter a policy and analytics surface. One institution, three different
                  control geometries, all grounded in approved content.
                </p>

                <div className="mt-8 flex flex-wrap gap-3">
                  {[
                    "Hallucination firewall",
                    "Mastery memory",
                    "Multi-tenant by design"
                  ].map((tag) => (
                    <div
                      key={tag}
                      className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 font-mono text-[11px] uppercase tracking-[0.24em] text-white/58"
                    >
                      {tag}
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid gap-4">
                {signalCards.map((item, index) => (
                  <article
                    key={item.metric}
                    className="rounded-[28px] border border-white/10 bg-[linear-gradient(180deg,rgba(255,255,255,0.08),rgba(255,255,255,0.03))] p-5"
                  >
                    <div className="flex items-center justify-between">
                      <p className="font-serif text-3xl text-white">{item.metric}</p>
                      <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-white/34">
                        0{index + 1}
                      </p>
                    </div>
                    <p className="mt-5 text-sm leading-6 text-white/62">{item.label}</p>
                  </article>
                ))}
              </div>
            </div>

            <div className="mt-10 grid gap-4 md:grid-cols-3">
              {surfaceCards.map((item) => (
                <article
                  key={item.label}
                  className="rounded-[28px] border border-white/10 bg-black/18 p-5"
                >
                  <p className="font-mono text-[11px] uppercase tracking-[0.3em] text-[#72e1ff]">
                    {item.label}
                  </p>
                  <h2 className="mt-4 font-serif text-2xl leading-tight text-white">
                    {item.title}
                  </h2>
                  <p className="mt-4 text-sm leading-7 text-white/64">{item.copy}</p>
                </article>
              ))}
            </div>
          </div>

          <section className="rounded-[34px] border border-white/10 bg-[linear-gradient(180deg,rgba(8,14,25,0.92),rgba(6,11,20,0.88))] p-6 shadow-[0_45px_140px_rgba(0,0,0,0.5)] backdrop-blur-2xl md:p-8">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="font-mono text-[11px] uppercase tracking-[0.34em] text-[#7bf1a8]">
                  Secure Entry
                </p>
                <h2 className="mt-4 max-w-lg font-serif text-4xl leading-tight text-white">
                  Sign in to the institution layer that matches your role.
                </h2>
              </div>

              <div className="hidden rounded-full border border-[#72e1ff]/16 bg-[#72e1ff]/10 px-4 py-2 font-mono text-[10px] uppercase tracking-[0.24em] text-[#72e1ff] md:block">
                Turnstile Protected
              </div>
            </div>

            <p className="mt-5 max-w-xl text-base leading-8 text-white/66">
              Enter your institution code, verify the Cloudflare challenge, and let the
              platform route you into the right dashboard with the right controls.
            </p>

            <div className="mt-6 rounded-[28px] border border-white/10 bg-white/[0.04] p-4">
              <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-white/46">
                Local pilot setup
              </p>
              <p className="mt-3 text-sm leading-7 text-white/62">
                Demo accounts are preseeded for development so you can move directly into
                role-based surfaces while we build the real institutional workflows.
              </p>
            </div>

            <div className="mt-8">
              <LoginForm />
            </div>
          </section>
        </section>
      </div>
    </main>
  );
}
