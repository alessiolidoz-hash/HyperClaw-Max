# HK Tools

Primary surfaces:
- health checks
- maintenance wrappers
- task and delegation state
- watchdogs
- validation scripts
- systemd templates

Suggested dependencies:
- systemd user services
- bash
- python
- log access
- optional Tailscale for remote operations

Expected future role:
- validate the product install
- observe runtime drift
- keep maintenance logic explainable

Privacy contract:
- no private incident archive required
- no personal channels required
- no secret-bearing state in tracked docs
