// Author registry — drives bylines, author bio boxes, and Person JSON-LD.
// Add new authors here; reference by key from a post's `author` frontmatter.
// Default author is used when frontmatter omits `author`.

export const SITE_URL = "https://marketmindai.com";

export const authors = {
  "amit-singh": {
    key: "amit-singh",
    name: "Amit Singh",
    jobTitle: "Founder & Lead Analyst",
    // First-hand experience is the core E-E-A-T signal Google weighs.
    bio:
      "Amit founded MarketMindAI after a decade building marketing and automation " +
      "systems for B2B companies. He personally runs every tool through real " +
      "production workloads — live calls, multi-week trials, and billed usage — " +
      "before it earns a recommendation here.",
    shortBio: "Founder of MarketMindAI. Tests every AI tool in production before recommending it.",
    url: SITE_URL + "/about",
    image: SITE_URL + "/icon-512.png",
    sameAs: [
      "https://twitter.com/marketmindai",
      "https://linkedin.com/company/marketmindai",
    ],
    knowsAbout: [
      "AI voice agents", "no-code AI automation", "CRM automation",
      "sales funnels", "marketing technology", "SaaS evaluation",
    ],
  },
};

export const DEFAULT_AUTHOR = "amit-singh";

export function getAuthor(key) {
  return authors[key] || authors[DEFAULT_AUTHOR];
}
