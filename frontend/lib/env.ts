export const env = {
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000",
  turnstileEnabled: (process.env.NEXT_PUBLIC_TURNSTILE_ENABLED ?? "true") !== "false",
  turnstileSiteKey:
    process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY ?? "1x00000000000000000000AA"
} as const;

