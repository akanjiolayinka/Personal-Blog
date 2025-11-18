Personal Blog (Flask)
- Filesystem storage (data/articles/*.json)
- HTTP Basic authentication for admin
- Markdown rendering
- Pages: Home, Article, Dashboard, Add, Edit, Delete

Run:
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py

Defaults:
- Username: Olayinka
- Password: 0987654321

Change with env vars: ADMIN_USERNAME / ADMIN_PASSWORD
