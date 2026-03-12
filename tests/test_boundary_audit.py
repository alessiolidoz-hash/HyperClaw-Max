import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.privacy_check import scan_repo


class BoundaryAuditTests(unittest.TestCase):
    def test_scan_repo_flags_secret_private_path_and_runtime_artifact(self) -> None:
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "src" / "hyperclaw_max").mkdir(parents=True)
            (repo / "runtime").mkdir(parents=True)
            (repo / "config").mkdir(parents=True)
            token = "sk-" + ("A" * 24)

            (repo / "src" / "hyperclaw_max" / "leak.py").write_text(
                f'TOKEN = "{token}"\nPRIVATE = "/root/.openclaw/openclaw.json"\n',
                encoding="utf-8",
            )
            (repo / "runtime" / "live.session").write_text("session residue\n", encoding="utf-8")
            (repo / "config" / "openclaw.json").write_text('{"private": true}\n', encoding="utf-8")

            findings = scan_repo(repo)
            self.assertTrue(findings["openai_key"])
            self.assertTrue(findings["private_root_path"])
            self.assertTrue(findings["private_runtime_artifact"])
            self.assertTrue(findings["private_live_config"])


if __name__ == "__main__":
    unittest.main()
