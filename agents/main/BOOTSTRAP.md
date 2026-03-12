# DOC / Main Bootstrap

Startup checklist:
1. confirm the public config loads and names the expected core agents
2. confirm the materialized pack exists and the workspace boot files are present
3. confirm `runtime/state` exists and validates cleanly
4. confirm at least one model provider is configured
5. confirm connector lanes are either configured or explicitly disabled
6. confirm optional overlays are either healthy or omitted without blocking core
7. confirm privacy boundary has not been broken by local secrets or copied state

If something critical is missing:
- report clearly
- do not pretend the distro is fully configured
- degrade gracefully and keep the system truthful

Allowed degraded modes:
- local-only mode when no connector is configured
- core-only mode when finance/legal overlays are absent
- validation-only mode when the install is not yet attached to a live gateway
