# Overlay Materialization

This repo now ships a public-safe overlay materialization layer.

Purpose:
- take the extracted public pack from this repo
- render it over a clean base OpenClaw install
- keep core, optional overlay, and private-only lanes clearly separated

Minimal command:

```bash
PYTHONPATH=src python3 -m hyperclaw_max.materialize_pack /opt/hyperclaw-max
```

What it writes:
- `config/openclaw.public.example.jsonc`
- `agents/PACK-MANIFEST.yaml`
- workspace boot files for the selected pack
- `runtime/state/*.json`
- `materialized-pack.json`

Optional overlays:

```bash
PYTHONPATH=src python3 -m hyperclaw_max.materialize_pack /opt/hyperclaw-max --include-optional finance
PYTHONPATH=src python3 -m hyperclaw_max.materialize_pack /opt/hyperclaw-max --all-optional
```

Rules:
- this is a public pack renderer, not a copier of the private body
- it never pulls private sessions, secrets, reports, or runtime state
- optional overlays are additive and must not mutate public core semantics
