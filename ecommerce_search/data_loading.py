import csv
import json
from pathlib import Path


def load_products(path: str):
    products = []
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            product = json.loads(line)
            products.append(product)
    return products


def load_queries_tsv(path: str):
    queries = []
    with Path(path).open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            queries.append((row["query_id"], row["query"]))
    return queries


def load_qrels_tsv(path: str):
    qrels = {}
    with Path(path).open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            query_id = row["query_id"]
            doc_id = row["doc_id"]
            relevance = int(row["relevance"])
            qrels.setdefault(query_id, {})[doc_id] = relevance
    return qrels


def load_synonyms(path: str):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)
