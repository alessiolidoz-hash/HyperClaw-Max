from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .pack import build_pack

DEFAULT_CASES = Path("fixtures/context_intel/canonical-cases-v1.jsonl")
DEFAULT_OUTDIR = Path("artifacts/context_intel/baseline-runs")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        cases.append(json.loads(line))
    return cases


def expected_hits(blob: str, signals: list[str]) -> int:
    low = blob.lower()
    return sum(1 for sig in signals if sig.lower() in low)


def validate_contract(item: dict[str, Any]) -> None:
    required = {
        "contract_version",
        "case_id",
        "title",
        "query",
        "mode",
        "toolchain",
        "metrics",
        "result_pack",
        "provenance",
    }
    missing = sorted(required - set(item.keys()))
    if missing:
        raise ValueError(f"missing keys: {missing}")


def run_baseline(cases_path: Path, outdir: Path, repo: Path, repo_intel_cmd: str | None = None, limit_cases: int = 0) -> dict[str, Any]:
    cases = load_cases(cases_path)
    if limit_cases > 0:
        cases = cases[:limit_cases]

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = outdir / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    results = []
    aggregate = {
        "generated_at": now_utc(),
        "case_count": len(cases),
        "avg_pack_latency_ms": 0.0,
        "tier5_case_hits": 0,
        "local_case_hits": 0,
        "expected_signal_hits": 0,
    }

    total_pack_latency = 0
    for case in cases:
        pack = build_pack(case["query"], repo=repo, profile="terse", repo_intel_cmd=repo_intel_cmd, symbol_slicing="python-only")
        blob = json.dumps(pack, ensure_ascii=False)
        signal_hits = expected_hits(blob, case.get("expected_signals", []))
        repo_intel_count = len(pack["repo_intel_candidates"])
        contract = {
            "contract_version": "v1",
            "case_id": case["case_id"],
            "title": case["title"],
            "query": case["query"],
            "mode": case.get("mode", "technical"),
            "toolchain": ["hyperclaw_context_pack"],
            "metrics": {
                "fusion_latency_ms": 0,
                "compare_latency_ms": pack["metrics"]["repo_intel_latency_ms"],
                "local_hit_count": len(pack["local_candidates"]),
                "tier5_hit_count": repo_intel_count,
                "compare_live_hits": repo_intel_count,
                "compare_release_hits": 0,
                "expected_signal_hits": signal_hits,
            },
            "result_pack": {
                "problem": case["title"],
                "local_candidates": pack["local_candidates"],
                "upstream_candidates": pack["repo_intel_candidates"],
                "release_candidates": [],
                "next_actions": pack["next_actions"],
            },
            "provenance": {
                "query_fusion": {
                    "engine": "hyperclaw_context_pack",
                    "metadata": {"query_signature": pack["problem"]["query_signature"]},
                },
                "compare_mode": {
                    "engine": "repo_intel_adapter",
                    "status": pack["compare_assessment"]["status"],
                },
            },
        }
        validate_contract(contract)
        total_pack_latency += int(pack["metrics"]["repo_intel_latency_ms"])
        results.append(contract)

    if results:
        aggregate["avg_pack_latency_ms"] = round(total_pack_latency / len(results), 2)
        aggregate["tier5_case_hits"] = sum(1 for r in results if r["metrics"]["tier5_hit_count"] > 0)
        aggregate["local_case_hits"] = sum(1 for r in results if r["metrics"]["local_hit_count"] > 0)
        aggregate["expected_signal_hits"] = sum(r["metrics"]["expected_signal_hits"] for r in results)

    json_path = run_dir / "baseline.json"
    md_path = run_dir / "baseline.md"
    json_path.write_text(json.dumps({"aggregate": aggregate, "cases": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# HyperClaw-Max Context Intelligence Baseline",
        "",
        f"Generated: {aggregate['generated_at']}",
        f"Cases: {aggregate['case_count']}",
        f"Avg pack latency: {aggregate['avg_pack_latency_ms']} ms",
        f"Cases with local hits: {aggregate['local_case_hits']}",
        f"Cases with repo-intel hits: {aggregate['tier5_case_hits']}",
        f"Expected signal hits: {aggregate['expected_signal_hits']}",
        "",
    ]
    for item in results:
        lines.extend(
            [
                f"## {item['case_id']}",
                f"- Title: {item['title']}",
                f"- Query: `{item['query']}`",
                f"- Local hits: `{item['metrics']['local_hit_count']}` | Repo-intel hits: `{item['metrics']['tier5_hit_count']}`",
                f"- Expected signal hits: `{item['metrics']['expected_signal_hits']}`",
                "",
            ]
        )
    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"ok": True, "outdir": str(run_dir), "json": str(json_path), "markdown": str(md_path), "aggregate": aggregate}


def main() -> int:
    ap = argparse.ArgumentParser(description="HyperClaw-Max baseline harness")
    ap.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    ap.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--repo-intel-cmd", default=None)
    ap.add_argument("--limit-cases", type=int, default=0)
    args = ap.parse_args()
    payload = run_baseline(args.cases, args.outdir, args.repo.resolve(), args.repo_intel_cmd, args.limit_cases)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
