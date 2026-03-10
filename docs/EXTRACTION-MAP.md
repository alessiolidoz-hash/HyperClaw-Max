# Extraction Map

Initial mapping from private OpenClaw surfaces to future public-distro surfaces.

## Copy First

Likely first-copy candidates after sanitization:
- `workspace/scripts/code-context-pack.py`
- `workspace/scripts/failure-diagnostics-clinic.py`
- `workspace/scripts/context-intel-eval.py`
- `workspace/scripts/context-intel-baseline.py`
- `workspace/scripts/context_symbol_slice.py`
- public-safe schemas and synthetic fixtures from `workspace/data/context-intel/`

## Rewrite Before Publish

Useful but too coupled to private assumptions in current form:
- `workspace/scripts/query-fusion.py`
- `workspace/scripts/local-llm/router.py`
- `workspace/scripts/local-llm/nightly_hybrid_indexing.sh`
- `workspace/scripts/monitoring/internal-agent-dispatch.py`
- `workspace/scripts/monitoring/system-operational-watchdog.py`

Main rewrite reasons:
- absolute paths
- private tier adapters
- personal runtime assumptions
- live state coupling

## Optional Adapter Lane

Do not bundle as mandatory core:
- GitNexus integration wrappers
- release compare helpers that assume private local paths

Keep as adapter lane:
- `workspace/scripts/upstream/compare_openclaw_upstream_tier5.py`
- `workspace/scripts/upstream/index_openclaw_upstream_gitnexus.sh`
- `workspace/scripts/upstream/sync_openclaw_upstream_live.sh`

## Exclude

Never extract into the public core:
- real `openclaw.json`
- `credentials/`
- `agents/*/sessions/`
- `workspace/memory/`
- `workspace/data/state/`
- private reports and operator traces
- personal channel and OAuth material
