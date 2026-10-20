import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ecommerce_search.data_loading import load_queries_tsv, load_synonyms
from ecommerce_search.indexing import load_index
from ecommerce_search.search import search


def parse_args():
    parser = argparse.ArgumentParser(description="Run search queries against a built index.")
    parser.add_argument("--index", required=True, help="Path to index JSON")
    parser.add_argument("--queries", required=True, help="Path to TSV with query_id and query")
    parser.add_argument("--mode", choices=["keyword", "bm25", "bm25_expanded"], default="keyword")
    parser.add_argument("--synonyms", help="Path to synonym JSON file (used for bm25_expanded)")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--run-out", required=True, help="Output TSV run file")
    return parser.parse_args()


def main():
    args = parse_args()
    index = load_index(args.index)
    queries = load_queries_tsv(args.queries)
    synonyms = load_synonyms(args.synonyms) if args.mode == "bm25_expanded" and args.synonyms else {}

    rows = []
    for query_id, query_text in queries:
        results = search(index, query_text, mode=args.mode, top_k=args.top_k, synonyms=synonyms)
        for item in results:
            rows.append(
                {
                    "query_id": query_id,
                    "doc_id": item["doc_id"],
                    "rank": item["rank"],
                    "score": f"{item['score']:.6f}",
                }
            )

    with open(args.run_out, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["query_id", "doc_id", "rank", "score"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} ranked results -> {args.run_out}")


if __name__ == "__main__":
    main()
