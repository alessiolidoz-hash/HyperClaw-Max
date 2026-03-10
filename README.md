# HyperClaw-Max

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-early%20but%20real-blue)
![Mode](https://img.shields.io/badge/deployment-local--first-black)
![Pack](https://img.shields.io/badge/agents-DOC%20%7C%20CODEX%20%7C%20PA%20%7C%20HK-orange)

> A local-first autonomous company in a box.
>
> One server. One private network. Persistent agents. Deep memory. Surgical operations.

HyperClaw-Max is a draft distro for people who want more than a chatbot.

It is being built to feel like this:
- your own private operator
- your own technical chief of staff
- your own memory-rich assistant company
- running on infrastructure you control

Not as a toy demo.
Not as a repo mirror.
Not as a one-shot coding script.

## Quick Start In 2 Minutes

If you just want to see whether the current repo is real:

```bash
git clone https://github.com/alessiolidoz-hash/HyperClaw-Max.git
cd HyperClaw-Max
PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .
PYTHONPATH=src python3 -m hyperclaw_max.privacy_check --repo .
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 -m hyperclaw_max.context_intel.pack "telegram inbound dedupe session scope" --repo . --format human
```

What this proves today:
- the repo installs as a real Python package surface
- the extracted core works
- the privacy boundary is checked
- the test suite passes

## What You Get In The Box

HyperClaw-Max is being built as a private AI operating layer with:
- a default persistent-agent pack
- layered memory
- operational fabric
- local or hybrid model routing
- optional repo intelligence
- guided self-hosting direction

In plain English:
- not one bot
- not one prompt
- not one repo tool
- a small autonomous operating system

## The Idea In Plain English

Most AI repos give you one impressive trick.

HyperClaw-Max is trying to combine the tricks into one disciplined system:
- agents that do different jobs
- memory that gets deeper over time
- workflows that can monitor, route, escalate, and recover
- optional repo intelligence for donor surgery and upstream comparison

If a normal agent repo is a smart intern, HyperClaw-Max is aiming to be a small autonomous company.

## What You Can Actually Use It For

Examples of the product direction:
- run a private operator stack on your own server
- keep long-lived memory across projects and tasks
- route work across specialist agents instead of one overloaded generalist
- inspect technical incidents with structured diagnostics
- compare your local system against donors or upstream before importing changes
- evolve from a personal assistant into a sector-aware operating team

## Why It Feels Different

The goal is not just "answer better."

The goal is:
- remember better
- route better
- work longer
- recover faster
- operate across channels and domains
- stay private by default

## The Superpowers

### 1. Persistent Specialist Agents

HyperClaw-Max is designed around long-lived agents with clear jobs:
- `DOC` = orchestrator
- `CODEX` = code and infrastructure
- `PA` = intake and routing
- `HK` = health and maintenance
- optional `FINANCE`
- optional `LEGAL`

This is closer to a team than a single bot.

### 2. Deep Memory Fabric

Instead of one flat memory bucket, the target model is layered:

```text
Tier 1 -> fast recall
Tier 2 -> graph relationships
Tier 3 -> episodic / timeline memory
Tier 4 -> synthesis layer
Tier 5 -> optional advisory / repo intelligence
```

Different questions should hit different memory surfaces.
That is one of the main moats of the product.

### 3. Operational Fabric

HyperClaw-Max is not just "prompt in, answer out".

It is being designed with a real fabric:
- task capture
- delegation state
- watchdogs
- routing observability
- delivery traceability

That means the system can eventually do more than generate text.
It can coordinate work like an operator.

### 4. Local and Hybrid Brains

The target product is local-first, but not local-only.

That means:
- cloud models when they make sense
- local models when they make sense
- hybrid routing when cost, privacy, or latency demand it

This is important because serious users want control, not lock-in.

### 5. Surgical Repo Intelligence

HyperClaw-Max does not want blind updates.
It wants surgical upgrades.

That is why repo intelligence exists as a second engine:
- inspect upstream
- inspect donor repos
- compare local vs external
- import only what actually helps

Not every user will need this.
But for serious operators, it becomes a superpower.

## Why It Is More Interesting Than A Typical Agent Repo

Typical agent repo:
- one agent
- one memory surface
- one chat loop
- weak or no operations layer

HyperClaw-Max direction:
- many agents
- layered memory
- task/delegation/watchdog fabric
- local-first privacy
- optional upstream/donor surgery lane

That is the big idea.
Not just “better answers”, but “better operations”.

## What It Looks Like

```text
                     HyperClaw-Max
     -------------------------------------------------
      User / Owner
           |
           v
    Telegram / future connectors
           |
           v
        DOC / Main
           |
   +-------+--------+-------------------+
   |       |        |                   |
   v       v        v                   v
 CODEX     PA       HK          Optional FINANCE / LEGAL
   |        |        |
   +--------+--------+
            |
            v
      Operational Fabric
   tasks | delegations | watchdogs | observability
            |
            v
        Memory Fabric
   T1 recall -> T2 graph -> T3 timeline -> T4 synthesis
            |
            v
   Optional Repo Intelligence Engine
     upstream compare | donor scouting | surgery
```

## What Makes It More Than Stock OpenClaw

OpenClaw already gives a powerful local-first base.

HyperClaw-Max is trying to go further by productizing:
- multi-agent role discipline
- deeper memory layering
- operational fabric
- optional repo-intelligence lane
- cleaner install story for a serious private deployment

So the difference is not "OpenClaw, but renamed."

The difference is:
- OpenClaw as a base
- extended into a richer operating system for autonomous work

## Choose Your Path

If you are:

- a builder:
  start from the extracted `context-intel` core and test surfaces
- an operator:
  read the architecture, hosting, and privacy docs first
- a grant reviewer:
  focus on the product shape, the current working core, and what funding would unlock
- a future adopter:
  treat this as an early but serious self-hosted distro

## Who It Is For

HyperClaw-Max is for people who want:
- a private AI operating layer on their own server
- persistent agents instead of disposable chats
- memory that compounds
- a Telegram-first assistant company
- room for sector packs like finance, legal, and eventually medical workflows

It is not optimized for:
- casual one-off chat users
- zero-config mass-market use
- people who want a hosted SaaS instead of running their own stack

## Suggested Early Deployment

Recommended first shape:
- Linux host
- systemd user services
- Tailscale for private access
- Telegram as the first real connector
- optional OpenAI / Anthropic keys
- optional local model endpoint

Suggested baseline host:
- Hetzner or equivalent VPS
- ARM64 or x86_64
- 8 vCPU / 16 GB RAM

Suggested dependencies:
- Python 3.11+
- Node 20+
- `git`
- `rg`
- `bash`
- optional `gh`
- optional Ollama or another local OpenAI-compatible endpoint

See:
- [docs/HOSTING-AND-DEPENDENCIES.md](docs/HOSTING-AND-DEPENDENCIES.md)

## Trust Signals

This repo already includes:
- MIT license
- security policy
- contribution guide
- changelog
- citation file
- CI workflow
- doctor command
- privacy-check command
- generated example outputs

That does not mean “finished”.
It means the project is trying to behave like a real product early.

## Guided Install Direction

The intended future install flow is:

1. clone the repo
2. run setup
3. choose your model providers
4. connect Tailscale
5. connect Telegram
6. enable the default agent pack
7. run validation
8. start working

This repo is not fully there yet.
But that is the direction.

See:
- [install/ONBOARDING.md](install/ONBOARDING.md)

## What Is Already Real Today

Already real:
- product architecture
- public-safe `context-intel` extraction
- synthetic fixtures
- tests
- privacy boundary docs
- generic boot drafts for `main`, `codex`, `pa`, and `hk`
- doctor and privacy-check commands
- generated example outputs
- CI workflow

Still in progress:
- public-safe `query-fusion` shell
- install and validation scripts
- richer connector templates
- repo-intel adapter contract
- broader memory backends
- sector overlays and advanced multimodal lanes

## Quick Proof

You can already run the current extracted core:

```bash
cd HyperClaw-Max
PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .
PYTHONPATH=src python3 -m hyperclaw_max.privacy_check --repo .
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 -m hyperclaw_max.context_intel.pack "telegram inbound dedupe session scope" --repo . --format human
PYTHONPATH=src python3 -m hyperclaw_max.context_intel.clinic --text "memory sync failed (search): openai embeddings failed: 401 provider=openai" --format human
```

See generated outputs:
- [examples/quickstart/README.md](examples/quickstart/README.md)

## Why A Grant Would Help

HyperClaw-Max does not need a grant to exist.
It needs a grant to accelerate the difficult parts:
- safer install automation
- stronger connectors
- richer memory tiers
- adapter hardening
- better guided onboarding
- more examples and validation

The point is not to fund an idea from zero.
The point is to turn a serious early system into a product more people can actually run.

## Privacy Boundary

HyperClaw-Max is being prepared for public visibility without leaking the private operator life behind it.

That means:
- no real secrets in repo
- no live session files
- no personal ids
- no private contacts, finance, legal, or calendar data
- no direct copies of private operator memory

See:
- [docs/PRIVACY-AND-SECRETS.md](docs/PRIVACY-AND-SECRETS.md)
- [docs/BOUNDARIES.md](docs/BOUNDARIES.md)

## Why The Grant Would Matter

HyperClaw-Max does not need funding to exist.
It needs funding to accelerate.

A grant would help turn the current serious draft into:
- better install automation
- stronger connector and model integration
- deeper memory layers
- safer repo-intelligence adapters
- better validations and examples
- a clearer path from private operator stack to public product

## Product Honesty

HyperClaw-Max is not finished.

That is not a weakness to hide.
That is the truth:
- the product direction is real
- the moat is real
- the early core is real
- the installable public distro is still being hardened

## Start Here

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/MEMORY-FABRIC.md](docs/MEMORY-FABRIC.md)
- [docs/HOSTING-AND-DEPENDENCIES.md](docs/HOSTING-AND-DEPENDENCIES.md)
- [docs/PRIVACY-AND-SECRETS.md](docs/PRIVACY-AND-SECRETS.md)
- [docs/CLI.md](docs/CLI.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [agents/PACK-MANIFEST.yaml](agents/PACK-MANIFEST.yaml)
