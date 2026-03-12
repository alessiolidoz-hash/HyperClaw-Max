from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


ACTIVE_TASK_STATUSES = {"open", "acked", "blocked", "done", "failed", "cancelled"}
DELEGATION_STATUSES = {"sent", "accepted", "pending", "in_progress", "done", "late", "failed", "cancelled"}
INCIDENT_STATUSES = {"open", "resolved", "suppressed"}
INCIDENT_SEVERITIES = {"low", "medium", "high", "critical", "none"}

STATE_FILENAMES = {
    "active_tasks": "active-tasks.json",
    "delegations": "delegations.json",
    "watchdog": "system-operational-watchdog.json",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def empty_active_tasks() -> dict[str, Any]:
    return {
        "meta": {
            "updatedAt": now_iso(),
        },
        "tasks": {},
    }


def empty_delegations() -> dict[str, Any]:
    return {
        "delegations": {},
    }


def empty_watchdog() -> dict[str, Any]:
    return {
        "meta": {
            "lastRunAt": None,
            "openTasks": 0,
            "openDelegations": 0,
            "gatewayIssues": 0,
            "unitIssues": 0,
            "cronIssues": 0,
            "candidates": 0,
            "dispatches": 0,
            "deliverableActivity": 0,
            "normalizedOwnerVisibleTasks": 0,
            "resolved": 0,
        },
        "incidents": {},
        "deliverables": {},
    }


EMPTY_STATE_PAYLOADS = {
    STATE_FILENAMES["active_tasks"]: empty_active_tasks,
    STATE_FILENAMES["delegations"]: empty_delegations,
    STATE_FILENAMES["watchdog"]: empty_watchdog,
}


def bootstrap_payload_for(filename: str) -> dict[str, Any]:
    factory = EMPTY_STATE_PAYLOADS[filename]
    return deepcopy(factory())
