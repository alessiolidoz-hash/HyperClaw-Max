# Memory Fabric

HyperClaw-Max is built around a layered memory idea.

## Target Tier Model

```text
Tier 1 = fast semantic recall
Tier 2 = graph/entity relationships
Tier 3 = episodic and temporal memory
Tier 4 = synthesis and structured notes
Tier 5 = optional advisory / repo intelligence lane
```

## Why Layers Matter

Different questions need different memory shapes.

Examples:
- "what file mentions this?" -> Tier 1
- "what is connected to this topic?" -> Tier 2
- "when did this change happen?" -> Tier 3
- "what is the synthesized understanding?" -> Tier 4
- "how does local compare to upstream?" -> Tier 5 or repo intelligence adapter

## Current Public-Core Progress

Already present in this repo:
- public-safe context pack logic
- feedback store
- failure clinic
- baseline harness
- scorecard harness

Still missing:
- a portable public-safe multi-tier `query-fusion` shell
- a default graph/episodic backend contract
- a documented Tier-4 synthesis workflow

## Design Rule

The public distro should not pretend all tiers are already equally mature.
It should expose:
- a clear tier model
- the public-safe core
- the extension points for deeper memory engines
