# Little Seeds & Peter Pan Schools — Website Prototype

Joyloo-inspired redesign prototype for **Little Seeds & Peter Pan Schools**.  
Built with plain HTML + CSS (no framework, no build step needed).

---

## Quick Start — Clone & Run

### Step 1 — Clone the repo

```bash
git clone -b develop https://github.com/rajeevagrawal/prashantwebsite.git
cd prashantwebsite/analyse-littleseedschildrenscenter/prototype
```

### Step 2 — Start the server

#### Mac
```bash
python3 -m http.server 8080
```

#### Windows (Command Prompt or PowerShell)
```cmd
python -m http.server 8080
```

> Don't have Python? Download from [python.org](https://www.python.org/downloads/) — it takes 2 minutes.  
> Alternatively, if you have Node.js: `npx serve .`

### Step 3 — Open in browser

[http://localhost:8080](http://localhost:8080)

Navigate between pages using the top nav bar.  
Press `Ctrl + C` in the terminal to stop the server.

---

## Pages

| Page | URL |
|---|---|
| Homepage | http://localhost:8080/index.html |
| About Us | http://localhost:8080/about.html |
| Our Schools | http://localhost:8080/school.html |
| Curriculum | http://localhost:8080/curriculum.html |
| Blog | http://localhost:8080/blog.html |
| Contact / Book a Tour | http://localhost:8080/contact.html |

---

## Stopping the Server

Press **`Ctrl + C`** in the terminal window.

---

## Design Token System

All colors, fonts, spacing, and sizing are controlled from a single file:

**`theme.css`** — change any value here and it propagates to every page automatically.

```css
/* Example: change the primary brand color site-wide */
--color-primary: #F4752C;   /* ← change this one line */
```

Key tokens:

| Token | Default | Controls |
|---|---|---|
| `--color-primary` | `#F4752C` | Buttons, highlights, CTAs |
| `--color-secondary` | `#5B9BD5` | Secondary buttons, icons |
| `--color-tertiary` | `#2BA899` | Teal badges, accents |
| `--color-bg-cream` | `#FDF6ED` | Alternating section backgrounds |
| `--color-bg-soft` | `#FFF1E4` | Hero, testimonial backgrounds |
| `--color-text-dark` | `#1E2A38` | All headlines and body text |
| `--font-display` | `'Nunito'` | All headings |
| `--font-body` | `'DM Sans'` | All body text |
| `--radius-pill` | `50px` | Button border-radius |
| `--section-pad-y` | `6rem` | Vertical section padding |

---

## Updating Content (CSV System)

All text and images are managed in the `content/` folder.  
After editing any CSV, run one command to regenerate all pages:

```bash
python3 generate.py
```

### How to change text

Open `content/global.csv` for site-wide text (brand name, navigation, footer, CTAs)  
or the page-specific CSV (e.g. `content/home.csv`) for page text.  
Change the `value` column for any row, save, then run `python3 generate.py`.

### How to add real photos

1. Drop your image files into `content/images/`  
   (e.g. `hero-classroom.jpg`, `school-alameda.jpg`)
2. Open the relevant CSV (e.g. `content/home.csv`) and set the image key's value  
   to the filename:  
   ```
   hero_image,hero-classroom.jpg
   ```
3. Run `python3 generate.py` — the page will now show the real photo.

If a filename is blank or the file doesn't exist, an emoji placeholder is shown instead.

### Content files

| File | Controls |
|---|---|
| `content/global.csv` | Brand name, nav, footer, CTAs — shared across all pages |
| `content/home.csv` | Homepage text |
| `content/about.csv` | About Us page |
| `content/school.csv` | Our Schools page |
| `content/curriculum.csv` | Curriculum page |
| `content/blog.csv` | Blog listing page |
| `content/contact.csv` | Contact / Book a Tour page |
| `content/images/` | Drop real photos here |
| `templates/` | HTML templates with `{{key}}` placeholders — edit only if changing layout |

---

## File Structure

```
prototype/
├── theme.css           ← Design tokens (edit here to change everything)
├── styles.css          ← Component styles (uses theme.css variables)
├── generate.py         ← Run this to rebuild all pages from CSVs
├── index.html          ← Homepage  (generated — edit home.csv, not this file)
├── about.html          ← About Us
├── school.html         ← Our Schools
├── curriculum.html     ← Curriculum
├── blog.html           ← Blog listing
├── contact.html        ← Contact / Book a Tour
├── content/
│   ├── global.csv      ← Site-wide text tokens
│   ├── home.csv        ← Homepage tokens
│   ├── about.csv
│   ├── school.csv
│   ├── curriculum.csv
│   ├── blog.csv
│   ├── contact.csv
│   └── images/         ← Drop real photos here
├── templates/          ← HTML templates (layout only — don't edit text here)
└── README.md
```

---

## Notes

- **No internet required** for layout — fonts load from Google Fonts CDN (requires internet for correct typography)
- **Images** are placeholders (emoji) — replace with real photos before Wix build
- **Forms** are HTML-only — not connected to any backend in this prototype
- This prototype is for design review only and is not the final Wix site
