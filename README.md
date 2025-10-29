### 📋 Project: Board/List/Task Management (Flask)

A modern, lightweight Board → List → Task management app. Users create boards, add lists to boards, and tasks to lists. Tasks support description and notes; status can be toggled (done/in progress). Clean, responsive UI powered by Jinja2.

### 🧰 Tech Stack
- 🐍 Flask, Flask-Login
- 🗄️ SQLAlchemy (ORM) + SQLite (default)
- 🧩 Jinja2 (templating)
- 🔐 python-dotenv (.env configuration)
- 🎨 Vanilla JS + CSS

### ✨ Features
- 🗂️ Board CRUD (create/update/delete)
- 🧱 List CRUD (create/update/delete)
- ✅ Task CRUD (create/update/delete)
- 🔁 Task status toggle (done/undo)
- 📝 Task description and notes
- 🔎 Task detail page (via link)
- 🪟 Modal forms (create/update)
- 🔔 Flash messages (success/warning)
- 📱 Responsive UI with line clamp for long text
- 🔒 Access control (no access to others’ resources)

### 🖼️ Screens
- Boards: `templates/boards.html`
- Board Detail: `templates/board_detail.html`
- Task Detail: `templates/quest_detail.html`
- Auth/User: `templates/login.html`, `templates/register.html`, `templates/user_detail.html`

### 🚀 Live Demo
- Demo: https://taskflow-flask-asp7.onrender.com/ (replace with your live URL)

### 🧪 Local Setup
1) Environment
- Python 3.10+
- Virtual env (Windows PowerShell):
  - `python -m venv .venv`
  - `.venv\Scripts\Activate.ps1`
- Install deps:
  - `pip install -r requirements.txt` (or quick start: `pip install flask flask-login sqlalchemy python-dotenv`)

2) .env file
Create a `.env` in project root:
```
FLASK_SECRET_KEY=your-long-random-secret
DATABASE_URL=sqlite:///instance/test.db
APP_ENV=development
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=False
REMEMBER_COOKIE_SECURE=False
```
Notes:
- In development keep `*_SECURE=False` (no HTTPS locally).
- In production set `*_SECURE=True`.

3) ▶️ Run
- `python main.py`
- Default: `http://127.0.0.1:5000/`

### ⚙️ Configuration
- Loaded from `.env` in `main.py`:
  - `FLASK_SECRET_KEY` → `app.config['SECRET_KEY']`
  - `DATABASE_URL` → `app.config['SQLALCHEMY_DATABASE_URI']`
- For Postgres, ensure URL scheme is `postgresql://`.

### 👤 Auth & Users
- Sign up with email/password.
- Access boards after login.
- User profile at `user_detail`.
- Sessions and protection via Flask-Login.

### 🧱 Data Model (Overview)
- User → Board (1–N)
- Board → List (1–N)
- List → Task (Quest) (1–N)
- Task fields: `title`, `description`, `notes`, `is_finished`, timestamps

### 🛣️ Key Routes
- `/` → landing/redirect
- `/login`, `/register`, `/logout`
- `/boards` → boards list + action-based POST (create/update/delete board)
- `/boards/<int:board_id>` → board detail (lists/tasks)
- `/quest_detail/<int:quest_id>` → task detail page

Action-based POST examples:
- `action=create_board`, `update_board`, `delete_board`
- `action=create_list`, `update_list`, `delete_list`
- `action=create_quest`, `update_quest`, `delete_quest`, `toggle_quest_status`

### 🎯 UI/UX
- Long titles/descriptions truncated with CSS line clamp.
- Actions (add/edit/delete) right under the list title.
- Task title is clickable → detail page.

### 🔐 Security Notes
- In production:
  - `SESSION_COOKIE_SECURE=True`
  - `REMEMBER_COOKIE_SECURE=True`
  - `SESSION_COOKIE_SAMESITE='Lax'` (or `Strict/None` as needed)
- Keep `FLASK_SECRET_KEY` strong and set via platform env.

### ☁️ Deployment (Overview)
- Set env vars on your platform (DATABASE_URL, FLASK_SECRET_KEY, ...)
- No FS write requirement (if using SQLite, ensure `instance/` is writable)
- App runs with `python main.py`; on prod prefer a WSGI server (e.g., gunicorn)

### 🛠️ Dev Tips
- Long-text overflow handled with `-webkit-line-clamp` and `word-break/overflow-wrap`.
- Modals controlled by inline JS in `templates/board_detail.html` (show/hide, focus).
- After CRUD, `handle_redirect` pattern shows flash and redirects.

### 🗺️ Roadmap (Optional)
- Search/filters
- Board sharing / team members
- Attachments / labels
- Drag & drop between lists (with backend persistence)

### 🤝 Contributing
- PRs are welcome. Keep code readable and simple.

---

Made with ❤️ by `watsonsk14`


