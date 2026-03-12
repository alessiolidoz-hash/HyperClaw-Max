# Boundary Audit

This document describes the current public-safety audit for `HyperClaw-Max`.

Current gate:
- the repo remains private until the owner explicitly approves `private -> public`

What the audit checks today:
- common secret formats
- accidental copies of private live config such as `openclaw.json`
- runtime residue such as `.session`, `.sqlite`, `.db`, `.p12`, or `.pfx`
- hard-coded `/root/.openclaw/...` paths inside installable public surfaces

What it does not claim:
- full static analysis of every possible leak class
- parity with the private incident or secret-rotation playbooks
- safety to publish without an owner review

Public-product rule:
- docs may describe the private body as reference context
- installable surfaces must not depend on private paths, live state, or copied credentials

Release gate before any visibility change:
1. `hyperclaw-doctor` passes
2. `hyperclaw-privacy-check` passes
3. `hyperclaw-first-run` passes on a clean target root
4. owner confirms the `private -> public` flip
