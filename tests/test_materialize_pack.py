import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.materialize_pack import load_pack_manifest, materialize_pack
from hyperclaw_max.ops_fabric.cli import validate_state_dir


REPO_ROOT = Path(__file__).resolve().parents[1]


class MaterializePackTests(unittest.TestCase):
    def test_pack_manifest_loads(self) -> None:
        manifest = load_pack_manifest(REPO_ROOT / "agents" / "PACK-MANIFEST.yaml")
        self.assertEqual(manifest["name"], "hyperclaw-max-default-pack")
        self.assertEqual(manifest["required_agents"][0]["id"], "main")
        self.assertEqual(manifest["optional_agents"][0]["id"], "finance")

    def test_materialize_pack_creates_core_layout(self) -> None:
        with TemporaryDirectory() as tmp:
            payload = materialize_pack(REPO_ROOT, Path(tmp))
            self.assertTrue(payload["ok"])

            config_path = Path(tmp) / "config" / "openclaw.public.example.jsonc"
            manifest_path = Path(tmp) / "agents" / "PACK-MANIFEST.yaml"
            metadata_path = Path(tmp) / "materialized-pack.json"
            state_dir = Path(tmp) / "runtime" / "state"

            self.assertTrue(config_path.exists())
            self.assertTrue(manifest_path.exists())
            self.assertTrue(metadata_path.exists())
            self.assertTrue((Path(tmp) / "workspace" / "AGENTS.md").exists())
            self.assertTrue((Path(tmp) / "workspace-codex" / "TOOLS.md").exists())
            self.assertTrue((Path(tmp) / "workspace-pa" / "BOOTSTRAP.md").exists())
            self.assertTrue((Path(tmp) / "workspace-hk" / "README.md").exists())

            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(metadata["status"], "public-core-beta")
            self.assertEqual(metadata["selected_agents"], ["main", "codex", "pa", "hk"])

            state_payload = validate_state_dir(state_dir)
            self.assertTrue(state_payload["ok"], state_payload["errors"])

    def test_materialize_pack_can_enable_optional_overlay(self) -> None:
        with TemporaryDirectory() as tmp:
            payload = materialize_pack(REPO_ROOT, Path(tmp), include_optional={"finance"})
            self.assertTrue(payload["ok"])
            self.assertTrue((Path(tmp) / "workspace-finance" / "AGENTS.md").exists())
            self.assertFalse((Path(tmp) / "workspace-legal").exists())


if __name__ == "__main__":
    unittest.main()
