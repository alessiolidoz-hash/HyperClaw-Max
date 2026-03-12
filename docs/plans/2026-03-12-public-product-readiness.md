# Public Product Readiness Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Bring `HyperClaw-Max` to the installable, operable, contributable threshold without crossing the private-to-public release boundary.

**Architecture:** Keep the public distro narrow and honest. Add a materialization layer that renders the public pack above a base OpenClaw install, a first-run orchestrator that proves installability from zero, richer public boot contracts for persistent agents, optional connector templates, and a final privacy/boundary audit surface.

**Tech Stack:** Python 3.11+, `setuptools`, JSON/JSONC, Markdown docs, shell/systemd templates, `unittest`

---

### Task 1: Materialized Public Pack

**Files:**
- Create: `src/hyperclaw_max/materialize_pack.py`
- Create: `install/overlay/README.md`
- Test: `tests/test_materialize_pack.py`
- Modify: `pyproject.toml`
- Modify: `src/hyperclaw_max/doctor.py`

**Step 1: Write the failing test**

Add `tests/test_materialize_pack.py` for:
- manifest loading
- workspace and boot file materialization
- ops-fabric bootstrap into a target runtime root
- metadata generation

**Step 2: Run test to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_materialize_pack -q`
Expected: FAIL because `hyperclaw_max.materialize_pack` does not exist.

**Step 3: Write minimal implementation**

Implement a CLI/module that:
- reads `agents/PACK-MANIFEST.yaml`
- copies public-safe config and manifest into a target root
- creates required and optional workspaces
- copies `README.md`, `AGENTS.md`, `BOOTSTRAP.md`, `TOOLS.md` when present
- bootstraps ops-fabric state under `runtime/state`
- emits `materialized-pack.json`

**Step 4: Run test to verify it passes**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_materialize_pack -q`
Expected: PASS

**Step 5: Commit**

Do not commit in this session unless explicitly requested.

### Task 2: Richer Public Boots

**Files:**
- Modify: `agents/PACK-MANIFEST.yaml`
- Modify: `agents/README.md`
- Modify: `agents/main/AGENTS.md`
- Modify: `agents/main/BOOTSTRAP.md`
- Modify: `agents/main/TOOLS.md`
- Modify: `agents/codex/AGENTS.md`
- Modify: `agents/codex/BOOTSTRAP.md`
- Modify: `agents/codex/TOOLS.md`
- Modify: `agents/pa/AGENTS.md`
- Modify: `agents/pa/BOOTSTRAP.md`
- Modify: `agents/pa/TOOLS.md`
- Modify: `agents/hk/AGENTS.md`
- Modify: `agents/hk/BOOTSTRAP.md`
- Modify: `agents/hk/TOOLS.md`
- Create: `agents/finance/AGENTS.md`
- Create: `agents/finance/BOOTSTRAP.md`
- Create: `agents/finance/TOOLS.md`
- Create: `agents/legal/AGENTS.md`
- Create: `agents/legal/BOOTSTRAP.md`
- Create: `agents/legal/TOOLS.md`

**Step 1: Write the failing test**

Extend doctor expectations to require the public boot contracts and overlay docs.

**Step 2: Run the doctor to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .`
Expected: FAIL after doctor expectations are raised.

**Step 3: Write minimal implementation**

Make each core role operationally legible for an external installer:
- mandate
- required baseline checks
- allowed degradation
- optional adapter boundaries

Add finance/legal as honest optional overlays, not fake parity claims.

**Step 4: Run the doctor to verify it passes**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .`
Expected: PASS

**Step 5: Commit**

Do not commit in this session unless explicitly requested.

### Task 3: First-Run And Install Reality

**Files:**
- Create: `src/hyperclaw_max/first_run.py`
- Test: `tests/test_first_run.py`
- Modify: `pyproject.toml`
- Modify: `README.md`
- Modify: `docs/CLI.md`
- Modify: `install/ONBOARDING.md`
- Modify: `tests/README.md`

**Step 1: Write the failing test**

Add a first-run smoke test that executes the orchestrator against a temp target root and verifies:
- config copy
- pack materialization
- ops-fabric bootstrap
- validation summary output

**Step 2: Run test to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_first_run -q`
Expected: FAIL because `hyperclaw_max.first_run` does not exist.

**Step 3: Write minimal implementation**

Implement a CLI that orchestrates:
- doctor
- privacy check
- config validation
- pack materialization
- ops-fabric validation
- next-step instructions

**Step 4: Run test to verify it passes**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_first_run -q`
Expected: PASS

**Step 5: Commit**

Do not commit in this session unless explicitly requested.

### Task 4: Connector Templates And Optional Adapters

**Files:**
- Create: `install/connectors/README.md`
- Create: `install/connectors/telegram.env.example`
- Create: `install/connectors/http-hook.env.example`
- Create: `install/connectors/gmail-watch.env.example`
- Create: `install/connectors/calendar-push.env.example`
- Modify: `docs/HOSTING-AND-DEPENDENCIES.md`
- Modify: `README.md`
- Modify: `config/openclaw.public.example.jsonc`

**Step 1: Add validation or doctor expectations**

Require the connector template folder and examples in the public install surface.

**Step 2: Run doctor to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .`
Expected: FAIL until connector templates are added.

**Step 3: Implement templates**

Ship honest examples for optional connector lanes without tokens, sessions, allowlists, or private routing doctrine.

**Step 4: Re-run checks**

Run doctor and privacy check.
Expected: PASS and no privacy findings.

**Step 5: Commit**

Do not commit in this session unless explicitly requested.

### Task 5: Privacy Sweep And Boundary Audit

**Files:**
- Create: `docs/BOUNDARY-AUDIT.md`
- Test: `tests/test_boundary_audit.py`
- Modify: `src/hyperclaw_max/privacy_check.py`
- Modify: `README.md`
- Modify: `docs/ROADMAP.md`

**Step 1: Write the failing test**

Add a test that asserts the privacy checker flags forbidden classes such as secrets, private host paths, personal identities, or copied runtime state when present in a temp repo.

**Step 2: Run test to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_boundary_audit -q`
Expected: FAIL until the new audit rules exist.

**Step 3: Implement minimal audit expansion**

Extend the boundary checker with public-product audit rules and document the current safety posture in `docs/BOUNDARY-AUDIT.md`.

**Step 4: Run full verification**

Run:
- `git diff --check`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -q`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m hyperclaw_max.privacy_check --repo .`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m hyperclaw_max.runtime_validate config/openclaw.public.example.jsonc`

Expected: all PASS

**Step 5: Final handoff**

Stop before any repo visibility change.
Ask for explicit `private -> public` confirmation only after the checks pass and the repo is credibly installable and contributable.
