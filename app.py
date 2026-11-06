from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
from werkzeug.utils import secure_filename
from backend.document_loader import load_documents, extract_text
from backend.search_engine import SearchEngine
from backend.database import init_db, save_search, get_history, clear_history

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
SAMPLE_DIR = BASE_DIR / "sample_documents"
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
app = Flask(__name__)
app.secret_key = "findit-student-project-key"
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
UPLOAD_DIR.mkdir(exist_ok=True)
init_db(BASE_DIR / "findit.db")

def engine():
    docs = load_documents([SAMPLE_DIR, UPLOAD_DIR])
    return SearchEngine(docs)

@app.route("/", methods=["GET", "POST"])
def index():
    results, query, stats = [], "", None
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            searcher = engine()
            results = searcher.search(query, limit=20)
            stats = {"documents": len(searcher.documents), "results": len(results)}
            save_search(BASE_DIR / "findit.db", query, len(results))
    return render_template("index.html", results=results, query=query, stats=stats)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("files")
        count = 0
        for file in files:
            if file and file.filename:
                name = secure_filename(file.filename)
                if "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
                    file.save(UPLOAD_DIR / name)
                    count += 1
        flash(f"{count} document(s) uploaded." if count else "Choose TXT, PDF, or DOCX files.", "success" if count else "error")
        return redirect(url_for("upload"))
    return render_template("upload.html", documents=load_documents([SAMPLE_DIR, UPLOAD_DIR]))

@app.route("/history")
def history():
    return render_template("history.html", items=get_history(BASE_DIR / "findit.db"))

@app.route("/history/clear", methods=["POST"])
def history_clear():
    clear_history(BASE_DIR / "findit.db")
    flash("Search history cleared.", "success")
    return redirect(url_for("history"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/health")
def health():
    return {"status": "ok", "documents": len(load_documents([SAMPLE_DIR, UPLOAD_DIR]))}

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
