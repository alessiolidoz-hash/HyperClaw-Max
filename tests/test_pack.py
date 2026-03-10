import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.context_intel.pack import build_pack


class PackTests(unittest.TestCase):
    def test_build_pack_finds_local_candidate(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            target = root / "src" / "relay.py"
            target.write_text(
                "def telegram_inbound_dedupe(session_scope: str) -> str:\n    return session_scope\n",
                encoding="utf-8",
            )
            pack = build_pack(
                "telegram inbound dedupe session scope",
                repo=root,
                profile="terse",
                symbol_slicing="python-only",
            )
            self.assertTrue(pack["local_candidates"])
            self.assertIn("relay.py", pack["local_candidates"][0]["rel_path"])


if __name__ == "__main__":
    unittest.main()
