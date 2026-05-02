"""
Crawls peterpanschools.com, takes full-page screenshots of every unique page,
and assembles them into a single PDF.
"""

import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

BASE_URL  = "https://www.peterpanschools.com"
OUT_DIR   = Path(__file__).parent
IMG_DIR   = OUT_DIR / "screenshots"
PDF_OUT   = OUT_DIR / "peterpanschools_all_pages.pdf"

IMG_DIR.mkdir(exist_ok=True)

def same_origin(url):
    p = urlparse(url)
    b = urlparse(BASE_URL)
    return p.netloc == b.netloc or p.netloc == ""

def normalise(url):
    u = urlparse(url)
    return u._replace(fragment="", query="").geturl().rstrip("/")

def collect_links(page, url):
    """Return all same-origin href links found on the current page."""
    links = page.eval_on_selector_all(
        "a[href]",
        "els => els.map(e => e.href)"
    )
    found = set()
    for href in links:
        abs_href = urljoin(url, href)
        if same_origin(abs_href):
            norm = normalise(abs_href)
            if norm.startswith(BASE_URL):
                found.add(norm)
    return found

def slug(url):
    path = urlparse(url).path.strip("/").replace("/", "_") or "home"
    return re.sub(r"[^a-zA-Z0-9_-]", "-", path)[:80]

def run():
    visited   = set()
    to_visit  = {normalise(BASE_URL)}
    screenshots = []   # ordered list of image paths

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page(viewport={"width": 1440, "height": 900})

        while to_visit:
            url = to_visit.pop()
            if url in visited:
                continue
            visited.add(url)

            print(f"  → {url}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(1)          # let lazy-load images settle
            except Exception as e:
                print(f"    SKIP (load error): {e}")
                continue

            # Screenshot
            img_path = IMG_DIR / f"{len(screenshots)+1:02d}_{slug(url)}.png"
            page.screenshot(path=str(img_path), full_page=True)
            screenshots.append(img_path)
            print(f"    saved {img_path.name}")

            # Discover new links
            new_links = collect_links(page, url) - visited
            to_visit |= new_links

        browser.close()

    print(f"\nCollected {len(screenshots)} screenshots. Building PDF…")

    # Build PDF by printing each screenshot as a page via a temp HTML wrapper
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page()

        pages_html = ""
        for img in screenshots:
            rel = img.resolve().as_uri()
            pages_html += (
                f'<div style="page-break-after:always;margin:0;padding:0;">'
                f'<img src="{rel}" style="width:100%;display:block;"></div>'
            )

        html = f"""<!DOCTYPE html>
<html><head>
<style>
  body {{ margin:0; padding:0; }}
  img  {{ max-width:100%; }}
</style>
</head><body>{pages_html}</body></html>"""

        page.set_content(html, wait_until="load")
        page.pdf(
            path=str(PDF_OUT),
            print_background=True,
            format="A3",
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        browser.close()

    print(f"PDF saved → {PDF_OUT}")

if __name__ == "__main__":
    run()
