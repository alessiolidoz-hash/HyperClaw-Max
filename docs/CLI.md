# CLI Reference

Current exposed commands:
- `hyperclaw-doctor`
- `hyperclaw-privacy-check`
- `hyperclaw-symbol-slice`
- `hyperclaw-feedback-store`
- `hyperclaw-context-pack`
- `hyperclaw-failure-clinic`
- `hyperclaw-context-baseline`
- `hyperclaw-context-scorecard`

## Minimal Usage

```bash
python3 -m hyperclaw_max.doctor --repo .
python3 -m hyperclaw_max.privacy_check --repo .
python3 -m hyperclaw_max.context_intel.pack "telegram inbound dedupe session scope" --repo . --format human
python3 -m hyperclaw_max.context_intel.clinic --text "memory sync failed (search): openai embeddings failed: 401 provider=openai" --format human
```

## Current Reality

These commands are already real.
They are not yet the full product surface of HyperClaw-Max.
