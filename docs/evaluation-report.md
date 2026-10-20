# Evaluation Report Template

## Experimental Setup
- Dataset: TREC-style product collection (plus optional sample data for smoke tests).
- Retrieval modes: keyword, BM25, BM25 + query expansion.
- Metrics: Precision@K, Recall@K, MAP@K, NDCG@K.

## Result Summary
Use `evaluation/evaluate_run.py` outputs to compare modes per query and in aggregate.

## Analysis Guidance
- Compare gains/losses by query intent type.
- Inspect failure cases and vocabulary mismatch queries.
- Use query-log zero-result analysis as prioritization input.

## Recommendations
- Expand synonym dictionary with high-impact terms.
- Tune BM25 parameters and consider learning-to-rank as next step.
