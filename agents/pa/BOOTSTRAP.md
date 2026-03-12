# PA Bootstrap

Startup checklist:
1. verify channel and hook config exists or is explicitly disabled
2. confirm owner destination is templated, not hard-coded
3. confirm escalation path to `main` is available
4. confirm intake can create or surface tasks without private connector state
5. confirm no personal connector state has leaked into tracked files

If connector state is incomplete:
- report missing setup
- do not simulate delivery

Allowed degraded mode:
- local-only intake with docs/templates only, no fake delivery claims
