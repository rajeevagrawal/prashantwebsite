#!/usr/bin/env python3
"""
Local content admin for Little Seeds & Peter Pan Schools.

Usage:
    python3 admin.py
    Then open http://localhost:8765 in your browser.

No external packages required — uses Python standard library only.
"""

import csv
import io
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote_plus

PORT    = 8765
BASE    = Path(__file__).parent.parent  # prototype/
CONTENT = BASE / "content"

PAGES = {
    "global":                        "🌐 Global (Nav · Footer · CTAs)",
    "home":                          "🏠 Homepage",
    "about":                         "👥 About Us",
    "little-seeds-childrens-center": "🌱 Little Seeds Children's Center",
    "peter-pan-academy":             "🎓 Peter Pan Academy",
    "peter-pan-preschool":           "🏫 Peter Pan Preschool",
    "curriculum":                    "📚 Curriculum",
    "blog":                          "✍️  Blog",
    "contact":                       "📞 Contact",
    "forms":                         "📋 Forms",
    "gallery":                       "📸 Gallery",
}

# ── CSV helpers ─────────────────────────────────────────────────────────────

def load_csv(name: str) -> list[dict]:
    path = CONTENT / f"{name}.csv"
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({"key": row["key"].strip(), "value": row["value"]})
    return rows

def save_csv(name: str, rows: list[dict]):
    path = CONTENT / f"{name}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "value"])
        for r in rows:
            w.writerow([r["key"], r["value"]])

def run_generate() -> str:
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "generate.py")],
        capture_output=True, text=True, cwd=str(BASE)
    )
    return (result.stdout + result.stderr).strip()

# ── HTML helpers ─────────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f7f3ee;
       color: #1e2a38; display: flex; min-height: 100vh; }

/* Sidebar */
aside {
  width: 240px; flex-shrink: 0; background: #1e2a38; color: #c9d2dc;
  padding: 0; position: sticky; top: 0; height: 100vh; overflow-y: auto;
}
.sidebar-logo {
  padding: 20px 18px 16px; font-size: 1rem; font-weight: 700;
  color: #F4752C; border-bottom: 1px solid rgba(255,255,255,0.08);
  letter-spacing: -0.01em;
}
.sidebar-logo span { display: block; font-size: 0.7rem; color: #7a8899;
  font-weight: 400; margin-top: 2px; }
nav a {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 18px; font-size: 0.82rem; color: #9aa4b2;
  text-decoration: none; transition: background 0.15s, color 0.15s;
  border-left: 3px solid transparent;
}
nav a:hover { background: rgba(255,255,255,0.06); color: #fff; }
nav a.active { background: rgba(244,117,44,0.15); color: #F4752C;
  border-left-color: #F4752C; }
.sidebar-footer { padding: 14px 18px; font-size: 0.72rem; color: #4a5568;
  border-top: 1px solid rgba(255,255,255,0.06); margin-top: auto; }

/* Main */
main { flex: 1; padding: 32px 40px; max-width: 900px; }
h1 { font-size: 1.4rem; font-weight: 700; color: #1e2a38;
     margin-bottom: 4px; }
.subtitle { font-size: 0.82rem; color: #6b7280; margin-bottom: 28px; }

/* Dashboard grid */
.dash-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px,1fr));
  gap: 14px; margin-top: 12px; }
.dash-card { background: #fff; border-radius: 12px; padding: 18px 20px;
  text-decoration: none; color: #1e2a38; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  transition: transform 0.15s, box-shadow 0.15s; border: 1.5px solid transparent; }
.dash-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  border-color: #F4752C; }
.dash-card .icon { font-size: 1.5rem; margin-bottom: 8px; }
.dash-card .name { font-size: 0.85rem; font-weight: 600; }
.dash-card .count { font-size: 0.72rem; color: #9aa4b2; margin-top: 3px; }

/* Form */
.form-header { display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.btn { display: inline-flex; align-items: center; gap: 6px;
  background: #F4752C; color: #fff; border: none; border-radius: 50px;
  padding: 10px 22px; font-size: 0.85rem; font-weight: 600; cursor: pointer;
  transition: background 0.15s; text-decoration: none; }
.btn:hover { background: #e05e1a; }
.btn-sm { padding: 7px 16px; font-size: 0.78rem; }
.btn-ghost { background: transparent; color: #6b7280; border: 1.5px solid #d1d5db; }
.btn-ghost:hover { background: #f3f4f6; color: #1e2a38; }

.field-group { margin-bottom: 14px; }
.field-group label { display: block; font-size: 0.72rem; font-weight: 600;
  color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;
  margin-bottom: 5px; }
.field-group input, .field-group textarea {
  width: 100%; padding: 9px 12px; border: 1.5px solid #e5e7eb;
  border-radius: 8px; font-size: 0.88rem; color: #1e2a38;
  background: #fff; transition: border-color 0.15s; font-family: inherit;
  resize: vertical;
}
.field-group input:focus, .field-group textarea:focus {
  outline: none; border-color: #F4752C; box-shadow: 0 0 0 3px rgba(244,117,44,0.12);
}
.field-group .key-hint { font-size: 0.68rem; color: #b0b7c3;
  margin-top: 3px; font-family: monospace; }

/* Section divider */
.section-divider { font-size: 0.7rem; font-weight: 700; color: #F4752C;
  text-transform: uppercase; letter-spacing: 0.08em; margin: 24px 0 12px;
  padding-bottom: 6px; border-bottom: 1.5px solid #ffe4d0; }

/* Toast */
.toast { display: none; background: #1e2a38; color: #fff; border-radius: 10px;
  padding: 14px 20px; margin-bottom: 20px; font-size: 0.84rem; line-height: 1.5; }
.toast.success { border-left: 4px solid #2BA899; }
.toast.error   { border-left: 4px solid #e53e3e; }
.toast pre { font-family: monospace; font-size: 0.75rem; margin-top: 8px;
  white-space: pre-wrap; color: #9aa4b2; }
"""

def sidebar(active=""):
    links = "\n".join(
        f'<a href="/edit/{k}" class="{"active" if k == active else ""}">{v}</a>'
        for k, v in PAGES.items()
    )
    return f"""
    <aside>
      <div class="sidebar-logo">⚙️ Content Admin
        <span>Little Seeds & Peter Pan Schools</span>
      </div>
      <nav>
        <a href="/" class="{"active" if active == "" else ""}">🏡 Dashboard</a>
        {links}
      </nav>
      <div class="sidebar-footer">python3 admin.py · port {PORT}</div>
    </aside>"""

def page_shell(title: str, body: str, active="") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Content Admin</title>
<style>{CSS}</style>
</head>
<body>
{sidebar(active)}
<main>{body}</main>
</body>
</html>"""

# ── Views ────────────────────────────────────────────────────────────────────

def view_dashboard() -> str:
    cards = ""
    for key, label in PAGES.items():
        rows = load_csv(key)
        icon, name = label.split(" ", 1)
        cards += f"""
        <a href="/edit/{key}" class="dash-card">
          <div class="icon">{icon}</div>
          <div class="name">{name.strip()}</div>
          <div class="count">{len(rows)} fields</div>
        </a>"""
    body = f"""
    <h1>Content Dashboard</h1>
    <p class="subtitle">Select a page to edit its content. Changes regenerate all HTML files automatically.</p>
    <div class="dash-grid">{cards}</div>"""
    return page_shell("Dashboard", body, active="")

def view_edit(page: str, toast: str = "", toast_type: str = "success") -> str:
    if page not in PAGES:
        return page_shell("Not Found", "<h1>Page not found</h1>")

    rows = load_csv(page)
    label = PAGES[page]

    # Group fields by prefix (first word of key before _)
    sections: dict[str, list] = {}
    for r in rows:
        prefix = r["key"].split("_")[0]
        sections.setdefault(prefix, []).append(r)

    fields_html = ""
    last_prefix = None
    for r in rows:
        prefix = r["key"].split("_")[0]
        if prefix != last_prefix:
            fields_html += f'<div class="section-divider">{prefix}</div>'
            last_prefix = prefix

        val   = r["value"]
        key   = r["key"]
        is_long = len(val) > 80 or "\n" in val
        esc_val = val.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

        if is_long:
            inp = f'<textarea name="{key}" rows="3">{esc_val}</textarea>'
        else:
            inp = f'<input type="text" name="{key}" value="{esc_val}">'

        fields_html += f"""
        <div class="field-group">
          <label>{key.replace("_", " ").title()}</label>
          {inp}
          <div class="key-hint">{{{{ {key} }}}}</div>
        </div>"""

    toast_html = ""
    if toast:
        toast_html = f"""
        <div class="toast {toast_type}" style="display:block">
          {'✅ Saved and site regenerated!' if toast_type=='success' else '❌ Error'}
          <pre>{toast}</pre>
        </div>"""

    body = f"""
    <div class="form-header">
      <div>
        <h1>{label}</h1>
        <p class="subtitle">Edit content below and click Save & Regenerate.</p>
      </div>
      <div style="display:flex;gap:8px;">
        <a href="/" class="btn btn-ghost btn-sm">← Dashboard</a>
      </div>
    </div>
    {toast_html}
    <form method="POST" action="/save/{page}">
      {fields_html}
      <div style="margin-top:24px;display:flex;gap:10px;align-items:center;">
        <button type="submit" class="btn">💾 Save &amp; Regenerate</button>
        <span style="font-size:0.78rem;color:#9aa4b2;">
          Saves {page}.csv and rebuilds all HTML pages
        </span>
      </div>
    </form>"""

    return page_shell(label, body, active=page)

# ── Request handler ──────────────────────────────────────────────────────────

class AdminHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {args[0]} {args[1]}")

    def send_html(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")

        if path == "" or path == "/":
            self.send_html(view_dashboard())
        elif path.startswith("/edit/"):
            page = path[len("/edit/"):]
            self.send_html(view_edit(page))
        else:
            self.send_html("<h1>404</h1>", 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")

        if not path.startswith("/save/"):
            self.send_html("<h1>404</h1>", 404)
            return

        page = path[len("/save/"):]
        if page not in PAGES:
            self.send_html("<h1>Not found</h1>", 404)
            return

        # Read POST body
        length = int(self.headers.get("Content-Length", 0))
        raw    = self.rfile.read(length).decode("utf-8")
        params = parse_qs(raw, keep_blank_values=True)

        # Rebuild rows preserving original key order
        original = load_csv(page)
        updated  = []
        for r in original:
            k   = r["key"]
            val = params.get(k, [""])[0]
            val = unquote_plus(val) if k not in params else val
            updated.append({"key": k, "value": val})

        save_csv(page, updated)
        output = run_generate()

        toast_type = "success" if "OK" in output else "error"
        self.send_html(view_edit(page, toast=output, toast_type=toast_type))


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    server = HTTPServer(("", PORT), AdminHandler)
    print(f"\n  🌱 Little Seeds Content Admin")
    print(f"  ─────────────────────────────")
    print(f"  Open → http://localhost:{PORT}")
    print(f"  Stop → Ctrl+C\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
