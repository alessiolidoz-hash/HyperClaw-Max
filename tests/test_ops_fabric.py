import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.ops_fabric.cli import bootstrap_state_dir, summarize_state_dir, validate_state_dir


REPO_ROOT = Path(__file__).resolve().parents[1]


class OpsFabricTests(unittest.TestCase):
    def test_bootstrap_creates_public_state_files(self) -> None:
        with TemporaryDirectory() as tmp:
            payload = bootstrap_state_dir(Path(tmp))
            self.assertTrue(payload["ok"])
            self.assertIn("active-tasks.json", payload["created"])
            self.assertIn("delegations.json", payload["created"])
            self.assertIn("system-operational-watchdog.json", payload["created"])

    def test_bootstrapped_state_validates(self) -> None:
        with TemporaryDirectory() as tmp:
            bootstrap_state_dir(Path(tmp))
            payload = validate_state_dir(Path(tmp))
            self.assertTrue(payload["ok"], payload["errors"])

    def test_sample_fixtures_validate_and_summarize(self) -> None:
        with TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            for name in (
                "active-tasks.sample.json",
                "delegations.sample.json",
                "system-operational-watchdog.sample.json",
            ):
                source = REPO_ROOT / "fixtures" / "ops_fabric" / name
                target = state_dir / name.replace(".sample", "")
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            validate_payload = validate_state_dir(state_dir)
            self.assertTrue(validate_payload["ok"], validate_payload["errors"])

            summary_payload = summarize_state_dir(state_dir)
            self.assertTrue(summary_payload["ok"])
            self.assertEqual(summary_payload["summary"]["active_tasks_total"], 1)
            self.assertEqual(summary_payload["summary"]["delegations_total"], 1)
            self.assertEqual(summary_payload["summary"]["incidents_total"], 1)

    def test_invalid_task_status_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            bootstrap_state_dir(state_dir)
            active_tasks = state_dir / "active-tasks.json"
            active_tasks.write_text(
                """{
  "meta": {"updatedAt": "2026-03-12T12:00:00Z"},
  "tasks": {
    "PUBLIC-TASK-001": {
      "id": "PUBLIC-TASK-001",
      "status": "mystery",
      "summary": "invalid status example"
    }
  }
}
""",
                encoding="utf-8",
            )
            payload = validate_state_dir(state_dir)
            self.assertFalse(payload["ok"])
            self.assertTrue(any("active-tasks.json:active-tasks.tasks.PUBLIC-TASK-001.status" == row["path"] for row in payload["errors"]))


if __name__ == "__main__":
    unittest.main()
