<!-- markdownlint-disable-file -->
# Changes: Issue 134 walkthrough (2026-11-10)

Plan: [plan](../plans/2026-11-10-walkthrough-plan-134-1110-plan.md). Status: complete; Review executed once (see review artifact). Review findings 1 and 3 applied: PROXY_NOTE and comment fix in perspective_walkthroughs.py.

## Admission

Root admitted P0, bounded P1, P2 and P3 (test-only; no product, API, UI, permission or oracle fix; no status enum change; no pass; no relaxation).

## P0

* Owned venv `/tmp/z134-venv` (system site packages, `pip install --no-deps -e` of src/core, src/agents, src/api only); imports of `zava_forward.core.perspective_walkthroughs` and `zava_forward.api.server` resolve under this worktree.
* `flock -n /tmp/ama-rpi-heavy.lock true` succeeded (non-queued); scratch `/tmp/z134-N`.

## P1

* `cd src/api && flock -n /tmp/ama-rpi-heavy.lock env ZF_BROWSER_SCRATCH=/tmp/z134-1 /tmp/z134-venv/bin/python -m checks.workbench_browser_check`: exit 0, 124 PASS lines, log `/tmp/z134-logs/p1-workbench.log`. Covers own queue, navigation, empty explanation, reset and status for the eight fixture logins; no specialist-screen keyboard or status coverage (the gap P2 targets).

## P2 (test-only)

* New `src/api/checks/specialist_keyboard_browser_check.py`: Tab, Shift+Tab and Enter only; per fixture login it enters Specialist screens, opens every served screen, selects the first listed home, reaches the labelled evidence region, the existing-workspace link and Reset screen view, and asserts the exact `#workspace-status` text; three negative controls (removed recovery link, blank status, unfocusable region). Endpoint and handoff wording is reported as text presence only.
* New `src/api/tests/test_specialist_keyboard_check.py`: two pure-helper tests (status text, marker reporting).
* Run: `cd src/api && flock -n /tmp/ama-rpi-heavy.lock env ZF_BROWSER_SCRATCH=/tmp/z134-2 /tmp/z134-venv/bin/python -m checks.specialist_keyboard_browser_check`. First attempt exit 1 (probe bug: it waited for a nonempty own queue, but the Retrofit Coordinator queue is empty; test-only fix, log `p2-run1.log`). Run 2 and the final run on the formatted file: exit 0, 236 PASS, 0 FAIL (`p2-run2.log`, `p2-final.log`). 8 logins, 13 distinct screens, 38 role-screen walks, 0 walks without a permitted home.
* Observed on the first listed home only (per screen, count of role walks showing the text or region): resident-choice endpoint 1/4, handoff 1/4; resident-service-issues endpoint 4/4, handoff 4/4, no evidence region 0/4; hazard-triage endpoint 0/3; safety-lead endpoint 0/3; procurement-packages handoff 0/2; finance-invoices handoff 0/3; finance-funding endpoint 0/3; contractor-job-pack handoff 0/1; quality-queue, finance-* and procurement-packages show no table region. These are explicit gaps (wording presence, not product defects confirmed), none repaired or waived. Keyboard reach, visible focus, reset and exact status held on every walked pair.
* Not covered: assistive-technology output, real authentication, Asset/Procurement/Auditor logins (proxy through manager roles), second home or page selection, AC-035 reassignment, AC-037 second-measure isolation (fixture holds one decision), AC-041 denominator and filter-impact text.

## P3 (register and reason only; statuses unchanged)

* `perspective_walkthroughs.py`: `NOTICE` and docstring reworded; `PROBE_OBSERVED` merges the probe as evidence per element only where observed; statuses stay partial or unmet, ELEMENTS unchanged. No pass, no tick.
* `journey_acceptance.py`: AC-034 reason replaces the stale "No browser run" text and adds the probe to evidence (still partial); AC-036 reason notes owner text presence is not label agreement (still deferred). Other criteria untouched.
* `src/api/README.md`: one paragraph documenting the probe.
* KB index/log not changed (checkpoint 440 owns its section; no KB file added or moved).

## Validation

* `ruff check` and `ruff format --check` (installed 0.17.3, pinned 0.17.1) and `mypy` (2.4.1, pinned 2.4.0) on the two new files and the two core files: pass.
* `src/core`: `python -m unittest tests.test_perspective_walkthroughs tests.test_journey_acceptance tests.test_scenario_manifest`: 16 OK.
* `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_specialist_keyboard_check.py"`: 2 OK; `-p "test_browser_*.py"`: 14 OK.
* No full gate, no `--changed`, no hosted CI observed. Logs: ROOT/134-admitted-evidence-1110/.
