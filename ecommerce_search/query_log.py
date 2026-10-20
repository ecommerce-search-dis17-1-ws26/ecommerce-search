import csv
from collections import Counter
from pathlib import Path


def analyze_query_logs(path: str, top_n=10):
    total_queries = 0
    zero_result_queries = 0
    query_counter = Counter()

    with Path(path).open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            total_queries += 1
            query_text = row["query"].strip().lower()
            result_count = int(row.get("result_count", "0"))
            query_counter[query_text] += 1
            if result_count == 0:
                zero_result_queries += 1

    zero_result_rate = (zero_result_queries / total_queries) if total_queries else 0.0
    return {
        "total_queries": total_queries,
        "zero_result_queries": zero_result_queries,
        "zero_result_rate": zero_result_rate,
        "top_queries": query_counter.most_common(top_n),
    }
