from __future__ import annotations
import os, re, json
from datetime import date, datetime
from pathlib import Path
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, abort, Response
import markdown as md

app = Flask(__name__)

# Basic auth defaults; can be overridden by env vars
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "Olayinka")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "0987654321")

BASE_DIR = Path(__file__).parent.resolve()
ART_DIR = BASE_DIR / "data" / "articles"
ART_DIR.mkdir(parents=True, exist_ok=True)

def make_slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", (text or "").lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s or "post"

def read_article(slug: str):
    p = ART_DIR / f"{slug}.json"
    if not p.exists(): return None
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_article(data: dict):
    (ART_DIR / f"{data['slug']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def remove_article(slug: str):
    p = ART_DIR / f"{slug}.json"
    if p.exists(): p.unlink()

def list_articles():
    items = []
    for p in ART_DIR.glob("*.json"):
        try:
            items.append(json.loads(p.read_text(encoding='utf-8')))
        except Exception:
            pass
    def to_date(x):
        try: return date.fromisoformat((x or "")[:10])
        except Exception: return date.min
    items.sort(key=lambda a: to_date(a.get("date")), reverse=True)
    return items

def check_auth():
    a = request.authorization
    return a and a.username == ADMIN_USERNAME and a.password == ADMIN_PASSWORD

def require_auth(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        if not check_auth():
            return Response("Auth required", 401, {"WWW-Authenticate": 'Basic realm=\"Admin Area\"'})
        return fn(*args, **kwargs)
    return _wrap

@app.get("/")
def home():
    return render_template("index.html", articles=list_articles())

@app.get("/article/<slug>")
def article(slug):
    a = read_article(slug)
    if not a: abort(404)
    html = md.markdown(a.get("content",""), extensions=["extra", "fenced_code", "tables"])
    return render_template("article.html", article=a, content_html=html)

@app.get("/admin/")
@require_auth
def dashboard():
    return render_template("admin/dashboard.html", articles=list_articles())

@app.get("/admin/add")
@require_auth
def add_form():
    return render_template("admin/add.html", today=date.today().isoformat())

@app.post("/admin/add")
@require_auth
def add_post():
    title = (request.form.get("title") or "").strip()
    content = (request.form.get("content") or "").strip()
    when = (request.form.get("date") or "").strip() or date.today().isoformat()
    if not title or not content:
        return render_template("admin/add.html", today=date.today().isoformat(), error="Title and content are required.")
    base = make_slug(title)
    slug = base
    i = 1
    while (ART_DIR / f"{slug}.json").exists():
        i += 1
        slug = f"{base}-{i}"
    write_article({
        "slug": slug,
        "title": title,
        "content": content,
        "date": when,
        "created_at": datetime.utcnow().isoformat()
    })
    return redirect(url_for("dashboard"))

@app.get("/admin/edit/<slug>")
@require_auth
def edit_form(slug):
    a = read_article(slug)
    if not a: abort(404)
    return render_template("admin/edit.html", article=a)

@app.post("/admin/edit/<slug>")
@require_auth
def edit_post(slug):
    a = read_article(slug)
    if not a: abort(404)
    title = (request.form.get("title") or "").strip()
    content = (request.form.get("content") or "").strip()
    when = (request.form.get("date") or "").strip() or a.get("date")
    if not title or not content:
        return render_template("admin/edit.html", article=a, error="Title and content are required.")
    a.update({"title": title, "content": content, "date": when})
    write_article(a)
    return redirect(url_for("dashboard"))

@app.post("/admin/delete/<slug>")
@require_auth
def delete_post(slug):
    if not read_article(slug): abort(404)
    remove_article(slug)
    return redirect(url_for("dashboard"))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
