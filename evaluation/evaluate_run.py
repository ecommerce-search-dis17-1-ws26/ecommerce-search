import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ecommerce_search.data_loading import load_qrels_tsv
from ecommerce_search.evaluation import evaluate_run


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate run output with standard IR metrics.")
    parser.add_argument("--run", required=True, help="Run file TSV path")
    parser.add_argument("--qrels", required=True, help="Qrels TSV path")
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--json-out", help="Optional path to write JSON metrics")
    return parser.parse_args()


def load_run(path):
    run = defaultdict(list)
    with open(path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        ordered_rows = sorted(reader, key=lambda row: (row["query_id"], int(row["rank"])))
        for row in ordered_rows:
            run[row["query_id"]].append(row["doc_id"])
    return run


def main():
    args = parse_args()
    run = load_run(args.run)
    qrels = load_qrels_tsv(args.qrels)

    report = evaluate_run(run, qrels, args.k)
    print(json.dumps(report["summary"], indent=2))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        print(f"Saved detailed report to {args.json_out}")


if __name__ == "__main__":
    main()
