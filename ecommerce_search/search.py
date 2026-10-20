from collections import defaultdict

from ecommerce_search.indexing import tokenize


def expand_query(tokens, synonyms):
    expanded = list(tokens)
    for token in tokens:
        for synonym in synonyms.get(token, []):
            expanded.append(synonym)
    return expanded


def score_keyword(index, query_tokens):
    scores = defaultdict(float)
    postings_map = index["inverted_index"]

    for token in query_tokens:
        postings = postings_map.get(token, {})
        for doc_id, term_freq in postings.items():
            scores[doc_id] += term_freq
    return scores


def score_bm25(index, query_tokens, k1=1.2, b=0.75):
    scores = defaultdict(float)
    postings_map = index["inverted_index"]
    doc_lengths = index["doc_lengths"]
    avg_doc_len = index["avg_doc_len"] or 1.0
    idf = index["idf"]

    for token in query_tokens:
        postings = postings_map.get(token, {})
        term_idf = idf.get(token, 0.0)
        for doc_id, term_freq in postings.items():
            doc_len = doc_lengths[doc_id]
            numerator = term_freq * (k1 + 1)
            denominator = term_freq + k1 * (1 - b + b * (doc_len / avg_doc_len))
            scores[doc_id] += term_idf * (numerator / denominator)
    return scores


def search(index, query, mode="keyword", top_k=10, synonyms=None):
    tokens = tokenize(query)
    if synonyms:
        tokens = expand_query(tokens, synonyms)

    if mode == "keyword":
        scores = score_keyword(index, tokens)
    elif mode in {"bm25", "bm25_expanded"}:
        scores = score_bm25(index, tokens)
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    results = []
    for rank, (doc_id, score) in enumerate(ranked[:top_k], start=1):
        doc = index["documents"][doc_id]
        results.append(
            {
                "doc_id": doc_id,
                "rank": rank,
                "score": score,
                "title": doc["title"],
            }
        )
    return results
