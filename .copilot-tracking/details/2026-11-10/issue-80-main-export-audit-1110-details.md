<!-- markdownlint-disable-file -->
# Details: issue #80 current-main export audit

Plan: `.copilot-tracking/plans/2026-11-10/issue-80-main-export-audit-1110-plan.md`.

## Phase 1: environment

* `python3 -m venv /tmp/ama-80-audit-venv-1110`; `pip install -e src/core -e src/agents -e src/api playwright==1.64.0` from this worktree.
* Verify: `python -c "import zava_forward.core, zava_forward.agents, zava_forward.api; print(__path__ of each)"` under `src/api`; all three paths must start with this worktree. Record in `origins.log`.
* Browser binaries are the existing Playwright cache; a missing browser is an actual failure to record, not a reason to install elsewhere.

## Phase 2: API checks

From `src/api`, with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../core/tests:../agents/tests`:

* `python -m unittest discover -s tests -p test_list_export_api.py` (expected 11 tests per the prior main verification; count is recorded, not forced).
* `... -p test_role_endpoint_inventory.py` (route inventory and role matrix).
* `... -p test_form_staging_api.py` (form-schemas CSV).
* Each run writes `$E/api-<name>.log` with its exit code; any failure or skip is preserved verbatim.

## Phase 3: browser checks

Environment: `ZF_BROWSER_SCRATCH=/tmp/ama80x-scratch` (absolute, outside the checkout), no credentials, explicit synthetic data through the harness (`ZF_DATA` is a temp synthetic JSON written by `design_system_browser_check.main`; `ROOT` is derived from `__file__`, so the harness binds to this worktree).

* `flock -n /tmp/ama-rpi-heavy.lock <venv>/python -m checks.schema_download_browser_check` once.
* `flock -n /tmp/ama-rpi-heavy.lock <venv>/python -m checks.progress_browser_check --axe /tmp/axepk/package/axe.min.js --out /tmp/ama80x-out/progress` once, after checking the axe sha256 matches the harness pin (the harness verifies it).
* Before reading any UI result as a review: fetch the current Web Interface Guidelines source named by `.github/skills/web-design-guidelines/SKILL.md`, and read `docs/reference/research/ux/design-system.md`, `wcag-conformance-baseline.md` and `content-standard.md`. Precedence: repository Fluent 2, WCAG baseline and plain-language standard over generic aesthetics; ASCII punctuation per Markdown style. Findings use `file:line`. No design change and no site audit.

## Phase 4: matrix

Sections: scope and decision; export routes (one row each: roles, source/version, filter, order, paging, visibility, export, one-way note, UI control, proof level); non-exported source-supported lists; classified non-lists; exclusions; check results; unknowns; exact owner decision; remaining scope for Root.

Proof levels: `S` source read only; `A` targeted API test names the route; `B` browser check drove the control; `N` none.

## Phase 5: review and commit

One Review artifact: execution, outcome, assessed boundary, routing. Commit tracking only with the repository-local noreply identity for author and committer and the Copilot trailer; run `rpi_phase_witness.py verify`.
