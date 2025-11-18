# Personal Blog

A simple Flask-based personal blog with guest-facing pages and an admin section protected by HTTP Basic Authentication. Articles are stored as JSON files (one per article) under `data/articles`.

## Features
- Home page: lists all articles with title, publication date, excerpt and link.
- Article page: shows full content (Markdown rendered) and publication date.
- Admin dashboard: lists articles with links to view, edit, and delete.
- Add article page: form with Title, Date, and Content (Markdown) fields.
- Edit article page: same fields plus slug display.
- Delete action: confirmation prompt in dashboard.
- 404 page for missing articles or routes.

## Requirements
- Python 3.12+
- Packages: `Flask`, `markdown` (see `requirements.txt`).

## Getting Started
```powershell
# Activate virtual environment (already present if previously configured)
& "C:/Users/User/OneDrive/Desktop/Personal-Blog Project/.venv/Scripts/Activate.ps1"

# Or create one if missing
python -m venv .venv
& ./.venv/Scripts/Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
"C:/Users/User/OneDrive/Desktop/Personal-Blog Project/.venv/Scripts/python.exe" app.py
# Visit http://127.0.0.1:5000/
```

## Admin Authentication
The admin area uses HTTP Basic Auth (browser credential prompt).

Environment variables override defaults:
- `ADMIN_USERNAME` (default: `Olayinka`)
- `ADMIN_PASSWORD` (default: `0987654321`)

Set them before running (PowerShell example):
```powershell
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "strong-password"
"C:/Users/User/OneDrive/Desktop/Personal-Blog Project/.venv/Scripts/python.exe" app.py
```

## Article Storage
Articles are stored as JSON files named `<slug>.json` in `data/articles/` with fields:
```json
{
  "slug": "my-first-post",
  "title": "My First Post",
  "content": "# Heading\nBody text...",
  "date": "2025-11-18",
  "created_at": "2025-11-18T12:00:00.000000"
}
```

## Customization Ideas
- Replace file storage with a database (e.g. PostgreSQL + SQLAlchemy).
- Add tagging or categories.
- Add pagination on the home page.
- Add search over titles/content.
- Add session-based login instead of Basic Auth.

## Project Structure
```
app.py
requirements.txt
data/
  articles/            # JSON article files
static/
  style.css            # Stylesheet
templates/
  base.html
  index.html
  article.html
  404.html
  admin/
    dashboard.html
    add.html
    edit.html
```

## Safety & Notes
- Delete action is immediate (after confirm) and cannot be undone.
- Slugs remain stable on edit to preserve existing links.
- Markdown is rendered with fenced code blocks and tables enabled.

