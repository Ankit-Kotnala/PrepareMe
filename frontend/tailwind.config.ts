import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./features/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        serif: ["var(--font-display)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"]
      },
      colors: {
        ink: "#101319",
        paper: "#f5f0e8",
        ember: "#d97706",
        sage: "#365446",
        mist: "#dfe7df",
        midnight: "#040814",
        panel: "#08111d",
        cyan: "#72e1ff",
        aurora: "#7bf1a8",
        steel: "#95a4c6"
      },
      boxShadow: {
        panel: "0 20px 50px rgba(16, 19, 25, 0.08)",
        neon: "0 0 0 1px rgba(114, 225, 255, 0.14), 0 20px 80px rgba(6, 17, 29, 0.42)"
      }
    }
  },
  plugins: []
};

export default config;

