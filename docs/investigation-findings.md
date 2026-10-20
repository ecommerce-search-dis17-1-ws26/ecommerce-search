# Investigation Findings

Common causes of weak e-commerce search quality addressed in this repository:

1. **Vocabulary mismatch** between user terms and catalog language.
   - Mitigation: synonym-based query expansion.
2. **Weak ranking quality** for multi-term queries.
   - Mitigation: BM25 ranking with document-length normalization.
3. **Limited observability of failure patterns**.
   - Mitigation: query-log analysis for zero-result queries and top repeated terms.
4. **Lack of standardized evaluation**.
   - Mitigation: reproducible metric pipeline (P@K, R@K, MAP@K, NDCG@K).
