# FindIt — Information Retrieval System

A Flask-based student project for the Web Search Mining course.

## Features
- Search TXT, PDF and DOCX documents
- BM25 relevance ranking
- Text preprocessing and stop-word removal
- Upload documents
- Search history using SQLite
- Responsive interface

## Run on Windows (VS Code terminal)

1. Extract the ZIP and open the `FindIt_IR_Project` folder in VS Code.
2. Open Terminal → New Terminal.
3. Run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

4. Open `http://127.0.0.1:5000` in your browser.

If PowerShell blocks activation, run this once in the terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

If `py` is not recognized, install Python 3.10+ and select **Add Python to PATH** during installation.

## GitHub submission

Create a new empty repository on GitHub. In the VS Code terminal, from this project folder:

```powershell
git init
git add .
git commit -m "Initial FindIt information retrieval project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL.

## Deployment
For a simple public demo, deploy this folder to a Python hosting service that supports Flask. Set the start command to `gunicorn app:app` (add `gunicorn` to requirements for that host).
