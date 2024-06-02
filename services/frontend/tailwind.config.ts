import type { Config } from 'tailwindcss';
import { shadcnPreset } from './src/lib/shadcn-preset';
import tailwindcssAnimate from 'tailwindcss-animate';

const config = {
    darkMode: 'class',
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    presets: [shadcnPreset],
    plugins: [tailwindcssAnimate],
} satisfies Config;

export default config;
