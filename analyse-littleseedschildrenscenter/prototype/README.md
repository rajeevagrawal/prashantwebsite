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

## File Structure

```
prototype/
├── theme.css        ← Design tokens (edit here to change everything)
├── styles.css       ← Component styles (uses theme.css variables)
├── index.html       ← Homepage
├── about.html       ← About Us
├── school.html      ← Our Schools (location page)
├── curriculum.html  ← Curriculum
├── blog.html        ← Blog listing
├── contact.html     ← Contact / Book a Tour
└── README.md        ← This file
```

---

## Notes

- **No internet required** for layout — fonts load from Google Fonts CDN (requires internet for correct typography)
- **Images** are placeholders (emoji) — replace with real photos before Wix build
- **Forms** are HTML-only — not connected to any backend in this prototype
- This prototype is for design review only and is not the final Wix site
