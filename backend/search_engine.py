from .ranking import bm25_scores

class SearchEngine:
    def __init__(self, documents):
        self.documents = documents

    def search(self, query, limit=20):
        if not query.strip() or not self.documents:
            return []
        scores = bm25_scores(query, self.documents)
        ranked = sorted(zip(self.documents, scores), key=lambda x: x[1], reverse=True)
        results = []
        for doc, score in ranked:
            if score <= 0:
                continue
            text = " ".join(doc["text"].split())
            results.append({**doc, "score": round(score, 4),
                            "snippet": text[:260] + ("…" if len(text) > 260 else "")})
            if len(results) >= limit:
                break
        return results
