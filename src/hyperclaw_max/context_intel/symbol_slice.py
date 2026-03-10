from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _enclosing_node(tree: ast.AST, line: int) -> ast.AST | None:
    matches: list[ast.AST] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = getattr(node, "lineno", None)
            end = getattr(node, "end_lineno", None)
            if start is None or end is None:
                continue
            if start <= line <= end:
                matches.append(node)
    if not matches:
        return None
    matches.sort(
        key=lambda n: (
            getattr(n, "end_lineno", 0) - getattr(n, "lineno", 0),
            getattr(n, "lineno", 0),
        )
    )
    return matches[0]


def _imports(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, ast.Import):
            imports.append(", ".join(alias.name for alias in node.names))
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names = ", ".join(alias.name for alias in node.names)
            imports.append(f"{mod}: {names}")
    return imports[:8]


def slice_python_symbol(path: Path, line: int, max_chars: int = 900) -> dict[str, Any]:
    try:
        source = read_source(path)
    except Exception as exc:  # noqa: BLE001
        return {"slice_status": "read_failed", "error": str(exc)}
    try:
        tree = ast.parse(source)
    except Exception as exc:  # noqa: BLE001
        return {"slice_status": "parse_failed", "error": str(exc)}

    node = _enclosing_node(tree, line)
    if node is None:
        return {"slice_status": "fallback_window"}

    start = getattr(node, "lineno", line)
    end = getattr(node, "end_lineno", line)
    lines = source.splitlines()
    excerpt = "\n".join(lines[start - 1 : end])
    if len(excerpt) > max_chars:
        excerpt = excerpt[: max_chars - 3].rstrip() + "..."
    return {
        "slice_status": "ok",
        "language": "python",
        "symbol": getattr(node, "name", None),
        "slice_kind": node.__class__.__name__,
        "span": {"start_line": start, "end_line": end},
        "imports": _imports(tree),
        "slice_excerpt": excerpt,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Python symbol slicer sidecar")
    ap.add_argument("path", type=Path)
    ap.add_argument("--line", type=int, required=True)
    ap.add_argument("--max-chars", type=int, default=900)
    args = ap.parse_args()
    payload = slice_python_symbol(args.path, args.line, max_chars=args.max_chars)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
