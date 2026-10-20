# E-Commerce Search Engine Improvement Project

This repository contains a complete, lightweight implementation of the project lifecycle for improving e-commerce product search quality.

## Repository Structure

- `docs/` – project plan, architecture, findings, lab book, evaluation report, presentation outline
- `data/` – sample products, sample queries, sample relevance judgments, sample query logs, synonyms
- `indexing/` – indexing CLI script
- `search-engines/` – search CLI script supporting multiple retrieval modes
- `evaluation/` – evaluation and query-log analysis CLI scripts
- `ecommerce_search/` – reusable Python modules for indexing, retrieval, evaluation, and log analysis
- `tests/` – focused unit tests

## Implemented Search Engines

1. **Baseline keyword search** (`keyword`) using simple term-overlap scoring.
2. **BM25 ranking** (`bm25`) with configurable `k1` and `b`.
3. **BM25 + query expansion** (`bm25_expanded`) with synonym expansion.

## Quick Start

### 1) Build an index

```bash
python indexing/build_index.py \
  --products data/sample_products.jsonl \
  --index-out data/sample_index.json
```

### 2) Run search

```bash
python search-engines/run_search.py \
  --index data/sample_index.json \
  --queries data/sample_queries.tsv \
  --mode bm25_expanded \
  --synonyms data/synonyms.json \
  --top-k 5 \
  --run-out data/sample_run.tsv
```

### 3) Evaluate run quality

```bash
python evaluation/evaluate_run.py \
  --run data/sample_run.tsv \
  --qrels data/sample_qrels.tsv \
  --k 5
```

### 4) Analyze query logs

```bash
python evaluation/analyze_query_logs.py \
  --logs data/sample_query_logs.tsv
```

## Testing

Run focused tests:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
