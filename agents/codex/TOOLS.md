# CODEX Tools

Required:
- Python 3.11+
- git
- rg
- bash

Useful:
- gh
- node
- optional local-model endpoint
- optional repo-intel adapter
- optional OpenAI / Anthropic keys

Core surfaces:
- `hyperclaw-materialize-pack`
- `hyperclaw-doctor`
- `hyperclaw-privacy-check`
- `hyperclaw-validate-config`
- `hyperclaw-ops-fabric`
- package source in `src/`
- fixtures in `fixtures/`
- tests in `tests/`
- docs and install surfaces

Expected work:
- extraction
- rewriting coupled scripts
- validating public-safe defaults

Hosting assumptions:
- portable workspace
- no absolute `/root/.openclaw/...`
- can run on laptop or VPS
