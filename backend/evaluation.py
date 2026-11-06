def precision_at_k(relevant, retrieved, k):
    if k <= 0:
        return 0.0
    return sum(1 for item in retrieved[:k] if item in relevant) / k

def recall_at_k(relevant, retrieved, k):
    if not relevant:
        return 0.0
    return sum(1 for item in retrieved[:k] if item in relevant) / len(relevant)
