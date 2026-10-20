import math


def precision_at_k(retrieved_doc_ids, relevant_doc_ids, k):
    subset = retrieved_doc_ids[:k]
    if not subset:
        return 0.0
    hits = sum(1 for doc_id in subset if doc_id in relevant_doc_ids)
    return hits / k


def recall_at_k(retrieved_doc_ids, relevant_doc_ids, k):
    if not relevant_doc_ids:
        return 0.0
    subset = retrieved_doc_ids[:k]
    hits = sum(1 for doc_id in subset if doc_id in relevant_doc_ids)
    return hits / len(relevant_doc_ids)


def average_precision_at_k(retrieved_doc_ids, relevant_doc_ids, k):
    if not relevant_doc_ids:
        return 0.0

    score = 0.0
    hits = 0
    for idx, doc_id in enumerate(retrieved_doc_ids[:k], start=1):
        if doc_id in relevant_doc_ids:
            hits += 1
            score += hits / idx
    return score / len(relevant_doc_ids)


def ndcg_at_k(retrieved_doc_ids, relevance_map, k):
    dcg = 0.0
    for idx, doc_id in enumerate(retrieved_doc_ids[:k], start=1):
        rel = relevance_map.get(doc_id, 0)
        dcg += (2**rel - 1) / math.log2(idx + 1)

    ideal_rels = sorted(relevance_map.values(), reverse=True)[:k]
    idcg = 0.0
    for idx, rel in enumerate(ideal_rels, start=1):
        idcg += (2**rel - 1) / math.log2(idx + 1)

    if idcg == 0:
        return 0.0
    return dcg / idcg


def evaluate_run(run_by_query, qrels, k):
    per_query = {}

    p_scores = []
    r_scores = []
    ap_scores = []
    ndcg_scores = []

    for query_id, relevance_map in qrels.items():
        retrieved_doc_ids = run_by_query.get(query_id, [])
        relevant_doc_ids = {doc_id for doc_id, rel in relevance_map.items() if rel > 0}

        p_at_k = precision_at_k(retrieved_doc_ids, relevant_doc_ids, k)
        r_at_k = recall_at_k(retrieved_doc_ids, relevant_doc_ids, k)
        ap_at_k = average_precision_at_k(retrieved_doc_ids, relevant_doc_ids, k)
        ndcg_k = ndcg_at_k(retrieved_doc_ids, relevance_map, k)

        per_query[query_id] = {
            f"precision@{k}": p_at_k,
            f"recall@{k}": r_at_k,
            f"ap@{k}": ap_at_k,
            f"ndcg@{k}": ndcg_k,
        }

        p_scores.append(p_at_k)
        r_scores.append(r_at_k)
        ap_scores.append(ap_at_k)
        ndcg_scores.append(ndcg_k)

    divisor = max(len(qrels), 1)
    return {
        "per_query": per_query,
        "summary": {
            f"mean_precision@{k}": sum(p_scores) / divisor,
            f"mean_recall@{k}": sum(r_scores) / divisor,
            f"map@{k}": sum(ap_scores) / divisor,
            f"mean_ndcg@{k}": sum(ndcg_scores) / divisor,
        },
    }
