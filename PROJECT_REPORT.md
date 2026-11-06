# FindIt — Information Retrieval System

## 1. Introduction
FindIt is a web-based Information Retrieval System developed as part of the Web Search Mining course. It allows users to search a local collection of documents and view ranked results.

## 2. Objectives
- Build a simple document search website.
- Extract and preprocess document text.
- Rank documents according to query relevance.
- Provide document upload and search history.

## 3. Technologies
Python, Flask, HTML, CSS, SQLite, BM25 ranking, pypdf and python-docx.

## 4. Methodology
Documents are loaded from the sample_documents and uploads folders. Text is extracted, converted to lowercase tokens, and common stop words are removed. For each query, BM25 calculates a relevance score for every document. Results are sorted by descending score and displayed with a text snippet.

## 5. Modules
- document_loader.py: reads TXT, PDF and DOCX files.
- text_processing.py: tokenization and stop-word removal.
- query_processor.py: processes search queries.
- ranking.py: computes BM25 scores.
- search_engine.py: returns ranked results.
- database.py: stores and retrieves search history.
- evaluation.py: provides Precision@K and Recall@K helper functions.

## 6. Conclusion
FindIt demonstrates the main stages of a basic information retrieval system: document collection, text processing, query processing, ranking, and result presentation.
