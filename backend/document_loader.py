from pathlib import Path

def extract_text(path):
    path = Path(path)
    suffix = path.suffix.lower()
    try:
        if suffix == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".pdf":
            from pypdf import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        if suffix == ".docx":
            from docx import Document
            return "\n".join(p.text for p in Document(str(path)).paragraphs)
    except Exception:
        return ""
    return ""

def load_documents(folders):
    docs = []
    for folder in folders:
        folder = Path(folder)
        if not folder.exists():
            continue
        for path in sorted(folder.iterdir()):
            if path.is_file() and path.suffix.lower() in {".txt", ".pdf", ".docx"}:
                text = extract_text(path)
                if text.strip():
                    docs.append({"id": path.name, "title": path.stem.replace("_", " ").title(),
                                 "filename": path.name, "text": text})
    return docs
