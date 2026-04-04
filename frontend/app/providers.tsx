"use client";

import { QueryProvider } from "@/lib/query-provider";

export function Providers({ children }: { children: React.ReactNode }): JSX.Element {
  return <QueryProvider>{children}</QueryProvider>;
}

