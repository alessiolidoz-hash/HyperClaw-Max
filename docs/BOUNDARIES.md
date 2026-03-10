# Boundaries

This file defines the three operating zones of the future public distro.

## 1. Public Core

Public core should include:
- portable memory orchestration
- local model router
- nightly maintenance wrappers
- task and delegation schemas
- default persistent-agent pack
- onboarding documentation
- public-safe context and advisory wrappers

Public core must not require:
- personal credentials
- personal channels
- private reports
- absolute `/root/.openclaw/...` assumptions

## 2. Optional Adapters

Optional adapters are integrations that improve the distro but should not be required for a clean OSS install.

Examples:
- GitNexus repo intelligence
- advanced observability surfaces
- extra providers
- richer mission-control style dashboards

Rule:
- optional adapters can be enabled later
- the base distro should still work without them

## 3. Private Overlay

Private overlay stays out of the public repo.

Examples:
- real `openclaw.json`
- real bot tokens and OAuth credentials
- allowlists
- personal contacts, calendars, legal and finance data
- live runtime state
- private incident and operator memory
- user-specific routing doctrine

## 4. Migration Rule

Every private feature must be classified before extraction:
- `copy` = already public-safe
- `rewrite` = useful but coupled to private assumptions
- `exclude` = must remain private
