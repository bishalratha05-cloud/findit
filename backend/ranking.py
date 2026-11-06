import math
from collections import Counter
from .text_processing import preprocess

def bm25_scores(query, documents, k1=1.5, b=0.75):
    tokenized = [preprocess(d.get("text", "")) for d in documents]
    lengths = [len(t) for t in tokenized]
    avgdl = sum(lengths) / max(len(lengths), 1)
    n = len(documents)
    df = Counter()
    for tokens in tokenized:
        df.update(set(tokens))
    qterms = preprocess(query)
    scores = []
    for doc, tokens, dl in zip(documents, tokenized, lengths):
        tf = Counter(tokens)
        score = 0.0
        for term in qterms:
            if term not in df:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf[term] + k1 * (1 - b + b * dl / max(avgdl, 1))
            score += idf * (tf[term] * (k1 + 1)) / max(denom, 1e-9)
        scores.append(score)
    return scores
