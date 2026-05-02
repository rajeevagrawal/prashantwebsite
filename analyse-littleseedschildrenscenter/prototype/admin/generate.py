#!/usr/bin/env python3
"""
Static site generator for Little Seeds & Peter Pan Schools prototype.

Usage:
    python3 generate.py

Reads content/*.csv and templates/*.html, writes output HTML files
to the prototype root directory.

Text tokens:    {{key}}
Image tokens:   {{IMAGE:csv_key:fallback_emoji:bg_css_var}}
  - If content/images/<value> exists  → <img src="content/images/<value>" ...>
  - Otherwise                         → emoji placeholder div
"""

import csv
import re
import sys
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent  # prototype/
CONTENT_DIR = BASE_DIR / "content"
IMAGES_DIR = CONTENT_DIR / "images"
TEMPLATES_DIR = BASE_DIR / "templates"
BLOG_DIR = CONTENT_DIR / "blog"
BLOG_OUT_DIR = BASE_DIR / "blog"

PAGES = [
    ("index.html",                          "home.csv"),
    ("about.html",                          "about.csv"),
    ("little-seeds-childrens-center.html",  "little-seeds-childrens-center.csv"),
    ("peter-pan-academy.html",              "peter-pan-academy.csv"),
    ("peter-pan-preschool.html",            "peter-pan-preschool.csv"),
    ("curriculum.html",                     "curriculum.csv"),
    ("blog.html",                           "blog.csv"),
    ("contact.html",                        "contact.csv"),
    ("forms.html",                          "forms.csv"),
    ("gallery.html",                        "gallery.csv"),
]

LOCATION_SOURCES = [
    ("location_1", "little-seeds-childrens-center.csv", "little-seeds-childrens-center.html"),
    ("location_2", "peter-pan-academy.csv",             "peter-pan-academy.html"),
    ("location_3", "peter-pan-preschool.csv",           "peter-pan-preschool.html"),
]

LOCATION_KEY_MAP = {
    "hero_title":       "name",
    "hero_address":     "address",
    "hero_ages":        "ages",
    "hero_hours":       "hours",
    "hero_status":      "status",
    "hero_status_type": "status_type",
    "hero_image":       "image",
}


def load_csv(path: Path) -> dict:
    data = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["key"].strip()] = row["value"]
    return data


def resolve_image_token(match: re.Match, data: dict) -> str:
    csv_key = match.group(1).strip()
    fallback_emoji = match.group(2).strip()
    bg_var = match.group(3).strip()
    filename = data.get(csv_key, "").strip()
    if filename:
        img_path = IMAGES_DIR / filename
        if img_path.exists():
            src = f"content/images/{filename}"
            return (
                f'<img src="{src}" alt="{csv_key.replace("_", " ")}" '
                f'style="width:100%;height:100%;object-fit:cover;border-radius:inherit;">'
            )
    return (
        f'<div class="img-placeholder" style="background:var({bg_var},#FFF1E4);">'
        f'{fallback_emoji}</div>'
    )


def render(template: str, data: dict) -> str:
    image_pattern = re.compile(r"\{\{IMAGE:([^:}]+):([^:}]+):([^}]+)\}\}")
    result = image_pattern.sub(lambda m: resolve_image_token(m, data), template)
    for key in sorted(data.keys(), key=len, reverse=True):
        result = result.replace("{{" + key + "}}", data[key])
    remaining = re.findall(r"\{\{[^}]+\}\}", result)
    if remaining:
        unique = sorted(set(remaining))
        print(f"  WARNING: unresolved tokens: {', '.join(unique)}", file=sys.stderr)
    return result


def parse_md(path: Path) -> tuple[dict, str]:
    """Parse a markdown file. Returns (frontmatter_dict, body_text)."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.S)
    if not m:
        return {}, text
    data = {}
    for line in m.group(1).splitlines():
        kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if kv:
            data[kv.group(1)] = kv.group(2)
    return data, m.group(2).strip()


def md_body_to_html(md: str) -> tuple[str, str, str]:
    """Convert markdown body to HTML.

    Returns (html, author, read_time).
    Strips the leading h1 (shown in page-hero) and any immediately following
    metadata list (author name / read time bullets).
    Also strips Wix-specific noise like 'Rated NaN out of 5 stars.'
    """
    lines = md.splitlines()
    author = ""
    read_time = "5 min read"

    # --- Phase 1: strip preamble (h1 + metadata list) ---
    body_start = 0
    skip_meta = True
    for idx, line in enumerate(lines):
        s = line.strip()
        if not skip_meta:
            body_start = idx
            break
        if s == "":
            # A blank line after we've captured some metadata ends the preamble
            if author or read_time != "5 min read":
                skip_meta = False
            continue
        if s.startswith("# "):
            continue  # drop the post-title h1
        if re.match(r"^[-*] ", s):
            item = s[2:].strip()
            if re.search(r"\d+\s*min\s*read", item, re.I):
                read_time = item
            elif item and not author:
                author = item.title()
            continue
        # Any other non-empty line → body starts here
        skip_meta = False
        body_start = idx
        break
    else:
        body_start = len(lines)

    # --- Phase 2: convert remaining lines to HTML ---
    html_parts = []
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

    for line in lines[body_start:]:
        s = line.strip()
        if s.startswith("#### "):
            close_ul()
            html_parts.append(f"<h4>{s[5:]}</h4>")
        elif s.startswith("### "):
            close_ul()
            html_parts.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("## "):
            close_ul()
            html_parts.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("# "):
            close_ul()
            html_parts.append(f"<h1>{s[2:]}</h1>")
        elif re.match(r"^[-*] ", s):
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{s[2:]}</li>")
        elif s == "":
            close_ul()
        else:
            close_ul()
            # Strip Wix noise prefix ("Rated NaN out of 5 stars.")
            clean = re.sub(r"^Rated [^.]+\.\s*", "", s).strip()
            if clean:
                html_parts.append(f"<p>{clean}</p>")

    close_ul()
    return "\n".join(html_parts), author, read_time


def parse_md_frontmatter(path: Path) -> dict:
    fm, _ = parse_md(path)
    return fm


def slug_to_local_url(md_filename: str) -> str:
    return f"blog/{Path(md_filename).stem}.html"


def build_blog_data(page_data: dict) -> dict:
    result = {}

    def inject(prefix: str, md_file: str):
        path = BLOG_DIR / md_file
        if not path.exists():
            print(f"  WARNING: blog md not found: {md_file}", file=sys.stderr)
            return
        fm = parse_md_frontmatter(path)
        for field in ("title", "date", "category", "category_class", "excerpt", "emoji", "bg"):
            if field in fm:
                result[f"{prefix}_{field}"] = fm[field]
        result[f"{prefix}_url"] = slug_to_local_url(md_file)
        date = fm.get("date", "")
        result[f"{prefix}_meta"] = f"{date} · 5 min read" if date else "5 min read"

    if "featured_post" in page_data:
        inject("featured", page_data["featured_post"])
    i = 1
    while f"post_{i}" in page_data:
        inject(f"post_{i}", page_data[f"post_{i}"])
        i += 1

    return result


def build_location_data() -> dict:
    data = {}
    for prefix, csv_name, output_html in LOCATION_SOURCES:
        school_data = load_csv(CONTENT_DIR / csv_name)
        for school_key, card_suffix in LOCATION_KEY_MAP.items():
            if school_key in school_data:
                data[f"{prefix}_{card_suffix}"] = school_data[school_key]
        data[f"{prefix}_url"] = output_html
    return data


def load_ordered_posts() -> list[dict]:
    """Return post metadata in blog.csv order for Recent Posts sections."""
    blog_csv = CONTENT_DIR / "blog.csv"
    if not blog_csv.exists():
        return []
    page_data = load_csv(blog_csv)
    ordered = []
    keys = ["featured_post"] + [f"post_{i}" for i in range(1, 100)]
    for key in keys:
        if key not in page_data:
            break
        md_file = page_data[key]
        md_path = BLOG_DIR / md_file
        if not md_path.exists():
            continue
        fm = parse_md_frontmatter(md_path)
        ordered.append({
            "slug":           md_path.stem,
            "title":          fm.get("title", md_path.stem),
            "category":       fm.get("category", ""),
            "category_class": fm.get("category_class", ""),
            "emoji":          fm.get("emoji", "📝"),
            "bg":             fm.get("bg", "--color-primary-light"),
            "date":           fm.get("date", ""),
            "local_url":      f"{md_path.stem}.html",  # relative within blog/
        })
    return ordered


def generate_blog_posts(global_data: dict):
    template_path = TEMPLATES_DIR / "blog-post.html"
    if not template_path.exists():
        print("  SKIP  blog posts — template blog-post.html not found", file=sys.stderr)
        return

    template_text = template_path.read_text(encoding="utf-8")
    BLOG_OUT_DIR.mkdir(exist_ok=True)

    ordered_posts = load_ordered_posts()
    default_author = global_data.get("blog_default_author", "Little Seeds Team")

    md_files = sorted(BLOG_DIR.glob("*.md"))
    count = 0
    for md_path in md_files:
        fm, body = parse_md(md_path)
        post_html, author, read_time = md_body_to_html(body)

        # 3 recent posts (first from ordered list that aren't this post)
        current_slug = md_path.stem
        recent = [p for p in ordered_posts if p["slug"] != current_slug][:3]
        recent_data = {}
        for i, p in enumerate(recent, 1):
            recent_data[f"recent_{i}_title"]          = p["title"]
            recent_data[f"recent_{i}_url"]            = p["local_url"]
            recent_data[f"recent_{i}_category"]       = p["category"]
            recent_data[f"recent_{i}_category_class"] = p["category_class"]
            recent_data[f"recent_{i}_emoji"]          = p["emoji"]
            recent_data[f"recent_{i}_bg"]             = p["bg"]
            recent_data[f"recent_{i}_date"]           = p["date"]

        date = fm.get("date", "")
        post_author = author or default_author
        # Resolve author avatar: pick image by author name, fallback to default, else initial
        author_image_map = {
            "alpana wadhwa":   global_data.get("blog_default_author_image", ""),
            "prashant wadhwa": "author-prashant.jpg",
        }
        author_img_file = author_image_map.get(post_author.lower(), global_data.get("blog_default_author_image", ""))
        if author_img_file and (IMAGES_DIR / author_img_file).exists():
            author_avatar_html = (
                f'<img src="../content/images/{author_img_file}" '
                f'alt="{post_author}" '
                f'style="width:100%;height:100%;object-fit:cover;border-radius:50%;">'
            )
        else:
            author_avatar_html = post_author[0].upper() if post_author else "A"

        data = {
            **global_data,
            **recent_data,
            "post_title":          fm.get("title", md_path.stem),
            "post_category":       fm.get("category", ""),
            "post_category_class": fm.get("category_class", ""),
            "post_date":           date,
            "post_meta":           f"{date} · {read_time}",
            "post_excerpt":        fm.get("excerpt", ""),
            "post_emoji":          fm.get("emoji", "📝"),
            "post_author":         post_author,
            "post_author_avatar":  author_avatar_html,
            "post_body":           post_html,
            "post_slug":           current_slug,
            "post_share_url":      f"https://littleseedschildrenscenter.com/blog/{current_slug}.html",
        }

        output_path = BLOG_OUT_DIR / f"{md_path.stem}.html"
        output_text = render(template_text, data)
        output_path.write_text(output_text, encoding="utf-8")
        count += 1

    print(f"  OK    blog posts ({count} pages → blog/)")


def generate():
    global_data = load_csv(CONTENT_DIR / "global.csv")
    location_data = build_location_data()

    generated = []
    for output_name, csv_name in PAGES:
        page_csv = CONTENT_DIR / csv_name
        template_path = TEMPLATES_DIR / output_name
        output_path = BASE_DIR / output_name

        if not template_path.exists():
            print(f"  SKIP  {output_name} — template not found", file=sys.stderr)
            continue
        if not page_csv.exists():
            print(f"  SKIP  {output_name} — CSV not found", file=sys.stderr)
            continue

        page_data = load_csv(page_csv)
        if csv_name == "blog.csv":
            blog_data = build_blog_data(page_data)
        elif output_name == "index.html":
            # Homepage blog preview pulls live post data (titles, URLs) from blog.csv
            blog_index_data = load_csv(CONTENT_DIR / "blog.csv")
            blog_data = build_blog_data(blog_index_data)
        else:
            blog_data = {}
        merged = {**global_data, **location_data, **blog_data, **page_data}

        template_text = template_path.read_text(encoding="utf-8")
        output_text = render(template_text, merged)
        output_path.write_text(output_text, encoding="utf-8")

        generated.append(output_name)
        print(f"  OK    {output_name}")

    generate_blog_posts(global_data)
    print(f"\nGenerated {len(generated)} page(s): {', '.join(generated)}")


if __name__ == "__main__":
    generate()
