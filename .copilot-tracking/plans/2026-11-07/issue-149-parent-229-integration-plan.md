---
title: Issue 149 parent integration of merged child 229 and current main, plan and critique
ms.date: 2026-11-07
---

## Plan (before any merge)

* Phase 1: `git merge origin/test/ux-evidence-149` (expected fast-forward to 4d95). Phase 2: `git merge origin/main` (b284) with a merge commit and trailer. No rebase, amend, reset, force, stash or ours/theirs. A conflict is resolved only if both intents (append-only log, README) are provably kept; otherwise stop with the exact intent.
* Phase 3: main-relative diff against origin/main; confirm doc_controls.py is two strings only and no product path changed.
* Phase 4: commit research, plan, details, changes, review and state for the integrated source; that commit is the frozen head. Later results stay external and are not committed.
* Phase 5 (manual FOCUSED validation, no receipt, no `--changed` or `--all`), run on the frozen head only:
  * Own small external snapshot (git archive of src/core, src/agents, src/api, docs) under a new /tmp root with a new venv; pip non-editable install of core, agents, api with repo-pinned ruff 0.17.1, mypy 2.4.0, playwright 1.64.0; prove installed doc_controls.py, data_operator_ai_state.py, both checker files and role-screens.js SHA-256 against HEAD.
  * Unit: 69 parent modules, test_data_operator_ai_state (12 child tests), and from src/core test_needs_inventory and test_scenario_manifest. Test helper PYTHONPATH only (core/tests, agents/tests); no production-src PYTHONPATH.
  * Ruff check, ruff format --check and mypy per component working directory as the CI does; pre-existing configured format exclusions are reported, not claimed away.
  * Browser: only if `flock -n /tmp/ama-rpi-heavy.lock` is free; else return a busy admission, no queue. Run `python -m checks.atlas_tensions_browser_check` (no axe step, no axe claim) and `python -m checks.data_operator_browser_check` with ZF_AXE_REQUIRED=1 and axe 4.10.3 (SHA 880970c0...a68bb, verified copy), PLAYWRIGHT_BROWSERS_PATH to the existing read-only cache (Chromium 1248), external TMPDIR and cache, screenshots off unless a new empty directory is set. Separate exits and logs; failed logs kept, no retry, sleep or weakening.
* Phase 6: original author Review executed once on the committed candidate; later external results are summarised in the PR handoff, not by a post-gate commit.

## Critique (once, prospective)

* Risk: scope widening through main. Applied: stop at FULL if the main-relative diff shows product changes.
* Risk: stale or foreign package imports. Applied: hash identity proof and no production-src path.
* Risk: browser contention. Applied: non-queued flock.
* Risk: pass read as acceptance. Applied: no WCAG, AT, user, human or model claim.
* Verdict: proceed unchanged.
