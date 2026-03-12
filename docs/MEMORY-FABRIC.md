# Memory Fabric

HyperClaw-Max is built around a layered memory model, but the public repo does not yet package the full live memory body of OpenClaw.

This document separates:
- what exists in the private system today
- what is already extracted in this repo
- what still needs a public-safe rewrite

## Target Tier Model

```text
Tier 1 = fast semantic recall
Tier 2 = graph/entity relationships
Tier 3 = episodic and temporal memory
Tier 4 = synthesis and structured notes
Tier 5 = advisory / repo intelligence lane
```

## Live Body Reality

In the private system, the memory story is already broader than the current public extraction:
- Tier 1 uses a real local recall lane
- Tier 2 and Tier 3 rely on graph and episodic stores
- Tier 4 uses a synthesis layer for durable notes
- Tier 5 supports technical compare and advisory work around repos, releases, and upstream drift

Important:
- these live tiers are real
- they are not yet fully packaged in `HyperClaw-Max`
- the public repo should not pretend they are

## Current Public Extraction

Already real in this repo:
- public-safe context pack logic
- feedback store
- failure clinic
- baseline harness
- scorecard harness
- synthetic fixtures for Stage 1 evaluation

This means the public repo already exposes:
- a real retrieval and triage core
- a real CLI surface
- a real testable extraction from the live body

It does not yet expose:
- the full multi-tier memory runtime
- the live graph and episodic adapters
- the live synthesis workflow
- the live Tier 5 compare/sync fabric

## Publicization Status By Surface

### Real Today In HyperClaw-Max

- Stage 1 context-intel commands
- synthetic fixtures and schemas
- privacy-safe examples
- docs that explain the tier model at a high level

### Template-Only Today

- install-time memory layout examples
- backend configuration examples
- future memory lane smoke flows

### Rewrite-Only Today

- `query-fusion` as a public-safe multi-tier shell
- graph backend contract
- episodic backend contract
- Tier 4 synthesis workflow
- nightly ingest wrappers that currently assume the private runtime
- Tier 5 compare/sync adapter surface

### Private-Only

- live local databases
- live graph stores
- live episodic traces
- private synthesis notes
- live repo-intel caches and worktrees
- operator memory and private corpora

## Why Layers Matter

Different questions need different memory shapes.

Examples:
- "what file mentions this?" -> Tier 1
- "what is connected to this topic?" -> Tier 2
- "when did this change happen?" -> Tier 3
- "what is the synthesized understanding?" -> Tier 4
- "how does local compare to upstream?" -> Tier 5

The product advantage is not one memory tool.
It is the disciplined combination of multiple memory surfaces with clear boundaries.

## Next Extraction Targets

The next credible memory pass is:
- rewrite a public-safe `query-fusion` shell
- define portable contracts for graph and episodic backends
- extract memory smoke tests that work without private data
- document a public-safe Tier 4 workflow
- keep Tier 5 optional and adapter-based

## Honesty Rule

The public distro should describe the tier model aggressively, but package it honestly.

Allowed:
- stating that the private system already proves the layered model
- exposing the parts already extracted
- documenting adapter seams for deeper tiers

Not allowed:
- implying that the repo already ships the full live memory stack
- implying that private backends or data are public-safe
- presenting Tier 2 to Tier 5 as equally packaged today
