# Connector Templates

These templates are optional adapter seams for the public distro.

They exist to make connector setup explicit without shipping:
- real bot tokens
- OAuth secrets
- allowlists from the private body
- copied inbox, calendar, or hook state

Current adapter posture:
- Telegram = first optional owner-facing connector
- HTTP hook = generic ingress seam for external events
- Gmail / Calendar = template-only examples, not public-core requirements

Rules:
- a clean install must work without any connector enabled
- enabling a connector must be deliberate and user-owned
- all secrets are injected post-install
