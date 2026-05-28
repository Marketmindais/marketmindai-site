"""Generate a 1200x630 hero/OG image per blog post via cowork.image_studio,
write to public/og/<slug>.png, and inject `image:` into the post frontmatter.
Idempotent: skips posts that already have an `image:` field. Re-run anytime.
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).parent
ROOT = SITE.parent.parent  # repo root (has cowork/)
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from cowork.image_studio import generate_image  # noqa: E402

BLOG = SITE / "src" / "pages" / "blog"
OUT = SITE / "public" / "og"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630


def field(fm: str, key: str) -> str:
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm, re.MULTILINE)
    return m.group(1).strip() if m else ""


def main():
    posts = sorted(BLOG.glob("*.md"))
    for p in posts:
        text = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            print("skip (no frontmatter):", p.name)
            continue
        fm = m.group(1)
        if re.search(r"^image:\s*\S", fm, re.MULTILINE):
            print("skip (has image):", p.name)
            continue

        slug = p.stem
        title = field(fm, "title") or slug
        product = field(fm, "affiliate_name")
        out_path = OUT / f"{slug}.png"

        subject = product or "AI tools for business"
        prompt = (
            f"{title}. "
            f"Professional editorial hero illustration about {subject}, "
            f"modern clean tech aesthetic, indigo and violet color scheme, "
            f"abstract AI and automation theme, soft gradient, high quality, no text."
        )
        req = generate_image(prompt, out_path, width=W, height=H, style="card")
        print(f"{p.name}: {req.backend_used} {req.bytes_written}B -> og/{slug}.png")

        # Inject image field into frontmatter (after title line for tidiness)
        new_fm = fm + f'\nimage: "/og/{slug}.png"'
        text = text.replace(m.group(0), f"---\n{new_fm}\n---\n", 1)
        p.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
