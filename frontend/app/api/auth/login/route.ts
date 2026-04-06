import { NextResponse } from "next/server";

import { env } from "@/lib/env";

type FrontendLoginRequest = {
  institutionSlug: string;
  email: string;
  password: string;
  turnstileToken?: string | null;
};

type BackendLoginResponse = {
  access_token: string;
  redirect_path: string;
};

export async function POST(request: Request): Promise<NextResponse> {
  const payload = (await request.json()) as FrontendLoginRequest;
  const forwardedFor =
    request.headers.get("cf-connecting-ip") ?? request.headers.get("x-forwarded-for");

  let response: Response;
  try {
    response = await fetch(`${env.apiBaseUrl}/v1/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(forwardedFor ? { "X-Forwarded-For": forwardedFor } : {})
      },
      body: JSON.stringify({
        institution_slug: payload.institutionSlug,
        email: payload.email,
        password: payload.password,
        turnstile_token: payload.turnstileToken ?? null
      }),
      cache: "no-store"
    });
  } catch {
    return NextResponse.json(
      {
        detail: "PrepareMe auth service is unreachable. Start the backend on http://localhost:8000."
      },
      { status: 503 }
    );
  }

  let data: (BackendLoginResponse & { detail?: string }) | null = null;
  try {
    data = (await response.json()) as BackendLoginResponse & { detail?: string };
  } catch {
    data = null;
  }

  if (!response.ok) {
    return NextResponse.json({ detail: data?.detail ?? "Unable to sign in." }, { status: response.status });
  }
  if (data === null) {
    return NextResponse.json(
      { detail: "PrepareMe auth service returned an invalid response." },
      { status: 502 }
    );
  }

  const nextResponse = NextResponse.json({
    redirectPath: data.redirect_path
  });
  nextResponse.cookies.set({
    name: "prepareme_access_token",
    value: data.access_token,
    httpOnly: true,
    sameSite: "lax",
    secure: false,
    path: "/",
    maxAge: 60 * 60
  });
  return nextResponse;
}
