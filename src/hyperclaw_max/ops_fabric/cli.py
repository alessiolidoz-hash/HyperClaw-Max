from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .contracts import (
    ACTIVE_TASK_STATUSES,
    DELEGATION_STATUSES,
    INCIDENT_SEVERITIES,
    INCIDENT_STATUSES,
    STATE_FILENAMES,
    bootstrap_payload_for,
)


def issue(path: str, message: str) -> dict[str, str]:
    return {"path": path, "message": message}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_object(value: Any, path: str, errors: list[dict[str, str]]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(issue(path, "must be an object"))
        return None
    return value


def ensure_list(value: Any, path: str, errors: list[dict[str, str]]) -> list[Any] | None:
    if not isinstance(value, list):
        errors.append(issue(path, "must be a list"))
        return None
    return value


def ensure_string(value: Any, path: str, errors: list[dict[str, str]], allow_null: bool = False) -> None:
    if value is None and allow_null:
        return
    if not isinstance(value, str):
        errors.append(issue(path, "must be a string"))


def validate_active_tasks(payload: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    data = ensure_object(payload, "active-tasks", errors)
    if data is None:
        return {"ok": False, "errors": errors}
    meta = ensure_object(data.get("meta", {}), "active-tasks.meta", errors)
    tasks = ensure_object(data.get("tasks", {}), "active-tasks.tasks", errors)
    if meta is not None and "updatedAt" in meta:
        ensure_string(meta["updatedAt"], "active-tasks.meta.updatedAt", errors, allow_null=True)
    if tasks is not None:
        for task_id, task in tasks.items():
            path = f"active-tasks.tasks.{task_id}"
            node = ensure_object(task, path, errors)
            if node is None:
                continue
            if "id" in node:
                ensure_string(node["id"], f"{path}.id", errors)
            if "status" in node:
                ensure_string(node["status"], f"{path}.status", errors)
                if isinstance(node["status"], str) and node["status"] not in ACTIVE_TASK_STATUSES:
                    errors.append(issue(f"{path}.status", f"must be one of {sorted(ACTIVE_TASK_STATUSES)}"))
            for key in ("createdAt", "openedAt", "updatedAt", "ownerAgent", "summary", "targetAgent", "targetSessionKey", "source", "dueAt", "lastAlertAt", "lastWatchdogAt", "lastError"):
                if key in node:
                    ensure_string(node[key], f"{path}.{key}", errors, allow_null=True)
            if "staleAfterSeconds" in node and not isinstance(node["staleAfterSeconds"], int):
                errors.append(issue(f"{path}.staleAfterSeconds", "must be an integer"))
            if "alertCount" in node and not isinstance(node["alertCount"], int):
                errors.append(issue(f"{path}.alertCount", "must be an integer"))
            if "deliverables" in node:
                rows = ensure_list(node["deliverables"], f"{path}.deliverables", errors)
                if rows is not None:
                    for idx, item in enumerate(rows):
                        ensure_string(item, f"{path}.deliverables[{idx}]", errors)
            if "tags" in node:
                rows = ensure_list(node["tags"], f"{path}.tags", errors)
                if rows is not None:
                    for idx, item in enumerate(rows):
                        ensure_string(item, f"{path}.tags[{idx}]", errors)
            if "closure" in node:
                closure = ensure_object(node["closure"], f"{path}.closure", errors)
                if closure is not None:
                    for key in ("closedAt", "closedBy", "note"):
                        if key in closure:
                            ensure_string(closure[key], f"{path}.closure.{key}", errors, allow_null=True)
                    if "forced" in closure and not isinstance(closure["forced"], bool):
                        errors.append(issue(f"{path}.closure.forced", "must be a boolean"))
                    if "missingDeliverablesAtClose" in closure:
                        rows = ensure_list(closure["missingDeliverablesAtClose"], f"{path}.closure.missingDeliverablesAtClose", errors)
                        if rows is not None:
                            for idx, item in enumerate(rows):
                                ensure_string(item, f"{path}.closure.missingDeliverablesAtClose[{idx}]", errors)
    return {"ok": not errors, "errors": errors}


def validate_delegations(payload: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    data = ensure_object(payload, "delegations", errors)
    if data is None:
        return {"ok": False, "errors": errors}
    delegations = ensure_object(data.get("delegations", {}), "delegations.delegations", errors)
    if delegations is not None:
        for delegation_id, delegation in delegations.items():
            path = f"delegations.delegations.{delegation_id}"
            node = ensure_object(delegation, path, errors)
            if node is None:
                continue
            for key in ("id", "startedAt", "status", "lastCheck", "lastError", "severity", "fromAgent", "toAgent", "sessionKey", "failedAt", "lastAlertAt", "lastAlertState", "dueAt"):
                if key in node:
                    ensure_string(node[key], f"{path}.{key}", errors, allow_null=True)
            if "status" in node and isinstance(node["status"], str) and node["status"] not in DELEGATION_STATUSES:
                errors.append(issue(f"{path}.status", f"must be one of {sorted(DELEGATION_STATUSES)}"))
            for key in ("alertCount", "timeoutSeconds", "graceSeconds"):
                if key in node and not isinstance(node[key], int):
                    errors.append(issue(f"{path}.{key}", "must be an integer"))
            if "isTest" in node and not isinstance(node["isTest"], bool):
                errors.append(issue(f"{path}.isTest", "must be a boolean"))
            if "deliverables" in node:
                rows = ensure_list(node["deliverables"], f"{path}.deliverables", errors)
                if rows is not None:
                    for idx, item in enumerate(rows):
                        ensure_string(item, f"{path}.deliverables[{idx}]", errors)
    return {"ok": not errors, "errors": errors}


def validate_watchdog(payload: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    data = ensure_object(payload, "system-operational-watchdog", errors)
    if data is None:
        return {"ok": False, "errors": errors}
    meta = ensure_object(data.get("meta", {}), "system-operational-watchdog.meta", errors)
    incidents = ensure_object(data.get("incidents", {}), "system-operational-watchdog.incidents", errors)
    deliverables = ensure_object(data.get("deliverables", {}), "system-operational-watchdog.deliverables", errors)
    if meta is not None:
        for key, value in meta.items():
            if value is None:
                continue
            if key.endswith("At"):
                ensure_string(value, f"system-operational-watchdog.meta.{key}", errors, allow_null=True)
            elif not isinstance(value, int):
                errors.append(issue(f"system-operational-watchdog.meta.{key}", "must be an integer or null"))
    if incidents is not None:
        for incident_id, incident in incidents.items():
            path = f"system-operational-watchdog.incidents.{incident_id}"
            node = ensure_object(incident, path, errors)
            if node is None:
                continue
            for key in ("id", "signature", "category", "severity", "summary", "source", "evidenceHash", "reportPath", "status", "createdAt", "updatedAt", "firstSeenAt", "lastSeenAt", "lastDispatchAt", "lastMainEventAt", "reportSeenAt"):
                if key in node:
                    ensure_string(node[key], f"{path}.{key}", errors, allow_null=True)
            if "severity" in node and isinstance(node["severity"], str) and node["severity"] not in INCIDENT_SEVERITIES:
                errors.append(issue(f"{path}.severity", f"must be one of {sorted(INCIDENT_SEVERITIES)}"))
            if "status" in node and isinstance(node["status"], str) and node["status"] not in INCIDENT_STATUSES:
                errors.append(issue(f"{path}.status", f"must be one of {sorted(INCIDENT_STATUSES)}"))
            for key in ("dispatchCount", "mainEventCount"):
                if key in node and not isinstance(node[key], int):
                    errors.append(issue(f"{path}.{key}", "must be an integer"))
            if "routes" in node:
                rows = ensure_list(node["routes"], f"{path}.routes", errors)
                if rows is not None:
                    for idx, item in enumerate(rows):
                        ensure_string(item, f"{path}.routes[{idx}]", errors)
            if "evidence" in node:
                rows = ensure_list(node["evidence"], f"{path}.evidence", errors)
                if rows is not None:
                    for idx, item in enumerate(rows):
                        ensure_string(item, f"{path}.evidence[{idx}]", errors)
    if deliverables is not None:
        for deliverable_path, deliverable in deliverables.items():
            path = f"system-operational-watchdog.deliverables.{deliverable_path}"
            node = ensure_object(deliverable, path, errors)
            if node is None:
                continue
            for key, value in node.items():
                if key.endswith("At"):
                    ensure_string(value, f"{path}.{key}", errors, allow_null=True)
                elif isinstance(value, (str, int, bool)) or value is None:
                    continue
                else:
                    errors.append(issue(f"{path}.{key}", "must be a string, integer, boolean, null, or a nested public-safe object"))
    return {"ok": not errors, "errors": errors}


def state_path_map(state_dir: Path) -> dict[str, Path]:
    return {
        "active_tasks": state_dir / STATE_FILENAMES["active_tasks"],
        "delegations": state_dir / STATE_FILENAMES["delegations"],
        "watchdog": state_dir / STATE_FILENAMES["watchdog"],
    }


def bootstrap_state_dir(state_dir: Path, force: bool = False) -> dict[str, Any]:
    files = state_path_map(state_dir)
    created: list[str] = []
    skipped: list[str] = []
    for path in files.values():
        if path.exists() and not force:
            skipped.append(path.name)
            continue
        write_json(path, bootstrap_payload_for(path.name))
        created.append(path.name)
    return {
        "ok": True,
        "state_dir": str(state_dir.resolve()),
        "created": created,
        "skipped": skipped,
    }


def validate_state_dir(state_dir: Path) -> dict[str, Any]:
    files = state_path_map(state_dir)
    errors: list[dict[str, str]] = []
    results: dict[str, Any] = {}
    validators = {
        "active_tasks": validate_active_tasks,
        "delegations": validate_delegations,
        "watchdog": validate_watchdog,
    }
    for key, path in files.items():
        if not path.exists():
            errors.append(issue(path.name, "missing state file"))
            continue
        try:
            payload = load_json(path)
        except Exception as exc:
            errors.append(issue(path.name, f"failed to parse JSON: {exc}"))
            continue
        result = validators[key](payload)
        results[key] = result
        for row in result["errors"]:
            errors.append(issue(f"{path.name}:{row['path']}", row["message"]))
    return {
        "ok": not errors,
        "state_dir": str(state_dir.resolve()),
        "errors": errors,
        "results": results,
    }


def summarize_state_dir(state_dir: Path) -> dict[str, Any]:
    files = state_path_map(state_dir)
    payload = validate_state_dir(state_dir)
    summary = {
        "state_dir": payload["state_dir"],
        "active_tasks_total": 0,
        "active_tasks_open": 0,
        "delegations_total": 0,
        "delegations_open": 0,
        "incidents_total": 0,
        "incidents_open": 0,
        "high_severity_incidents": 0,
    }
    if not payload["ok"]:
        return {"ok": False, "errors": payload["errors"], "summary": summary}

    active = load_json(files["active_tasks"])
    tasks = active.get("tasks", {})
    summary["active_tasks_total"] = len(tasks)
    summary["active_tasks_open"] = sum(1 for item in tasks.values() if isinstance(item, dict) and item.get("status") in {"open", "acked", "blocked"})

    delegations = load_json(files["delegations"]).get("delegations", {})
    summary["delegations_total"] = len(delegations)
    summary["delegations_open"] = sum(1 for item in delegations.values() if isinstance(item, dict) and item.get("status") in {"sent", "accepted", "pending", "in_progress", "late"})

    incidents = load_json(files["watchdog"]).get("incidents", {})
    summary["incidents_total"] = len(incidents)
    summary["incidents_open"] = sum(1 for item in incidents.values() if isinstance(item, dict) and item.get("status") == "open")
    summary["high_severity_incidents"] = sum(1 for item in incidents.values() if isinstance(item, dict) and item.get("severity") in {"high", "critical"})

    return {"ok": True, "summary": summary}


def render_human_bootstrap(payload: dict[str, Any]) -> str:
    lines = [
        "=== HyperClaw-Max Ops Fabric Bootstrap ===",
        f"State dir: {payload['state_dir']}",
    ]
    for name in payload["created"]:
        lines.append(f"- created: {name}")
    for name in payload["skipped"]:
        lines.append(f"- skipped: {name}")
    lines.append("Overall: OK")
    return "\n".join(lines)


def render_human_validate(payload: dict[str, Any]) -> str:
    lines = [
        "=== HyperClaw-Max Ops Fabric Validate ===",
        f"State dir: {payload['state_dir']}",
    ]
    if payload["errors"]:
        for row in payload["errors"]:
            lines.append(f"- error: {row['path']}: {row['message']}")
    lines.append(f"Overall: {'OK' if payload['ok'] else 'FAIL'}")
    return "\n".join(lines)


def render_human_summary(payload: dict[str, Any]) -> str:
    lines = ["=== HyperClaw-Max Ops Fabric Summary ==="]
    if not payload["ok"]:
        for row in payload["errors"]:
            lines.append(f"- error: {row['path']}: {row['message']}")
        lines.append("Overall: FAIL")
        return "\n".join(lines)
    summary = payload["summary"]
    lines.append(f"State dir: {summary['state_dir']}")
    lines.append(f"- active tasks: {summary['active_tasks_total']} total / {summary['active_tasks_open']} open")
    lines.append(f"- delegations: {summary['delegations_total']} total / {summary['delegations_open']} open")
    lines.append(f"- incidents: {summary['incidents_total']} total / {summary['incidents_open']} open")
    lines.append(f"- high severity incidents: {summary['high_severity_incidents']}")
    lines.append("Overall: OK")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap and validate public-safe HyperClaw-Max operational fabric state")
    sub = ap.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--state-dir", type=Path, default=Path("runtime/state"))
    common.add_argument("--format", choices=["json", "human"], default="human")

    bootstrap = sub.add_parser("bootstrap", parents=[common], help="Create empty public-safe ops fabric state files")
    bootstrap.add_argument("--force", action="store_true", help="Overwrite existing state files")

    sub.add_parser("validate", parents=[common], help="Validate ops fabric state files")
    sub.add_parser("summary", parents=[common], help="Summarize ops fabric state")

    args = ap.parse_args()
    state_dir = args.state_dir.resolve()

    if args.command == "bootstrap":
        payload = bootstrap_state_dir(state_dir, force=args.force)
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_human_bootstrap(payload))
        return 0

    if args.command == "validate":
        payload = validate_state_dir(state_dir)
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_human_validate(payload))
        return 0 if payload["ok"] else 1

    payload = summarize_state_dir(state_dir)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_human_summary(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
