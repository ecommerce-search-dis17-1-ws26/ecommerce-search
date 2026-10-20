import unittest

from ecommerce_search.evaluation import evaluate_run
from ecommerce_search.indexing import build_index
from ecommerce_search.search import search


class SearchProjectTests(unittest.TestCase):
    def setUp(self):
        self.products = [
            {
                "id": "P1",
                "title": "Wireless Mouse",
                "description": "Ergonomic bluetooth mouse",
                "categories": ["electronics"],
            },
            {
                "id": "P2",
                "title": "Running Shoes",
                "description": "Comfort sneakers for road running",
                "categories": ["sports"],
            },
        ]
        self.index = build_index(self.products)

    def test_keyword_search_returns_expected_doc(self):
        results = search(self.index, "bluetooth mouse", mode="keyword", top_k=1)
        self.assertEqual(results[0]["doc_id"], "P1")

    def test_query_expansion_matches_synonym(self):
        results = search(
            self.index,
            "sneakers",
            mode="bm25_expanded",
            top_k=1,
            synonyms={"sneakers": ["shoes"]},
        )
        self.assertEqual(results[0]["doc_id"], "P2")

    def test_evaluation_metrics_include_required_keys(self):
        run = {"Q1": ["P1", "P2"]}
        qrels = {"Q1": {"P1": 2, "P2": 0}}
        report = evaluate_run(run, qrels, k=2)
        self.assertIn("mean_precision@2", report["summary"])
        self.assertIn("mean_recall@2", report["summary"])
        self.assertIn("map@2", report["summary"])
        self.assertIn("mean_ndcg@2", report["summary"])


if __name__ == "__main__":
    unittest.main()
