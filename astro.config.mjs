import { defineConfig } from 'astro/config';

// gpt6-astra-3d.pages.dev is the default subdomain assigned by Cloudflare Pages
// for the project name "gpt6-astra-3d". Update it here after binding a custom
// domain so canonical/OG links stay correct.
export default defineConfig({
  site: 'https://gpt6-astra-3d.pages.dev',
});
