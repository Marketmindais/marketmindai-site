import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://marketmindai.com",
  integrations: [
    tailwind(),
    sitemap({
      // Skip non-public routes if they ever appear; index only blog + product pages.
      filter: (page) =>
        !page.includes("/admin") &&
        !page.includes("/draft") &&
        !page.includes("/_"),
      changefreq: "weekly",
      priority: 0.7,
      lastmod: new Date(),
    }),
  ],
  output: "static",
});
