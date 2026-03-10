import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hyperclaw_max.context_intel.symbol_slice import slice_python_symbol


class SymbolSliceTests(unittest.TestCase):
    def test_slice_python_symbol_extracts_function(self) -> None:
        with TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample.py"
            target.write_text(
                "import os\n\n\ndef hello(name: str) -> str:\n    return f'hello {name}'\n",
                encoding="utf-8",
            )
            payload = slice_python_symbol(target, 4)
            self.assertEqual(payload["slice_status"], "ok")
            self.assertEqual(payload["symbol"], "hello")
            self.assertEqual(payload["span"]["start_line"], 4)


if __name__ == "__main__":
    unittest.main()
