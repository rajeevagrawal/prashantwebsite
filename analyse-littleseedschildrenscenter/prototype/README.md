# Little Seeds & Peter Pan Schools — Website Prototype

Joyloo-inspired redesign prototype for **Little Seeds & Peter Pan Schools**.  
Built with plain HTML + CSS (no framework, no build step).

---

## Pages

| Page | File |
|---|---|
| Homepage | `index.html` |
| About Us | `about.html` |
| Our Schools | `school.html` |
| Curriculum | `curriculum.html` |
| Blog | `blog.html` |
| Contact / Book a Tour | `contact.html` |

---

## How to Run Locally

### Mac

**Option 1 — Python (recommended, no install needed)**
```bash
cd prototype
python3 -m http.server 8080
```
Then open your browser at: [http://localhost:8080](http://localhost:8080)

**Option 2 — Node.js (if installed)**
```bash
cd prototype
npx serve .
```
Then open the URL shown in the terminal.

---

### Windows

**Option 1 — Python (recommended)**

1. Check if Python is installed:
   ```cmd
   python --version
   ```
   If not installed, download from [python.org](https://www.python.org/downloads/)

2. Open **Command Prompt** or **PowerShell**, navigate to the prototype folder:
   ```cmd
   cd path\to\prototype
   python -m http.server 8080
   ```
   Then open your browser at: [http://localhost:8080](http://localhost:8080)

**Option 2 — Node.js (if installed)**
```cmd
cd path\to\prototype
npx serve .
```

**Option 3 — VS Code Live Server (easiest for non-developers)**
1. Install [VS Code](https://code.visualstudio.com/)
2. Install the **Live Server** extension (by Ritwick Dey)
3. Open the `prototype` folder in VS Code
4. Right-click `index.html` → **Open with Live Server**
5. Browser opens automatically

---

## Stopping the Server

- **Mac / Windows terminal:** Press `Ctrl + C`
- **VS Code Live Server:** Click **Port: 5500** in the bottom status bar → Stop

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
