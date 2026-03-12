# Architecture

HyperClaw-Max aims to package the public-safe body of the live private OpenClaw system as a real installable product.

The key architectural rule is simple:
- the live body is the reference
- the public repo is the extracted product surface
- the two must stay clearly separated

## North Star

The public distro should feel like:
- a local-first agent operating system
- not a code sample
- not a single-purpose maintainer toolkit
- not a direct mirror of the private runtime

## Logical Layers

```text
User / Owner
  |
  +--> Private network boundary
  |     - Tailscale or equivalent
  |
  +--> Channels and ingress
  |     - Telegram first
  |     - optional WhatsApp
  |     - optional Gmail / Calendar / Drive hooks
  |     - optional voice / browser lane
  |
  +--> Control plane
  |     - patched OpenClaw gateway
  |     - public-safe config shape
  |     - validator / preflight
  |     - service templates
  |
  +--> Persistent agent pack
  |     - main / DOC
  |     - codex
  |     - pa
  |     - hk
  |     - optional finance / legal overlays
  |     - future optional specialist overlays
  |
  +--> Operational fabric
  |     - task capture
  |     - delegations
  |     - watchdogs
  |     - delivery / outbox
  |     - routed-model observability
  |
  +--> Memory fabric
  |     - Tier 1 local recall
  |     - Tier 2 graph relationships
  |     - Tier 3 episodic ingest
  |     - Tier 4 synthesis layer
  |     - Tier 5 advisory / repo intelligence
  |
  `--> Optional adapters
        - local / hybrid routing
        - repo-intel engine
        - voice / RTC stack
        - sector overlays
```

## Publicization Zones

### Public Core

The public core should eventually include:
- gateway and service templates
- a default persistent agent pack
- public-safe config examples
- validation and doctor surfaces
- Stage 1 context-intel core
- memory and operational fabric contracts
- onboarding and install docs

### Optional Adapters

These are useful lanes, but they should not be required for a clean OSS install:
- repo intelligence adapters
- local / hybrid model routing
- richer hooks and connector packs
- voice / browser / RTC surfaces
- finance and legal overlays
- future specialist packs beyond the default core

### Private Overlay

These remain outside the public repo:
- real `openclaw.json`
- real auth profiles and tokens
- live sessions and runtime state
- private corpora and operator memory
- personal routing doctrine
- live patch payloads tied to one production body

## Design Rules

- Public core must run without private services or private data.
- Connectors must be template-based and user-configured.
- Patch-aware control-plane behavior must be described honestly, not hand-waved as "just config".
- Repo intelligence must be optional.
- Voice, hooks, and specialist overlays should land as adapters, not as accidental leakage from production.
- The default install should stay useful even without finance/legal or repo-intel overlays.

## Current Reality

Today the public repo already contains:
- a real Stage 1 extraction
- real tests and fixtures
- a real CLI surface
- a real default pack skeleton
- honest privacy and boundary docs

Today it does not yet contain:
- the full control-plane install surface
- the full operational fabric
- the full connector / hook stack
- the live voice / browser lane
- the full Tier 5 compare / sync surface

## First Deliverable

The first real deliverable is not full parity with the private environment.

It is:
- a credible installable public core
- a default agent pack
- a public-safe context and memory entrypoint
- a templated config and validation surface
- a clear boundary between OSS core, optional adapters, and private overlay
