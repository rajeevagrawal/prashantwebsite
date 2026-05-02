"""
Crawls peterpanschools.com, takes full-page screenshots of every unique page,
stamps the URL as a header bar on each image, and assembles them into a PDF.
"""

import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import img2pdf
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

BASE_URL  = "https://www.peterpanschools.com"
OUT_DIR   = Path(__file__).parent
IMG_DIR   = OUT_DIR / "screenshots"
PDF_OUT   = OUT_DIR / "peterpanschools_all_pages.pdf"

IMG_DIR.mkdir(exist_ok=True)

BAR_HEIGHT  = 48   # px height of the URL header bar
BAR_COLOR   = (30, 42, 56)     # dark navy
TEXT_COLOR  = (255, 255, 255)  # white
FONT_SIZE   = 22


def stamp_url(img_path: Path, url: str):
    """Add a dark URL bar at the top of the screenshot image in-place."""
    img = Image.open(img_path).convert("RGB")
    w, h = img.size

    canvas = Image.new("RGB", (w, h + BAR_HEIGHT), BAR_COLOR)
    canvas.paste(img, (0, BAR_HEIGHT))

    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", FONT_SIZE)
    except Exception:
        font = ImageFont.load_default()

    draw.text((16, (BAR_HEIGHT - FONT_SIZE) // 2), url, fill=TEXT_COLOR, font=font)
    canvas.save(img_path)


def same_origin(url):
    p = urlparse(url)
    b = urlparse(BASE_URL)
    return p.netloc == b.netloc or p.netloc == ""


def normalise(url):
    u = urlparse(url)
    return u._replace(fragment="", query="").geturl().rstrip("/")


def collect_links(page, url):
    links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
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
    visited     = set()
    to_visit    = {normalise(BASE_URL)}
    screenshots = []   # (img_path, url) tuples in visit order

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
                time.sleep(1)
            except Exception as e:
                print(f"    SKIP (load error): {e}")
                continue

            img_path = IMG_DIR / f"{len(screenshots)+1:02d}_{slug(url)}.png"
            page.screenshot(path=str(img_path), full_page=True)
            stamp_url(img_path, url)
            screenshots.append(img_path)
            print(f"    saved {img_path.name}")

            new_links = collect_links(page, url) - visited
            to_visit |= new_links

        browser.close()

    print(f"\nCollected {len(screenshots)} screenshots. Building PDF…")

    with open(PDF_OUT, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in screenshots]))

    import os
    size_mb = os.path.getsize(PDF_OUT) / 1024 / 1024
    print(f"PDF saved → {PDF_OUT}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    run()
