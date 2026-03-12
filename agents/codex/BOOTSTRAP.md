# CODEX Bootstrap

Startup checklist:
1. run doctor, privacy check, and config validation
2. verify the package imports and CLI entrypoints resolve
3. verify the materialized pack metadata matches the selected agent set
4. run unit tests for the extracted public surfaces
5. inspect roadmap and extraction map before widening the surface
6. confirm optional adapters are not blocking the base distro
7. verify no secret-bearing files leaked into tracked surfaces

Golden rule:
- public-safe first

Failure rule:
- if a feature needs private state to look healthy, mark it optional or exclude it
