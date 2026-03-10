import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.context_intel.feedback_store import append_event, normalize_query_signature, summarize_feedback


class FeedbackStoreTests(unittest.TestCase):
    def test_feedback_store_dedupes_same_event(self) -> None:
        with TemporaryDirectory() as tmp:
            log = Path(tmp) / "feedback.jsonl"
            query_sig = normalize_query_signature("telegram dedupe")
            event = {
                "ts": "2026-03-10T00:00:00Z",
                "source": "eval",
                "case_id": "case-1",
                "query_signature": query_sig,
                "candidate_id": "src/app.py",
                "vote": 1,
                "reason_code": "accepted_candidate",
                "operator": "tester",
                "git": {"dirty_count": 0},
            }
            append_event(event, log)
            append_event(event, log)
            summary = summarize_feedback(query_sig, log)
            self.assertEqual(summary["src/app.py"]["support"], 1)
            self.assertEqual(summary["src/app.py"]["raw_support"], 2)


if __name__ == "__main__":
    unittest.main()
