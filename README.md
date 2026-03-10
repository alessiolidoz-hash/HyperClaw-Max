# HyperClaw-Max

Confirmed working name for the first public-distro staging tree.

This is not a runnable product yet.
It is a sanitized skeleton for an installable public OpenClaw distribution derived from the private system.

## Goal

Build a public distro that keeps the real strengths of the private environment:
- persistent specialist agents
- layered memory
- local/hybrid model routing
- operational fabric
- optional repo intelligence

Without exposing:
- secrets
- live personal data
- runtime state
- private reports
- personal channels and accounts

## Product Shape

This staging tree assumes a product-like public repo, not a toolkit-only repo and not a backup mirror.

Core layers:
- `agents/` = default persistent-agent pack
- `config/` = public-safe example configuration
- `docs/` = architecture and boundary map
- `install/` = onboarding and setup plan
- `adapters/` = optional integrations such as GitNexus

## Current Status

Status today:
- skeleton only
- no secrets
- no live runtime files
- no direct copies of private boot files
- no extracted code yet

The current purpose is to decide:
- what the public distro should contain
- what must remain private
- what can be rewritten as portable public-safe modules

## Naming

`HyperClaw-Max` is the confirmed working name.
Branding can still evolve later without changing the structure.

## Next Stage

After skeleton validation, the next step is staged extraction:
1. public-safe core scripts
2. portable config templates
3. default agent pack
4. optional repo-intelligence adapter
5. onboarding docs
