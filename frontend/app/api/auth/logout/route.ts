import { NextResponse } from "next/server";

export async function POST(request: Request): Promise<NextResponse> {
  const response = NextResponse.redirect(new URL("/", request.url));
  response.cookies.set({
    name: "prepareme_access_token",
    value: "",
    httpOnly: true,
    sameSite: "lax",
    secure: false,
    path: "/",
    maxAge: 0
  });
  return response;
}

