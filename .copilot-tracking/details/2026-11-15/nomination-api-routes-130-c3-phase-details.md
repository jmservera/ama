<!-- markdownlint-disable-file -->
# RPI Phase Details: Pass Node Test Payloads via Stdin and Trim Redundant Nomination Panel Formatting

## Metadata

* Task ID: nomination-api-routes-130-c3
* Task slug: nomination-api-routes-130-c3
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md (`C1`–`C8`, `W1`)

## Phase Index

| Phase ID | Name                                                                                                               | Status  | Detail sections        |
|----------|--------------------------------------------------------------------------------------------------------------------|---------|------------------------|
| P01      | Pass JavaScript payloads via `stdin` across `src/api/tests/test_case_journey.py` and add `MAX_ARG_STRLEN` test     | complete | P01, P01-T01, P01-T02  |
| P02      | Trim redundant comments and formatting verbosity in `#130` nomination helpers inside `panels.js`                   | complete | P02, P02-T01           |
| P03      | Run Focused Tier validation from `src/api` across unit, WCAG baseline, lint, format, and type checks               | complete | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Pass JavaScript payloads via `stdin` across `src/api/tests/test_case_journey.py` and add `MAX_ARG_STRLEN` regression test

### Context

In GitHub Actions run `43707070068` (`job 132790451775`) on `PR #1776`, `test_case_journey.CaseJourney.test_quality_errors_and_manual_action_pending_siblings` failed with `OSError: [Errno 7] Argument list too long: 'node'` (`E2BIG`) (`C1`). That test concatenates `DOM + shipped_helpers() + (WEB / "ops.js").read_text() + (WEB / "panels.js").read_text()` plus its inline assertion harness into a single `script` string (`129,031` UTF-8 bytes on `HEAD` `f53340e8f`, exceeding Linux's `131,072`-byte `MAX_ARG_STRLEN` limit once merged with parent branch commit `50bd5acc0`) and passes `script` as a command-line argument via `subprocess.run(["node", "-e", script], text=True, capture_output=True)` (`C1`, `C6`). Across `src/api/tests/test_case_journey.py`, 22 `subprocess.run` calls invoke `node` with `-e` (20 `["node", "-e", script]`, 1 `["node", "-e", source + ...]` inside `evaluate()`, and 1 `["node", "--unhandled-rejections=strict", "-e", script]`), and zero scripts in `test_case_journey.py` or `src/api/src/zava_forward/api/web/*.js` inspect `process.stdin`, `__filename`, `__dirname`, or `process.argv` (`C2`, `C3`). Meanwhile, `src/api/tests/test_safety_panel_ux.py` imports `DOM, WEB, shipped_helpers` from `test_case_journey` (`C5`).

### Intent

Route all 22 Node script evaluations in `src/api/tests/test_case_journey.py` over `stdin` (`"-"`, `input=...`) so `argv` carries only tiny static flags regardless of shipped JavaScript file growth, and lock that guarantee with a deterministic `>131,072`-byte regression test.

### Boundaries

* Included: Updating all 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` to use `"-"` and `input=...`, and adding `1` regression test method (`test_node_stdin_handles_scripts_above_linux_max_arg_strlen`) in `CaseJourney` (`exact removals: none`, `max additions: 1`).
* Excluded: Altering `DOM`, `WEB`, or `shipped_helpers` signatures/exports (`C5`), weakening any assertion in `test_case_journey.py`, or touching other `src/api/tests/test_*.py` files (`C4`).

### Likely Targets

* `src/api/tests/test_case_journey.py`: `evaluate()` helper and `CaseJourney` test methods.

### Dependencies

* None.

### Validation Expectations

* All existing `CaseJourney` tests plus `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` pass (`OK`), `test_safety_panel_ux.py` passes (`OK`), and `ruff check` / `ruff format --check` / `mypy` report `0` issues on `tests/test_case_journey.py`.

### Completion Evidence

* Zero remaining `"-e"` flags in `src/api/tests/test_case_journey.py` and passing `-v` output for `CaseJourney` recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Convert all 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` from `-e <script>` on `argv` to `"-"` with `input=<script>`

#### Context

Implements Caller Requirement 1 (`C1`–`C5`). Passing `"-"` instructs Node.js to execute CommonJS source from `stdin` (`require("node:assert/strict")` works identically to `-e`), while preserving per-call options (`text=True`, `capture_output=True`, `timeout=30`, `check=True`, and `--unhandled-rejections=strict`).

#### Intent

Remove large JavaScript strings from `execve` `argv` across every `node` call in `src/api/tests/test_case_journey.py`.

#### Boundaries

* Included:
  * `evaluate(expression: str) -> Any`: `subprocess.run(["node", "-"], input=source + f"\nconsole.log(JSON.stringify({expression}));", text=True, capture_output=True, check=True)`
  * Standard `CaseJourney` harnesses (20 sites, including `test_quality_errors_and_manual_action_pending_siblings`): `subprocess.run(["node", "-"], input=script, ...)` preserving `text=True`, `capture_output=True`, and any `timeout=30` or `check=True` kwargs
  * Strict unhandled-rejections harness (1 site): `subprocess.run(["node", "--unhandled-rejections=strict", "-"], input=script, text=True, capture_output=True, timeout=30)`
* Excluded: Changing any JavaScript assertion body or `DOM` / `WEB` / `shipped_helpers` module exports.

#### Likely Targets

* `src/api/tests/test_case_journey.py`.

#### Dependencies

* None.

#### Validation Expectations

* `grep` confirms `0` `"-e"` matches in `src/api/tests/test_case_journey.py`, and all existing `CaseJourney` tests pass.

#### Completion Evidence

* Clean diff in `src/api/tests/test_case_journey.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `>131,072`-byte `MAX_ARG_STRLEN` stdin regression test in `src/api/tests/test_case_journey.py`

#### Context

On standalone `HEAD` before merging `50bd5acc0`, `DOM + shipped_helpers() + ops.js + panels.js` is ~`129 KB`, just beneath Linux's `131,072`-byte `MAX_ARG_STRLEN` limit (`C1`, `C6`). Adding `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` constructs a script combining `DOM + shipped_helpers() + ops.js + panels.js`, appends a `>16,384`-byte comment pad so `len(script.encode("utf-8")) > 131_072` is explicitly asserted in Python, and executes shipped helper assertions (`nominationPanel._routeForm` and `panelOwned`) via `["node", "-"]` with `input=script`. Without the `stdin` fix (`["node", "-e", script]`), `execve` immediately fails with `OSError: [Errno 7] Argument list too long: 'node'` on Linux; with `["node", "-"]` and `input=script`, it succeeds deterministically.

#### Intent

Provide permanent standalone regression proof against `MAX_ARG_STRLEN` (`131,072` bytes) even before branch merges grow `ops.js` or `panels.js`.

#### Boundaries

* Included: Adding `test_node_stdin_handles_scripts_above_linux_max_arg_strlen(self) -> None` to `CaseJourney` in `src/api/tests/test_case_journey.py`.
* Excluded: Modifying any other test file.

#### Likely Targets

* `src/api/tests/test_case_journey.py`: `CaseJourney`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Test asserts `len(script.encode("utf-8")) > 131_072`, runs `["node", "-"]` with `input=script`, and passes (`returncode == 0`, stdout `"ok"`), formatted and typed cleanly for `ruff` and `mypy`.

#### Completion Evidence

* Passing verbose `unittest` execution of `test_node_stdin_handles_scripts_above_linux_max_arg_strlen`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Trim redundant comments and formatting verbosity in `#130` nomination helpers inside `panels.js`

### Context

Caller Requirement 1 asks to keep `src/api/src/zava_forward/api/web/panels.js` concise if redundant comments or whitespace can be trimmed without changing behavior. Research (`C6`–`C8`, `W1`) established three strict safety boundaries on `panels.js`:
1. **Stacked-parent merge boundary (`C6`)**: `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`) edits `actForm` and `residentPanel` near the top of `panels.js`. Any edit in `panels.js` must stay strictly inside `#130`'s `nominationPanel` / `nominationPanel._explanationView` / `nominationPanel._routeForm` region so `PR #1776` merges cleanly with zero conflict.
2. **Test slice anchors (`C8`)**: `test_nomination_screen.py` slices `function nominationPanel` .. `\nfunction affectedChallengePanel`, and `test_case_journey.py` slices `const panelOwned = `, `\nconst PANEL_SUPPORT`, `function bindCaseMutationForm`, `function actForm`, `function captureChallengeDrafts`, `function affectedChallengePanel`, `  const residentForm = `, `  const serviceForm`, `  const formFor = `, and `  const staff`. All anchor strings must remain untouched.
3. **Accessibility and content invariants (`C7`, `W1`)**: `setAttribute("aria-invalid", "true")` count across `web/*.js` must stay `9`, `input.focus()` in `nominationPanel._routeForm` must stay within `±4` lines of `input.setAttribute("aria-invalid", "true")`, `"aria-describedby": status.id` and `tabindex: -1` must remain intact, and zero user-visible copy strings may change.

Inside `nominationPanel`, `nominationPanel._explanationView`, and `nominationPanel._routeForm`, duplicated `assisted_channel` option lists across `ackForm` and `corrForm` can share a local constant inside `nominationPanel`, redundant inline comment lines can be removed, and expanded 1-property-per-line field/config object literals can be formatted concisely on single readable lines, trimming ~`1.5–2.5 KB` without altering a single runtime instruction, DOM attribute, or user-visible character.

### Intent

Trim redundant comments, duplicated local option boilerplate, and verbose multiline whitespace inside `#130`'s `nominationPanel` helpers in `src/api/src/zava_forward/api/web/panels.js` with zero behavioral, accessibility, or merge impact.

### Boundaries

* Included: Behavior-preserving conciseness edits strictly between `function nominationPanel(` and `\nfunction affectedChallengePanel(` in `src/api/src/zava_forward/api/web/panels.js`.
* Excluded: Any edit outside `nominationPanel` .. `nominationPanel._routeForm`, any change to user-facing copy or DOM attributes, or any edit moving `input.focus()` away from `input.setAttribute("aria-invalid", "true")`.

### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `nominationPanel`, `nominationPanel._explanationView`, and `nominationPanel._routeForm`.

### Dependencies

* P01 (`P01-T01`, `P01-T02`).

### Validation Expectations

* `node --check src/api/src/zava_forward/api/web/panels.js` exits `0`, `panels.js` byte length is reduced, and all nomination, case-journey, Epic #149, WCAG 2.2 baseline, and content-standard tests pass.

### Completion Evidence

* Before/after byte count of `panels.js` and passing static/unit suite results recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Compact redundant comment and multiline descriptor formatting inside `nominationPanel` and `nominationPanel._routeForm`

#### Context

Implements the second clause of Caller Requirement 1 (`C6`–`C8`, `W1`).

#### Intent

Keep `nominationPanel`, `nominationPanel._explanationView`, and `nominationPanel._routeForm` concise and readable while preserving 100% identical runtime semantics and static-test anchors.

#### Boundaries

* Included: Sharing the repeated `assistedMediums` option array and `isNonDigital` predicate across `ackForm` and `corrForm` inside `nominationPanel` and compacting expanded multi-line field-descriptor objects inside `nominationPanel` / `_explanationView` / `_routeForm` while keeping every `panelOwned(` call on its single source line and preserving the `±4`-line window around `input.setAttribute("aria-invalid", "true")` and `input.focus()`.
* Excluded: Touching `actForm`, `residentPanel`, `captureChallengeDrafts`, `restoreChallengeDrafts`, `affectedChallengePanel`, or any user-visible label/message text.

#### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`.

#### Dependencies

* P01-T01 and P01-T02.

#### Validation Expectations

* `node --check`, `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_case_journey.py`, `test_epic149_form_error_summary_associations.py`, `test_accessibility_baseline.py`, and `test_content_standard.py` all exit `0`.

#### Completion Evidence

* Verified diff in `src/api/src/zava_forward/api/web/panels.js`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Run Focused Tier validation from `src/api` across unit, WCAG baseline, lint, format, and type checks

### Context

Under Focused Tier validation (owner decision D4 / `#1294` and Caller Requirement 2), Cycle 3 verifies `tests/test_case_journey.py` and `tests/test_accessibility_baseline.py` (`-v`), coupled nomination/Epic #149/content-standard/safety-panel unit suites, and `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` from `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api`. Because the shared host Python environment has an editable `.pth` pointing at an absent sibling worktree, prepending `src` to `PYTHONPATH` (`PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`) resolves `zava_forward.api` to this worktree without mutating shared `site-packages`.

### Intent

Confirm zero unit, accessibility, lint, format, or static-type regressions before committing Cycle 3 locally.

### Boundaries

* Included: Running the targeted `unittest -v` suites and `ruff check . && ruff format --check . && mypy` from `src/api`.
* Excluded: Mutating global/shared `pip` editable installs or pushing to `origin`.

### Likely Targets

* Read-only verification from `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api`; results recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.

### Dependencies

* P02 (`P02-T01`).

### Validation Expectations

* Every validation command exits `0` with `0` skipped/errored tests in `test_case_journey.py` and `test_accessibility_baseline.py`.

### Completion Evidence

* Exact commands, test counts, and exit codes recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute targeted `unittest`, `ruff check`, `ruff format --check`, and `mypy` suites from `src/api`

#### Context

Implements Caller Requirement 2 (`C5`, `C7`, `C8`).

#### Intent

Run all planned Focused Tier checks from `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api` and confirm `0` failures.

#### Boundaries

* Included:
  * `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_accessibility_baseline.py -v`
  * `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_nomination_screen.py tests/test_nomination_api_routes.py tests/test_epic149_form_error_summary_associations.py tests/test_content_standard.py tests/test_safety_panel_ux.py -q`
  * `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy`
* Excluded: Remote Git operations.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.

#### Dependencies

* P01-T01, P01-T02, and P02-T01.

#### Validation Expectations

* All commands exit `0`.

#### Completion Evidence

* Logged command outputs and counts in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.

#### Unresolved Items

* None.
