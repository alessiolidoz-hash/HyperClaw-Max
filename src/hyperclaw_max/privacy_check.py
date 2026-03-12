from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "google_api_key": re.compile(r"AIza[0-9A-Za-z\\-_]{20,}"),
    "github_pat": re.compile(r"ghp_[0-9A-Za-z]{20,}"),
    "openai_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "private_root_path": re.compile(r"/root/\.openclaw(?:/|$)"),
}
PATH_ONLY_PATTERNS = {
    "private_live_config": re.compile(r"(^|/)openclaw\.json$"),
    "private_runtime_artifact": re.compile(r"\.(session|sqlite|db|p12|pfx)$"),
    "private_token_dump": re.compile(r"(^|/)(token|credentials)\.json$"),
}
SKIP_DIRS = {".git", "__pycache__", "build", "artifacts", "logs", "tmp", "node_modules"}


def should_scan_content_pattern(rel: str, name: str) -> bool:
    if name != "private_root_path":
        return True
    return rel == "README.md" or rel.startswith("config/") or rel.startswith("install/") or rel.startswith("src/")


def scan_repo(repo: Path) -> dict[str, list[dict[str, str]]]:
    findings: dict[str, list[dict[str, str]]] = {name: [] for name in PATTERNS | PATH_ONLY_PATTERNS}
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(repo)
        if any(part in SKIP_DIRS for part in rel_path.parts):
            continue
        rel = rel_path.as_posix()
        for name, pattern in PATH_ONLY_PATTERNS.items():
            if pattern.search(rel):
                findings[name].append({"path": rel, "line": ""})
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for name, pattern in PATTERNS.items():
            if not should_scan_content_pattern(rel, name):
                continue
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
                    suffix = f":{row['line']}" if row["line"] else ""
                    print(f"- {name}: {row['path']}{suffix}")
    return 0 if count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
