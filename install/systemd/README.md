# Systemd Templates

These templates are the public-safe control-plane starting point for HyperClaw-Max.

They are intentionally generic:
- no live secrets
- no private paths
- no private routing doctrine

What is included:
- `openclaw-gateway.service`
- `openclaw-gateway.service.d/env-override.conf.example`

What is not included:
- live dist artifacts
- private environment files
- production service overrides from the private body

Recommended flow:
1. Copy the service template into `~/.config/systemd/user/`.
2. Copy the drop-in example into `~/.config/systemd/user/openclaw-gateway.service.d/`.
3. Fill the placeholder environment values for repo root, config path, and dist entrypoint.
4. Run `hyperclaw-validate-config` on the chosen config before any first start.
5. Only then enable or start the user unit.
