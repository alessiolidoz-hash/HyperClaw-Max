# HyperClaw-Max

HyperClaw-Max is a local-first multi-agent distro built around layered memory, operational fabric, and optional repo intelligence.

Status:
- installable product shape: draft
- public-safe core extraction: in progress
- private overlay separation: in progress
- fine-tuning, donor surgery, and adapter work: still in progress

This repo is intentionally not finished yet.
The goal is to make the product real and credible enough for early adopters and a future grant request, while still being honest that it is under active development.

## What HyperClaw-Max Is

HyperClaw-Max is meant to package the strongest public-safe ideas from a private OpenClaw-based operating environment:
- persistent specialist agents
- layered memory
- local or hybrid model routing
- task/delegation/watchdog fabric
- optional repo intelligence for donor and upstream work

This is not:
- a toy repo
- a single maintainer script
- a raw backup mirror
- a finished product

This is:
- a draft distro
- with a real product direction
- and a real privacy boundary

## Why It Exists

Most agent repos give you one or two of these:
- local model support
- coding tools
- memory
- MCP or browser control
- multi-agent scaffolding

HyperClaw-Max is trying to combine them into one coherent operating system:
- memory that has layers and jobs
- agents that have roles
- fabric that tracks work
- optional repo intelligence that helps compare, inspect, and import surgically

## Core Product Pillars

### 1. Memory Fabric

Target model:
- Tier 1 = fast semantic recall
- Tier 2 = graph/entity relationships
- Tier 3 = episodic or temporal memory
- Tier 4 = synthesis layer
- optional Tier 5 style advisory lane through repo intelligence adapters

See:
- [docs/MEMORY-FABRIC.md](docs/MEMORY-FABRIC.md)

### 2. Operational Fabric

Target model:
- task capture
- delegation state
- watchdog sweeps
- routing observability
- delivery traceability

### 3. Persistent Agent Pack

Default pack:
- DOC / main
- CODEX
- PA
- HK

Optional overlays:
- FINANCE
- LEGAL

See:
- [agents/PACK-MANIFEST.yaml](agents/PACK-MANIFEST.yaml)

### 4. Repo Intelligence

Repo intelligence is treated as a second engine, not as the heart of the distro.

Current stance:
- optional adapter
- useful for upstream compare, donor scouting, and repo archaeology
- must not be required for a clean base install

See:
- [adapters/gitnexus/README.md](adapters/gitnexus/README.md)

## Suggested Deployment Shape

Recommended early deployment:
- Linux host
- systemd user services
- Tailscale for private reachability
- Telegram as first real connector
- optional OpenAI / Anthropic keys
- optional local model endpoint

Suggested baseline host:
- Hetzner or equivalent VPS
- ARM64 or x86_64 both acceptable
- 8 vCPU / 16 GB RAM is a reasonable early target

Suggested dependencies:
- Python 3.11+
- Node 20+
- `git`
- `rg`
- `bash`
- optional `gh`
- optional Ollama or another OpenAI-compatible local endpoint

See:
- [docs/HOSTING-AND-DEPENDENCIES.md](docs/HOSTING-AND-DEPENDENCIES.md)

## Privacy and Security Boundary

HyperClaw-Max must stay publicly understandable without leaking private operator life.

That means:
- no real secrets in repo
- no live session files
- no personal account ids
- no personal contacts, legal docs, finance data, or calendars
- no direct copies of private operator memory

See:
- [docs/PRIVACY-AND-SECRETS.md](docs/PRIVACY-AND-SECRETS.md)
- [docs/BOUNDARIES.md](docs/BOUNDARIES.md)

## Repo Shape

Core layers:
- `agents/` = default persistent-agent pack
- `config/` = public-safe example configuration
- `docs/` = architecture and boundary map
- `install/` = onboarding and setup plan
- `adapters/` = optional integrations such as GitNexus
- `src/` = extracted public-safe code
- `fixtures/` = synthetic evaluation and clinic fixtures
- `tests/` = stdlib tests for the extracted core

## Current Status

What already exists:
- staging architecture
- first public-safe `context-intel` extraction
- fixtures
- tests
- example config
- onboarding draft
- agent-pack manifest
- generic boot drafts for `main`, `codex`, `pa`, and `hk`

What still needs work:
- public-safe `query-fusion` shell
- install and validation scripts
- real connector templates
- repo-intel adapter contract
- example deployment flows

## Naming

`HyperClaw-Max` is the confirmed working name.
Branding can still evolve later without changing the structure.

## Quick Start Today

This is not yet one-command install.

Today you can already:
1. inspect the product architecture
2. inspect the agent-pack plan
3. run the extracted `context-intel` package locally
4. run the fixtures and test suite

Example:

```bash
cd HyperClaw-Max
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 -m hyperclaw_max.context_intel.pack "telegram inbound dedupe session scope" --repo . --format human
```

## Product Honesty

The point of this repo is not to pretend HyperClaw-Max is complete.
The point is to show:
- what it is
- why it is different
- which parts are already real
- and where grant-backed acceleration would actually matter

## Key Documents

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/MEMORY-FABRIC.md](docs/MEMORY-FABRIC.md)
- [docs/HOSTING-AND-DEPENDENCIES.md](docs/HOSTING-AND-DEPENDENCIES.md)
- [docs/PRIVACY-AND-SECRETS.md](docs/PRIVACY-AND-SECRETS.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [install/ONBOARDING.md](install/ONBOARDING.md)
