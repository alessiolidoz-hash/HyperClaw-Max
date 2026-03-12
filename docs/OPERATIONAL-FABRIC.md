# Operational Fabric

This document describes the current public-safe operational-fabric slice shipped in `HyperClaw-Max`.

## What Is Real Today

The repo now includes a public base for:
- active task state
- delegation state
- watchdog incident state
- bootstrap, validation, and summary CLI wrappers

These surfaces are intentionally smaller than the live private body.

## What This Wave Includes

Current public artifacts:
- `schemas/ops_fabric/active-tasks.schema.json`
- `schemas/ops_fabric/delegations.schema.json`
- `schemas/ops_fabric/system-operational-watchdog.schema.json`
- `fixtures/ops_fabric/*.sample.json`
- `hyperclaw-ops-fabric`

Current CLI flow:

```bash
PYTHONPATH=src python3 -m hyperclaw_max.ops_fabric.cli bootstrap --state-dir runtime/state
PYTHONPATH=src python3 -m hyperclaw_max.ops_fabric.cli validate --state-dir runtime/state
PYTHONPATH=src python3 -m hyperclaw_max.ops_fabric.cli summary --state-dir runtime/state
```

## Public-Core Goal

The goal of this slice is not to copy the private operational fabric.

It is to give an external user:
- a clear state layout
- a public-safe contract for task, delegation, and watchdog files
- enough scaffolding to bootstrap the core pack honestly
- enough shape to contribute without seeing the private runtime

## What Is Still Missing

Still not packaged here:
- live task-capture behavior
- live internal-dispatch behavior
- live watchdog routing and outbox glue
- live logs, incidents, and report production
- richer observability and dashboard surfaces

Those remain separate extraction work.

## Private Boundary

Never copy into the public repo:
- live `workspace/data/state/*`
- live outbox indexes
- private incident histories
- private report paths that reveal operator context
- personal routing and escalation doctrine

## Design Rule

The public operational fabric should stay:
- schema-first
- explainable
- bootstrap-friendly
- decoupled from one private host

It should not pretend that the full live automation fabric is already portable.
