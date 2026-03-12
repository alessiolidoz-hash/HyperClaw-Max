# Onboarding Plan

This is the current honest onboarding path for HyperClaw-Max.

It describes:
- what a user can bootstrap today
- what is template-only today
- what remains a future adapter or extraction step

Important:
- there is no one-click setup wizard yet
- the public core now has a real first-run bootstrap
- the private live body is the reference, not the thing being copied wholesale

## Phase 0: Bootstrap The Host

Status:
- real today

Do:
- clone the repo
- install the core dependencies
- decide whether this will be a dry local install or a private-network deployment
- set up a private network boundary such as Tailscale if remote reachability is needed

Minimum baseline:
- Linux host
- Python 3.11+
- Node 20+
- `git`, `bash`, `rg`, `curl`
- `systemctl --user`

## Phase 1: Choose The Model Lane

Status:
- real today for config templating
- broader local / hybrid routing remains a later extraction

Do:
- choose at least one provider path for the public core
- keep local / hybrid routing optional until that adapter surface is extracted
- decide the default primary and fallback models for the base agent pack

Typical public-core choice:
- one cloud provider
- one fallback provider

## Phase 2: Render The Core Config

Status:
- real today

Do:
- run `PYTHONPATH=src python3 -m hyperclaw_max.first_run /target/root`
- edit `/target/root/config/openclaw.public.example.jsonc`
- fill in gateway, agents, models, and minimal tool settings
- leave optional connector and hook lanes disabled until you are ready to configure them
- treat `wizard` as metadata only, not as an automation promise

At this phase you should have:
- a gateway section
- a default agent pack (`main`, `codex`, `pa`, `hk`)
- one provider path
- no live secrets committed anywhere
- a materialized target root with runtime state and workspace boots

## Phase 3: Turn On The Public Core

Status:
- real today for installable public core

Do:
- run `doctor`, `privacy_check`, and `validate-config`
- re-run `hyperclaw-materialize-pack /target/root --force` whenever you refresh the workspace boots
- validate `runtime/state` after each refresh

Current public-core checks:
- `PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .`
- `PYTHONPATH=src python3 -m hyperclaw_max.privacy_check --repo .`
- `PYTHONPATH=src python3 -m hyperclaw_max.first_run /target/root`
- `PYTHONPATH=src python3 -m hyperclaw_max.runtime_validate /target/root/config/openclaw.public.example.jsonc`
- `PYTHONPATH=src python3 -m hyperclaw_max.ops_fabric.cli validate --state-dir /target/root/runtime/state`
- `PYTHONPATH=src python3 -m unittest discover -s tests -q`

What this proves:
- the extracted core is wired correctly
- the repo remains public-safe
- the public core can be materialized on a clean target root
- the Stage 1 and public-core commands are usable

What this does not yet prove:
- full gateway bootstrap
- full connector setup
- full voice / repo-intel / overlay extraction

## Phase 4: Enable Optional Channels And Hooks

Status:
- template-first today, with honest examples shipped

Do only if needed:
- add Telegram values to the config template
- use `install/connectors/*.env.example` as operator-owned input examples
- configure hook path and token
- add WhatsApp or richer hook lanes only when the matching adapter is available

Keep disabled or omitted until required:
- WhatsApp plugin surface
- Gmail / Calendar / Drive hook receivers
- any channel flow tied to private accounts or routing doctrine

## Phase 5: Run Validation And Smoke Checks

Status:
- real today for public core, mixed for optional adapters

Run now:
- doctor
- privacy check
- first-run
- runtime validation
- ops-fabric validation and summary
- unit tests

Run later as those surfaces land:
- connector smoke checks
- memory and operational fabric smoke checks
- local / hybrid model healthcheck
- optional repo-intel smoke

## Phase 6: Add Optional Adapters

Status:
- future extraction / adapter lane

Examples:
- finance overlay
- legal overlay
- repo-intel adapter
- local / hybrid routing
- voice / browser / RTC lane

Rule:
- optional adapters should extend the distro
- they should not be required for a clean public-core install

## What This Onboarding Deliberately Does Not Promise

- full parity with the private live body
- a finished setup wizard
- copied production hooks or sessions
- private auth, tokens, or operator memory
