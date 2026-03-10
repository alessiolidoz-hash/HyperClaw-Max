from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pack import build_pack

DEFAULT_FIXTURES = Path("fixtures/context_intel/failure-clinic-cases-v1.jsonl")


@dataclass
class Pattern:
    category: str
    severity: str
    routes: list[str]
    summary: str
    probable_cause: str
    next_step: str
    query_seed: str
    regexes: list[str]


PATTERNS = [
    Pattern(
        category="gateway_memory_drift",
        severity="high",
        routes=["codex", "hk"],
        summary="Gateway memory sync drift or embedding provider mismatch",
        probable_cause="The memory subsystem is invoking the wrong embedding provider or an older path is bypassing local embedding configuration.",
        next_step="Verify the active provider, then inspect the path that still points at a remote embedding flow.",
        query_seed="gateway memory sync drift openai embeddings failed 401 provider local embeddinggemma",
        regexes=[r"openai embeddings failed: 401", r"memory sync failed", r"provider=local"],
    ),
    Pattern(
        category="gateway_model_policy",
        severity="high",
        routes=["codex", "hk"],
        summary="Gateway rejected a model selection or transport policy",
        probable_cause="Model allowlist or routing policy does not match the active agent/session path.",
        next_step="Check model policy, session path, and transport mapping before changing config or dist behavior.",
        query_seed="gpt-5.4 transport fallback context token reset model switch",
        regexes=[r"model not allowed", r"gpt-5\.4", r"transport", r"sessions_spawn"],
    ),
    Pattern(
        category="provider_rate_limit",
        severity="medium",
        routes=["codex", "hk"],
        summary="Provider rate limit detected",
        probable_cause="Burst traffic or retries exceeded quota or concurrency headroom.",
        next_step="Reduce concurrency, add cooldown, and inspect the hot path creating repeated requests.",
        query_seed="provider rate limit 429 gateway retry concurrency cooldown",
        regexes=[r"rate_limit_error", r"rate limit", r"429"],
    ),
    Pattern(
        category="gateway_operator_scope",
        severity="medium",
        routes=["codex", "hk"],
        summary="Gateway operator.read scope failure",
        probable_cause="The caller lacks operator.read scope for the requested RPC route.",
        next_step="Align the caller auth scope or use a local transport path that already has the needed permission.",
        query_seed="operator.read sessions.list route.ts gateway rpc",
        regexes=[r"missing scope: operator\.read"],
    ),
    Pattern(
        category="gateway_operator_pairing_scope",
        severity="medium",
        routes=["codex", "hk"],
        summary="Gateway operator.pairing scope failure",
        probable_cause="The caller lacks operator.pairing scope for a pairing or device route.",
        next_step="Inspect the auth scope and pairing path before retrying the action.",
        query_seed="operator.pairing device pairing gateway rpc mission control",
        regexes=[r"missing scope: operator\.pairing"],
    ),
    Pattern(
        category="pa_hook_unforwarded",
        severity="medium",
        routes=["pa", "hk"],
        summary="PA hook not handled or escalated cleanly",
        probable_cause="PA neither notified the owner directly nor escalated the item through the expected dispatch path.",
        next_step="Verify the direct-vs-escalation rule and then inspect the task capture or watchdog path.",
        query_seed="PA hook direct telegram sessions_send agent:main:main native task capture",
        regexes=[r"PA hook not handled or escalated", r"PA HOOK ALERT", r"agent:main:main", r"replyStatus=timeout"],
    ),
    Pattern(
        category="calendar_push_invalid_token",
        severity="high",
        routes=["pa", "hk"],
        summary="Calendar push receiver rejected token",
        probable_cause="Receiver token drift or stale watch registration.",
        next_step="Re-apply the watch token, restart the receiver, and validate with a push healthcheck.",
        query_seed="calendar push invalid token receiver watch renewal",
        regexes=[r"calendar push receiver rejected token", r"invalid token", r"calendar-push-receiver"],
    ),
    Pattern(
        category="browser_relay_attach_missing",
        severity="medium",
        routes=["codex", "hk"],
        summary="Browser relay listener active but no attached tab",
        probable_cause="The relay server is reachable but no browser tab is attached to the session.",
        next_step="Check relay status and attach a real tab before debugging the server path.",
        query_seed="browser relay bind host wildcard rewrite tab not found",
        regexes=[r"tab not found", r"cdpReady=false", r"browser relay", r"no tabs"],
    ),
]


def load_fixtures(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            items.append(json.loads(line))
    return items


def classify_text(text: str) -> dict[str, Any]:
    low = text.lower()
    best = None
    best_score = -1
    for pattern in PATTERNS:
        matched = [rx for rx in pattern.regexes if re.search(rx, low, re.IGNORECASE)]
        if not matched:
            continue
        score = len(matched)
        if score > best_score:
            best_score = score
            best = (pattern, matched)
    if best is None:
        return {
            "category": "unclassified",
            "severity": "unknown",
            "routes": [],
            "summary": "No clinic pattern matched",
            "probable_cause": "No known failure signature matched the supplied evidence.",
            "next_step": "Escalate to manual triage and gather a tighter excerpt.",
            "query_seed": None,
            "matched_regexes": [],
        }
    pattern, matched = best
    return {
        "category": pattern.category,
        "severity": pattern.severity,
        "routes": pattern.routes,
        "summary": pattern.summary,
        "probable_cause": pattern.probable_cause,
        "next_step": pattern.next_step,
        "query_seed": pattern.query_seed,
        "matched_regexes": matched,
    }


def evaluate_fixtures(path: Path) -> dict[str, Any]:
    rows = []
    fixtures = load_fixtures(path)
    for row in fixtures:
        result = classify_text(row["text"])
        rows.append(
            {
                "case_id": row["case_id"],
                "expected_category": row["expected_category"],
                "actual_category": result["category"],
                "ok": row["expected_category"] == result["category"],
            }
        )
    accuracy = round(sum(1 for row in rows if row["ok"]) / len(rows), 4) if rows else 0.0
    return {"summary": {"count": len(rows), "accuracy": accuracy}, "rows": rows}


def render_human(result: dict[str, Any]) -> str:
    lines = [
        "=== Failure Diagnostics Clinic ===",
        f"Category: {result['category']} | Severity: {result['severity']}",
        f"Routes: {', '.join(result.get('routes', [])) or '-'}",
        f"Summary: {result['summary']}",
        "",
        "Probable cause:",
        f"- {result['probable_cause']}",
        "",
        "Next step:",
        f"- {result['next_step']}",
    ]
    if result.get("query_seed"):
        lines.extend(["", "Query seed:", f"- {result['query_seed']}"])
    if result.get("pack"):
        assess = result["pack"]["compare_assessment"]
        lines.extend(["", "Pack assessment:", f"- {assess['status']}"])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Failure diagnostics clinic")
    ap.add_argument("--text")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--with-pack", action="store_true")
    ap.add_argument("--pack-profile", choices=["terse", "standard", "full"], default="terse")
    ap.add_argument("--repo-intel-cmd", default=None)
    ap.add_argument("--eval", type=Path)
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args()

    if args.eval:
        payload = evaluate_fixtures(args.eval)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not args.text:
        raise SystemExit("--text or --eval is required")

    result = classify_text(args.text)
    if args.with_pack and result.get("query_seed"):
        result["pack"] = build_pack(
            result["query_seed"],
            repo=args.repo,
            profile=args.pack_profile,
            repo_intel_cmd=args.repo_intel_cmd,
        )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_human(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
