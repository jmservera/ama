# Changes: issue #1828

* Date: 2026-11-16
* Status: implementation complete; validation below. Base main 18d3de459f20018e91fab3af87ab0d89123661c6.
* Tier: FOCUSED. Basis: one local browser check file, wait logic only; no app, permission, consent, SQL, deployment,
  workflow, dependency or gate-semantics change; assertion text and strength unchanged (strengthened by a post-key
  observation hold). Hosted CI does not run this browser harness, so it is a direct local check.

## Source change (single file)

`src/api/checks/map_fullscreen_browser_check.py`

* `settle_map_reads`: replaces `expect(aria-busy)` plus `wait_for_load_state("networkidle")` in
  `check_browser_shortcuts`. Observes first, resets on any `/api/map?` request or busy state, requires a 400 ms quiet
  window (twice Leaflet's 200 ms debounce), 10 s deadline, listener removed in `finally`.
* `check_browser_shortcuts`: 400 ms post-key observation hold before the unchanged assertion
  `{mode} browser shortcuts issue no map requests`.
* `check_viewport_change_requests_map`: proves a real viewport change still requests the map (ordinary viewport reads
  kept).
* `check_shortcuts_after_pending_resize`: deterministic regression; resizes the viewport and immediately runs the shortcut
  check.
* Both new checks run in `run_browser` before the existing embedded shortcut check.

Edit method note: the first stage-1 edit was applied with a Python replace script rather than the edit tool; the diff
was reviewed afterwards. Later edits used the edit tool.

Not edited: app JS (diagnosis shows app behaviour correct), `style.css`, `case_journey_browser_check.py`, the #440
worktree.

## Failing-first

Scratch driver `/tmp/1828/ff.py` (not committed) with stage 1 code and the old wait: 5 of 5 runs FAIL with
`embedded after a pending resize browser shortcuts issue no map requests` (`/tmp/1828/failing-first.log`). After the
settle: 5 of 5 PASS, and an injected delayed key-triggered read (`mutant`, ctrl keydown then 100 ms fetch) still FAILS
the assertion (`/tmp/1828/after-fix.log`).

## Validation (venv `/tmp/1828/venv`, editable installs of this worktree, axe 4.10.3 sha256 880970c0...a68bb verified by the check)

| Command | Result |
| --- | --- |
| Base, unmodified full map check | exit 0, 272 PASS (timing dependent; original failure not reproduced in this one run) |
| Base instrumented probe, 6 runs | 3 FAIL (resize at 5926 ms, fetch at 6126 ms, first key 6135 ms), 3 PASS |
| `python -m checks.map_fullscreen_browser_check --axe ... --out /tmp/1828/full1` (from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`, under `flock -n /tmp/ama-rpi-heavy.lock`) | exit 0, 330 PASS, 0 FAIL, 0 skip lines, 14 axe scans, 0 violations |
| Same, `/tmp/1828/full2` | exit 0, 330 PASS, 0 FAIL |
| Same after the review fix (premise-check viewport restore in `try/finally`), `/tmp/1828/full3`, final head content | exit 0, 330 PASS, 0 FAIL, 0 skip lines; `ruff check` and `ruff format --check` pass (`full3-final.log`) |
| 330 minus 272 | 58 new PASS lines: 1 premise + 56 shortcut results + 1 no-request |
| unittest discover `test_map_sensors.py` | Ran 13, OK |
| unittest discover `test_role_*.py` | Ran 78, OK |
| `test_ui_support.py` / `test_browser_harness_scratch.py` / `test_employee_acceptance_check.py` | Ran 12 / 4 / 13, OK |
| `ruff check` and `ruff format --check` on the check file | pass |

An initial `python -m unittest tests.test_...` invocation errored (5 errors) because of the wrong import layout
(`tests` is not a package for that call); it is not a test result and was rerun with the repository's `discover`
form above.

Raw logs: `/tmp/1828/` and a committed copy under `.copilot-tracking/evidence/2026-11-16/issue-1828-map-shortcuts/`
(the 3.3 MB axe JSON is reduced to `full1-axe-summary.tsv`: state, violations, incomplete; 14 scans, 0 violations, 1
incomplete item each, none an `aria-` rule, as the check requires). External witness log:
`/home/azureuser/.local/share/ama/phase-witness/rpi-1828-map-shortcuts-20261116T162749Z/`.

## Limits

* The original #440 failure was not reproduced by the unmodified full check in this run; the cause rests on the
  instrumented probe (3 of 6 failing, stack and timing evidence), not on that single run.
* Not run: complete local gate, SQL, resident or quality checks (out of scope for FOCUSED), hosted CI, assistive
  technology testing. Heavy lock was free for every browser run; the other session's Playwright driver and Chromium
  were not touched.
