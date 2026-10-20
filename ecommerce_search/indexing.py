import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokenize(text: str):
    return TOKEN_PATTERN.findall(text.lower())


def build_index(products):
    documents = {}
    term_doc_freq = defaultdict(int)
    inverted_index = defaultdict(dict)
    doc_lengths = {}

    for product in products:
        doc_id = str(product["id"])
        searchable_text = " ".join(
            [
                str(product.get("title", "")),
                str(product.get("description", "")),
                " ".join(product.get("categories", [])),
            ]
        )
        terms = tokenize(searchable_text)
        term_counts = Counter(terms)

        documents[doc_id] = {
            "id": doc_id,
            "title": product.get("title", ""),
            "description": product.get("description", ""),
            "categories": product.get("categories", []),
            "price": product.get("price"),
        }
        doc_lengths[doc_id] = sum(term_counts.values())

        for term, freq in term_counts.items():
            inverted_index[term][doc_id] = freq
            term_doc_freq[term] += 1

    doc_count = len(documents)
    avg_doc_len = (sum(doc_lengths.values()) / doc_count) if doc_count else 0.0

    idf = {}
    for term, df in term_doc_freq.items():
        idf[term] = math.log(1 + (doc_count - df + 0.5) / (df + 0.5))

    return {
        "documents": documents,
        "inverted_index": {term: postings for term, postings in inverted_index.items()},
        "doc_lengths": doc_lengths,
        "doc_count": doc_count,
        "avg_doc_len": avg_doc_len,
        "idf": idf,
    }


def save_index(index, path: str):
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(index, handle, ensure_ascii=False, indent=2)


def load_index(path: str):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)
