from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "google_api_key": re.compile(r"AIza[0-9A-Za-z\\-_]{20,}"),
    "github_pat": re.compile(r"ghp_[0-9A-Za-z]{20,}"),
    "openai_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
}
SKIP_DIRS = {".git", "__pycache__", "build", "artifacts", "logs", "tmp", "node_modules"}


def scan_repo(repo: Path) -> dict[str, list[dict[str, str]]]:
    findings: dict[str, list[dict[str, str]]] = {name: [] for name in PATTERNS}
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = path.relative_to(repo).as_posix()
        for name, pattern in PATTERNS.items():
            for idx, line in enumerate(text.splitlines(), start=1):
                if pattern.search(line):
                    findings[name].append({"path": rel, "line": str(idx)})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="HyperClaw-Max privacy / secret scan")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args()

    repo = args.repo.resolve()
    findings = scan_repo(repo)
    count = sum(len(rows) for rows in findings.values())
    payload = {"repo": str(repo), "ok": count == 0, "findings": findings}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=== HyperClaw-Max Privacy Check ===")
        if count == 0:
            print("No matching secret patterns found.")
        else:
            for name, rows in findings.items():
                for row in rows:
                    print(f"- {name}: {row['path']}:{row['line']}")
    return 0 if count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
