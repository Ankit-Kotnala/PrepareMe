import type { Route } from "next";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { env } from "@/lib/env";

export type AppRole =
  | "student"
  | "teacher"
  | "course_admin"
  | "institution_admin"
  | "platform_admin";

export type UserSession = {
  accessToken: string;
  userId: string;
  institutionId: string;
  institutionName: string | null;
  institutionSlug: string | null;
  role: AppRole;
  email: string | null;
  displayName: string | null;
};

export type DashboardPath = Route<"/teacher" | "/student" | "/admin">;

const ACCESS_TOKEN_COOKIE = "prepareme_access_token";

type BackendMeResponse = {
  user_id: string;
  institution_id: string;
  institution_name?: string | null;
  institution_slug?: string | null;
  role: AppRole;
  email?: string | null;
  display_name?: string | null;
};

export function dashboardPathForRole(role: AppRole): DashboardPath {
  if (role === "student") {
    return "/student";
  }
  if (role === "institution_admin" || role === "platform_admin") {
    return "/admin";
  }
  return "/teacher";
}

export async function getServerSession(): Promise<UserSession | null> {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get(ACCESS_TOKEN_COOKIE)?.value;

  if (!accessToken) {
    return null;
  }

  const response = await fetch(`${env.apiBaseUrl}/v1/auth/me`, {
    headers: {
      Authorization: `Bearer ${accessToken}`
    },
    cache: "no-store"
  });

  if (!response.ok) {
    return null;
  }

  const payload = (await response.json()) as BackendMeResponse;
  return {
    accessToken,
    userId: payload.user_id,
    institutionId: payload.institution_id,
    institutionName: payload.institution_name ?? null,
    institutionSlug: payload.institution_slug ?? null,
    role: payload.role,
    email: payload.email ?? null,
    displayName: payload.display_name ?? null
  };
}

export async function requireServerSession(
  allowedRoles?: readonly AppRole[]
): Promise<UserSession> {
  const session = await getServerSession();
  if (!session) {
    redirect("/");
  }

  if (allowedRoles && !allowedRoles.includes(session.role)) {
    redirect(dashboardPathForRole(session.role));
  }

  return session;
}
