# Contributing

HyperClaw-Max is still in a pre-public hardening stage.

Current contribution posture:
- issues and PRs are welcome after the repo becomes public
- changes should prefer public-safe abstractions over private-path copies
- adapters must remain optional unless clearly license-compatible and portable

## Contribution Rules

- keep secrets out of the repo
- avoid hard-coded personal or host-specific paths
- prefer synthetic fixtures over real private data
- keep the base distro useful without optional adapters
- keep docs aligned with actual runtime behavior

## Before Opening A PR

Run:

```bash
python3 -m hyperclaw_max.doctor --repo .
python3 -m hyperclaw_max.privacy_check --repo .
python3 -m unittest discover -s tests -q
```
