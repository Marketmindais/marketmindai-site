import rss from '@astrojs/rss';

export async function GET(context) {
  const posts = import.meta.glob('./blog/*.md', { eager: true });
  const items = Object.values(posts)
    .sort((a, b) => new Date(b.frontmatter.date) - new Date(a.frontmatter.date))
    .map(post => ({
      title: post.frontmatter.title,
      pubDate: post.frontmatter.date,
      description: post.frontmatter.description,
      link: post.url,
    }));

  return rss({
    title: 'MarketMindAI Blog',
    description: 'AI marketing tips, SEO guides, and growth strategies.',
    site: context.site,
    items,
  });
}
