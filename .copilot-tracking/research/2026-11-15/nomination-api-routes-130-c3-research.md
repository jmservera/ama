<!-- markdownlint-disable-file -->

# Task Research: nomination-api-routes-130-c3

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (RPI Agent automatic session)                                     |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md |

## Research Brief

* What to research: Root cause and complete fix for `OSError: [Errno 7] Argument list too long: 'node'` (`E2BIG` on Linux `MAX_ARG_STRLEN` = `131,072` bytes) in `src/api/tests/test_case_journey.py` (`test_quality_errors_and_manual_action_pending_siblings` at line 1040 and all other `subprocess.run(["node", ..., "-e", script], ...)` calls in `test_case_journey.py`), potential `MAX_ARG_STRLEN` exposure in adjacent `src/api/tests/` harnesses, and safe conciseness opportunities in `src/api/src/zava_forward/api/web/panels.js`.
* Why it matters: In `PR #1776` (`f53340e8f`), 9/10 CI checks passed and `3,599/3,600` `src-api` unit tests passed, with only `test_case_journey.CaseJourney.test_quality_errors_and_manual_action_pending_siblings` failing on `E2BIG` when `DOM + shipped_helpers() + ops.js + panels.js + test_harness` exceeded `131,072` bytes on `argv` in GitHub Actions' PR merge checkout (`refs/pull/1776/merge` merging `f53340e8f` with `50bd5acc0`).
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this continuous automatic RPI execution.
* Scope: `src/api/tests/test_case_journey.py`, `src/api/src/zava_forward/api/web/panels.js`, adjacent `src/api/tests/` `node -e` invocations (read-only audit), and Git merge-preview diff against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`).
* Non-goals: Pushing to `origin`, rebasing or rewriting history, deleting or modifying Cycle 1 or Cycle 2 `.copilot-tracking/` artifacts, or changing runtime behavior in `panels.js`.
* Criteria: Passing `script` via stdin (`["node", "-"]` or `["node", "--unhandled-rejections=strict", "-"]` with `input=script`) eliminates `argv` `MAX_ARG_STRLEN` failures across all 22 `node` invocations in `test_case_journey.py`; conciseness trims in `panels.js` stay strictly inside `#130`-owned lines (`329–925`, disjoint from `50bd5acc0` lines `43–290`) and preserve behavior, static Epic #149 / content-standard / WCAG invariants, and Web Interface Guidelines (`W1`); requested unit, accessibility, Ruff, and Mypy checks pass.
* Requested outputs: Converged Cycle 3 fix specification ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                   |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q4 covering `MAX_ARG_STRLEN` trigger mechanics, all `node -e` sites in `test_case_journey.py` (and `node -` stdin semantics), adjacent test risks, and safe merge-clean `panels.js` conciseness trims. |
| Codebase scope                       | `src/api/tests/`, `src/api/src/zava_forward/api/web/`                                                                                   |
| External scope                       | Vercel Web Interface Guidelines (`raw.githubusercontent.com/vercel-labs/web-interface-guidelines`) per repository Web Development Guidance |
| Initial internal candidate areas     | `src/api/tests/test_case_journey.py`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_content_standard.py` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                |
| Research posture                     | focused                                                                                                                                 |
| Posture provenance                   | default (bounded CI `E2BIG` test-invocation fix + safe conciseness check with named files and failure log)                              |
| Explicit limits / deadline           | Focused validation tier; single continuous RPI run ending in clean local commit on `feat/ux-130-api-routes` without push                |
| Posture-specific completion basis    | Focused scope and materiality: all `node` `argv` lengths, `node -` stdin semantics, and `panels.js` static/merge invariants verified    |
| Edits allowed during research?       | no, research-only                                                                                                                       |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                            |
| Known constraints / excluded sources | Never read private datasets; preserve `c1` and `c2` `.copilot-tracking/` artifacts unchanged; do NOT push                               |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                                 | Match and provenance                                             | Scoped authority or output contract                                           | Selected / skipped reason                                                                 |
|---------------------|-----------------------------------------------------------|------------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repo Instructions) | `applyTo: "**"` matches workspace and tracking paths             | Enforces branch reuse (`feat/ux-130-api-routes`), focused tier, and web rules | Selected: governs reuse of `PR #1776` head branch, focused validation, and web review     |
| Skill               | `web-design-guidelines`                                   | Required by Web Development Guidance before editing `panels.js`  | Fetches current Vercel Web Interface Guidelines (`W1`) for `file:line` review | Selected: loaded and fetched (`W1`) before planning/implementing `panels.js` edits        |
| Skill               | `redesign-existing-projects`                              | Existing-app design improvements                                 | Scoped visual/UX redesign guidance                                            | Skipped: task is a subprocess stdin fix + behavior-preserving formatting trim             |
| Research specialist | `hve-core-all:rpi-researcher`                             | Registered general RPI research worker                           | Independent subagent lane artifact                                            | Skipped for inline execution: bounded 2-file trace resolved in `<6` direct reads          |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                              | Answers / unanswered          | Resulting decision or selected further research                                           |
|------------------|------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------------------|
| Intake           | Non-interactive runtime; caller supplied exact CI stack trace, root cause (`MAX_ARG_STRLEN`), target files, and validation commands | N/A (non-interactive runtime) | Proceed automatically in confirmed `automatic` RPI mode                                   |
| Direction change | Verified why local `HEAD` (`f53340e8f`, `129,031` bytes) passed while CI PR merge commit (`+50bd5acc0`, `>131,072` bytes) hit `E2BIG` | N/A (evidence confirmation)   | Keep `panels.js` conciseness trims strictly below line 329 to stay disjoint from `50bd5acc0` |
| Convergence      | All 4 research questions answered with primary CI log, codebase, Node runtime, and Git merge-diff evidence                          | N/A (non-interactive runtime) | Converge on stdin (`["node", "-"]`, `input=...`) across `test_case_journey.py` + safe `panels.js` trim |

## Scope and Success Criteria

* Scope: Update `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` to pass JavaScript payloads on `stdin` (`["node", "-"]` / `["node", "--unhandled-rejections=strict", "-"]` with `input=...`) instead of `-e script` on `argv`, trim redundant whitespace/duplicate field-option boilerplate inside `#130`-owned `nominationPanel` / `_routeForm` lines in `src/api/src/zava_forward/api/web/panels.js` without changing behavior or touching `50bd5acc0` hunks, verify all requested unit/WCAG/lint/type checks, and commit cleanly on `feat/ux-130-api-routes` without pushing.
* Assumptions: Verified rather than trusted—inspected GitHub Actions run `43707070068` (`job 132790451775`), measured exact UTF-8 byte counts, audited all 57 test files using `node -e` across `src/api/tests/`, and verified `node -` / `node --unhandled-rejections=strict -` stdin execution.
* Success criteria:
  * Every research question is answered with primary `path:line` (`C1`–`C8`) and external (`W1`) evidence.
  * Findings, decisions, and readiness cite Evidence Log IDs.
  * Alternatives are evaluated and one recommendation is selected in `convergence` mode.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Replace `-e script` on `argv` with stdin (`["node", "-"]` with `input=script`) in `src/api/tests/test_case_journey.py` (line 1040 and other concatenated JS calls); keep `src/api/src/zava_forward/api/web/panels.js` concise if redundant comments/whitespace can be trimmed without changing behavior; run `test_case_journey.py`, `test_accessibility_baseline.py`, `ruff check`, `ruff format --check`, and `mypy` from `src/api`; record `c3` RPI artifacts preserving `c1`/`c2` unchanged; commit cleanly on `feat/ux-130-api-routes` without pushing.
* Inferred research questions: Explain why `test_quality_errors_and_manual_action_pending_siblings` failed on GitHub Actions `PR #1776` while passing on local `f53340e8f`; audit all 22 `node -e` calls in `test_case_journey.py` and all other `src/api/tests/test_*.py` files for `MAX_ARG_STRLEN` exposure and `process.stdin`/`__dirname`/`__filename` compatibility; verify slice anchors and static checks on `panels.js` (`test_nomination_screen.py`, `test_epic149_form_error_summary_associations.py`, `test_accessibility_baseline.py`, `test_content_standard.py`) plus diff disjointness against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`).
* Caller constraints and non-goals: Focused validation tier; preserve `c1` and `c2` `.copilot-tracking/` artifacts unchanged; do NOT push from inside the session.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                                 | Source / checkpoint   | Effect on active brief, evidence, or revalidation                                    |
|----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-----------------------|--------------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier on `src/api` (`test_case_journey.py`, `test_accessibility_baseline.py`, coupled nomination/content checks, `ruff`, `mypy`) | Caller prompt + D4/#1294 | Targets `test_case_journey.py` and `#130` slice of `panels.js`                       |
| exclude                                                  | Do NOT push to remote; do NOT modify or delete Cycle 1 or Cycle 2 `.copilot-tracking/` artifacts                      | Caller + repo rules   | Uses new `-c3` slug `nomination-api-routes-130-c3` on `feat/ux-130-api-routes`       |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type            | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Why did `test_quality_errors_and_manual_action_pending_siblings` fail with `E2BIG` on CI (`PR #1776`), and which `node -e` calls in `test_case_journey.py` are exposed? | depth           | H        | answered |
| Q2 | Does passing `script` via stdin (`["node", "-"]` and `["node", "--unhandled-rejections=strict", "-"]` with `input=script`) preserve exact CommonJS/exit/assertion semantics across all 22 calls in `test_case_journey.py`? | depth           | H        | answered |
| Q3 | Are any other `src/api/tests/test_*.py` files concatenating full shipped JS modules onto `node -e` `argv`, or importing symbols from `test_case_journey.py`? | breadth         | M        | answered |
| Q4 | Which redundant comments/whitespace/formatting in `src/api/src/zava_forward/api/web/panels.js` can be trimmed without changing behavior, breaking static/slice tests, or conflicting with `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`)? | depth           | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/nomination-api-routes-130-c2-state.json`, `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md`, and `.copilot-tracking/reviews/logs/2026-11-15/nomination-api-routes-130-c2-review.md`.
* Reused (verified) findings: Active `PR #1776` head branch is `feat/ux-130-api-routes` targeting `feat/demo-233-same-home-tensions-0825`; Epic #149 `9`-site `aria-invalid` count and 4-line focus window invariants (`C7`) and `test_content_standard.py` `panelOwned` rules (`C8`) remain active.
* Superseded / stale: Cycle 2 ran `test_case_journey.py` against local `HEAD` `f53340e8f` (`129,031` UTF-8 bytes on `argv`, `2,041` bytes under `MAX_ARG_STRLEN`), before base branch `feat/demo-233-same-home-tensions-0825` advanced to `50bd5acc0` (`#1786`, adding `+52` net lines in `panels.js` and `+13` net lines in `app.js`), which pushed GitHub Actions' `refs/pull/1776/merge` commit past `131,072` bytes (`C1`, `C2`, `C6`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier; preserve `c1` and `c2` `.copilot-tracking/` artifacts; commit locally on `feat/ux-130-api-routes` without push
* Active research posture and completion basis: `focused`; focused scope and materiality across `test_case_journey.py`, `panels.js`, adjacent `src/api/tests/` `node -e` callers, and base-branch merge diff
* Explicit limits or deadline effect: Read-only during Research; edits and test runs deferred to Implement

#### Wave 1: Wider

* Plan and independent lanes: Inline inspection of GitHub Actions run `43707070068` (`job 132790451775`), byte sizes of `src/api/src/zava_forward/api/web/*.js`, all 22 `subprocess.run` sites in `src/api/tests/test_case_journey.py`, all 57 test files using `"node"` + `"-e"` across `src/api/tests/`, and live `web-design-guidelines` rules (`W1`).
* Worker evidence relationships or inline fallback: Inline (`<6` bounded inspections) -> `Q1`/`C1`-`C2`, `Q3`/`C4`-`C5`, `W1`.
* Reflection: Confirmed `test_quality_errors_and_manual_action_pending_siblings` was the sole failure out of `3,600` tests in `src-api` (`9/10` CI jobs green), measured `ops.js` (`51,171` B) + `panels.js` (`66,477` B) + `DOM + shipped_helpers()` (`8,751` B) + harness = `129,031` B locally, and explained why `refs/pull/1776/merge` with `50bd5acc0` crossed `131,072` B (`MAX_ARG_STRLEN`). Also found `test_safety_panel_ux.py:7` imports `DOM, WEB, shipped_helpers` from `test_case_journey` (`C5`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact inventory of all 22 `subprocess.run(["node", ..., "-e", ...])` calls in `test_case_journey.py` (including `evaluate()` at line 96 and `--unhandled-rejections=strict` at line 1169), verification of `node -` stdin execution, and audit of `panels.js` lines `329–925` vs `50bd5acc0` diff (`lines 43–290`) and slice anchors.
* Plan and independent lanes: Inline check of `node -` and `node --unhandled-rejections=strict -`, `grep` for `stdin`/`__dirname`/`__filename`/`process.argv` across `test_case_journey.py` and `web/*.js`, and hunk-by-hunk inspection of `panels.js` (`C3`, `C6`, `C7`, `C8`).
* Worker evidence relationships or inline fallback: Inline -> `Q2`/`C3`, `Q4`/`C6`-`C8`.
* Reflection: Zero scripts in `test_case_journey.py` or `web/*.js` reference `stdin`, `__dirname`, `__filename`, or `process.argv` (`C3`). Converting all 22 `subprocess.run` calls in `test_case_journey.py` from `-e <script>` on `argv` to `"-"` with `input=<script>` eliminates `MAX_ARG_STRLEN` risk for every combination (`ops.js + panels.js`, `assistants.js + ops.js + app.js`, `panels.js + app.js`, `chat-widget.js + chat.js`, etc.). Furthermore, `50bd5acc0` modified only lines `43–290` of `panels.js` (`actForm` and `residentPanel`), completely disjoint from `#130`'s `nominationPanel` / `_explanationView` / `_routeForm` (`lines 329–784`) (`C6`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: (1) What if only line 1040 in `test_case_journey.py` were changed to `["node", "-"]` while leaving lines 536 (`assistants.js + ops.js + app.js`, ~85 KB), 791 (`panels.js + app.js`), or 1270 (`chat-widget.js + chat.js`, ~60 KB) on `-e`? Future growth in `ops.js`, `panels.js`, `app.js`, or `chat.js` would trigger the exact same `E2BIG` failure on another line in `test_case_journey.py`. Converting all 22 `node -e` calls in `test_case_journey.py` to stdin (`["node", "-"]` / `["node", "--unhandled-rejections=strict", "-"]` with `input=...`) removes the class of bug across the entire module with uniform style. (2) Could any other file in `src/api/tests/` hit `E2BIG` right now? Audited all 57 files (`C4`): other harnesses either pass a short `SCRIPT` (<10 KB) using `fs.readFileSync(process.argv[1] + ...)` inside Node or slice a single 15-line helper (<3 KB), so no out-of-scope test file needs modification. (3) Could trimming `panels.js` break slice anchors in `test_nomination_screen.py` (`function nominationPanel` .. `\nfunction affectedChallengePanel`), `test_case_journey.py:688` (`function affectedChallengePanel`, `  const residentForm = `, `  const formFor = `, `  const staff`), or `test_epic149_form_error_summary_associations.py` (4-line focus window around `input.setAttribute("aria-invalid", "true")`)? Preserving exact function headers, exact copy literals, and the 4-line `aria-invalid` focus window while compacting redundant vertical whitespace/multiline field-descriptor formatting inside `nominationPanel` and `nominationPanel._routeForm` (`lines 329–784`) keeps every anchor, string literal, and `50bd5acc0` merge boundary 100% intact (`C6`, `C7`, `C8`). (4) Notice in this shared VM environment, `pip list` currently has editable `zava-forward-*` pointing to another worktree (`feat-164-chat-revocation-0042`), so running `unittest` from `src/api` without `src` on `PYTHONPATH` fails inside `test_priority_creation_after_a_real_committed_outcome_offers_no_repeat` (`from zava_forward.api import server`); during validation we must run both the exact caller command with `./src` included (`PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`) and check whether `PYTHONPATH=.` vs `PYTHONPATH=src:...` is needed without mutating shared global `pip` state for other worktrees!
* Plan and independent lanes: Inline verification of slice anchors (`C7`, `C8`) and shared-environment `PYTHONPATH` resolution.
* Worker evidence relationships or inline fallback: Inline -> confirms converting all 22 `test_case_journey.py` `node` calls to `stdin` + safe `#130`-scoped formatting conciseness in `panels.js` is complete, surgical, and conflict-free (`C1`–`C8`, `W1`).
* Reflection: All contrarian checks resolved cleanly; no second research cycle is required.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|--------------|--------------------|--------------------------|----------------------------|
| Convert all 22 `subprocess.run(["node", ..., "-e", ...])` calls in `src/api/tests/test_case_journey.py` to pass scripts via `stdin` (`"-"`, `input=...`) while preserving exported `DOM`, `WEB`, `shipped_helpers` | `C1`–`C5` | accepted | Fixes line 1040 `E2BIG` immediately and eliminates `MAX_ARG_STRLEN` exposure across every JS-concatenating test in `test_case_journey.py` | Selected recommendation (Part 1) |
| Trim redundant comments and verbose multiline object/array whitespace inside `#130`-owned `nominationPanel` / `_routeForm` (`lines 329–784` of `panels.js`), preserving all copy, anchors, Epic #149 windows, and `50bd5acc0` disjointness | `C6`–`C8`, `W1` | accepted | Keeps `panels.js` concise without altering runtime behavior, accessibility semantics, or merge cleanliness with `PR #1639` (`50bd5acc0`) | Selected recommendation (Part 2) |
| Modify other `src/api/tests/test_*.py` files outside `test_case_journey.py` | `C4`, `C5` | rejected | Audited all 57 `node -e` test files; other files either read JS via `fs.readFileSync` inside Node or pass `<3 KB` helper slices, and caller scoped the fix to `test_case_journey.py` and `panels.js` | Documented as verified non-exposure |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope and materiality satisfied; exact CI failure, `MAX_ARG_STRLEN` mechanism, `node -` stdin behavior, and `panels.js` static/merge constraints verified from primary sources.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded 2-file CI `E2BIG` root-cause trace and static-invariant audit completed in `<6` direct reads, where subagent delegation would add latency without improving context isolation.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `test_quality_errors_and_manual_action_pending_siblings` concatenates `DOM + shipped_helpers() + ops.js + panels.js + harness` (`129,031` UTF-8 bytes on `f53340e8f`) and invokes `subprocess.run(["node", "-e", script], text=True, capture_output=True)`, raising `OSError: [Errno 7] Argument list too long: 'node'` on CI (`refs/pull/1776/merge`). | `src/api/tests/test_case_journey.py:973` | view / bash (`gh run view 43707070068`) | high | Line `1040` is the exact failing `subprocess.run` call in CI job `132790451775` |
| C2 | `test_case_journey.py` contains 22 `subprocess.run(["node", ..., "-e", ...])` invocations (lines `96, 190, 268, 336, 418, 536, 656, 791, 880, 969, 1040, 1093, 1168, 1270, 1309, 1359, 1495, 1643, 1682, 1729, 1855, 1895`), several concatenating large web bundles (`ops.js` `51,171` B, `panels.js` `66,477` B, `chat.js` `35,428` B, `assistants.js` `21,811` B). | `src/api/tests/test_case_journey.py:96` | grep / bash | high | Line `1169` also passes `--unhandled-rejections=strict` before `-e` |
| C3 | Zero files in `src/api/tests/test_case_journey.py` or `src/api/src/zava_forward/api/web/*.js` reference `stdin`, `__filename`, `__dirname`, or `process.argv`, and both `["node", "-"]` and `["node", "--unhandled-rejections=strict", "-"]` execute CommonJS via `input=script` identically to `-e`. | `src/api/tests/test_case_journey.py:18` | grep / bash | high | Verified directly with Python `subprocess.run` against installed `node` |
| C4 | Across all 57 `src/api/tests/test_*.py` files containing `"node"` and `"-e"`, no file outside `test_case_journey.py` concatenates multi-file web bundles onto `argv`; other harnesses read files from disk via `fs.readFileSync(process.argv[1] + ...)` or slice single tiny helpers (`<3 KB`). | `src/api/tests/test_safety_panel_ux.py:12` | grep / bash | high | `test_workspace_scripts.py:592` already passes `input=source` on stdin |
| C5 | `test_safety_panel_ux.py` imports `DOM, WEB, shipped_helpers` from `test_case_journey`, so those module-level symbols and signatures must remain unchanged. | `src/api/tests/test_safety_panel_ux.py:7` | grep / view | high | Preserves cross-test compatibility |
| C6 | Base branch `origin/feat/demo-233-same-home-tensions-0825` advanced to `50bd5acc0` (`#1786`), adding `+52` net lines in `panels.js` strictly within lines `43–290` (`actForm` and `residentPanel`), which pushed `refs/pull/1776/merge` over `131,072` bytes while remaining completely disjoint from `#130`'s lines `329–925`. | `src/api/src/zava_forward/api/web/panels.js:329` | bash (`git diff`) / view | high | Trimming only inside lines `329–784` avoids any merge conflict with `50bd5acc0` |
| C7 | `test_accessibility_baseline.py` pins `9` `setAttribute("aria-invalid", "true")` sites across `web/*.js`, and `test_epic149_form_error_summary_associations.py` checks `"aria-describedby": status.id`, `id: \`${key}-feedback\``, `tabindex: -1`, `"before recording this challenge."`, and `.focus()` within `±4` lines of `input.setAttribute("aria-invalid", "true")`. | `src/api/tests/test_epic149_form_error_summary_associations.py:54` | view | high | Keep `aria-invalid` and `input.focus()` within 4 lines in `panels.js` |
| C8 | `test_nomination_screen.py` slices `panels.js` using `src.indexOf("function nominationPanel")` to `src.indexOf("\nfunction affectedChallengePanel")`, and `test_case_journey.py:684` slices `const panelOwned = `, `\nconst PANEL_SUPPORT`, `function bindCaseMutationForm`, `function actForm`, `function captureChallengeDrafts`, `function affectedChallengePanel`, `  const residentForm = `, `  const serviceForm`, `  const formFor = `, and `  const staff`. | `src/api/tests/test_nomination_screen.py:13` | view | high | All slice boundary markers in `panels.js` must be preserved verbatim |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Form controls, polite status regions (`aria-live="polite"`), inline error recovery guidance, and programmatic focus states must remain intact across web edits. | Vercel Web Interface Guidelines (`command.md`) | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-15 | main (retrieved 2026-11-15) | high |

### Contradictions / Conflicts

* Shared-environment `pip` editable paths vs caller `PYTHONPATH`: In this shared host environment, `python3 -m pip list` shows editable `zava-forward-api` pointing to `/home/azureuser/source/ama-demo-wt/feat-164-chat-revocation-0042/src/api` (an absent worktree), so running `python3 -m unittest` from `src/api` without `src` on `PYTHONPATH` raises `ModuleNotFoundError: No module named 'zava_forward.api'` in `test_priority_creation_after_a_real_committed_outcome_offers_no_repeat`. Resolved without touching shared host `pip` packages -> run from `src/api` with `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests` (and avoid mutating shared `site-packages` used by other worktrees).

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `test_quality_errors_and_manual_action_pending_siblings` hit Linux `MAX_ARG_STRLEN` (`131,072` B) on GitHub Actions' merge commit (`f53340e8f` + `50bd5acc0`) because `ops.js + panels.js + DOM + shipped_helpers()` was passed as a single `argv` element via `node -e`. | `C1`, `C2`, `C6` | high | Replace `-e <script>` on `argv` with `stdin` (`"-"`, `input=<script>`). |
| Q2 | Converting all 22 `subprocess.run(["node", ..., "-e", ...])` calls in `test_case_journey.py` to `["node", "-"]` (and `["node", "--unhandled-rejections=strict", "-"]` at line 1169) with `input=...` preserves identical execution, stdout/stderr capture, timeouts, and CommonJS `require(...)` behavior. | `C2`, `C3` | high | Apply stdin pattern uniformly across all 22 `node` calls in `test_case_journey.py`. |
| Q3 | No other `src/api/tests/test_*.py` file concatenates multi-file web bundles onto `node -e` `argv`; `test_safety_panel_ux.py` imports `DOM, WEB, shipped_helpers` from `test_case_journey`. | `C4`, `C5` | high | Keep `DOM, WEB, shipped_helpers` untouched; no out-of-scope test edits needed. |
| Q4 | Redundant comments and expanded multiline object/option-array formatting in `#130`-owned `nominationPanel` / `_routeForm` (`lines 329–784` of `panels.js`) can be compacted by ~1.5–2 KB with zero behavioral change, zero slice/Epic #149 regressions, and zero overlap with `50bd5acc0` (`lines 43–290`). | `C6`, `C7`, `C8`, `W1` | high | Perform surgical behavior-preserving formatting conciseness pass in `panels.js` lines `329–784`. |

## Key Discoveries

* Linux enforces `MAX_ARG_STRLEN = PAGE_SIZE * 32 = 131,072` bytes per individual `execve` argument regardless of total `ARG_MAX` (`2 MB`); passing concatenated JS modules on `stdin` via `["node", "-"]` with `input=script` removes that `128 KB` ceiling completely (`C1`, `C2`, `C3`).
* Converting all 22 `node` invocations in `src/api/tests/test_case_journey.py` (including `evaluate()` and `--unhandled-rejections=strict`) future-proofs the entire test module as `app.js`, `ops.js`, `panels.js`, `assistants.js`, and `chat.js` evolve (`C2`, `C3`).
* Restricting `panels.js` conciseness edits to `#130`-owned lines `329–784` guarantees clean automatic merging with `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`, which edits only lines `43–290`) while preserving every test slice anchor and Epic #149 focus window (`C6`, `C7`, `C8`).

### Complete Examples

```python
# In src/api/tests/test_case_journey.py
result = subprocess.run(
    ["node", "-"],
    input=script,
    text=True,
    capture_output=True,
)
```

## Alternatives and Decision State

### Selected Recommendation

* Approach: Update all 22 `subprocess.run(["node", ..., "-e", ...])` invocations in `src/api/tests/test_case_journey.py` to pass JavaScript source via `stdin` (`["node", "-"]` or `["node", "--unhandled-rejections=strict", "-"]` with `input=...`), trim redundant comments and verbose multiline formatting inside `#130`-owned `nominationPanel` and `nominationPanel._routeForm` (`lines 329–784` of `src/api/src/zava_forward/api/web/panels.js`) without changing runtime behavior or touching `50bd5acc0` hunks, validate unit, WCAG baseline, content-standard, Epic #149, Ruff, and Mypy checks, and commit cleanly on `feat/ux-130-api-routes` without pushing.
* Rationale: Permanently eliminates `execve` `MAX_ARG_STRLEN` (`131,072` bytes) failures across `test_case_journey.py`, keeps `panels.js` concise and merge-clean against `PR #1639` (`50bd5acc0`), and preserves all accessibility and content invariants (`C1`–`C8`, `W1`).
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `W1`
* Implementation impact: `src/api/tests/test_case_journey.py`, `src/api/src/zava_forward/api/web/panels.js`, and Cycle 3 `.copilot-tracking/` artifacts.
* Confidence: high

File tree:

```text
src/api/
  src/zava_forward/api/web/
    panels.js                        (modified: trim redundant comment/multiline whitespace in #130 section)
  tests/
    test_case_journey.py             (modified: pass JS scripts via stdin ["node", "-"] with input=...)
.copilot-tracking/
  research/2026-11-15/nomination-api-routes-130-c3-research.md
  plans/2026-11-15/nomination-api-routes-130-c3-plan.md
  details/2026-11-15/nomination-api-routes-130-c3-phase-details.md
  reviews/plans/2026-11-15/nomination-api-routes-130-c3-plan-critique.md
  changes/2026-11-15/nomination-api-routes-130-c3-changes.md
  reviews/logs/2026-11-15/nomination-api-routes-130-c3-review.md
  rpi-sessions/2026-11-15/nomination-api-routes-130-c3-state.json
```

### Alternative: Trim `panels.js` only and keep `["node", "-e", script]` on `argv`

* Approach: Minify whitespace in `panels.js` to drop `script` a few kilobytes below `131,072` bytes while retaining `node -e`.
* Trade-offs: Temporarily ducks beneath `131,072` bytes today, but any subsequent UX/accessibility addition in `ops.js`, `panels.js`, or `app.js` will immediately break CI with `E2BIG` again.
* Evidence refs: `C1`, `C2`, `C6`
* Rejection rationale: Fragile workaround that leaves an arbitrary `128 KB` `argv` time-bomb in `test_case_journey.py` and violates caller requirement 1.

### Alternative: Change only line 1040 in `test_case_journey.py` and leave the other 21 `node -e` calls on `argv`

* Approach: Convert only `test_quality_errors_and_manual_action_pending_siblings` to `["node", "-"]` with `input=script`.
* Trade-offs: Smaller diff in `test_case_journey.py`, but leaves line 536 (`assistants.js + ops.js + app.js`, ~85 KB), line 791 (`panels.js + app.js`), and line 1270 (`chat-widget.js + chat.js`, ~60 KB) exposed to `MAX_ARG_STRLEN` as modules grow.
* Evidence refs: `C2`, `C3`
* Rejection rationale: Converting all 22 `node` calls in `test_case_journey.py` to `stdin` is equally mechanical, 100% consistent across the file, and eliminates `MAX_ARG_STRLEN` across the entire module permanently.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: In this shared environment, avoid running `pip install -e` globally because another worktree shares the user environment; pass `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests` when invoking `unittest` from `src/api` so `zava_forward.api` resolves cleanly to this worktree.
* Follow-up: Pushing `feat/ux-130-api-routes` to `origin` so GitHub Actions re-runs `src-api` on `PR #1776`, running independent exact-head review, and completing human governance items `OD-41`/`OD-42` remain post-session owner actions.
* Residual uncertainty: none within local Focused Tier validation; hosted CI green check awaits owner push.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Reuse active `PR #1776` branch `feat/ux-130-api-routes` and commit locally without pushing or rewriting `c1`/`c2` artifacts | confirmed | Caller prompt + AMA branch rules | Preserves Cycle 1 and Cycle 2 history and tracking evidence cleanly | `C6` | Add a clean Cycle 3 commit on `feat/ux-130-api-routes`; do NOT push |
| Pass JS scripts via `stdin` (`["node", "-"]` / `["node", "--unhandled-rejections=strict", "-"]` with `input=...`) across all 22 `subprocess.run` calls in `src/api/tests/test_case_journey.py` | proposed | Caller prompt + evidence (`C1`–`C5`) | Eliminates `execve` `MAX_ARG_STRLEN` (`131,072` B) failures across the entire module while keeping `DOM, WEB, shipped_helpers` intact | `C1`–`C5` | Surgical 22-site `subprocess.run` update in `test_case_journey.py` |
| Trim redundant comment and multiline formatting whitespace strictly within `#130`-owned lines `329–784` of `src/api/src/zava_forward/api/web/panels.js` | proposed | Caller prompt + evidence (`C6`–`C8`, `W1`) | Keeps `panels.js` concise while preserving all runtime behavior, test slice anchors, Epic #149 windows, and merge cleanliness with `50bd5acc0` | `C6`–`C8`, `W1` | Behavior-preserving conciseness pass in `panels.js` verified against all static/unit/WCAG suites |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Remote push of `feat/ux-130-api-routes` to `PR #1776` and hosted GitHub Actions `src-api` check | Owner push after session completes | Repository owner | Turns hosted `PR #1776` `src-api` check green (`10/10`) | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Interactive axe-core 4.10.3 disclosure scan in `src/api/checks/nomination_browser_check.py` | Automated WCAG scan parity on expanded dual-route nomination forms | Post-CI follow-up selection | deferred | Q4; `C7`, `W1` |

## Planning Readiness

* Status: Ready
* Decision state: Converged on stdin Node script execution (`["node", "-"]`, `input=...`) across `src/api/tests/test_case_journey.py`, `#130`-scoped behavior-preserving conciseness trim in `src/api/src/zava_forward/api/web/panels.js`, and Focused Tier verification (`test_case_journey.py`, `test_accessibility_baseline.py`, coupled nomination/content/Epic #149 suites, `ruff`, and `mypy`).
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `W1`
* Preconditions met: Exact CI `E2BIG` failure log inspected, byte counts and merge-commit growth verified, `node -` stdin compatibility verified, slice anchors and Epic #149 invariants verified, `web-design-guidelines` rules (`W1`) fetched.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                            |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                          |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                            |
| Lane evidence or inline fallback | Inline fallback: bounded 2-file `E2BIG` root-cause trace and static-anchor audit resolved in `<6` direct reads    |
| Research disposition             | executed                                                                                                          |
| Planning Readiness               | Ready (`C1`–`C8`, `W1`)                                                                                           |
| Blockers                         | none                                                                                                              |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic transition to `Plan`                                                     |

## Advisory Next Step

| Field                            | Record                                                                                                 |
|----------------------------------|--------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                               |
| Planning Readiness               | Ready (`C1`–`C8`, `W1`)                                                                                |
| Output mode and planning support | `convergence`; yes — single evidence-backed specification ready for planning                           |
| Acting owner                     | Confirmed automatic RPI Agent                                                                          |
| Required gates or confirmations  | Research waves complete (`passed`); Planning Readiness `Ready` (`passed`); pre-transition state write  |
| Continuation result              | Automatic continuation to `rpi-plan`                                                                   |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md                         |
| Notes for planning or re-entry   | Preserve all slice anchors (`C8`), Epic #149 4-line focus windows (`C7`), and `50bd5acc0` disjointness (`C6`) |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All questions answered with high-confidence primary evidence; further research would be redundant.

## Sources

* W1 - Vercel Web Interface Guidelines (`command.md`) - https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-11-15, main)

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives and Decision State, Open Questions, Current/Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
* Missing or limited sections: none
