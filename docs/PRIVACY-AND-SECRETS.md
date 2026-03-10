# Privacy And Secrets

HyperClaw-Max is being prepared for public visibility.
That makes privacy boundaries a first-class design concern.

## Never Commit

- real API keys
- OAuth client secrets
- bot tokens
- real allowlists
- session stores
- WhatsApp or Telegram session material
- personal or business data
- private operator memory

## Public Repo Rule

If a file reveals:
- who the real owner is
- how the real private system is wired
- or what real private accounts exist

then it does not belong in the public core.

## Allowed In Public Core

- templates
- placeholders
- synthetic fixtures
- sample configs with env variables
- generic agent roles
- generic connector docs

## Product Honesty Rule

The repo should be open about what is still draft.
It should never fake privacy safety by simply forgetting to remove a secret.
