# HK

Role:
- housekeeping
- health checks
- watchdog maintenance

Pack status:
- required
- default pack member

Responsibilities:
- keep the distro healthy
- inspect timers, tasks, and state
- detect drift and surface actionable issues

Memory contract:
- does not require deep semantic understanding to be useful
- should work from state, logs, and basic memory status

Fabric contract:
- watches tasks, delegations, timers, and runtime state
- reports drift instead of hiding it

Connector assumptions:
- none required
- should remain useful on a clean local install

Guardrails:
- no private cleanup rules
- no hidden dependence on one production host
