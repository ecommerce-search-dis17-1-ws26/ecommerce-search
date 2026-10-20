import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ecommerce_search.data_loading import load_products
from ecommerce_search.indexing import build_index, save_index


def parse_args():
    parser = argparse.ArgumentParser(description="Build an index from product JSONL data.")
    parser.add_argument("--products", required=True, help="Path to products JSONL file")
    parser.add_argument("--index-out", required=True, help="Path to write generated index JSON")
    return parser.parse_args()


def main():
    args = parse_args()
    products = load_products(args.products)
    index = build_index(products)
    save_index(index, args.index_out)
    print(f"Indexed {index['doc_count']} products -> {args.index_out}")


if __name__ == "__main__":
    main()
