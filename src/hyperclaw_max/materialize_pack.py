from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ops_fabric.cli import bootstrap_state_dir


BOOT_FILES = ("README.md", "AGENTS.md", "BOOTSTRAP.md", "TOOLS.md")
LIST_SECTIONS = {"required_agents", "optional_agents", "pack_rules"}
REQUIRED_MANIFEST_KEYS = {"version", "name", "status", "required_agents", "optional_agents", "pack_rules"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_scalar(value: str) -> Any:
    if value.isdigit():
        return int(value)
    if value in {"true", "false"}:
        return value == "true"
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_pack_manifest(path: Path) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    section: str | None = None
    current_item: dict[str, Any] | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            current_item = None
            if stripped.endswith(":"):
                section = stripped[:-1]
                payload[section] = [] if section in LIST_SECTIONS else {}
                continue
            key, sep, value = stripped.partition(":")
            if not sep:
                raise ValueError(f"Unsupported manifest line {line_number}: {raw_line}")
            payload[key.strip()] = parse_scalar(value.strip())
            section = None
            continue

        if indent == 2 and stripped.startswith("- "):
            if section is None or not isinstance(payload.get(section), list):
                raise ValueError(f"Unexpected list item on line {line_number}: {raw_line}")
            value = stripped[2:].strip()
            if ":" in value:
                key, item_value = value.split(":", 1)
                current_item = {key.strip(): parse_scalar(item_value.strip())}
                payload[section].append(current_item)
            else:
                payload[section].append(parse_scalar(value))
                current_item = None
            continue

        if indent >= 4 and current_item is not None and ":" in stripped:
            key, item_value = stripped.split(":", 1)
            current_item[key.strip()] = parse_scalar(item_value.strip())
            continue

        raise ValueError(f"Unsupported manifest structure on line {line_number}: {raw_line}")

    missing = sorted(REQUIRED_MANIFEST_KEYS - set(payload))
    if missing:
        raise ValueError(f"Manifest missing keys: {', '.join(missing)}")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_file(source: Path, target: Path, force: bool) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        return "skipped"
    shutil.copyfile(source, target)
    return "copied"


def selected_agents(
    manifest: dict[str, Any],
    include_optional: set[str] | None = None,
    include_all_optional: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    include_optional = include_optional or set()
    optional_rows = manifest["optional_agents"]
    available_optionals = {row["id"] for row in optional_rows}
    unknown = sorted(include_optional - available_optionals)
    if unknown:
        raise ValueError(f"Unknown optional agents: {', '.join(unknown)}")

    selected = list(manifest["required_agents"])
    enabled_optional_ids: list[str] = []
    for row in optional_rows:
        if include_all_optional or row["id"] in include_optional:
            selected.append(row)
            enabled_optional_ids.append(row["id"])
    return selected, enabled_optional_ids


def materialize_pack(
    repo: Path,
    target_root: Path,
    include_optional: set[str] | None = None,
    include_all_optional: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    repo = repo.resolve()
    target_root = target_root.resolve()
    manifest_path = repo / "agents" / "PACK-MANIFEST.yaml"
    manifest = load_pack_manifest(manifest_path)
    agents, enabled_optional_ids = selected_agents(manifest, include_optional=include_optional, include_all_optional=include_all_optional)

    copied: list[str] = []
    skipped: list[str] = []

    for source, target in (
        (repo / "config" / "openclaw.public.example.jsonc", target_root / "config" / "openclaw.public.example.jsonc"),
        (repo / "agents" / "PACK-MANIFEST.yaml", target_root / "agents" / "PACK-MANIFEST.yaml"),
        (repo / "agents" / "README.md", target_root / "agents" / "README.md"),
    ):
        status = copy_file(source, target, force=force)
        record = target.relative_to(target_root).as_posix()
        if status == "copied":
            copied.append(record)
        else:
            skipped.append(record)

    materialized_workspaces: list[dict[str, Any]] = []
    for agent in agents:
        agent_id = agent["id"]
        workspace_dir = target_root / agent["workspace"]
        workspace_dir.mkdir(parents=True, exist_ok=True)

        copied_files: list[str] = []
        skipped_files: list[str] = []
        source_dir = repo / "agents" / agent_id
        for name in BOOT_FILES:
            source = source_dir / name
            if not source.exists():
                continue
            status = copy_file(source, workspace_dir / name, force=force)
            if status == "copied":
                copied_files.append(name)
            else:
                skipped_files.append(name)
        materialized_workspaces.append(
            {
                "id": agent_id,
                "workspace": agent["workspace"],
                "copied_files": copied_files,
                "skipped_files": skipped_files,
            }
        )

    ops_fabric = bootstrap_state_dir(target_root / "runtime" / "state", force=force)
    metadata = {
        "generatedAt": now_iso(),
        "pack_name": manifest["name"],
        "status": manifest["status"],
        "selected_agents": [agent["id"] for agent in agents],
        "enabled_optional_agents": enabled_optional_ids,
        "source_repo": str(repo),
        "target_root": str(target_root),
    }
    write_json(target_root / "materialized-pack.json", metadata)
    copied.append("materialized-pack.json")

    return {
        "ok": True,
        "repo": str(repo),
        "target_root": str(target_root),
        "pack": manifest["name"],
        "status": manifest["status"],
        "selected_agents": metadata["selected_agents"],
        "enabled_optional_agents": enabled_optional_ids,
        "copied": copied,
        "skipped": skipped,
        "workspaces": materialized_workspaces,
        "ops_fabric": ops_fabric,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Materialize the public HyperClaw-Max pack over a target root")
    ap.add_argument("target_root", type=Path, help="Destination root that will host config, workspaces, and runtime state")
    ap.add_argument("--repo", type=Path, default=repo_root())
    ap.add_argument("--include-optional", action="append", default=[], help="Optional agent id to materialize")
    ap.add_argument("--all-optional", action="store_true", help="Materialize all optional overlay agents")
    ap.add_argument("--force", action="store_true", help="Overwrite existing materialized files")
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args()

    payload = materialize_pack(
        args.repo,
        args.target_root,
        include_optional=set(args.include_optional),
        include_all_optional=args.all_optional,
        force=args.force,
    )
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=== HyperClaw-Max Materialize Pack ===")
        print(f"Repo: {payload['repo']}")
        print(f"Target: {payload['target_root']}")
        print(f"Pack: {payload['pack']} | Status: {payload['status']}")
        print(f"Selected agents: {', '.join(payload['selected_agents'])}")
        if payload["enabled_optional_agents"]:
            print(f"Enabled optional agents: {', '.join(payload['enabled_optional_agents'])}")
        print(f"Copied: {len(payload['copied'])} | Skipped: {len(payload['skipped'])}")
        print(f"Ops fabric bootstrap: {'OK' if payload['ops_fabric']['ok'] else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
