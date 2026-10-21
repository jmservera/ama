<!-- markdownlint-disable-file -->
# RPI Changes: issue-151-cited-answer-contrast

## Metadata

* Task ID: issue-151-cited-answer-contrast
* Related plan: .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/issue-151-cited-answer-contrast-phase-details.md
* Implementation date: 2026-10-21

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: all tasks have completion evidence below. Complete local RPI gate and hosted CI are not part of this scope and were not run.

## Execution Summary

Reproduced the failure class deterministically, wrote the regressions first and confirmed they fail on the unfixed CSS, removed the button background fade, restored four certifi requirement files and validated with the focused checks.

## Completed Work

### Red evidence before the fix (P01)

* Related phase or task: P01-T01, P01-T02
* Files: src/api/tests/test_regulatory_ux_check.py, src/api/checks/regulatory_ux_check.py
* Unit red: `test_button_background_is_not_animated` failed: `['background-color'] != []` ("Buttons must not fade their background...").
* Browser red (new helper, unfixed CSS): `AssertionError: Re-enabled lookup button background is rgb(100, 151, 160) at 35% of its fade; expected the brand colour (animated: ['background-color', 'border-bottom-color', ...])`.
* Axe red on the same state (uncommitted probe, before the helper existed): `color-contrast` 3.24:1, #ffffff on #6497a0, 16px normal, target `#regulatory-chat > form > button[type="submit"]`. In the committed helper the colour assertion fires before axe, so axe's own violation on red was observed through the probe, not the committed helper. This differs from AC-1 wording and is disclosed.
* Reproduction note: baseline natural runs pass locally (17 states); the natural hosted timing was not reproduced, only the frozen mid-fade state.

### Button transition fix (P02-T01)

* Related phase or task: P02-T01
* Files: src/api/src/zava_forward/api/web/style.css (line 191 split: `button,.btn` transitions border-color only; `.item,.tile` unchanged)
* Axe rules, tags, selectors and existing states unchanged; reduced-motion override unchanged; focus, native semantics untouched.

### Browser helper and unit test (P01)

* Files: src/api/checks/regulatory_ux_check.py (`scan_mid_fade`, called after `cited-answer`; adds states `cited-answer-fade-35pct` and `-50pct`; restores focus to the question field and cancels paused animations); src/api/tests/test_regulatory_ux_check.py.

### Requirements files (P03-T01)

* Files: src/api/requirements.txt, src/core/requirements.txt, src/importer/requirements.txt, src/orchestrator/requirements.txt
* Restored by path from a3257c71f4963d98a88c501d040b3d07eada4392 (certifi 2026.7.22 to 2026.10.19, GHSA-6q48-6c7w-9gw2). The diff was verified to contain only the certifi version and its two hash lines in each file. No tracking files copied.

### README (P03-T02)

* Files: src/api/README.md (one paragraph describing the mid-fade states and their limits).

## Validation

Environment: /tmp/ama-221-pr419-venv interpreter (an existing local venv whose editable installs point at another worktree) with PYTHONPATH set to this worktree's src (verified `zava_forward.api.web.__path__` resolves here); PYTHONDONTWRITEBYTECODE=1; axe /tmp/ama-220-axe.min.js, SHA-256 880970c0...a68bb verified by the check. This environment is an unrecorded local prerequisite, not a reproducible install.

| Command (from repo root unless noted) | Result |
| --- | --- |
| `python src/api/checks/regulatory_ux_check.py --axe /tmp/ama-220-axe.min.js --out ...` on base CSS before changes | PASS 17 states |
| same, new helper, unfixed CSS (twice) | FAIL as quoted above |
| same, fixed CSS | PASS: 19 browser states ... axe executed |
| `(cd src/api && python -m checks.design_system_browser_check)` | PASS (tail: partial AC-034/043 only) |
| `(cd src/api && python -m unittest tests.test_regulatory_ux_check -q)` | unfixed CSS: 1 failure; fixed: Ran 5, OK |
| `python -m unittest test_regulatory_chat_api test_rule_alerts test_chat_panel test_chat_isolation test_accessibility_baseline test_design_system test_role_matrix -q` | Ran 94, OK (rerun on the final tree after the last edits) |
| `(cd src/api && ruff check .)` | pass after renaming an unused loop variable (an earlier run reported B007 on my test; fixed) |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/regulatory_ux_check.py` and `ruff format --isolated --line-length 100 --check` | pass |
| `(cd src/api && mypy)` | Success: no issues found in 63 source files |
| Observation: `.alt` button hover computed style | rgb(255, 255, 255) background, rgb(11, 93, 107) text (critique PC-004 confirmed; no defect) |
| web-design-guidelines source fetched 2026-10-21 before edits; Animation rule "list properties explicitly" and reduced-motion rule respected | retrieved in full |

Not performed: complete local RPI gate (`tools/rpi-checks.py --all`), Docker/SQL/full suites, hosted CI, manual screen-reader or keyboard session.

## Deviations and Follow-Up Items

* Divergence: the committed red state fails on the helper's colour assertion rather than directly on axe (disclosed above).
* No follow-up items. The `.alt` hover item was dropped after observation.

## Integration Continuation (2026-10-21)

* New base: origin/main ca4baf75837de57c99718f7423716d5dc0b0e244 (includes merged PR #420).
* Run-owned branch fix/regulatory-contrast-151 rebased locally without conflicts. Not pushed. The rebase dropped the four certifi requirements restores because main already carries certifi 2026.10.19 from PR #420 (verified in all four files); the issue-specific CSS, helper, test, README and RPI evidence are preserved.
* The earlier P03-T01 requirements evidence above is historical; the final branch diff no longer touches the requirements files.
* The single original Review is unchanged and still stands as the historical verdict. Prior exact-head gate evidence is historical, not current acceptance.
* Focused validation on the rebased tree: `unittest tests.test_regulatory_ux_check` Ran 5, OK; `regulatory_ux_check.py` PASS 19 browser states, axe executed. Same unrecorded local venv with PYTHONPATH as above.
* Not run: complete local RPI gate, hosted CI, Docker, Azure. The coordinator serializes the complete gate on the new head.
* Residual work unchanged: RV-001 optional cleanup, RV-002 optional guard, RV-003 complete gate and hosted check, RV-004 environment reproducibility.
