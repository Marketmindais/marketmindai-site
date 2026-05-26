import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";

// NOTE: @astrojs/sitemap @ 3.x has a 'pages.reduce of undefined' bug at the
// astro:build:done hook on Astro 4 + output:'static'. We bypass it entirely
// by generating sitemap.xml as a regular static file in public/ via
// cowork/sitemap_gen.py (called after every content publish). Cloudflare
// then serves it as a normal /sitemap.xml at the standard URL.
export default defineConfig({
  site: "https://marketmindai.com",
  integrations: [tailwind()],
  output: "static",
});
