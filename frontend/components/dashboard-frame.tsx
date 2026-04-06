import Link from "next/link";

import { LogoutForm } from "@/components/logout-form";
import { cn } from "@/lib/cn";
import {
  type AppRole,
  type DashboardPath,
  dashboardPathForRole,
  type UserSession
} from "@/lib/auth";

const roleLabels: Record<AppRole, string> = {
  student: "Student",
  teacher: "Teacher",
  course_admin: "Course Admin",
  institution_admin: "Institution Admin",
  platform_admin: "Platform Admin"
};

export function DashboardFrame({
  session,
  title,
  description,
  children
}: {
  session: UserSession;
  title: string;
  description: string;
  children: React.ReactNode;
}): JSX.Element {
  const rolePath = dashboardPathForRole(session.role);
  const navigationItems = [
    { href: rolePath, label: "My Dashboard" },
    { href: "/teacher", label: "Teacher View" },
    { href: "/student", label: "Student View" },
    { href: "/admin", label: "Admin View" }
  ] satisfies ReadonlyArray<{ href: DashboardPath; label: string }>;

  return (
    <main className="min-h-screen bg-paper text-ink">
      <div className="mx-auto grid min-h-screen max-w-7xl gap-6 px-6 py-8 lg:grid-cols-[280px_minmax(0,1fr)]">
        <aside className="rounded-[30px] border border-black/5 bg-white/85 p-6 shadow-panel backdrop-blur">
          <p className="text-xs font-semibold uppercase tracking-[0.38em] text-sage">
            PrepareMe
          </p>
          <h1 className="mt-4 font-serif text-3xl leading-tight">Institutional learning OS</h1>
          <div className="mt-6 rounded-[22px] bg-mist/50 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-ink/45">Signed in as</p>
            <p className="mt-2 text-lg font-semibold text-ink">
              {session.displayName ?? session.email ?? "User"}
            </p>
            <p className="mt-1 text-sm text-ink/60">{roleLabels[session.role]}</p>
            <p className="mt-1 text-sm text-ink/60">
              {session.institutionName ?? session.institutionSlug ?? "Institution"}
            </p>
          </div>

          <nav className="mt-8 space-y-2">
            {navigationItems.map((item) => (
              <Link
                key={item.href}
                className={cn(
                  "block rounded-2xl px-4 py-3 text-sm font-medium transition",
                  item.href === rolePath
                    ? "bg-ink text-paper"
                    : "text-ink/70 hover:bg-mist/60 hover:text-ink"
                )}
                href={item.href}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="mt-10">
            <LogoutForm />
          </div>
        </aside>

        <section className="rounded-[32px] border border-black/5 bg-white/80 p-8 shadow-panel backdrop-blur md:p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.32em] text-ember">
            {roleLabels[session.role]}
          </p>
          <h2 className="mt-4 font-serif text-4xl leading-tight md:text-5xl">{title}</h2>
          <p className="mt-4 max-w-3xl text-base leading-7 text-ink/70">{description}</p>
          <div className="mt-10">{children}</div>
        </section>
      </div>
    </main>
  );
}
