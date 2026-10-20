# System Architecture

1. **Data Ingestion**: Product, query, qrels, and log files loaded from TSV/JSONL.
2. **Indexing**: Inverted index with per-document term frequencies, lengths, and IDF values.
3. **Retrieval Layer**:
   - Keyword overlap baseline.
   - BM25 ranking.
   - BM25 + synonym query expansion.
4. **Evaluation Layer**: Computes Precision@K, Recall@K, MAP@K, NDCG@K.
5. **Analysis Layer**: Query-log diagnostics (zero-result rate and frequent queries).
