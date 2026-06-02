"""Regenerate clean 1200x630 hero/OG images for every blog post.

Uses cowork.og_card (Pillow-only, no AI backends -> no gibberish text).
Always overwrites existing images; idempotent and safe to re-run after any
title change. Also updates each post's `image:` frontmatter to match the
canonical filename.
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).parent
ROOT = SITE.parent.parent  # repo root
sys.path.insert(0, str(ROOT))

from cowork.og_card import render_hero_card  # noqa: E402

BLOG = SITE / "src" / "pages" / "blog"
OUT = SITE / "public" / "og"


def _slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:80]


def _field(fm: str, key: str) -> str:
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _slug_for_post(p: Path, title: str) -> str:
    """Match the slug publisher.py would write for a fresh post: title-slug
    (no date prefix). Falls back to the .md stem minus the date prefix."""
    if title:
        return _slugify(title)
    stem = p.stem  # 2026-MM-DD-<slug>
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    posts = sorted(BLOG.glob("*.md"))

    for p in posts:
        text = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            print("skip (no frontmatter):", p.name)
            continue

        fm = m.group(1)
        title = _field(fm, "title")
        if not title:
            print("skip (no title):", p.name)
            continue

        slug = _slug_for_post(p, title)
        out_path = OUT / f"{slug}.png"
        render_hero_card(title, out_path)
        print(f"{p.name[:60]:60s} -> og/{slug}.png")

        # Ensure frontmatter image: is canonical.
        want = f'image: "/og/{slug}.png"'
        if re.search(r"^image:\s*\S", fm, re.MULTILINE):
            new_fm = re.sub(r"^image:.*$", want, fm, count=1, flags=re.MULTILINE)
        else:
            new_fm = fm + "\n" + want
        if new_fm != fm:
            text = text.replace(m.group(0), f"---\n{new_fm}\n---\n", 1)
            p.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
