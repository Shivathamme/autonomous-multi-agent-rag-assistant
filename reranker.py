def rerank_documents(docs, query, top_k=3): # rerank pick best 3 
    if not docs:
        return []

    query_words = set(query.lower().split())

    def score(doc):
        content = doc.page_content.lower()
        keyword_score = sum(1 for word in query_words if word in content)
        length_score = min(len(content) / 1000, 1)  # cap length influence
        return keyword_score + length_score

    return sorted(docs, key=score, reverse=True)[:top_k]