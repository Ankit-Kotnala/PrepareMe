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
      colors: {
        ink: "#101319",
        paper: "#f5f0e8",
        ember: "#d97706",
        sage: "#365446",
        mist: "#dfe7df"
      },
      boxShadow: {
        panel: "0 20px 50px rgba(16, 19, 25, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;

