# Security Policy

HyperClaw-Max is a local-first agent distro and privacy boundary matters.

## Supported Security Posture

Current stage:
- private staging repo
- pre-public hardening
- no telemetry by default

## Reporting Security Issues

Until the repo is public:
- report privately to the maintainer
- do not open public disclosures

## Security Principles

- no secrets in git
- no live personal runtime state in git
- template-only connector config
- private overlay must remain separable from public core
- optional adapters must not silently weaken the base distro
