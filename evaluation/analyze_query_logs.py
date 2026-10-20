import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ecommerce_search.query_log import analyze_query_logs


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze e-commerce query logs.")
    parser.add_argument("--logs", required=True, help="Path to query log TSV file")
    return parser.parse_args()


def main():
    args = parse_args()
    report = analyze_query_logs(args.logs)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
