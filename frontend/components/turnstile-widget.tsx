"use client";

import { useEffect, useRef, useState } from "react";
import Script from "next/script";

type TurnstileTheme = "auto" | "dark" | "light";
type TurnstileSize = "compact" | "flexible" | "normal";
type TurnstileAppearance = "always" | "execute" | "interaction-only";

type TurnstileRenderOptions = {
  sitekey: string;
  theme?: TurnstileTheme;
  size?: TurnstileSize;
  appearance?: TurnstileAppearance;
  callback?: (token: string) => void;
  "expired-callback"?: () => void;
  "error-callback"?: () => void;
};

type TurnstileApi = {
  render: (container: HTMLElement, options: TurnstileRenderOptions) => string;
  remove: (widgetId: string) => void;
  reset: (widgetId: string) => void;
};

declare global {
  interface Window {
    turnstile?: TurnstileApi;
  }
}

export function TurnstileWidget({
  siteKey,
  resetSignal,
  onTokenChange
}: {
  siteKey: string;
  resetSignal: number;
  onTokenChange: (token: string | null) => void;
}): JSX.Element {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const widgetIdRef = useRef<string | null>(null);
  const [scriptReady, setScriptReady] = useState(false);
  const [statusMessage, setStatusMessage] = useState("Preparing Cloudflare security check...");

  useEffect(() => {
    if (typeof window !== "undefined" && window.turnstile) {
      setScriptReady(true);
    }
  }, []);

  useEffect(() => {
    if (!scriptReady || containerRef.current === null || widgetIdRef.current !== null) {
      return;
    }
    if (typeof window === "undefined" || window.turnstile === undefined) {
      return;
    }

    widgetIdRef.current = window.turnstile.render(containerRef.current, {
      sitekey: siteKey,
      theme: "dark",
      size: "flexible",
      appearance: "always",
      callback: (token: string) => {
        setStatusMessage("Security check complete. You can continue.");
        onTokenChange(token);
      },
      "expired-callback": () => {
        setStatusMessage("Security check expired. Please complete it again.");
        onTokenChange(null);
      },
      "error-callback": () => {
        setStatusMessage("Cloudflare security check failed to load. Refresh and try again.");
        onTokenChange(null);
      }
    });

    return () => {
      if (widgetIdRef.current !== null && window.turnstile !== undefined) {
        window.turnstile.remove(widgetIdRef.current);
        widgetIdRef.current = null;
      }
    };
  }, [onTokenChange, scriptReady, siteKey]);

  useEffect(() => {
    if (resetSignal === 0 || widgetIdRef.current === null) {
      return;
    }
    if (typeof window === "undefined" || window.turnstile === undefined) {
      return;
    }

    window.turnstile.reset(widgetIdRef.current);
    setStatusMessage("Security check reset. Please verify again.");
    onTokenChange(null);
  }, [onTokenChange, resetSignal]);

  return (
    <div className="rounded-[26px] border border-white/10 bg-black/25 p-4">
      <Script
        onReady={() => setScriptReady(true)}
        src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"
        strategy="afterInteractive"
      />
      <div
        className="min-h-[74px] rounded-2xl border border-white/6 bg-[#060d18]/90 p-3"
        ref={containerRef}
      />
      <p className="mt-3 font-mono text-[11px] uppercase tracking-[0.22em] text-[#9aa9c7]">
        {statusMessage}
      </p>
    </div>
  );
}
