from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from typing import Any

from .doctor import OPTIONAL_TOOLS, REQUIRED_TOOLS, check_files, check_tools
from .materialize_pack import materialize_pack, repo_root
from .ops_fabric.cli import summarize_state_dir, validate_state_dir
from .privacy_check import scan_repo
from .runtime_validate import validate_config_path


def run_doctor(repo: Path) -> dict[str, Any]:
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
    payload["missing_required_files"] = missing_required_files
    payload["missing_required_tools"] = missing_required_tools
    payload["ok"] = not missing_required_files and not missing_required_tools and sys.version_info >= (3, 11)
    return payload


def run_privacy_check(repo: Path) -> dict[str, Any]:
    findings = scan_repo(repo)
    count = sum(len(rows) for rows in findings.values())
    return {"repo": str(repo), "ok": count == 0, "findings": findings}


def run_first_run(
    repo: Path,
    target_root: Path,
    include_optional: set[str] | None = None,
    include_all_optional: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    repo = repo.resolve()
    target_root = target_root.resolve()

    doctor_payload = run_doctor(repo)
    privacy_payload = run_privacy_check(repo)
    source_config_validation = validate_config_path(repo / "config" / "openclaw.public.example.jsonc")

    materialize_payload = materialize_pack(
        repo,
        target_root,
        include_optional=include_optional,
        include_all_optional=include_all_optional,
        force=force,
    )

    target_config = target_root / "config" / "openclaw.public.example.jsonc"
    config_validation = validate_config_path(target_config)
    ops_state_dir = target_root / "runtime" / "state"
    ops_fabric_validation = validate_state_dir(ops_state_dir)
    ops_fabric_summary = summarize_state_dir(ops_state_dir)

    ok = all(
        (
            doctor_payload["ok"],
            privacy_payload["ok"],
            source_config_validation["ok"],
            materialize_payload["ok"],
            config_validation["ok"],
            ops_fabric_validation["ok"],
            ops_fabric_summary["ok"],
        )
    )

    next_steps = [
        f"Edit {target_config} with real provider and connector values.",
        f"Run `PYTHONPATH=src python3 -m hyperclaw_max.runtime_validate {target_config}` after each config change.",
        f"Use `PYTHONPATH=src python3 -m hyperclaw_max.materialize_pack {target_root} --force` to refresh workspace boots.",
        "Install the public-safe systemd templates only after config values are ready.",
        "Enable optional overlays or connector adapters only when you actually need them.",
    ]

    return {
        "ok": ok,
        "repo": str(repo),
        "target_root": str(target_root),
        "doctor": doctor_payload,
        "privacy": privacy_payload,
        "source_config_validation": source_config_validation,
        "materialize": materialize_payload,
        "config_validation": config_validation,
        "ops_fabric_validation": ops_fabric_validation,
        "ops_fabric_summary": ops_fabric_summary,
        "next_steps": next_steps,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the public HyperClaw-Max first-run bootstrap")
    ap.add_argument("target_root", type=Path, help="Destination root for the materialized public pack")
    ap.add_argument("--repo", type=Path, default=None)
    ap.add_argument("--include-optional", action="append", default=[], help="Optional agent id to materialize")
    ap.add_argument("--all-optional", action="store_true", help="Materialize all optional overlay agents")
    ap.add_argument("--force", action="store_true", help="Overwrite existing materialized files")
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args()

    payload = run_first_run(
        args.repo.resolve() if args.repo is not None else repo_root(),
        args.target_root,
        include_optional=set(args.include_optional),
        include_all_optional=args.all_optional,
        force=args.force,
    )

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=== HyperClaw-Max First Run ===")
        print(f"Repo: {payload['repo']}")
        print(f"Target: {payload['target_root']}")
        print(f"Doctor: {'OK' if payload['doctor']['ok'] else 'FAIL'}")
        print(f"Privacy: {'OK' if payload['privacy']['ok'] else 'FAIL'}")
        print(f"Source config: {'OK' if payload['source_config_validation']['ok'] else 'FAIL'}")
        print(f"Materialize: {'OK' if payload['materialize']['ok'] else 'FAIL'}")
        print(f"Target config: {'OK' if payload['config_validation']['ok'] else 'FAIL'}")
        print(f"Ops fabric: {'OK' if payload['ops_fabric_validation']['ok'] else 'FAIL'}")
        print(f"Overall: {'OK' if payload['ok'] else 'FAIL'}")
        print("Next steps:")
        for step in payload["next_steps"]:
            print(f"- {step}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
