# Agent Pack

This directory defines the default public persistent-agent pack and its optional overlays.

Current reality:
- `main`, `codex`, `pa`, and `hk` are the public core pack
- `finance` and `legal` are optional overlays
- `hyperclaw-materialize-pack` renders these boots over a clean base install

Boundaries:
- core pack = required for a credible public install
- optional overlays = additive, explicit, and disable cleanly
- private overlay = owner-specific routing, memory, auth, sessions, and doctrine that never ship here

What these files are for:
- `README.md` explains the lane honestly
- `AGENTS.md` defines role and guardrails
- `BOOTSTRAP.md` defines startup checks and degradation rules
- `TOOLS.md` defines the expected public-safe surfaces for that role
