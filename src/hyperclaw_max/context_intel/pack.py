from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .feedback_store import normalize_query_signature, summarize_feedback
from .symbol_slice import slice_python_symbol

STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "what", "when", "where",
    "which", "about", "into", "your", "have", "has", "had", "was", "were", "are",
    "been", "will", "would", "could", "should", "can", "how", "why", "who", "all",
    "any", "our", "their", "them", "its", "but", "not", "than", "then", "also",
    "over", "under", "via", "per", "agent", "session", "sessions",
}
IGNORE_GLOBS = [
    "--glob", "!.git/**",
    "--glob", "!node_modules/**",
    "--glob", "!artifacts/**",
    "--glob", "!logs/**",
    "--glob", "!tmp/**",
    "--glob", "!tests/**",
    "--glob", "!fixtures/**",
    "--glob", "!examples/**",
    "--glob", "!docs/**",
    "--glob", "!**/__pycache__/**",
]
PROFILE_PRESETS: dict[str, dict[str, int]] = {
    "terse": {"limit": 3, "max_chars": 5200, "max_local_snippets": 1, "max_repo_intel": 2},
    "standard": {"limit": 5, "max_chars": 9000, "max_local_snippets": 2, "max_repo_intel": 4},
    "full": {"limit": 7, "max_chars": 14000, "max_local_snippets": 3, "max_repo_intel": 6},
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str], timeout: int = 120, cwd: Path | None = None) -> tuple[int, str, str, int]:
    started = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(cwd) if cwd else None)
    elapsed = int((time.perf_counter() - started) * 1000)
    return proc.returncode, proc.stdout, proc.stderr, elapsed


def extract_keywords(query: str, limit: int = 8) -> list[str]:
    out: list[str] = []
    seen = set()
    for token in re.findall(r"[a-z0-9][a-z0-9._/-]*", query.lower()):
        if len(token) < 3 or token in STOPWORDS:
            continue
        if token in seen:
            continue
        seen.add(token)
        out.append(token)
        if len(out) >= limit:
            break
    return out


def git_context(repo: Path) -> dict[str, Any]:
    if not (repo / ".git").exists():
        return {"repo": str(repo), "branch": None, "dirty_count": 0, "dirty_files": [], "diffstat": []}
    rc_b, out_b, _, _ = run(["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"], timeout=20)
    branch = out_b.strip() if rc_b == 0 else None
    rc_s, out_s, _, _ = run(["git", "-C", str(repo), "status", "--short"], timeout=30)
    dirty_files: list[dict[str, str]] = []
    if rc_s == 0:
        for raw in out_s.splitlines():
            if not raw.strip():
                continue
            status = raw[:2].strip() or "??"
            path = raw[3:].strip()
            dirty_files.append({"status": status, "path": path})
    rc_d, out_d, _, _ = run(["git", "-C", str(repo), "diff", "--stat"], timeout=45)
    return {
        "repo": str(repo),
        "branch": branch,
        "dirty_count": len(dirty_files),
        "dirty_files": dirty_files[:12],
        "diffstat": [line for line in out_d.splitlines() if line.strip()][:12] if rc_d == 0 else [],
    }


def fallback_search(repo: Path, keywords: list[str]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    lowered = [kw.lower() for kw in keywords]
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo).as_posix()
        if any(part in {".git", "node_modules", "__pycache__", "artifacts", "logs", "tmp"} for part in path.parts):
            continue
        if any(part in {"tests", "fixtures", "examples", "docs"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        matches = []
        for idx, line in enumerate(text.splitlines(), start=1):
            low = line.lower()
            if any(kw in low or kw in rel.lower() for kw in lowered):
                matches.append({"line": idx, "text": line.strip()[:220]})
                if len(matches) >= 2:
                    break
        if matches:
            grouped[str(path)] = matches
    return grouped


def search_repo(repo: Path, keywords: list[str], timeout: int = 60) -> dict[str, list[dict[str, Any]]]:
    if not keywords:
        return {}
    if shutil.which("rg") is None:
        return fallback_search(repo, keywords)
    cmd = ["rg", "-n", "-S", "-m", "2"]
    for kw in keywords:
        cmd.extend(["-e", kw])
    cmd.extend(IGNORE_GLOBS)
    cmd.append(str(repo))
    rc, out, _, _ = run(cmd, timeout=timeout)
    if rc not in {0, 1}:
        return fallback_search(repo, keywords)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for raw in out.splitlines():
        parts = raw.split(":", 2)
        if len(parts) != 3:
            continue
        path, line_no, text = parts
        grouped.setdefault(path, []).append({"line": int(line_no), "text": text.strip()[:220]})
    return grouped


def build_local_candidates(query: str, repo: Path, git_meta: dict[str, Any], hits: dict[str, list[dict[str, Any]]], limit: int) -> list[dict[str, Any]]:
    dirty_index = {entry["path"]: entry["status"] for entry in git_meta.get("dirty_files", [])}
    keywords = extract_keywords(query)
    candidates = []
    for path, snippets in hits.items():
        rel_path = Path(path).resolve().relative_to(repo.resolve()).as_posix()
        score = len(snippets)
        reasons = []
        path_matches = [kw for kw in keywords if kw in rel_path.lower()]
        text_matches = [kw for kw in keywords if any(kw in sn["text"].lower() for sn in snippets)]
        matched_keywords = list(dict.fromkeys(path_matches + text_matches))
        if path_matches:
            score += min(8, len(path_matches) * 3)
            reasons.append(f"path-match:{','.join(path_matches[:4])}")
        if text_matches:
            score += min(4, len(text_matches))
            reasons.append(f"text-match:{','.join(text_matches[:4])}")
        dirty_status = dirty_index.get(rel_path)
        if dirty_status:
            score += 2
            reasons.append(f"dirty:{dirty_status}")
        if rel_path.startswith("src/"):
            score += 2
            reasons.append("source-boost")
        if rel_path.endswith((".service", ".timer", ".sh")):
            score += 1
            reasons.append("ops-surface")
        if rel_path.endswith(".md"):
            score -= 2
            reasons.append("docs-deboost")
        elif rel_path.endswith((".json", ".jsonl")):
            score -= 1
            reasons.append("data-deboost")
        candidates.append(
            {
                "path": str(Path(path).resolve()),
                "rel_path": rel_path,
                "base_score": score,
                "feedback_delta": 0,
                "final_score": score,
                "score": score,
                "reasons": reasons,
                "feedback_reasons": [],
                "matched_keywords": matched_keywords[:6],
                "snippets": snippets[:2],
            }
        )
    candidates.sort(key=lambda item: (item["final_score"], item["rel_path"]), reverse=True)
    return candidates[:limit]


def apply_feedback_rerank(candidates: list[dict[str, Any]], *, query: str, mode: str, feedback_log: Path) -> list[dict[str, Any]]:
    if mode != "read-only" or not candidates:
        return candidates
    feedback = summarize_feedback(normalize_query_signature(query), feedback_log)
    reranked: list[dict[str, Any]] = []
    for item in candidates:
        row = dict(item)
        summary = feedback.get(row["rel_path"]) or {}
        support = int(summary.get("support", 0))
        sum_votes = int(summary.get("sum_votes", 0))
        dirty = int(summary.get("max_dirty_count", 0))
        sources = set(summary.get("sources") or [])
        if support < 2 or dirty > 0:
            if support == 1 and dirty == 0 and "accepted_candidate" in set(summary.get("reason_codes") or []) and sources & {"eval", "manual", "gold"}:
                delta = 1 if sum_votes > 0 else -1 if sum_votes < 0 else 0
                reasons = [f"feedback:{code}" for code in summary.get("reason_codes", [])[:3]]
                reasons.append("feedback:single-trusted-support")
            else:
                delta = 0
                reasons = []
        else:
            delta = max(-2, min(2, sum_votes))
            reasons = [f"feedback:{code}" for code in summary.get("reason_codes", [])[:3]]
            reasons.append("feedback:multi-support")
        row["feedback_delta"] = delta
        row["feedback_reasons"] = reasons
        row["final_score"] = row["base_score"] + delta
        row["score"] = row["final_score"]
        reranked.append(row)
    reranked.sort(key=lambda item: (item["final_score"], item["rel_path"]), reverse=True)
    return reranked


def enrich_symbol_slices(candidates: list[dict[str, Any]], *, mode: str) -> list[dict[str, Any]]:
    if mode != "python-only":
        return candidates
    enriched: list[dict[str, Any]] = []
    for item in candidates:
        row = dict(item)
        row.setdefault("slice_status", "not_requested")
        path = Path(row["path"])
        snippets = row.get("snippets") or []
        if path.suffix != ".py" or not snippets:
            enriched.append(row)
            continue
        payload = {"slice_status": "fallback_window"}
        attempted_lines: list[int] = []
        for snippet in snippets[:3]:
            line = int(snippet.get("line", 1))
            attempted_lines.append(line)
            payload = slice_python_symbol(path, line)
            if payload.get("slice_status") == "ok":
                break
        row.update(payload)
        row["slice_anchor_lines"] = attempted_lines
        enriched.append(row)
    return enriched


def build_repo_intel_candidates(repo_intel_payload: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    rows = repo_intel_payload.get("candidates") or []
    out = []
    for item in rows[:limit]:
        out.append(
            {
                "kind": item.get("kind") or "repo-intel",
                "locator": item.get("locator") or item.get("path") or "-",
                "name": item.get("name") or item.get("summary") or "-",
                "score": item.get("score", 0),
                "source": item.get("source") or "adapter",
            }
        )
    return out


def run_repo_intel_adapter(query: str, repo: Path, repo_intel_cmd: str | None, timeout: int) -> tuple[dict[str, Any], int]:
    if not repo_intel_cmd:
        return {"status": "adapter_not_configured", "candidates": []}, 0
    cmd = shlex.split(repo_intel_cmd) + [query, "--repo", str(repo)]
    rc, out, err, elapsed = run(cmd, timeout=timeout)
    if rc != 0:
        return {"status": "adapter_error", "stderr": err.strip(), "candidates": []}, elapsed
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        payload = {"status": "adapter_invalid_json", "stdout": out[:400], "candidates": []}
    if "status" not in payload:
        payload["status"] = "ok"
    if "candidates" not in payload:
        if isinstance(payload, list):
            payload = {"status": "ok", "candidates": payload}
        else:
            payload["candidates"] = []
    return payload, elapsed


def build_citations(local_candidates: list[dict[str, Any]], repo_intel_candidates: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = []
    for idx, item in enumerate(local_candidates[:4], start=1):
        snippet = (item.get("snippets") or [{}])[0]
        citations.append(
            {
                "citation_id": f"L{idx}",
                "source_kind": "local",
                "label": item.get("rel_path"),
                "locator": f"{item.get('rel_path')}:{snippet.get('line', 1)}",
                "reason": ",".join(item.get("reasons") or []) or "local-candidate",
                "evidence": str(snippet.get("text") or "")[:160],
            }
        )
    for idx, item in enumerate(repo_intel_candidates[:4], start=1):
        citations.append(
            {
                "citation_id": f"R{idx}",
                "source_kind": "repo_intel",
                "label": item.get("source") or "repo-intel",
                "locator": item.get("locator"),
                "reason": item.get("kind") or "repo-intel-candidate",
                "evidence": str(item.get("name") or "")[:160],
            }
        )
    return citations[:limit]


def compare_assessment(repo_intel_payload: dict[str, Any], repo_intel_candidates: list[dict[str, Any]]) -> dict[str, Any]:
    status = repo_intel_payload.get("status") or "unknown"
    if status == "adapter_not_configured":
        rationale = "No repo-intelligence adapter configured; local candidates only."
    elif status == "ok" and repo_intel_candidates:
        rationale = "Repo-intelligence adapter returned relevant candidates."
    elif status == "ok":
        rationale = "Repo-intelligence adapter is configured but returned no candidates."
    else:
        rationale = "Repo-intelligence adapter is present but currently unhealthy or not parseable."
    return {
        "status": status,
        "rationale": rationale,
        "repo_intel_candidate_count": len(repo_intel_candidates),
    }


def build_next_actions(local_candidates: list[dict[str, Any]], repo_intel_candidates: list[dict[str, Any]]) -> list[str]:
    actions = []
    if local_candidates:
        top = local_candidates[0]["rel_path"]
        actions.append(f"inspect local candidate `{top}` first")
        if any("dirty:" in reason for reason in local_candidates[0].get("reasons", [])):
            actions.append(f"review local uncommitted changes for `{top}` before patching")
    if repo_intel_candidates:
        top = repo_intel_candidates[0]
        actions.append(f"inspect repo-intel candidate `{top.get('locator')}` to compare structural context")
    if not actions:
        actions.append("fallback to direct file inspection; no strong candidates found")
    return actions[:4]


def trim_pack(pack: dict[str, Any], max_chars: int) -> dict[str, Any]:
    def size(obj: Any) -> int:
        return len(json.dumps(obj, ensure_ascii=False))

    while size(pack) > max_chars:
        if len(pack.get("next_actions", [])) > 2:
            pack["next_actions"] = pack["next_actions"][:2]
            continue
        if len(pack.get("git_context", {}).get("diffstat", [])) > 4:
            pack["git_context"]["diffstat"] = pack["git_context"]["diffstat"][:4]
            continue
        if len(pack.get("repo_intel_candidates", [])) > 2:
            pack["repo_intel_candidates"].pop()
            continue
        if pack["local_candidates"]:
            last = pack["local_candidates"][-1]
            if last.get("snippets") and len(last["snippets"]) > 1:
                last["snippets"] = last["snippets"][:1]
                continue
            if len(pack["local_candidates"]) > 1:
                pack["local_candidates"].pop()
                continue
        break
    return pack


def finalize_pack_budget(pack: dict[str, Any], max_chars: int) -> dict[str, Any]:
    pack = trim_pack(pack, max_chars)
    pack["citations"] = build_citations(pack["local_candidates"], pack["repo_intel_candidates"])
    pack = trim_pack(pack, max_chars)
    pack["citations"] = build_citations(pack["local_candidates"], pack["repo_intel_candidates"])
    pack_chars = len(json.dumps(pack, ensure_ascii=False))
    pack["metrics"]["approx_chars"] = pack_chars
    pack["metrics"]["approx_tokens"] = int(pack_chars / 4)
    pack["metrics"]["citation_count"] = len(pack.get("citations", []))
    return pack


def build_pack(
    query: str,
    *,
    repo: Path,
    profile: str = "standard",
    limit: int | None = None,
    max_chars: int | None = None,
    timeout: int = 120,
    feedback: str = "off",
    feedback_log: Path | None = None,
    symbol_slicing: str = "off",
    repo_intel_cmd: str | None = None,
) -> dict[str, Any]:
    preset = PROFILE_PRESETS[profile]
    effective_limit = limit if limit is not None else int(preset["limit"])
    effective_max_chars = max_chars if max_chars is not None else int(preset["max_chars"])
    repo = repo.resolve()
    feedback_log = feedback_log or repo / "artifacts" / "context_intel" / "feedback-events-v1.jsonl"
    keywords = extract_keywords(query)
    git_meta = git_context(repo)
    hits = search_repo(repo, keywords, timeout=min(timeout, 60))
    local_candidates = build_local_candidates(query, repo, git_meta, hits, effective_limit)
    local_candidates = apply_feedback_rerank(
        local_candidates,
        query=query,
        mode=feedback,
        feedback_log=feedback_log,
    )
    local_candidates = enrich_symbol_slices(local_candidates, mode=symbol_slicing)
    repo_intel_payload, repo_intel_latency_ms = run_repo_intel_adapter(query, repo, repo_intel_cmd, timeout=min(timeout, 90))
    repo_intel_candidates = build_repo_intel_candidates(repo_intel_payload, int(preset["max_repo_intel"]))
    assessment = compare_assessment(repo_intel_payload, repo_intel_candidates)
    next_actions = build_next_actions(local_candidates, repo_intel_candidates)
    pack = {
        "contract_version": "v2",
        "generated_at": now_utc(),
        "problem": {
            "query": query,
            "keywords": keywords,
            "repo": str(repo),
            "mode": "technical-pack",
            "query_signature": normalize_query_signature(query),
        },
        "metrics": {
            "local_candidate_count": len(local_candidates),
            "repo_intel_candidate_count": len(repo_intel_candidates),
            "approx_chars": 0,
            "approx_tokens": 0,
            "budget_profile": profile,
            "budget_limit": effective_limit,
            "budget_max_chars": effective_max_chars,
            "citation_count": 0,
            "feedback_mode": feedback,
            "symbol_slicing_mode": symbol_slicing,
            "repo_intel_latency_ms": repo_intel_latency_ms,
        },
        "git_context": git_meta,
        "local_candidates": local_candidates,
        "repo_intel_candidates": repo_intel_candidates,
        "compare_assessment": assessment,
        "citations": [],
        "next_actions": next_actions,
        "provenance": {
            "query_fusion": {
                "engine": "hyperclaw_max_context_pack",
                "mode": "local-search",
                "metadata": {"search_backend": "rg-or-fallback"},
            },
            "compare_mode": {
                "engine": "repo_intel_adapter",
                "status": repo_intel_payload.get("status"),
                "command": repo_intel_cmd,
            },
            "feedback": {"mode": feedback, "log": str(feedback_log)},
        },
    }
    pack = finalize_pack_budget(pack, effective_max_chars)
    return pack


def write_pack(pack: dict[str, Any], repo: Path) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = repo / "artifacts" / "context_intel" / "packs" / ts
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "code-context-pack.json"
    outpath.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return outpath


def render_human(pack: dict[str, Any]) -> str:
    lines = [
        "=== HyperClaw-Max Code Context Pack ===",
        f"Query: {pack['problem']['query']}",
        f"Repo: {pack['problem']['repo']}",
        f"Profile: {pack['metrics']['budget_profile']}",
        f"Keywords: {', '.join(pack['problem']['keywords']) or 'none'}",
        f"Local candidates: {len(pack['local_candidates'])} | Repo intel: {len(pack['repo_intel_candidates'])}",
        f"Approx tokens: {pack['metrics']['approx_tokens']}",
        "",
        "Local candidates:",
    ]
    for item in pack["local_candidates"]:
        lines.append(f"- {item['rel_path']} | score={item['score']} | reasons={','.join(item['reasons']) or '-'}")
        for snip in item.get("snippets", []):
            lines.append(f"  L{snip['line']}: {snip['text']}")
    lines.extend(["", "Repo-intel candidates:"])
    for item in pack["repo_intel_candidates"]:
        lines.append(f"- {item['kind']} | {item['locator']} | {item['name']}")
    lines.extend(["", "Compare assessment:", f"- {pack['compare_assessment']['status']}", f"  {pack['compare_assessment']['rationale']}"])
    lines.extend(["", "Next actions:"])
    for action in pack["next_actions"]:
        lines.append(f"- {action}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Structural Code Context Pack")
    ap.add_argument("query", nargs="+")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--limit", type=int)
    ap.add_argument("--max-chars", type=int)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--profile", choices=["terse", "standard", "full"], default="standard")
    ap.add_argument("--format", choices=["json", "human"], default="human")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--feedback", choices=["off", "read-only"], default="off")
    ap.add_argument("--feedback-log", type=Path)
    ap.add_argument("--symbol-slicing", choices=["off", "python-only"], default="off")
    ap.add_argument("--repo-intel-cmd", default=None)
    args = ap.parse_args()

    pack = build_pack(
        " ".join(args.query),
        repo=args.repo,
        profile=args.profile,
        limit=args.limit,
        max_chars=args.max_chars,
        timeout=args.timeout,
        feedback=args.feedback,
        feedback_log=args.feedback_log,
        symbol_slicing=args.symbol_slicing,
        repo_intel_cmd=args.repo_intel_cmd,
    )
    if args.write:
        pack["artifact"] = str(write_pack(pack, args.repo.resolve()))
    if args.format == "json":
        print(json.dumps(pack, ensure_ascii=False, indent=2))
    else:
        print(render_human(pack), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
