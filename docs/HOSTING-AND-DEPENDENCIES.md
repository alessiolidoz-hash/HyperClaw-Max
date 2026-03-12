# Hosting And Dependencies

This file describes the intended public deployment shape for HyperClaw-Max, based on the live OpenClaw body but trimmed to a public-safe install surface.

## Baseline Host

Recommended baseline:
- Hetzner or equivalent VPS
- ARM64 or x86_64
- 8 vCPU
- 16 GB RAM
- 160 GB SSD or equivalent room for logs, fixtures, and optional local-model lanes

Why this shape:
- it already matches a proven reference footprint in the private body
- it has enough room for gateway, services, tests, and a first adapter lane
- it can host the public core without forcing a cluster or managed cloud stack

## Recommended Network Shape

Recommended:
- private reachability with Tailscale or equivalent
- no broad public exposure by default
- connectors enabled only after configuration and smoke checks

Why:
- keeps the distro usable while reducing blast radius during bootstrap
- fits the local-first, owner-controlled operating model

## Core Runtime Dependencies

Required for the public core:
- Python 3.11+
- Node 20+
- `git`
- `bash`
- `rg`
- `curl`
- `systemctl --user`

Useful during setup and support:
- `jq`
- `gh`

Core provider requirement:
- at least one working provider path configured in the public config

## Optional Adapter Dependencies

Local / hybrid model lane:
- local OpenAI-compatible endpoint or equivalent local runtime
- optional model assets and healthcheck wrappers

Connector lanes:
- Telegram bot token
- optional WhatsApp / webhook / OAuth credentials when those adapters are enabled
- public connector templates are shipped under `install/connectors/`

Voice / browser lane:
- optional voice provider credentials
- optional RTC/browser assets and service templates

Repo-intel lane:
- optional GitHub / repo adapter credentials
- optional local upstream mirror tooling

## Dependency Matrix

| Surface | Required For Public Core | Optional Adapter Dependencies |
|---|---|---|
| Base runtime | Python, Node, git, bash, rg, curl, systemd user services | gh, jq |
| Models | one provider path | local endpoint, hybrid routing |
| Default pack | public config + workspaces | extra overlays |
| Connectors | none for dry local use | Telegram, WhatsApp, Gmail/Calendar/Drive hooks |
| Voice / browser | none | TTS / STT / RTC providers and service shells |
| Repo intelligence | none | GitNexus-style or equivalent adapter |
| Hosting | Linux host | Hetzner, Tailscale |

## Reference Surfaces In The Live Body

The live private system already proves these surfaces:
- patch-aware gateway and validator flow
- persistent agents with dedicated workspaces
- task / delegation / watchdog lanes
- Telegram plus richer hook ingress
- local-first and hybrid routing lanes
- voice/browser services
- upstream and release advisory sync

Important:
- that does not mean all of these are already extracted here
- it means the public distro should describe them honestly and package them incrementally

## Deployment Philosophy

HyperClaw-Max should be usable in three increasingly rich modes:
- cloud-model only
- local-model assisted
- hybrid

The public distro should not require every mode or every adapter on day one.

A good first install is:
- one Linux host
- one provider path
- one default pack
- one baseline memory/context surface
- one materialized target root produced by `hyperclaw-first-run`
- optional channels and adapters enabled later
