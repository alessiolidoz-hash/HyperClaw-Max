# Hosting And Dependencies

This file describes the intended early deployment shape for HyperClaw-Max.

## Suggested Host

Recommended early target:
- Hetzner or equivalent VPS
- ARM64 or x86_64
- 8 vCPU
- 16 GB RAM
- SSD storage

Why:
- enough room for system services
- enough room for a first local-model lane
- enough room for logs, fixtures, and memory artifacts

## Suggested Network Shape

Recommended:
- private reachability with Tailscale
- no public exposure by default
- connectors opened only after configuration

Why:
- keeps the product usable while reducing blast radius during setup

## Base Software Dependencies

Required:
- Python 3.11+
- Node 20+
- `git`
- `bash`
- `rg`

Useful:
- `gh`
- `curl`
- `systemctl --user`

Optional:
- Ollama or another local OpenAI-compatible endpoint
- OpenAI API key
- Anthropic API key
- Telegram bot token

## Dependency Matrix

| Surface | Required | Optional |
|---|---|---|
| Base runtime | Python, Node, git, bash, rg | gh |
| Connectors | none for dry local use | Telegram, OAuth providers |
| Models | one provider path | local endpoint, hybrid routing |
| Repo intelligence | none | GitNexus-style adapter |
| Hosting | Linux host | Hetzner, Tailscale |

## Connector Strategy

Early recommended connector:
- Telegram first

Later optional connectors:
- email/calendar
- voice
- repo intelligence

## Runtime Philosophy

HyperClaw-Max should be able to run in three modes:
- cloud-model only
- local-model assisted
- hybrid

The public distro should not require every mode to be configured on day one.
