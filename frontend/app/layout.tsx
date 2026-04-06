import type { Metadata, Viewport } from "next";
import { IBM_Plex_Mono, Space_Grotesk, Syne } from "next/font/google";

import { Providers } from "@/app/providers";

import "./globals.css";

const sans = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-sans"
});

const display = Syne({
  subsets: ["latin"],
  variable: "--font-display"
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500", "600"]
});

export const metadata: Metadata = {
  title: "PrepareMe",
  description: "Curriculum-aware institutional AI learning operating system"
};

export const viewport: Viewport = {
  themeColor: "#040814"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>): JSX.Element {
  return (
    <html lang="en" className={`${sans.variable} ${display.variable} ${mono.variable}`}>
      <body className="font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

