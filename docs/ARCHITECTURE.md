# Architecture

This distro aims to package the public-safe body of the private OpenClaw system as an installable product.

## North Star

The public distro should feel like:
- a local-first agent operating system
- not a code sample
- not a single-purpose maintainer toolkit

## Logical Layers

```text
User
  |
  +--> Telegram / optional connectors
  |
  +--> DOC orchestrator
        |
        +--> Persistent specialists
        |     - CODEX
        |     - PA
        |     - HK
        |     - optional FINANCE
        |     - optional LEGAL
        |
        +--> Memory Fabric
        |     - Tier 1 local semantic recall
        |     - Tier 2 graph sync
        |     - Tier 3 episodic ingest
        |     - Tier 4 synthesis layer
        |
        +--> Operational Fabric
        |     - tasks
        |     - delegations
        |     - watchdogs
        |     - observability
        |
        `--> Repo Intelligence
              - optional GitNexus adapter
              - future OSS repo-engine adapter
```

## Design Rules

- Public core must run without private services or private data.
- Connectors must be template-based and user-configured.
- Repo intelligence must be optional.
- Private overlay must remain separable from the public distro.
- The default install should be useful even without finance/legal overlays.

## First Deliverable

The first deliverable is not full feature parity with the private environment.

It is:
- a clean installable skeleton
- a default agent pack
- a public-safe memory/context core
- a clear boundary between OSS core and private overlay
