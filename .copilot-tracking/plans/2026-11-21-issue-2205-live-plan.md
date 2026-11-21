# Plan: issue 2205 effective Quality scope (2026-11-21)

Tier: FULL (src change); targeted tests only, no `rpi-checks.py --all`. Refs #2205.

## Plan

* [x] Phase 1 research (see research note)
* [ ] Phase 2: add `Service.quality_scope()` returning mode, homes, trigger and background-scan fields; include it in both `registry()` returns
* [ ] Phase 3: tests in `src/api/tests/test_assistants.py` for set, invalid, unset
* [ ] Phase 4: runbook preflight and api README text; knowledge-base research note, index and log
* [ ] Phase 5: targeted tests, mypy, ruff; local Playwright/endpoint proof is not applicable (no web UI change)

## Critique (single pass, executed)

* Verdict: accept. Additive read-only key; no behaviour change to enforcement. Risk: contract tests that compare registry key sets; run `test_assistants`, `test_assistant_release`, `test_assistant_panel_a11y_159`. No web files change, so accessibility tests are not triggered.
* Rejected: setting the env var on the live app (Azure write, forbidden by this brief).
* Model-call authority is referenced, not granted: the block names `ZF_ASSIST_AUTHORITY` presence only as a boolean, never its value.
