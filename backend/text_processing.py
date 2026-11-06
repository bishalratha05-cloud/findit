import re
from collections import Counter

STOP_WORDS = set("""
a an the and or but if while with to from in on at by for of is are was were be been being
this that these those it its as into about over under after before than then so such not no
we you they he she i our your their can could should would will may might do does did have has
had also more most some any all each other which who what when where why how
""".split())

def tokenize(text):
    return re.findall(r"[a-z0-9]+", (text or "").lower())

def preprocess(text):
    return [w for w in tokenize(text) if w not in STOP_WORDS and len(w) > 1]

def term_frequency(tokens):
    counts = Counter(tokens)
    total = max(len(tokens), 1)
    return {term: count / total for term, count in counts.items()}
