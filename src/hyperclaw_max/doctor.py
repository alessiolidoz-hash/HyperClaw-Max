from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "pyproject.toml",
    "src/hyperclaw_max/context_intel/pack.py",
    "src/hyperclaw_max/context_intel/clinic.py",
    "fixtures/context_intel/canonical-cases-v1.jsonl",
    "tests/test_pack.py",
]
OPTIONAL_TOOLS = ["gh", "node"]
REQUIRED_TOOLS = ["git", "bash", "rg"]


def check_files(repo: Path) -> list[dict[str, str]]:
    results = []
    for rel in REQUIRED_FILES:
        path = repo / rel
        results.append({"path": rel, "status": "ok" if path.exists() else "missing"})
    return results


def check_tools(names: list[str], required: bool) -> list[dict[str, str]]:
    rows = []
    for name in names:
        rows.append(
            {
                "tool": name,
                "status": "ok" if shutil.which(name) else ("missing" if required else "optional-missing"),
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="HyperClaw-Max environment doctor")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args()

    repo = args.repo.resolve()
    payload = {
        "repo": str(repo),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "required_files": check_files(repo),
        "required_tools": check_tools(REQUIRED_TOOLS, required=True),
        "optional_tools": check_tools(OPTIONAL_TOOLS, required=False),
    }
    missing_required_files = [row["path"] for row in payload["required_files"] if row["status"] != "ok"]
    missing_required_tools = [row["tool"] for row in payload["required_tools"] if row["status"] != "ok"]
    payload["ok"] = not missing_required_files and not missing_required_tools and sys.version_info >= (3, 11)
    payload["missing_required_files"] = missing_required_files
    payload["missing_required_tools"] = missing_required_tools

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=== HyperClaw-Max Doctor ===")
        print(f"Repo: {payload['repo']}")
        print(f"Python: {payload['python']} | Platform: {payload['platform']}")
        for row in payload["required_files"]:
            print(f"- file {row['path']}: {row['status']}")
        for row in payload["required_tools"]:
            print(f"- tool {row['tool']}: {row['status']}")
        for row in payload["optional_tools"]:
            print(f"- optional {row['tool']}: {row['status']}")
        print(f"Overall: {'OK' if payload['ok'] else 'FAIL'}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
