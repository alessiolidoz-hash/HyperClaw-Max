from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .baseline import DEFAULT_CASES, run_baseline
from .clinic import DEFAULT_FIXTURES, evaluate_fixtures
from .pack import build_pack

OUTDIR = Path("artifacts/context_intel/scorecards")


def load_cases(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            items.append(json.loads(line))
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description="HyperClaw-Max context-intel scorecard")
    ap.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    ap.add_argument("--failure-cases", type=Path, default=DEFAULT_FIXTURES)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--repo-intel-cmd", default=None)
    ap.add_argument("--limit-cases", type=int, default=0)
    args = ap.parse_args()

    outdir = OUTDIR / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir.mkdir(parents=True, exist_ok=True)

    baseline = run_baseline(args.cases, outdir, args.repo.resolve(), args.repo_intel_cmd, args.limit_cases)
    clinic = evaluate_fixtures(args.failure_cases)
    cases = load_cases(args.cases)
    if args.limit_cases > 0:
        cases = cases[: args.limit_cases]

    pack_rows = []
    for case in cases:
        pack = build_pack(case["query"], repo=args.repo.resolve(), profile="terse", repo_intel_cmd=args.repo_intel_cmd)
        pack_rows.append(
            {
                "case_id": case["case_id"],
                "query": case["query"],
                "tokens": pack["metrics"]["approx_tokens"],
                "chars": pack["metrics"]["approx_chars"],
                "citations": pack["metrics"]["citation_count"],
                "assessment": pack["compare_assessment"]["status"],
                "local_candidates": len(pack["local_candidates"]),
                "repo_intel_candidates": len(pack["repo_intel_candidates"]),
            }
        )

    assessment_counts: dict[str, int] = {}
    for row in pack_rows:
        assessment_counts[row["assessment"]] = assessment_counts.get(row["assessment"], 0) + 1

    summary: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "clinic_accuracy": clinic["summary"]["accuracy"],
        "pack_case_count": len(pack_rows),
        "pack_avg_tokens": round(sum(r["tokens"] for r in pack_rows) / len(pack_rows), 2) if pack_rows else 0.0,
        "pack_avg_citations": round(sum(r["citations"] for r in pack_rows) / len(pack_rows), 2) if pack_rows else 0.0,
        "pack_cases_with_local_candidates": sum(1 for r in pack_rows if r["local_candidates"] > 0),
        "pack_cases_with_repo_intel_candidates": sum(1 for r in pack_rows if r["repo_intel_candidates"] > 0),
        "assessment_counts": assessment_counts,
        "baseline": baseline["aggregate"],
    }

    payload = {"summary": summary, "packs": pack_rows, "clinic": clinic, "baseline": baseline}
    (outdir / "scorecard.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        "# HyperClaw-Max Context Intel Scorecard",
        "",
        f"Generated: {summary['generated_at']}",
        f"Clinic accuracy: {summary['clinic_accuracy']}",
        f"Pack avg tokens: {summary['pack_avg_tokens']}",
        f"Pack avg citations: {summary['pack_avg_citations']}",
        "",
        "## Assessments",
    ]
    for key, value in sorted(assessment_counts.items()):
        md_lines.append(f"- {key}: {value}")
    md_lines.extend(["", "## Pack cases"])
    for row in pack_rows:
        md_lines.append(
            f"- {row['case_id']}: tokens={row['tokens']} citations={row['citations']} assessment={row['assessment']}"
        )
    (outdir / "scorecard.md").write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "outdir": str(outdir), "summary": summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
