# Extraction Map

This file is the publicization matrix for turning the live private OpenClaw body into a real public distro.

It is not a changelog and not a promise that every listed surface is already packaged.

Rule of use:
- live filesystem evidence is the source of truth
- `HyperClaw-Max` must package only public-safe surfaces
- every surface must be classified before extraction

Classification:
- `copy` = already public-safe with little or no structural change
- `copy with templating` = portable only after replacing paths, secrets, identities, or environment assumptions
- `rewrite` = concept is reusable, but the current implementation is too coupled to the private body
- `exclude` = must stay private

## Control Plane And Patch Substrate

### Copy

- patch doctrine and operator guidance from public-safe docs
- generic release-compare concepts and scorecard ideas

### Copy With Templating

- gateway systemd unit templates
- runtime validation entrypoints based on `workspace/scripts/validate_openclaw_runtime.py`
- service bootstrap order and preflight checks

### Rewrite

- dist patch ledger shape from the private runtime patch ledger
- patch application helpers that currently assume the private compiled dist path
- pre-start sync helpers such as `workspace/scripts/sync_agent_main_thinking.py`
- any control-plane helper that assumes live session stores under the private runtime root

### Exclude

- live patch payloads tied to the private production body
- private compiled dist artifacts
- private service env files and auth material

## Config And Runtime Shape

### Copy

- public-safe config docs
- config comments and naming conventions that do not reveal private topology

### Copy With Templating

- `config/openclaw.public.example.jsonc`
- gateway, channels, hooks, tools, skills, and wizard example sections
- optional systemd env override examples

### Rewrite

- minimal installable public config shape derived from the live `openclaw.json`
- validation rules for optional adapters vs required public core
- install-time config generation and first-run wizard flow

### Exclude

- real `openclaw.json`
- auth profiles
- live bindings to personal channels, identities, or accounts
- secrets env files and private tokens

## Memory Fabric

### Copy

- `workspace/scripts/code-context-pack.py`
- `workspace/scripts/failure-diagnostics-clinic.py`
- `workspace/scripts/context-intel-eval.py`
- `workspace/scripts/context-intel-baseline.py`
- `workspace/scripts/context_symbol_slice.py`
- synthetic fixtures and public-safe schemas from `workspace/data/context-intel/`

### Copy With Templating

- public-safe memory smoke tests
- sample storage layout and retention docs
- synthetic Tier 1 and Tier 5 fixtures

### Rewrite

- `workspace/scripts/query-fusion.py`
- `workspace/scripts/local-llm/nightly_hybrid_indexing.sh`
- graph and episodic adapter contracts
- public-safe Tier 4 synthesis workflow
- memory ingestion wrappers that currently assume live local databases and notes paths

### Exclude

- live Tier 1 SQLite stores
- live graph stores and caches
- live synthesis stores
- private operator memory and live episodic traces

## Operational Fabric

### Copy

- task and delegation concepts
- public-safe state schemas
- observability report formats that do not reveal private operations

### Copy With Templating

- active task, delegation, and watchdog JSON schemas
- outbox payload contracts
- synthetic event fixtures for task capture and dispatch

### Rewrite

- `workspace/scripts/tasks/native-task-capture.py`
- `workspace/scripts/monitoring/internal-agent-dispatch.py`
- `workspace/scripts/monitoring/system-operational-watchdog.py`
- `workspace/scripts/monitoring/routed_model_observability.py`
- secretary delivery/outbox glue
- mission-control and dashboard-facing wrappers

### Exclude

- live state under `workspace/data/state/`
- live outbox indexes and logs
- private incidents, closures, and operator traces

## Connectors And Hooks

### Copy

- generic connector docs
- public-safe hook contract docs

### Copy With Templating

- hook path and preset examples
- Telegram and WhatsApp channel examples
- Gmail / Calendar / Drive hook templates
- `hooks/transforms/secretary-enrich.mjs` concepts and interface shape

### Rewrite

- hook mappings and transforms that assume private routing doctrine
- calendar / drive / gmail receiver wrappers
- connector setup flows that depend on personal accounts or allowlists
- channel-side delivery rules that depend on the private operator

### Exclude

- real bot tokens
- real allowlists, chat ids, and account identifiers
- WhatsApp / Telegram session state
- OAuth material and connector secrets

## Voice And Browser Surface

### Copy

- public-safe voice architecture docs
- browser/PWA concepts and screenshots that do not reveal private data

### Copy With Templating

- `voice-client/web/` shell and static assets
- service templates for browser web and broker processes
- public-safe voice smoke scripts

### Rewrite

- `workspace/scripts/rtc-gateway-proxy.py`
- `workspace/scripts/ink-stt.sh`
- `voice-client/agent/agent.py`
- `voice-client/broker/server.py`
- env-driven provider selection, RTC bootstrap, and call guardrails

### Exclude

- voice env files
- private voice secrets
- live call logs and session state
- any fallback that scrapes private notes for secrets

## Repo Intelligence And Tier 5

### Copy

- advisory lane concepts
- compare/eval scorecard docs
- public-safe output contracts for repo-intel examples

### Copy With Templating

- release-compare examples
- GitNexus adapter docs and interface seams
- synthetic upstream fixtures

### Rewrite

- `workspace/scripts/upstream/compare_openclaw_upstream_tier5.py`
- `workspace/scripts/upstream/index_openclaw_upstream_gitnexus.sh`
- `workspace/scripts/upstream/sync_openclaw_upstream_live.sh`
- release and prerelease sync wrappers

### Exclude

- live upstream worktrees
- release caches and manifests populated from the private body
- any repo-intel surface that reveals private paths or local mirrors

## Agent Packs And Overlays

### Copy

- public default pack docs for `main`, `codex`, `pa`, and `hk`
- generic role contracts and boot drafts

### Copy With Templating

- finance and legal overlay docs
- optional pack manifests for additional lanes
- public-safe workspace layout examples

### Rewrite

- optional overlays for `doctor`, `newsmaster`, `tier5-monitor`, `twinmind-extractor`, and `kimi`
- specialist boot files that still assume private routing or private corpora
- pack enablement flow and install-time selection

### Exclude

- live specialist workspaces
- private medical, legal, or finance corpora
- real agent session stores
- personal routing doctrine

## Docs, Tests, And Examples

### Copy

- trust layer docs
- Stage 1 tests and fixtures already in this repo
- public-safe examples and screenshots

### Copy With Templating

- install smoke tests
- validation examples
- connector and voice walkthroughs with placeholders

### Rewrite

- architecture, hosting, roadmap, and onboarding docs as the public surface expands
- test plans for config, router, operational fabric, connectors, and overlays

### Exclude

- private reports
- daily memory
- internal incident analysis
- anything derived from live operator conversations or private business data

## Release Gate

Before any future public flip, every promoted surface must answer:
- is it in the right classification?
- is the public-safe version real?
- does it avoid private paths, secrets, and personal routing?
- do docs describe the current packaged reality rather than the target end state?
