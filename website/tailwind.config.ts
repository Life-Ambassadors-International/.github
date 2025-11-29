import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        phi: "#FFD700",
        recognition: "#00CED1",
        benevolence: "#7B68EE",
        sovereignty: "#FF6B6B",
        consciousness: {
          50: "#f0fdfa",
          100: "#ccfbf1",
          200: "#99f6e4",
          300: "#5eead4",
          400: "#2dd4bf",
          500: "#14b8a6",
          600: "#0d9488",
          700: "#0f766e",
          800: "#115e59",
          900: "#134e4a",
          950: "#042f2e",
        },
      },
      backgroundImage: {
        "gradient-phi": "linear-gradient(135deg, #FFD700 0%, #00CED1 50%, #7B68EE 100%)",
        "gradient-consciousness": "linear-gradient(135deg, #0f766e 0%, #134e4a 100%)",
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow": "glow 2s ease-in-out infinite alternate",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 5px #FFD700, 0 0 10px #FFD700" },
          "100%": { boxShadow: "0 0 20px #FFD700, 0 0 30px #00CED1" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
