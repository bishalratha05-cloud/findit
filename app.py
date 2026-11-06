import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from werkzeug.utils import secure_filename

from backend.database import (
    initialize_database,
    add_document,
    get_all_documents,
    get_document,
    delete_document,
    save_search_history,
    get_search_history,
    get_database_statistics
)

from backend.document_loader import DocumentLoader


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "docx",
    "md",
    "html",
    "htm",
    "csv"
}

app = Flask(__name__)

app.secret_key = "findit-information-retrieval-secret-key"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

loader = DocumentLoader()

initialize_database()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def perform_search(query):

    query_words = query.lower().split()

    documents = get_all_documents()

    results = []

    for document in documents:

        content = str(
            document.get("content", "")
        )

        title = str(
            document.get("filename", "")
        )

        searchable_text = (
            title + " " + content
        ).lower()

        score = sum(
            searchable_text.count(word)
            for word in query_words
        )

        if score > 0:

            result = document.copy()

            result["score"] = score

            results.append(result)

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():

    try:
        statistics = get_database_statistics()

    except Exception:
        statistics = {}

    return render_template(
        "index.html",
        statistics=statistics
    )


# ==========================================
# SEARCH PAGE
# ==========================================

@app.route("/search", methods=["GET", "POST"])
def search():

    query = request.values.get(
        "query",
        ""
    ).strip()

    results = []

    if query:

        results = perform_search(query)

        try:

            save_search_history(
                query,
                len(results)
            )

        except Exception as error:
            print("Search history error:", error)

    return render_template(
        "index.html",
        query=query,
        results=results,
        search_performed=bool(query)
    )


# ==========================================
# DOCUMENT UPLOAD
# ==========================================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if "file" not in request.files:

            flash(
                "No file was selected.",
                "danger"
            )

            return redirect(url_for("upload"))

        file = request.files["file"]

        if not file.filename:

            flash(
                "Please select a file.",
                "warning"
            )

            return redirect(url_for("upload"))

        if not allowed_file(file.filename):

            flash(
                "Unsupported file format.",
                "danger"
            )

            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        try:

            file.save(filepath)

            content = loader.extract_text(filepath)

            add_document(
                filename=filename,
                filepath=filepath,
                content=content
            )

            flash(
                "Document uploaded successfully!",
                "success"
            )

            return redirect(url_for("upload"))

        except Exception as error:

            if os.path.exists(filepath):
                os.remove(filepath)

            flash(
                f"Upload failed: {error}",
                "danger"
            )

            return redirect(url_for("upload"))

    return render_template("upload.html")


# ==========================================
# DOCUMENT LIST
# ==========================================

@app.route("/documents")
def documents():

    all_documents = get_all_documents()

    return render_template(
        "index.html",
        documents=all_documents,
        show_documents=True
    )


# ==========================================
# DOCUMENT DETAILS
# ==========================================

@app.route("/document/<int:document_id>")
def document_details(document_id):

    document = get_document(document_id)

    if not document:

        flash(
            "Document not found.",
            "danger"
        )

        return redirect(url_for("documents"))

    return render_template(
        "index.html",
        selected_document=document
    )


# ==========================================
# DELETE DOCUMENT
# ==========================================

@app.route("/delete/<int:document_id>", methods=["POST"])
def delete(document_id):

    document = get_document(document_id)

    if document:

        filepath = document.get("filepath")

        delete_document(document_id)

        if filepath and os.path.exists(filepath):

            try:
                os.remove(filepath)

            except OSError:
                pass

        flash(
            "Document deleted successfully.",
            "success"
        )

    else:

        flash(
            "Document not found.",
            "danger"
        )

    return redirect(url_for("documents"))


# ==========================================
# SEARCH HISTORY
# ==========================================

@app.route("/history")
def history():

    search_history = get_search_history()

    return render_template(
        "history.html",
        history=search_history
    )


# ==========================================
# ABOUT PAGE
# ==========================================

@app.route("/about")
def about():

    return render_template("about.html")


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        "Page not found.",
        404
    )


@app.errorhandler(413)
def file_too_large(error):

    flash(
        "File size exceeds the 16 MB limit.",
        "danger"
    )

    return redirect(url_for("upload"))


# ==========================================
# RUN APPLICATION
# ==========================================
@app.route("/search", methods=["GET", "POST"])
def search():

    query = request.values.get("query", "").strip()

    results = []

    if query:
        results = perform_search(query)

        try:
            save_search_history(query, len(results))
        except Exception as error:
            print("Search history error:", error)

    return render_template(
        "index.html",
        query=query,
        results=results,
        search_performed=bool(query)
    )
if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )