# Roadmap

This roadmap reflects the current state of the public repo relative to the live private OpenClaw body.

It is ordered around real extraction work, not only presentation.

## Stage 0: Baseline Already Landed

Already real in this repo:
- product README and trust layer
- boundary and privacy docs
- default agent pack skeleton
- Stage 1 context-intel extraction
- tests, fixtures, and CI for the extracted core

This stage proves:
- the repo is real
- the public lane is separate
- at least one useful public-safe slice already exists

## Stage 1: Publicization Matrix And Config Surface

Goal:
- replace the old marker view with a current extraction map derived from the live body

Deliverables:
- publicization matrix by surface
- richer public config example aligned to the real config shape
- onboarding flow that is honest about what is real vs roadmap
- runtime validation surface for the public core

Exit criteria:
- `EXTRACTION-MAP.md` classifies every major lane as `copy`, `copy with templating`, `rewrite`, or `exclude`
- `openclaw.public.example.jsonc` reflects the minimum installable public shape
- onboarding no longer implies a setup surface that does not exist

## Stage 2: Control Plane And Install Surface

Goal:
- package the minimum public-safe control plane needed for a real install

Current status:
- gateway templates are public
- `hyperclaw-materialize-pack` and `hyperclaw-first-run` are public
- the public core can now be rendered over a clean target root

Deliverables:
- gateway and service templates
- public-safe validator entrypoints
- install scripts and first-run checks
- default pack enablement flow

Mostly expected status:
- `copy with templating` for service units and validation wrappers
- `rewrite` for private-path-dependent helpers

Exit criteria:
- a user can configure and validate the public core without private files
- docs match the real install flow

## Stage 3: Memory And Operational Fabric Extraction

Goal:
- move beyond Stage 1 context-intel into a real public-safe fabric layer

Current status:
- initial task, delegation, and watchdog schemas are now public
- bootstrap, validation, and summary wrappers are now public
- materialized installs now bootstrap public-safe runtime state by default
- richer dispatch and observability behavior is still pending

Deliverables:
- public-safe `query-fusion` shell
- dispatch, watchdog, and observability contracts
- synthetic fixtures for operational smoke tests

Mostly expected status:
- `copy` for schemas and public-safe fixtures
- `rewrite` for task capture, dispatch, watchdog, and live state handling

Exit criteria:
- the public repo exposes more than isolated tools
- memory and operational fabric are represented as real installable surfaces

## Stage 4: Connectors, Hooks, And Voice

Goal:
- package connector and voice surfaces as adapters, not as private residue

Current status:
- public connector env templates now exist for Telegram, HTTP hooks, Gmail watch, and calendar push
- live connector and voice automation remains a later adapter extraction

Deliverables:
- Telegram and WhatsApp template surfaces
- Gmail / Calendar / Drive hook templates
- voice/browser architecture docs and service templates
- public-safe RTC and voice adapter seams

Mostly expected status:
- `copy with templating` for connector examples and service shells
- `rewrite` for hook transforms, voice proxying, and provider-specific glue

Exit criteria:
- connector and voice lanes are documented as real optional surfaces
- no private tokens, allowlists, or session material are required in-repo

## Stage 5: Optional Overlays And Tier 5

Goal:
- add richer optional lanes without bloating the public core

Current status:
- finance and legal now ship as explicit optional overlay boots
- Tier 5 repo-intel adapter extraction is still pending

Deliverables:
- GitNexus or equivalent repo-intel adapter contract
- optional finance and legal overlays
- optional specialist pack extensions for non-core lanes
- richer observability and mission-control style adapters

Exit criteria:
- optional lanes are useful but not required
- the base distro stays valuable without private overlays

## Stage 6: Public Flip Readiness

Goal:
- reach a state where the repo can be presented as a real public distro without overstating maturity

Current status:
- boundary audit doc exists
- privacy scan now checks for private live config, runtime residue, and hard-coded private-root paths in installable surfaces
- repo visibility change is still blocked pending owner confirmation

Deliverables:
- owner privacy audit
- public-safety verification pass
- install and smoke-test proof
- docs pass across README, architecture, hosting, onboarding, and roadmap

Exit criteria:
- packaged reality matches public claims
- private-only surfaces are clearly excluded
- repo is credible even without grant framing

## Non-Goals For This Roadmap

- copying the private body wholesale
- pretending feature parity with the live system
- making optional adapters mandatory
- claiming installability before the install surface is real
