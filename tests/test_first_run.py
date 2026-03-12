import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.first_run import run_first_run
from hyperclaw_max.ops_fabric.cli import validate_state_dir


REPO_ROOT = Path(__file__).resolve().parents[1]


class FirstRunTests(unittest.TestCase):
    def test_first_run_materializes_and_validates_public_core(self) -> None:
        with TemporaryDirectory() as tmp:
            payload = run_first_run(REPO_ROOT, Path(tmp))
            self.assertTrue(payload["ok"], payload)
            self.assertTrue(payload["doctor"]["ok"])
            self.assertTrue(payload["privacy"]["ok"])
            self.assertTrue(payload["config_validation"]["ok"])
            self.assertTrue(payload["materialize"]["ok"])
            self.assertTrue(payload["ops_fabric_validation"]["ok"])
            self.assertTrue((Path(tmp) / "config" / "openclaw.public.example.jsonc").exists())
            self.assertTrue((Path(tmp) / "materialized-pack.json").exists())
            self.assertTrue(validate_state_dir(Path(tmp) / "runtime" / "state")["ok"])
            self.assertTrue(payload["next_steps"])

    def test_first_run_can_enable_optional_overlays(self) -> None:
        with TemporaryDirectory() as tmp:
            payload = run_first_run(REPO_ROOT, Path(tmp), include_optional={"finance", "legal"})
            self.assertTrue(payload["ok"], payload)
            self.assertTrue((Path(tmp) / "workspace-finance" / "AGENTS.md").exists())
            self.assertTrue((Path(tmp) / "workspace-legal" / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
