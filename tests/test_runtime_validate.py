import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.runtime_validate import load_jsonc, validate_config, validate_config_path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RuntimeValidateTests(unittest.TestCase):
    def test_example_config_is_valid(self) -> None:
        payload = validate_config_path(REPO_ROOT / "config" / "openclaw.public.example.jsonc")
        self.assertTrue(payload["ok"], payload["errors"])

    def test_control_plane_templates_exist(self) -> None:
        service = REPO_ROOT / "install" / "systemd" / "openclaw-gateway.service"
        override = REPO_ROOT / "install" / "systemd" / "openclaw-gateway.service.d" / "env-override.conf.example"
        self.assertTrue(service.exists())
        self.assertTrue(override.exists())
        self.assertIn("hyperclaw_max.runtime_validate", service.read_text(encoding="utf-8"))

    def test_jsonc_comments_and_trailing_commas_are_supported(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.jsonc"
            path.write_text(
                """{
  // gateway comment
  "gateway": {
    "mode": "gateway",
    "bind": "127.0.0.1",
    "port": 18789,
  },
  "agents": {
    "defaults": {
      "workspace": "./workspace",
      "model": {
        "primary": "openai/gpt-5.2",
        "fallbacks": [],
      },
    },
    "list": [
      {
        "id": "main",
        "workspace": "./workspace",
      },
    ],
  },
  "models": {
    "providers": {
      "openai": {
        "apiKey": "${OPENAI_API_KEY}",
      },
    },
  },
}""",
                encoding="utf-8",
            )
            cfg = load_jsonc(path)
            self.assertEqual(cfg["gateway"]["port"], 18789)
            self.assertTrue(validate_config(cfg)["ok"])

    def test_duplicate_agent_ids_fail(self) -> None:
        cfg = {
            "gateway": {"mode": "gateway", "bind": "127.0.0.1", "port": 18789},
            "agents": {
                "defaults": {
                    "workspace": "./workspace",
                    "model": {"primary": "openai/gpt-5.2", "fallbacks": []},
                },
                "list": [
                    {"id": "main", "workspace": "./workspace"},
                    {"id": "main", "workspace": "./workspace-codex"},
                ],
            },
            "models": {"providers": {"openai": {"apiKey": "${OPENAI_API_KEY}"}}},
        }
        payload = validate_config(cfg)
        self.assertFalse(payload["ok"])
        self.assertIn("must be unique", json.dumps(payload["errors"]))

    def test_missing_required_top_level_keys_fail(self) -> None:
        payload = validate_config({"gateway": {"mode": "gateway", "bind": "127.0.0.1", "port": 18789}})
        self.assertFalse(payload["ok"])
        self.assertIn("agents", json.dumps(payload["errors"]))
        self.assertIn("models", json.dumps(payload["errors"]))


if __name__ == "__main__":
    unittest.main()
