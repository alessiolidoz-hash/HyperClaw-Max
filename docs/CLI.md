# CLI Reference

Current exposed commands:
- `hyperclaw-doctor`
- `hyperclaw-privacy-check`
- `hyperclaw-validate-config`
- `hyperclaw-ops-fabric`
- `hyperclaw-materialize-pack`
- `hyperclaw-first-run`
- `hyperclaw-symbol-slice`
- `hyperclaw-feedback-store`
- `hyperclaw-context-pack`
- `hyperclaw-failure-clinic`
- `hyperclaw-context-baseline`
- `hyperclaw-context-scorecard`

## Minimal Usage

```bash
python3 -m hyperclaw_max.doctor --repo .
python3 -m hyperclaw_max.privacy_check --repo .
python3 -m hyperclaw_max.first_run ./.hyperclaw-max-demo
python3 -m hyperclaw_max.runtime_validate ./.hyperclaw-max-demo/config/openclaw.public.example.jsonc
python3 -m hyperclaw_max.ops_fabric.cli validate --state-dir ./.hyperclaw-max-demo/runtime/state
python3 -m hyperclaw_max.ops_fabric.cli summary --state-dir ./.hyperclaw-max-demo/runtime/state
python3 -m hyperclaw_max.context_intel.pack "telegram inbound dedupe session scope" --repo . --format human
python3 -m hyperclaw_max.context_intel.clinic --text "memory sync failed (search): openai embeddings failed: 401 provider=openai" --format human
```

## Install Surface

The current public extraction now also ships:
- `hyperclaw-materialize-pack`
- `hyperclaw-first-run`
- `install/overlay/README.md`
- `install/connectors/*.env.example`

This is the real public-core bootstrap surface.
It renders config, workspace boots, and runtime state over a clean target root.

## Control-Plane Templates

The current public extraction now also ships:
- `install/systemd/openclaw-gateway.service`
- `install/systemd/openclaw-gateway.service.d/env-override.conf.example`

These templates are public-safe starting points for the gateway control plane.
They are not copied production units.

## Operational Fabric Base

The current public extraction now also ships:
- `docs/OPERATIONAL-FABRIC.md`
- `schemas/ops_fabric/*.schema.json`
- `fixtures/ops_fabric/*.sample.json`
- `hyperclaw-ops-fabric`

This is the public-safe bootstrap layer for task, delegation, and watchdog state.
It is not the full private automation fabric.

## Current Reality

These commands are already real for the public core.
Voice, richer hooks, repo-intel, and private overlays are still separate lanes.
