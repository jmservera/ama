<!-- markdownlint-disable-file -->
# RPI Phase Details: Rebase Issue 130 Branch and Fix Refusal Feedback Focus-Blur Clearing

## Metadata

* Task ID: nomination-api-routes-130-c2
* Task slug: nomination-api-routes-130-c2
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md (`C1`–`C7`, `W1`)

## Phase Index

| Phase ID | Name                                                                                           | Status  | Detail sections        |
|----------|------------------------------------------------------------------------------------------------|---------|------------------------|
| P01      | Fetch and rebase `feat/ux-130-api-routes` onto `origin/feat/demo-233-same-home-tensions-0825`   | complete    | P01, P01-T01           |
| P02      | Restrict `_routeForm` `"change"` clearing to `<select>` controls and add unit regression test   | complete    | P02, P02-T01, P02-T02  |
| P03      | Run Focused Tier validation across unit tests, `case_journey_browser_check.py`, `ruff`, `mypy` | complete    | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Fetch and rebase `feat/ux-130-api-routes` onto `origin/feat/demo-233-same-home-tensions-0825`

### Context

`PR #1776` (`feat/ux-130-api-routes`) is stacked onto `PR #1639` (`feat/demo-233-same-home-tensions-0825`). Since merge-base `a1d0be5f6`, the parent branch advanced by commit `6510b6fbc` (`#1784`, programme coordinator WCAG 2.2 conformance), while `feat/ux-130-api-routes` holds `2215209cb` and `2786009ee` (`C6`). The only file modified on both branches is `src/api/src/zava_forward/api/web/app.js`, in completely disjoint functions (`isRoleScreensDestination`, `mapPanel`, `coordinatorView` versus `caseView`), and untracked Cycle 2 `-c2-` files under `.copilot-tracking/` do not overlap with any tracked path on either side (`C6`).

### Intent

Bring `feat/ux-130-api-routes` cleanly onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) before applying the Cycle 2 `panels.js` fix.

### Boundaries

* Included: Running `git fetch origin feat/demo-233-same-home-tensions-0825` and `git rebase origin/feat/demo-233-same-home-tensions-0825` on active branch `feat/ux-130-api-routes`, then verifying ancestry and commit replay.
* Excluded: Pushing to `origin`, renaming `feat/ux-130-api-routes`, or rewriting commits on `origin/feat/demo-233-same-home-tensions-0825`.

### Likely Targets

* Local Git branch `feat/ux-130-api-routes` in `/home/azureuser/source/ama-demo-wt/feat-130-api-routes`.

### Dependencies

* Clean tracked working tree (`git status --short --untracked-files=no` empty) prior to `git rebase`.

### Validation Expectations

* `git rebase` completes with exit code `0`, `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) is the base of the two replayed `#130` commits, and both `#1784` (`app.js` coordinator changes) and `#130` (`caseView` `nominationPanel(c, id, refresh)`) remain intact.

### Completion Evidence

* Post-rebase `git log --oneline -n 4` and `git merge-base` verification recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fetch target parent branch and rebase `feat/ux-130-api-routes` onto `6510b6fbc`

#### Context

Implements Caller Step 1 (`C6`).

#### Intent

Rebase `feat/ux-130-api-routes` cleanly onto the freshly fetched `origin/feat/demo-233-same-home-tensions-0825` ref.

#### Boundaries

* Included: `git fetch origin feat/demo-233-same-home-tensions-0825`, `git rebase origin/feat/demo-233-same-home-tensions-0825`, and read-only verification of `git log` and `app.js`.
* Excluded: Remote push or force-push.

#### Likely Targets

* Git branch history on `feat/ux-130-api-routes`.

#### Dependencies

* None.

#### Validation Expectations

* `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exits `0` with zero conflict markers.

#### Completion Evidence

* Rebased commit SHAs recorded in the changes artifact.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Restrict `_routeForm` `"change"` clearing to `<select>` controls and add unit regression test

### Context

In `src/api/checks/case_journey_browser_check.py` (`mutation_reconstruction`, `family == "challenge"`, `outcome == "refusal"`), `page.locator("#challenge-open-request").fill("Later evidence")` edits and focuses `#challenge-open-request` (`<input type="text">`) while the challenge POST is pending (`C1`). When the `409` refusal arrives, `nominationPanel._routeForm` sets `mutation.message` and `mutation.focus = true`, then `finally` sets `mutation.pending = false` and calls `mutation.update()` (`C2`). Inside `bindCaseMutationForm`, `status.textContent = state.message` is followed immediately by `status.focus()`, which synchronously blurs `#challenge-open-request` and fires a native DOM `"change"` event (`C2`). Because `nominationPanel._routeForm` attached `input.addEventListener("change", clearInvalid)` to all controls (`C3`)—unlike original `formFor`, which only attached `"input"` (`C4`)—`clearInvalid` sees `!mutation.pending && !session?.historyBarrier` and wipes `mutation.message` and `status.textContent` to `""`.

### Intent

Ensure `<input>` and `<textarea>` controls in `nominationPanel._routeForm` clear invalid/feedback state only on genuine `"input"` events, while `<select>` controls (`Boolean(options)`) continue handling both `"input"` and `"change"`, backed by a deterministic Node unit regression test.

### Boundaries

* Included: Surgical listener update in `nominationPanel._routeForm` (`src/api/src/zava_forward/api/web/panels.js`) and `1` new test method in `src/api/tests/test_nomination_screen.py` (`exact removals: none`, `max additions: 1`).
* Excluded: Modifying `bindCaseMutationForm`, altering DOM structure or `aria-invalid` counts (`9`), introducing banned content-standard words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), or touching `case_journey_browser_check.py`.

### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `nominationPanel._routeForm` field descriptor mapping and event listener loop.
* `src/api/tests/test_nomination_screen.py`: `NominationScreen` test class.

### Dependencies

* P01 (`P01-T01`).

### Validation Expectations

* `test_nomination_screen.py` passes with the new regression test, and `test_case_journey.py` continues passing all `31` slice/state-machine tests.

### Completion Evidence

* Minimal surgical diffs in `panels.js` and `test_nomination_screen.py` plus passing Node unit test output recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Scope `addEventListener("change", clearInvalid)` to `<select>` elements in `nominationPanel._routeForm`

#### Context

Inside `nominationPanel._routeForm` (`src/api/src/zava_forward/api/web/panels.js`), `options` is truthy if and only if the control is rendered as `h("select", ...)` (`C3`, `C5`). Recording `isSelect: Boolean(options)` on each `inputs` entry and guarding `if (isSelect) input.addEventListener("change", clearInvalid);` preserves `<select>` `"change"` behavior (including conditional `showWhen` visibility toggles for `channel` and `raised_by`) while preventing blur-triggered `"change"` events on `<input type="text">`, `<input type="date">`, and `<textarea>` from clearing `mutation.message` (`C3`–`C5`, `C7`, `W1`).

#### Intent

Eliminate blur-triggered clearing of `mutation.message` on non-`<select>` controls in `nominationPanel._routeForm`.

#### Boundaries

* Included: Adding `isSelect: Boolean(options)` to the returned field descriptor in `nominationPanel._routeForm` and changing `input.addEventListener("change", clearInvalid);` to `if (isSelect) input.addEventListener("change", clearInvalid);`.
* Excluded: Changing validation messages, `aria-invalid` / `aria-describedby` attributes, `tabindex: -1`, or `affectedChallengePanel` slice boundaries (`const formFor` .. `const staff`).

#### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `nominationPanel._routeForm`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `case_journey_browser_check.py`, `test_case_journey.py`, `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_epic149_form_error_summary_associations.py`, and `test_content_standard.py` all pass.

#### Completion Evidence

* Verified diff in `src/api/src/zava_forward/api/web/panels.js`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add Node unit regression test in `src/api/tests/test_nomination_screen.py`

#### Context

The existing Node unit harness did not simulate focus transfer where `status.focus()` blurs the currently focused `<input>` and dispatches `"change"` (`C2`, `C5`). Adding a single deterministic Node test in `src/api/tests/test_nomination_screen.py` evaluates `bindCaseMutationForm` + `panelOwned` + `nominationPanel._routeForm` with a realistic active-element blur->`"change"` hook so any regression is caught in `<1s` even outside Playwright.

#### Intent

Prove semantically in `src/api/tests/test_nomination_screen.py` that:
1. Submitting a `_routeForm` form, editing and focusing a text `<input>` while pending, and rejecting with HTTP `409` triggers `status.focus()`, blurs the `<input>` (firing `"change"`), and **preserves** the `409` refusal message on `#...-feedback`.
2. Firing `"input"` on that `<input>` afterwards clears `mutation.message` and `aria-invalid`.
3. Firing `"change"` on a `<select>` control (`channel`) updates conditional `showWhen` visibility (`assisted_channel`) and clears stale invalid/feedback state.

#### Boundaries

* Included: Adding `test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear` to `NominationScreen` in `src/api/tests/test_nomination_screen.py`.
* Excluded: Removing or weakening any existing test in `test_nomination_screen.py`.

#### Likely Targets

* `src/api/tests/test_nomination_screen.py`: `NominationScreen`.

#### Dependencies

* P02-T01.

#### Validation Expectations

* `test_nomination_screen.py` passes (`OK`) and fails if `if (isSelect)` is removed from `panels.js`.

#### Completion Evidence

* Passing `unittest` run of `src/api/tests/test_nomination_screen.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Run Focused Tier validation across unit tests, `case_journey_browser_check.py`, `ruff`, and `mypy`

### Context

Under Focused Tier validation (owner decision D4 / `#1294` and explicit caller boundary excluding `tools/rpi-checks.py`), Cycle 2 requires executing all targeted unit suites across `src/core` and `src/api` (plus coupled `test_case_journey.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, and rebased parent `test_programme_coordinator_wcag_230.py`), the end-to-end Playwright + axe-core `src/api/checks/case_journey_browser_check.py` harness, `ruff check`, `ruff format --check`, and `mypy`.

### Intent

Verify end-to-end resolution of `mutation_reconstruction` and complete static/unit cleanliness on the rebased branch before committing locally.

### Boundaries

* Included: Running the 6 caller-specified validation commands plus coupled `src/api` regression tests.
* Excluded: Running `tools/rpi-checks.py` or pushing to `origin`.

### Likely Targets

* Read-only validation across `src/core` and `src/api`; outputs recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.

### Dependencies

* P02 (`P02-T01`, `P02-T02`).

### Validation Expectations

* Every command exits `0`, including `case_journey_browser_check.py` end-to-end `mutation_reconstruction`.

### Completion Evidence

* Exact commands, test counts, and exit codes recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute targeted unit suites, `case_journey_browser_check.py`, `ruff`, and `mypy`

#### Context

Implements Caller Step 3 (`C1`, `C5`–`C7`). Note that `test_case_journey.py` resolves `tests.test_mvp` when `src/core` is included on `PYTHONPATH`.

#### Intent

Run all Focused Tier checks and verify `0` failures, `0` lint/format issues, and `0` type errors.

#### Boundaries

* Included:
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/core/tests -p "test_*nomination*.py" -q`
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/api/tests -p "test_*nomination*.py" -q`
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_resident_api.py src/api/tests/test_accessibility_baseline.py -q`
  * `PYTHONPATH=src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_case_journey.py src/api/tests/test_content_standard.py src/api/tests/test_epic149_form_error_summary_associations.py src/api/tests/test_programme_coordinator_wcag_230.py -q`
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 src/api/checks/case_journey_browser_check.py`
  * `python3 -m ruff check src/core src/api && python3 -m ruff format --check src/core src/api`
  * `(cd src/core && python3 -m mypy) && (cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`
* Excluded: `tools/rpi-checks.py`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.

#### Dependencies

* P02-T01 and P02-T02.

#### Validation Expectations

* All 7 commands exit `0`.

#### Completion Evidence

* Command results logged in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.

#### Unresolved Items

* None.
