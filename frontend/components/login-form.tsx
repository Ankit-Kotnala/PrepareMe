"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { TurnstileWidget } from "@/components/turnstile-widget";
import { type DashboardPath } from "@/lib/auth";
import { env } from "@/lib/env";

type LoginFormState = {
  institutionSlug: string;
  email: string;
  password: string;
};

type DemoAccount = LoginFormState & {
  label: string;
  accent: string;
};

const demoAccounts: readonly DemoAccount[] = [
  {
    label: "Admin",
    accent: "Policy + Analytics",
    institutionSlug: "prepareme-demo",
    email: "admin@prepareme.local",
    password: "Admin@123"
  },
  {
    label: "Teacher",
    accent: "Review + Publish",
    institutionSlug: "prepareme-demo",
    email: "teacher@prepareme.local",
    password: "Teacher@123"
  },
  {
    label: "Student",
    accent: "Revision + Mastery",
    institutionSlug: "prepareme-demo",
    email: "student@prepareme.local",
    password: "Student@123"
  }
];

const initialState: LoginFormState = {
  institutionSlug: "prepareme-demo",
  email: "teacher@prepareme.local",
  password: "Teacher@123"
};

const fieldClassName =
  "w-full rounded-[22px] border border-white/10 bg-white/[0.04] px-4 py-3.5 text-sm text-white outline-none transition placeholder:text-white/28 focus:border-[#72e1ff] focus:bg-white/[0.07]";

export function LoginForm(): JSX.Element {
  const router = useRouter();
  const [form, setForm] = useState<LoginFormState>(initialState);
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const [turnstileResetSignal, setTurnstileResetSignal] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const selectedDemoAccount =
    demoAccounts.find(
      (account) =>
        account.institutionSlug === form.institutionSlug &&
        account.email === form.email &&
        account.password === form.password
    ) ?? null;

  function applyDemoAccount(account: DemoAccount): void {
    setForm({
      institutionSlug: account.institutionSlug,
      email: account.email,
      password: account.password
    });
    setError(null);
    setTurnstileToken(null);
    setTurnstileResetSignal((value) => value + 1);
  }

  async function onSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();

    if (env.turnstileEnabled && turnstileToken === null) {
      setError("Complete the Cloudflare security check before entering the workspace.");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...form,
          turnstileToken
        })
      });

      const payload = (await response.json()) as {
        detail?: string;
        redirectPath?: DashboardPath;
      };

      if (!response.ok) {
        setError(payload.detail ?? "Unable to sign in. Please verify your details and try again.");
        setIsSubmitting(false);
        setTurnstileToken(null);
        setTurnstileResetSignal((value) => value + 1);
        return;
      }

      startTransition(() => {
        router.push(payload.redirectPath ?? "/");
        router.refresh();
      });
    } catch {
      setError("Login service is unreachable. Start the backend and try again.");
      setIsSubmitting(false);
      setTurnstileToken(null);
      setTurnstileResetSignal((value) => value + 1);
    }
  }

  const isSubmitDisabled = isSubmitting || (env.turnstileEnabled && turnstileToken === null);

  return (
    <form className="space-y-6" onSubmit={onSubmit}>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <p className="font-mono text-[11px] uppercase tracking-[0.28em] text-white/48">
            Quick Fill Access
          </p>
          {selectedDemoAccount ? (
            <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-[#7bf1a8]">
              {selectedDemoAccount.accent}
            </p>
          ) : null}
        </div>
        <div className="grid gap-2 sm:grid-cols-3">
          {demoAccounts.map((account) => {
            const isSelected = selectedDemoAccount?.label === account.label;
            return (
              <button
                key={account.label}
                className={[
                  "rounded-[22px] border px-4 py-3 text-left transition",
                  isSelected
                    ? "border-[#72e1ff] bg-[#0b1828] shadow-[0_0_0_1px_rgba(114,225,255,0.18)]"
                    : "border-white/8 bg-white/[0.03] hover:border-white/18 hover:bg-white/[0.06]"
                ].join(" ")}
                onClick={() => applyDemoAccount(account)}
                type="button"
              >
                <p className="text-sm font-semibold text-white">{account.label}</p>
                <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.2em] text-white/42">
                  {account.accent}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2 sm:col-span-2">
          <label className="font-mono text-[11px] uppercase tracking-[0.28em] text-white/48" htmlFor="institutionSlug">
            Institution Code
          </label>
          <input
            className={fieldClassName}
            id="institutionSlug"
            name="institutionSlug"
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                institutionSlug: event.target.value
              }))
            }
            placeholder="prepareme-demo"
            value={form.institutionSlug}
          />
        </div>

        <div className="space-y-2 sm:col-span-2">
          <label className="font-mono text-[11px] uppercase tracking-[0.28em] text-white/48" htmlFor="email">
            Account Email
          </label>
          <input
            className={fieldClassName}
            id="email"
            name="email"
            onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
            placeholder="teacher@prepareme.local"
            type="email"
            value={form.email}
          />
        </div>

        <div className="space-y-2 sm:col-span-2">
          <label className="font-mono text-[11px] uppercase tracking-[0.28em] text-white/48" htmlFor="password">
            Password
          </label>
          <input
            className={fieldClassName}
            id="password"
            name="password"
            onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))}
            placeholder="Enter your password"
            type="password"
            value={form.password}
          />
        </div>
      </div>

      <div className="space-y-3 rounded-[28px] border border-white/10 bg-white/[0.03] p-4">
        <div className="flex items-center justify-between">
          <p className="font-mono text-[11px] uppercase tracking-[0.28em] text-white/48">
            Security Layer
          </p>
          <p className="rounded-full border border-[#7bf1a8]/18 bg-[#7bf1a8]/8 px-3 py-1 font-mono text-[10px] uppercase tracking-[0.22em] text-[#7bf1a8]">
            Cloudflare Turnstile
          </p>
        </div>

        {env.turnstileEnabled ? (
          <TurnstileWidget
            onTokenChange={setTurnstileToken}
            resetSignal={turnstileResetSignal}
            siteKey={env.turnstileSiteKey}
          />
        ) : (
          <div className="rounded-[22px] border border-dashed border-white/12 bg-black/20 px-4 py-5">
            <p className="font-mono text-[11px] uppercase tracking-[0.22em] text-white/44">
              Security challenge is disabled in this environment.
            </p>
          </div>
        )}
      </div>

      {error ? (
        <div className="rounded-[24px] border border-[#ff6b6b]/25 bg-[#251114] px-4 py-4">
          <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-[#ff8f8f]">
            Sign-in failed
          </p>
          <p className="mt-2 text-sm leading-6 text-[#ffd2d2]">{error}</p>
        </div>
      ) : null}

      <button
        className="w-full rounded-full bg-[linear-gradient(135deg,#72e1ff_0%,#7bf1a8_100%)] px-6 py-3.5 text-sm font-semibold text-[#061018] transition hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={isSubmitDisabled}
        type="submit"
      >
        {isSubmitting
          ? "Securing session..."
          : env.turnstileEnabled && turnstileToken === null
            ? "Complete security check"
            : "Enter workspace"}
      </button>

      <div className="grid gap-3 rounded-[28px] border border-white/8 bg-black/20 p-4 sm:grid-cols-3">
        {[
          {
            label: "Routing",
            copy: "Teacher, student, and admin sessions land in different operational surfaces."
          },
          {
            label: "Grounding",
            copy: "This sign-in surface is for the platform that only serves approved institutional context."
          },
          {
            label: "Local Demo",
            copy: "Preset accounts are preloaded for development so you can move fast without fake boilerplate."
          }
        ].map((item) => (
          <div key={item.label}>
            <p className="font-mono text-[11px] uppercase tracking-[0.22em] text-white/42">
              {item.label}
            </p>
            <p className="mt-2 text-sm leading-6 text-white/62">{item.copy}</p>
          </div>
        ))}
      </div>
    </form>
  );
}
