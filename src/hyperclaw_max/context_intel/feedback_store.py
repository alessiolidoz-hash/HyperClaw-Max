from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

DEFAULT_LOG = Path("artifacts/context_intel/feedback-events-v1.jsonl")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_query_signature(query: str) -> str:
    compact = " ".join(query.lower().split())
    return sha256(compact.encode("utf-8")).hexdigest()[:16]


def load_events(path: Path = DEFAULT_LOG) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def append_event(event: dict[str, Any], path: Path = DEFAULT_LOG) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def summarize_feedback(query_signature: str, path: Path = DEFAULT_LOG) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "sum_votes": 0,
            "support": 0,
            "raw_support": 0,
            "reason_codes": set(),
            "sources": set(),
            "operators": set(),
            "max_dirty_count": 0,
            "latest_ts": None,
            "seen_keys": set(),
        }
    )
    for row in load_events(path):
        if row.get("query_signature") != query_signature:
            continue
        candidate_id = str(row.get("candidate_id") or "")
        if not candidate_id:
            continue
        bucket = grouped[candidate_id]
        bucket["raw_support"] += 1
        dedupe_key = (
            row.get("source"),
            row.get("case_id"),
            row.get("query_signature"),
            row.get("candidate_id"),
            row.get("vote"),
            row.get("reason_code"),
            row.get("operator"),
        )
        if dedupe_key in bucket["seen_keys"]:
            continue
        bucket["seen_keys"].add(dedupe_key)
        vote = int(row.get("vote", 0))
        bucket["sum_votes"] += vote
        bucket["support"] += 1
        if row.get("reason_code"):
            bucket["reason_codes"].add(str(row["reason_code"]))
        if row.get("source"):
            bucket["sources"].add(str(row["source"]))
        if row.get("operator"):
            bucket["operators"].add(str(row["operator"]))
        dirty = int(row.get("git", {}).get("dirty_count", 0)) if isinstance(row.get("git"), dict) else 0
        bucket["max_dirty_count"] = max(bucket["max_dirty_count"], dirty)
        bucket["latest_ts"] = max(filter(None, [bucket["latest_ts"], row.get("ts")]), default=row.get("ts"))
    out: dict[str, dict[str, Any]] = {}
    for candidate_id, bucket in grouped.items():
        out[candidate_id] = {
            "sum_votes": bucket["sum_votes"],
            "support": bucket["support"],
            "raw_support": bucket["raw_support"],
            "reason_codes": sorted(bucket["reason_codes"]),
            "sources": sorted(bucket["sources"]),
            "operators": sorted(bucket["operators"]),
            "max_dirty_count": bucket["max_dirty_count"],
            "latest_ts": bucket["latest_ts"],
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Context-intel feedback event recorder / inspector")
    sub = ap.add_subparsers(dest="cmd", required=True)

    rec = sub.add_parser("record")
    rec.add_argument("--query", required=True)
    rec.add_argument("--candidate-id", required=True)
    rec.add_argument("--vote", type=int, choices=[-1, 1], required=True)
    rec.add_argument("--reason-code", required=True)
    rec.add_argument("--source", default="manual")
    rec.add_argument("--case-id", default="")
    rec.add_argument("--candidate-kind", default="local_file")
    rec.add_argument("--artifact", default="")
    rec.add_argument("--operator", default="hyperclaw")
    rec.add_argument("--git-branch", default="")
    rec.add_argument("--git-dirty-count", type=int, default=0)
    rec.add_argument("--log", type=Path, default=DEFAULT_LOG)

    show = sub.add_parser("show")
    show.add_argument("--query", required=True)
    show.add_argument("--log", type=Path, default=DEFAULT_LOG)

    args = ap.parse_args()

    if args.cmd == "record":
        query_signature = normalize_query_signature(args.query)
        event = {
            "ts": now_utc(),
            "event_id": sha256(
                f"{now_utc()}|{args.query}|{args.candidate_id}|{args.vote}|{args.reason_code}".encode("utf-8")
            ).hexdigest()[:16],
            "source": args.source,
            "case_id": args.case_id,
            "query_signature": query_signature,
            "candidate_kind": args.candidate_kind,
            "candidate_id": args.candidate_id,
            "vote": args.vote,
            "reason_code": args.reason_code,
            "artifact": args.artifact,
            "operator": args.operator,
            "git": {"branch": args.git_branch, "dirty_count": args.git_dirty_count},
        }
        append_event(event, args.log)
        print(json.dumps({"ok": True, "event": event, "log": str(args.log)}, ensure_ascii=False, indent=2))
        return 0

    payload = {
        "ok": True,
        "query_signature": normalize_query_signature(args.query),
        "feedback": summarize_feedback(normalize_query_signature(args.query), args.log),
        "log": str(args.log),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
