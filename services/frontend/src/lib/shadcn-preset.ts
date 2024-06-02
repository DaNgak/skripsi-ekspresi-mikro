import type { Config } from 'tailwindcss';
import { shadcnPlugin } from './shadcn-plugin';

export const shadcnPreset = {
    content: [],
    plugins: [shadcnPlugin],
} satisfies Config;
