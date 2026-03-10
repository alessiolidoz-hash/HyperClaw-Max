# DOC / Main Bootstrap

Startup checklist:
1. confirm config loads
2. confirm agent pack is present
3. confirm memory core is healthy
4. confirm at least one connector is configured
5. confirm optional adapters are either healthy or disabled
6. confirm privacy boundary has not been broken by local secrets or state

If something critical is missing:
- report clearly
- do not pretend the distro is fully configured
- degrade gracefully and keep the system truthful
