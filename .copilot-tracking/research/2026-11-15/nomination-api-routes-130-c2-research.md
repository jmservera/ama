<!-- markdownlint-disable-file -->

# Task Research: nomination-api-routes-130-c2

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (RPI Agent automatic session)                                     |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md |

## Research Brief

* What to research: Root cause and surgical fix for the `src-api` browser-check failure (`case_journey_browser_check.py` `mutation_reconstruction`, `family == "challenge"`, `outcome == "refusal"`) on `PR #1776` (`feat/ux-130-api-routes`), `<select>` vs `<input>`/`<textarea>` event expectations across nomination and case-journey tests, and rebase compatibility onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, `PR #1639`).
* Why it matters: Focusing `#challenge-open-feedback` inside `bindCaseMutationForm.update()` synchronously blurs `#challenge-open-request`, firing a native DOM `change` event that causes `nominationPanel._routeForm`'s `clearInvalid` listener to wipe out `mutation.message` immediately after a 409 refusal resolves. In addition, `PR #1776` must be cleanly rebased onto the updated parent branch `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`).
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this continuous automatic RPI execution.
* Scope: `src/api/src/zava_forward/api/web/panels.js`, `src/api/checks/case_journey_browser_check.py`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_nomination_api_routes.py`, `src/api/tests/test_case_journey.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_resident_api.py`, and Git ancestry between `feat/ux-130-api-routes` and `origin/feat/demo-233-same-home-tensions-0825`.
* Non-goals: Pushing to `origin`, renaming `PR #1776`'s active head branch `feat/ux-130-api-routes`, running `tools/rpi-checks.py`, or deleting/overwriting earlier `.copilot-tracking/` artifacts.
* Criteria: `case_journey_browser_check.py` passes `mutation_reconstruction` end-to-end; `<select>` `change` and `<input>`/`<textarea>` `input` listeners continue clearing stale invalid/feedback states on genuine user edits; rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) preserves all `#130` and `#1639` changes cleanly; focused unit, browser, lint, and type checks pass.
* Requested outputs: Converged Cycle 2 fix and rebase specification ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q4 covering `panels.js` focus/blur `change` ordering, `<select>` vs `<input>`/`<textarea>` test assertions, rebase diff/conflict analysis against `origin/feat/demo-233-same-home-tensions-0825`, and regression test coverage. |
| Codebase scope                       | `src/api/`, `src/core/tests/`, `.copilot-tracking/`                                                                                        |
| External scope                       | Vercel Web Interface Guidelines (`raw.githubusercontent.com/vercel-labs/web-interface-guidelines`) per repository Web Development Guidance |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/web/panels.js`, `src/api/checks/case_journey_browser_check.py`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_nomination_api_routes.py`, `src/api/tests/test_case_journey.py` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                   |
| Research posture                     | focused                                                                                                                                    |
| Posture provenance                   | default (bounded CI browser-check bugfix + parent-branch rebase with named targets and failure trace)                                       |
| Explicit limits / deadline           | Focused validation tier (do NOT run `tools/rpi-checks.py`); single continuous run ending in clean local commit without push                 |
| Posture-specific completion basis    | Focused scope and materiality: blur/change root cause, `<select>` test contract, and rebase ancestry verified from primary code/Git state   |
| Edits allowed during research?       | no, research-only                                                                                                                          |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                               |
| Known constraints / excluded sources | Never read private datasets; preserve existing `.copilot-tracking/` files; preserve WCAG (`aria-invalid` / `table` baselines) and content rules |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                                 | Match and provenance                                             | Scoped authority or output contract                                           | Selected / skipped reason                                                                 |
|---------------------|-----------------------------------------------------------|------------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repo Instructions) | `applyTo: "**"` matches workspace and tracking paths             | Enforces branch reuse for open PRs, focused validation tier, and web checks   | Selected: governs reuse of `PR #1776` head branch `feat/ux-130-api-routes` and web review |
| Skill               | `web-design-guidelines`                                   | Required by Web Development Guidance before editing `panels.js`  | Fetches current Vercel Web Interface Guidelines (`W1`) for `file:line` review | Selected: loaded and fetched (`W1`) before planning/implementing `panels.js` edits        |
| Skill               | `redesign-existing-projects`                              | Existing-app design improvements                                 | Scoped visual/UX redesign guidance                                            | Skipped: task is a DOM event-listener bugfix and Git rebase with zero visual redesign     |
| Research specialist | `hve-core-all:rpi-researcher`                             | Registered general RPI research worker                           | Independent subagent lane artifact                                            | Skipped for inline execution: tightly coupled DOM/Git trace resolved in <5 direct reads   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                              | Answers / unanswered          | Resulting decision or selected further research                                           |
|------------------|------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------------------|
| Intake           | Non-interactive runtime; caller supplied exact root cause, target base `origin/feat/demo-233-same-home-tensions-0825`, and checks  | N/A (non-interactive runtime) | Reconcile branch shorthand against live `PR #1776` metadata and proceed automatically     |
| Direction change | Verified live `PR #1776` branch in worktree is `feat/ux-130-api-routes` (`HEAD` `2786009ee`, targeting `PR #1639` base branch)     | N/A (repository branch rule)  | Rebase active `PR #1776` branch `feat/ux-130-api-routes` onto `6510b6fbc` without rename  |
| Convergence      | All 4 research questions answered with primary code, browser-harness, and Git ancestry evidence                                    | N/A (non-interactive runtime) | Converge on `isSelect`-scoped `"change"` listener + unit regression test + clean rebase   |

## Scope and Success Criteria

* Scope: Rebase `feat/ux-130-api-routes` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), scope `"change"` `clearInvalid` listener registration in `nominationPanel._routeForm` (`src/api/src/zava_forward/api/web/panels.js`) strictly to `<select>` controls (`Boolean(options)`), add a focused unit regression test in `src/api/tests/test_nomination_screen.py` covering blur/`change` after refusal focus vs `<select>` `change`, run focused unit + `case_journey_browser_check.py` + `ruff` + `mypy` validation, and commit locally with `Refs #130` and the Copilot trailer without pushing.
* Assumptions: Verified rather than trusted—caller shorthand `feat/ux-130-nomination-api-routes` was verified against `gh pr view 1776` (`headRefName: "feat/ux-130-api-routes"`), and rebase hunk disjointness in `app.js` was verified directly via `git diff`.
* Success criteria:
  * Every research question is answered with primary `path:line` (`C1`–`C7`) and external (`W1`) evidence.
  * Findings, decisions, and readiness cite Evidence Log IDs.
  * Alternatives are evaluated and one recommendation is selected in `convergence` mode.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`); fix `nominationPanel._routeForm` in `panels.js` so `status.focus()` blurring an edited `<input>`/`<textarea>` does not clear `mutation.message`; verify `test_nomination_screen.py` `<select>` event usage; run focused unit tests, `case_journey_browser_check.py`, `ruff`, and `mypy`; commit locally without pushing.
* Inferred research questions: Reconcile live `PR #1776` branch name, verify `app.js` diff disjointness across `a1d0be5f6..6510b6fbc` vs `a1d0be5f6..HEAD`, check `test_case_journey.py` and `test_epic149_form_error_summary_associations.py` invariants, and verify how original `formFor` bound `input` listeners at `a1d0be5f6`.
* Caller constraints and non-goals: Focused validation tier only (do NOT run `tools/rpi-checks.py`); do NOT push; do NOT overwrite or delete existing `.copilot-tracking/` files.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                                 | Source / checkpoint   | Effect on active brief, evidence, or revalidation                                    |
|----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|-----------------------|--------------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier only; surgical `panels.js` listener fix + regression test + rebase onto `6510b6fbc`           | Caller prompt         | Excludes `tools/rpi-checks.py` and unrelated UI changes                              |
| exclude                                                  | Do NOT push to remote; do NOT overwrite existing `.copilot-tracking/` Cycle 1 artifacts                               | Caller + repo rules   | Uses new `-c2` slug `nomination-api-routes-130-c2` on `feat/ux-130-api-routes`       |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type            | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How does `bindCaseMutationForm.update()` interact with `nominationPanel._routeForm` listeners during `case_journey_browser_check.py` 409 refusal? | depth           | H        | answered |
| Q2 | Do any unit or browser tests rely on `"change"` events on `<input>`/`<textarea>` vs `<select>` in `nominationPanel._routeForm`?                   | depth           | H        | answered |
| Q3 | What commits/files diverged on `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), and will rebasing `feat/ux-130-api-routes` conflict? | straightforward | H        | answered |
| Q4 | Does scoping `"change"` to `<select>` preserve Epic #149 `aria-invalid` static windows and Vercel Web Interface Guidelines (`W1`)?                | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/nomination-api-routes-130-state.json`, `.copilot-tracking/rpi-sessions/2026-11-15/nomination-api-routes-130-ci-fix-state.json`, and `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md`.
* Reused (verified) findings: Active `PR #1776` head branch in this worktree is `feat/ux-130-api-routes` targeting `feat/demo-233-same-home-tensions-0825` (`PR #1639`); Epic #149 `9`-site `aria-invalid` and focus-window guards remain enforced (`C7`).
* Superseded / stale: Cycle 1 (`2786009ee`) verified the Node unit harness in `test_case_journey.py` (which mocks `focus()` as a no-op that never blurs focused inputs or dispatches native DOM `"change"` events), so it missed the real Chromium focus-transfer `blur` -> `"change"` sequence in `case_journey_browser_check.py` (`C1`, `C2`, `C3`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier (`no tools/rpi-checks.py`); preserve existing `.copilot-tracking/` artifacts; commit locally without push
* Active research posture and completion basis: `focused`; focused scope and materiality across `panels.js`, `case_journey_browser_check.py`, nomination/case-journey tests, and Git ancestry
* Explicit limits or deadline effect: Read-only during Research; `git fetch` and `git rebase` deferred to Implement

#### Wave 1: Wider

* Plan and independent lanes: Inline inspection of `PR #1776` metadata, remote/local `feat/demo-233-same-home-tensions-0825` SHA (`6510b6fbc`), `panels.js`, `case_journey_browser_check.py`, `src/api/tests/` event listener/dispatch patterns, and live `web-design-guidelines` rules (`W1`).
* Worker evidence relationships or inline fallback: Inline (`<6` bounded direct reads across tightly coupled files) -> `Q1`/`C1`-`C3`, `Q2`/`C5`, `Q3`/`C6`, `W1`.
* Reflection: Confirmed exact causal chain (`C1`–`C3`), live branch identity (`feat/ux-130-api-routes` on `PR #1776`), and remote base SHA (`6510b6fbc38533a16b9492cacd3ab7e7331c1610`, already matching local `origin/feat/demo-233-same-home-tensions-0825`, with fresh `git fetch` scheduled in Implement per prompt step 1).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Original `formFor` listener behavior at merge-base `a1d0be5f6`, `test_nomination_screen.py` / `test_nomination_api_routes.py` / `test_case_journey.py` `<select>` vs `<input>` expectations, and `app.js` diff overlap between `a1d0be5f6..6510b6fbc` and `a1d0be5f6..2786009ee`.
* Plan and independent lanes: Inline comparison of `git show a1d0be5f6:src/api/src/zava_forward/api/web/panels.js` (`C4`), test scripts (`C5`), and `git diff` hunks on `app.js` (`C6`).
* Worker evidence relationships or inline fallback: Inline -> `Q1`/`C4`, `Q2`/`C5`, `Q3`/`C6`.
* Reflection: At merge-base `a1d0be5f6`, original `formFor` ONLY registered `input.addEventListener("input", ...)` (`C4`). `#130` added `input.addEventListener("change", clearInvalid)` to handle `<select>` controls (`Boolean(options)`), inadvertently causing text `<input>` and `<textarea>` controls to fire `clearInvalid` when blurred by `status.focus()`. Meanwhile, `app.js` changes on `6510b6fbc` (`lines 376, 2530, 2736`) and `HEAD` (`line 1197`) are over 800 lines apart (`C6`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: (1) Could `<input type="date">` (`next_update`) also blur-fire `"change"` if `tagName === "SELECT"` vs `isSelect` (`Boolean(options)`) were wrong? Both agree (`<input type="date">` has `options` falsy and `tagName === "INPUT"`), so `isSelect: Boolean(options)` excludes `<input type="date">`, `<input type="text">`, and `<textarea>` from blur-triggered `"change"` clearing while keeping `"input"` active on all of them. (2) Could removing `"change"` from `<input>`/`<textarea>` break `syncVisibility()` or `form.dataset.unsaved`? No: `form` has `oninput` calling `syncVisibility()` and setting `dataset.unsaved = "true"`, and every conditional `showWhen` predicate in `nominationPanel` depends on `<select>` fields (`channel`, `raised_by`), which retain `"change"`. (3) Could editing `panels.js` trip `test_epic149_form_error_summary_associations.py`? Checked `SITES`, `FOCUSABLE_MESSAGE`, `RECOVERY_COPY`, and `RAW_ERROR` (`C7`)—none are affected.
* Plan and independent lanes: Inline verification of `showWhen` predicates in `panels.js` and `test_epic149_form_error_summary_associations.py` (`C3`, `C7`).
* Worker evidence relationships or inline fallback: Inline -> confirms `isSelect: Boolean(options)` guard on `input.addEventListener("change", clearInvalid)` has zero adverse side effects (`C3`, `C5`, `C7`).
* Reflection: Contrarian checks passed completely; adding a deterministic Node unit test in `test_nomination_screen.py` that simulates pending edit -> 409 refusal -> `status.focus()` blur `"change"` on `<input>` (preserving `mutation.message`) followed by `"input"` (clearing `mutation.message`) and `<select>` `"change"` (updating visibility & clearing stale message) prevents any future regression even without Playwright.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                              | Evidence IDs       | Parent disposition | Evidence-based rationale                                                                                                                     | Primary-artifact treatment       |
|-------------------------------------------------------------------------------------------------------------------------------|--------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| Attach `"change"` `clearInvalid` listener in `nominationPanel._routeForm` ONLY when `isSelect` (`Boolean(options)`) is true   | `C1`–`C5`, `W1`    | accepted           | Restores original `formFor` behavior for `<input>`/`<textarea>` on blur while keeping `<select>` `"change"` support for dual-route forms     | Selected recommendation (Part 1) |
| Rebase `feat/ux-130-api-routes` (`PR #1776`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) without rename | `C6`               | accepted           | Reuses open `PR #1776` head branch per AMA branch workflow; `app.js` hunks are completely disjoint                                           | Selected recommendation (Part 2) |
| Add focused unit regression test in `src/api/tests/test_nomination_screen.py` for blur-`change` refusal preservation          | `C2`, `C3`, `C5`   | accepted           | Guards the exact focus-transfer blur -> `"change"` sequence in fast Node unit tests alongside end-to-end `case_journey_browser_check.py`     | Selected recommendation (Part 3) |
| Suppress `clearInvalid` during `status.focus()` via a temporary re-entrancy flag while keeping `"change"` on text inputs      | `C2`, `C3`         | rejected           | Fragile and unnecessary: a later blur caused by user Tab/click out of the text field after refusal would STILL fire `"change"` and wipe the error message before the user edited anything! Removing `"change"` from non-select controls fixes both programmatic `status.focus()` blur AND manual Tab blur. | Alternative rejected             |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All 4 research questions answered from primary codebase, browser check, and Git evidence; contrarian checks surfaced an important insight (manual Tab blur after refusal would also fail under a `status.focus()`-only guard, confirming `isSelect`-only `"change"` registration is strictly superior).
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded single-component DOM event trace and Git ancestry inspection resolved in `<6` direct reads

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `mutation_reconstruction` (`family == "challenge"`, `outcome == "refusal"`) calls `page.locator("#challenge-open-request").fill("Later evidence")` while the request is pending (leaving `#challenge-open-request` focused and unblurred) and asserts `expect(feedback).to_contain_text("Synthetic mutation result")` after fulfilling HTTP `409`. | `src/api/checks/case_journey_browser_check.py:456` | view | high | Assertion fails at line `514` when `feedback` text is wiped to `""`. |
| C2 | `bindCaseMutationForm`'s `update()` sets `status.textContent = state.message` (`line 30`) and immediately executes `if (state.focus) { status.focus(); state.focus = false; }` (`line 36`), synchronously blurring `#challenge-open-request` and firing its native DOM `"change"` event. | `src/api/src/zava_forward/api/web/panels.js:30` | view | high | `mutation.focus = true` is set in `_routeForm` `catch` (`panels.js:747`) before `finally` sets `mutation.pending = false` and calls `mutation.update()` (`panels.js:749-750`). |
| C3 | `nominationPanel._routeForm` creates `<select>` when `options` is truthy (`line 596`) and `<textarea>`/`<input>` otherwise (`lines 600-610`), then registers both `input.addEventListener("input", clearInvalid)` and `input.addEventListener("change", clearInvalid)` (`lines 662-663`), where `clearInvalid` clears `mutation.message = ""` whenever `!mutation.pending && !session?.historyBarrier` (`lines 659-660`). | `src/api/src/zava_forward/api/web/panels.js:654` | view | high | Blurring `#challenge-open-request` after 409 refusal fires `"change"` while `mutation.pending === false` and `historyBarrier === false`, wiping `mutation.message`. |
| C4 | At merge-base `a1d0be5f6`, original `formFor` in `panels.js` (`lines 449-454`) and `recordedChangeForm` in `app.js` (`line 1542`) registered ONLY `input.addEventListener("input", ...)`. | `src/api/src/zava_forward/api/web/app.js:1542` | bash / view | high | Verified against `git show a1d0be5f6:src/api/src/zava_forward/api/web/panels.js`. |
| C5 | Neither `test_nomination_screen.py` (`lines 185-259`), `test_case_journey.py` (`lines 706-785`), nor `test_nomination_api_routes.py` (`lines 575-665`) dispatches `"change"` on `<input>` or `<textarea>` controls; `<select>` controls use `page.select_option(...)` / `"change"`. | `src/api/tests/test_nomination_screen.py:185` | view / grep | high | Scoping `"change"` to `isSelect` (`Boolean(options)`) preserves all `<select>` interactions and fixes `<input>`/`<textarea>` blur behavior. |
| C6 | `PR #1776` head branch is `feat/ux-130-api-routes` (`2786009ee`) targeting `feat/demo-233-same-home-tensions-0825`; `origin/feat/demo-233-same-home-tensions-0825` is `6510b6fbc` (`#1784`, 1 commit ahead of merge-base `a1d0be5f6`), with disjoint hunks in the only shared file `src/api/src/zava_forward/api/web/app.js` (`lines 376, 2530, 2736` vs `line 1197`). | `src/api/src/zava_forward/api/web/app.js:1197` | bash (`gh pr view`, `git diff`) | high | Rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) is conflict-free. |
| C7 | `test_epic149_form_error_summary_associations.py` enforces `9` `setAttribute("aria-invalid", "true")` sites, `tabindex: -1` on `#...-feedback`, and a `±4`-line `.focus()` window around `input.setAttribute("aria-invalid", "true")`. | `src/api/tests/test_epic149_form_error_summary_associations.py:72` | view | high | Preserved unchanged by editing only `inputs` entry metadata and listener registration in `panels.js:615-665`. |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Async validation and refusal messages must use polite live status regions (`aria-live="polite"`), associate errors with form fields, and preserve visible/announced error recovery text when moving focus. | Vercel Web Interface Guidelines (`command.md`) | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-15 | main (retrieved 2026-11-15) | high |

### Contradictions / Conflicts

* Caller branch shorthand vs live PR head branch: Prompt summary wrote `feat/ux-130-nomination-api-routes`, whereas `git branch --show-current` and `gh pr view 1776` confirm the active `PR #1776` head branch in `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` is `feat/ux-130-api-routes` (`C6`); resolved by primary Git/GitHub PR state and AMA branch-reuse rules -> keep and rebase `feat/ux-130-api-routes`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Focusing `#challenge-open-feedback` on 409 refusal blurs `#challenge-open-request` and fires native DOM `"change"`, triggering `_routeForm`'s `clearInvalid` while `mutation.pending === false` and wiping `mutation.message`. | `C1`, `C2`, `C3` | high | Remove `"change"` listener registration from non-`<select>` controls in `nominationPanel._routeForm`. |
| Q2 | No test dispatches `"change"` on `<input>`/`<textarea>`; `<select>` controls (`Boolean(options)`) use `"change"` (`select_option`) and never fire delayed `"change"` on `blur()`. | `C4`, `C5` | high | Record `isSelect: Boolean(options)` on each `_routeForm` field entry and attach `"change"` only when `isSelect` is true. |
| Q3 | `origin/feat/demo-233-same-home-tensions-0825` advanced 1 commit (`6510b6fbc`, `#1784`) from merge-base `a1d0be5f6` with completely disjoint hunks in `app.js`. | `C6` | high | Fetch and rebase `feat/ux-130-api-routes` cleanly onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`). |
| Q4 | Scoping `"change"` to `isSelect` preserves Epic #149 `aria-invalid` invariants and ensures polite live refusal messages remain intact upon programmatic focus (`W1`). | `C7`, `W1` | high | Ready for `rpi-plan` with focused-tier validation. |

## Key Discoveries

* Blurring an edited `<input>` or `<textarea>`—whether synchronously via `status.focus()` inside `bindCaseMutationForm.update()` or manually when a user presses `Tab` away from the input after reading a 409 refusal—fires a native DOM `"change"` event without any new user edit (`C2`, `C3`).
* Scoping `input.addEventListener("change", clearInvalid)` strictly to `<select>` elements (`isSelect: Boolean(options)`) solves both programmatic focus-transfer blur and manual blur while keeping `"input"` clearing on `<input>`/`<textarea>` and `"change"` clearing/visibility sync on `<select>` (`C3`, `C4`, `C5`).
* Rebasing `feat/ux-130-api-routes` (`2215209cb` and `2786009ee`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) touches disjoint sections of `app.js` and no other overlapping files (`C6`).

### Complete Examples

```javascript
// Inside nominationPanel._routeForm (src/api/src/zava_forward/api/web/panels.js)
return {
  name,
  label,
  labelNode,
  input,
  isSelect: Boolean(options),
  requiredWhen: config.requiredWhen || null,
  showWhen: config.showWhen || null,
};
// ...
for (const { input, isSelect } of inputs) {
  if (typeof input.addEventListener === "function") {
    const clearInvalid = () => {
      input.removeAttribute("aria-invalid");
      syncVisibility();
      if (!mutation.pending && !session?.historyBarrier) mutation.message = "";
      mutation.update();
    };
    input.addEventListener("input", clearInvalid);
    if (isSelect) input.addEventListener("change", clearInvalid);
  }
}
```

## Alternatives and Decision State

### Selected Recommendation

* Approach: Fetch `origin/feat/demo-233-same-home-tensions-0825` and rebase `feat/ux-130-api-routes` onto `6510b6fbc`; update `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js` so `input.addEventListener("change", clearInvalid)` is registered only when `isSelect` (`Boolean(options)`) is true; add a focused Node regression test in `src/api/tests/test_nomination_screen.py` proving that `<input>` blur/`"change"` during `status.focus()` after a 409 refusal preserves `mutation.message` while subsequent `"input"` and `<select>` `"change"` events still clear invalid state and sync conditional visibility; validate with all requested focused checks and commit locally.
* Rationale: Directly eliminates the root cause for both programmatic `status.focus()` blur and manual user blur on `<input>`/`<textarea>`, restores exact parity with original `formFor` (`C4`), retains `<select>` `"change"` handling (`C5`), and cleanly rebases `PR #1776` onto `PR #1639`'s latest tip (`C6`).
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `W1`
* Implementation impact: `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_nomination_screen.py`, Git history rebase onto `6510b6fbc`, and Cycle 2 `.copilot-tracking/` artifacts.
* Confidence: high

File tree:

```text
src/api/
  src/zava_forward/api/web/
    panels.js                        (modified: attach "change" clearInvalid only for <select>)
  tests/
    test_nomination_screen.py        (modified: add regression test for refusal focus-blur vs input/select events)
.copilot-tracking/
  research/2026-11-15/nomination-api-routes-130-c2-research.md
  plans/2026-11-15/nomination-api-routes-130-c2-plan.md
  details/2026-11-15/nomination-api-routes-130-c2-phase-details.md
  reviews/plans/2026-11-15/nomination-api-routes-130-c2-plan-critique.md
  changes/2026-11-15/nomination-api-routes-130-c2-changes.md
  reviews/logs/2026-11-15/nomination-api-routes-130-c2-review.md
  rpi-sessions/2026-11-15/nomination-api-routes-130-c2-state.json
```

### Alternative: Guard `status.focus()` with a temporary `suppressBlurClear` flag

* Approach: Keep `input.addEventListener("change", clearInvalid)` on `<input>` and `<textarea>`, and set a boolean flag around `status.focus()` in `bindCaseMutationForm`.
* Trade-offs: Prevents clearing during the synchronous `status.focus()` call, but if a user stays focused in or re-focuses an edited text field and blurs out via `Tab` without editing after a refusal, `"change"` could still fire unexpectedly, and it modifies shared `bindCaseMutationForm` instead of localizing the fix to `nominationPanel._routeForm`.
* Evidence refs: `C2`, `C3`, `C4`
* Rejection rationale: Strictly inferior to `isSelect`-scoped `"change"` registration, which aligns with native HTML event semantics (`"input"` for text edits, `"change"` for `<select>` choices) and keeps `bindCaseMutationForm` untouched.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Because rebasing `feat/ux-130-api-routes` onto `6510b6fbc` rewrites local commits `2215209cb` and `2786009ee`, the owner will need `--force-with-lease` when later pushing `feat/ux-130-api-routes` to `PR #1776` (out of scope here since pushing is prohibited).
* Follow-up: Extending `src/api/checks/nomination_browser_check.py` with interactive axe-core 4.10.3 disclosure scans and resolving external human governance items `OD-41`/`OD-42` remain separate post-PR follow-ups from Cycle 1.
* Residual uncertainty: none within focused-tier local scope; hosted GitHub Actions verification requires owner-authorized push.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Reuse active `PR #1776` branch `feat/ux-130-api-routes` and rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) | confirmed | Repository branch rule + caller prompt | Matches open `PR #1776` head ref and cleanly incorporates parent `#1784` (`6510b6fbc`) | `C6` | Do not rename branch; do not push |
| Register `"change"` `clearInvalid` listener in `nominationPanel._routeForm` only when `isSelect` (`Boolean(options)`) is true | proposed | Evidence (`C1`–`C5`, `W1`) + caller prompt | Prevents blur-triggered `"change"` on `<input>`/`<textarea>` from clearing 409 refusal feedback while keeping `<select>` change handling | `C1`–`C5`, `W1` | Surgical 3-line update in `panels.js` + regression test in `test_nomination_screen.py` |
| Execute Focused Validation Tier without `tools/rpi-checks.py` | confirmed | Caller prompt + D4/#1294 tier rules | Small bugfix + rebase on stacked topic branch with explicit caller exclusion of `tools/rpi-checks.py` | `C1`, `C5`, `C7` | Run targeted core/api unit suites, `case_journey_browser_check.py`, `ruff`, and `mypy` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Remote `--force-with-lease` push of rebased `feat/ux-130-api-routes` to `PR #1776` and hosted CI check | Owner push authorization | Repository owner | Needed after local RPI loop to turn hosted `PR #1776` checks green | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Interactive axe-core scan of open dual-route nomination forms in `nomination_browser_check.py` | Automated WCAG scan parity on newly expanded `<details>` states | Follow-up selection after `PR #1776` CI is green | deferred | Q4; `C7`, `W1` |

## Planning Readiness

* Status: Ready
* Decision state: Converged on clean rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), `isSelect`-guarded `"change"` listener in `panels.js`, unit regression test in `test_nomination_screen.py`, and focused-tier validation including `case_journey_browser_check.py`.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `W1`
* Preconditions met: Exact root cause verified, rebase target SHA `6510b6fbc` and diff disjointness verified, static/unit/browser test contracts verified, `web-design-guidelines` rules (`W1`) fetched.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                       |
| Lane evidence or inline fallback | Inline fallback: tightly coupled single-file JS event bugfix and Git ancestry resolved in `<6` direct reads  |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C7`, `W1`)                                                                                      |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic transition to `Plan`                                                |

## Advisory Next Step

| Field                            | Record                                                                                                |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                              |
| Planning Readiness               | Ready (`C1`–`C7`, `W1`)                                                                               |
| Output mode and planning support | `convergence`; yes — single evidence-backed fix and rebase specification ready for planning           |
| Acting owner                     | Confirmed automatic RPI Agent                                                                         |
| Required gates or confirmations  | Research waves complete (`passed`); Planning Readiness `Ready` (`passed`); pre-transition state write |
| Continuation result              | Automatic continuation to `rpi-plan`                                                                  |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md                        |
| Notes for planning or re-entry   | Sequence rebase onto `6510b6fbc` as Phase 1 before editing `panels.js` and `test_nomination_screen.py`|

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

