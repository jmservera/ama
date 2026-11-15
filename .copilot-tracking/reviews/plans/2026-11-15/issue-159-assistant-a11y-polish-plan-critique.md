<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #159 Conversational Assistant Accessibility Final Precision Polish (`RV-001` to `RV-002`)

## Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-polish
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Child precision-polish plan resolving `RV-001` and `RV-002` from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md` under Parent task `2026-11-15-issue-159-assistant-a11y-remediation`, with zero edits to production web files (`src/api/src/zava_forward/api/web/*`), untouched historical critique/review records, exact 1-for-1 parity between `docs/reference/research/ux/wcag-conformance-baseline.md` and `src/api/tests/test_assistant_panel_a11y_159.py`, Focused-tier validation, and specific verification of Chromium `Tab`/`Shift+Tab` DOM-order focus boundaries plus Chromium CDP `Accessibility.getFullAXTree` `expanded` and `pressed` representations.
* Research and evidence considered: `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md`, `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md`, `.copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md`, `src/api/tests/test_assistant_panel_a11y_159.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/src/zava_forward/api/web/index.html`, `src/api/src/zava_forward/api/web/chat-widget.js`, `src/api/src/zava_forward/api/web/chat.js`, `src/api/src/zava_forward/api/web/app.js`, `src/core/src/zava_forward/core/chat_panel.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/log.md`.
* Decisions, dependencies, and acceptance criteria considered: Zero production web edits; Focused validation tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `git diff --cached --check`); canonical edited files locked to `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/log.md`; `FR-01`, `FR-02`, `NFR-01`, `AC-01`, and `P01` (`P01-T01`, `P01-T02`).
* Assessment boundary: Evaluates technical accuracy, runtime test passability in Node `vm` and headless Chromium/CDP, 1-for-1 test-to-documentation parity, resource cleanup, and EOF/whitespace validation against supplied repository sources. Does not evaluate deferred Full-tier CI workflow edits or human desktop assistive-technology testing (#151, #155, #619).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `RV-001` / `FR-01` (CDP `expanded` and `pressed`, `relevant`) | Partial | `FR-01` and `P01-T01` look up `#employee-chat-launcher` with `name == "Employee assistant"` instead of its actual `aria-label` `"Chat"`, do not sequence `Dock to right edge` lookup after expanding `<details class="chat-widget-size">`, omit `<summary>` `DisclosureTriangle` `expanded` (`False` to `True`), and use loose substring/tuple checks instead of exact CDP values (`PC-001`). |
| `RV-001` / `FR-01` (post-`403` and post-`401` `MutationObserver` read) | Partial | `LIVE_OBSERVER_INIT_SCRIPT` only calls upward `el.closest(...)` on `addedNodes`, which misses `<p class="err" role="alert">` mounted inside `<form class="card login">` by `app.js` `login(...)` on `401` (`PC-002`). |
| `RV-001` / `FR-01` (no-keyboard-trap exit from `#employee-chat`) | Partial | `#employee-chat` is appended last in `document.body`, so `Tab` on `Send` blurs to `document.body` at document end rather than focusing an `#app` control; bidirectional WCAG 2.1.2 verification also requires `Shift+Tab` from `Close chat` into `#employee-chat-launcher` and `<main id="app">` (`PC-003`). |
| `RV-001` / `FR-01` (`#employee-chat-question` `Enter` skill submit + `Send` `Enter` refusal submit) | Covered | `P01-T01` cleanly separates direct `Enter` submission from `#employee-chat-question` after `ArrowDown` on `#employee-chat-skill` (`article` count `4`, `Skill: {selected_skill}.`) from a second `Send`-focused `Enter` refusal turn (`article` count `6`, `Outcome: refused`). |
| `RV-002` / `FR-02` (`_SyntheticWorkbenchHarness.__init__` cleanup) | Covered | Initializing `self.store = None` and `self.app = None` before `try: ... except BaseException: self.close(); raise` and guarding `close()` prevents temp-dir, worker, simulation, and SQLite leaks on partial initialization failure. |
| `RV-002` / `FR-02` / `AC-01` / `P01-T02` (EOF newline and staged whitespace check) | Partial | `FR-02`, `AC-01`, and `P01-T02` cite unstaged `git diff --check`, which skips untracked new files and does not fail on missing final `\n` (`PC-004`). |
| `NFR-01` (`mypy --strict`, `ruff check`, `ruff format --check`) | Covered | Planned annotations and validation commands preserve strict typing and formatting across `src/api`. |

## Verdict

* Verdict: Revise
* Rationale: Two planned `P01-T01` assertions (`PC-001` launcher AX node name `"Employee assistant"` / pre-disclosure `Dock to right edge` lookup, and `PC-002` post-`401` `MutationObserver` alert capture on a mounted `<form>` subtree) will deterministically fail in Chromium as written, and two precision gaps (`PC-003` Chromium end-of-document `Tab` vs reverse `Shift+Tab` from `Close chat`, and `PC-004` `git diff --cached --check` + explicit single-`\n` EOF check) need direct planner corrections before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Incorrect `#employee-chat-launcher` accessible name, unsequenced closed-`<details>` lookup for `Dock to right edge`, and incomplete CDP `expanded` / `pressed` / `relevant` assertions

* Related IDs: `FR-01`, `AC-01`, `P01`, `P01-T01`, `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` (`What You May Not Know`, `FR-01`), `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` (`P01-T01`), `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md` (`RV-001`), `src/api/src/zava_forward/api/web/index.html:45`, `src/api/src/zava_forward/api/web/chat-widget.js:9-13,32-39,64-90`, and `src/api/tests/test_assistant_panel_a11y_159.py:586-619,704-725,856-875`
* Concern:
  * `#employee-chat-launcher` sets `aria-label="Chat"` (`index.html:45`, `chat-widget.js:11`) with an `aria-hidden="true"` SVG child. In Chromium CDP `Accessibility.getFullAXTree`, its AX node has `role == "button"` and `name == "Chat"` (sibling of `#employee-chat`, outside `_dialog_ax_subtree`), exposing `expanded: False` (`bool`, CDP type `booleanOrUndefined`) when closed, `expanded: True` (`bool`) when open and undocked, and becoming `ignored: True` once docked (`launcher.hidden = true` at `chat-widget.js:90`). `"Employee assistant"` is the accessible name of the `role == "dialog"` `<section id="employee-chat">` (`modal: False`) and its `heading`, never a `button`. Querying a launcher `button` with `name == "Employee assistant"` in `FR-01` and `P01-T01` matches zero AX nodes.
  * `Dock to right edge` (`<button type="button" aria-pressed="false">`) is inside `<details class="chat-widget-size">` (`chat-widget.js:64-67`), which opens closed (`open == False`). Until `Chat size` `<summary>` is activated, `Dock to right edge` is `ignored: True` in Chromium's AXTree and absent from `_dialog_ax_subtree`.
  * In Chromium CDP `Accessibility.getFullAXTree`, `pressed` uses CDP type `'tristate'` with string values `"false"` before toggle and `"true"` after toggle (never Python `bool`), whereas `<summary>` disclosures (`About this chat`, `Chat size`, `Sources (N)`) have `role == "DisclosureTriangle"` (not `<details>`, which has `role == "Details"` without `expanded`) and expose `expanded: False` (`bool`) before activation and `expanded: True` (`bool`) after activation. In addition, `role="log"` exposes `relevant` (`'tokenList'`) as exact `"additions"` (not `"additions text"`). `FR-01` and `P01-T01` mention `<summary>` disclosures in `What You May Not Know` and `RV-001` but omit asserting `DisclosureTriangle` `expanded` (`False` to `True`), use loose `pressed in ("false", False)` / `("true", True)` in `P01-T01`, and check `"additions"` by substring in `P01-T01` rather than exact `== "additions"`.
* Impact: Implementing `P01-T01` as specified will fail `test_browser_launcher_keyboard_resize_dock_and_escape_focus` on launcher AX lookup (and on `Dock to right edge` lookup if run before expanding `Chat size`) and will leave `<summary>` disclosure `expanded` and exact `pressed`/`relevant` values partially aligned with `RV-001` and `wcag-conformance-baseline.md`.
* Smallest useful change: Revise `What You May Not Know`, `FR-01`, `P01-T01`, and `P01-T02` to: (1) query unignored full `ax_nodes` for `(role == "button", name == "Chat")` to assert `expanded is False` when closed and `expanded is True` when open and undocked (plus `modal is False` on `(role == "dialog", name == "Employee assistant")`); (2) assert `DisclosureTriangle` `expanded is False` before and `expanded is True` after activating `About this chat` and `Chat size` `<summary>` inside `_dialog_ax_subtree`; (3) query `Dock to right edge` (`role == "button"`, `name == "Dock to right edge"`) **after** expanding `Chat size` `<summary>`, asserting exact `pressed == "false"` before Space toggle and `pressed == "true"` after Space toggle; and (4) assert `log_props.get("relevant") == "additions"` with matching wording in `wcag-conformance-baseline.md`.
* Action owner: planning parent
* Exact resolving evidence: Updated `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` and `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` specifying `name == "Chat"` for `#employee-chat-launcher`, `DisclosureTriangle` `expanded` (`False` to `True`), post-`Chat size`-expansion `pressed == "false"` to `"true"` on `Dock to right edge`, and exact `relevant == "additions"`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `LIVE_OBSERVER_INIT_SCRIPT` only traverses upward via `el.closest(...)` on `addedNodes`, missing the nested `role="alert"` mounted on `401` session expiry

* Related IDs: `FR-01`, `AC-01`, `P01`, `P01-T01`
* Evidence: `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` (`FR-01`), `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` (`P01-T01`), `src/api/tests/test_assistant_panel_a11y_159.py:482-511,1050-1071`, and `src/api/src/zava_forward/api/web/app.js:131-161`
* Concern: When `/api/chat/threads/*/ask` returns `401`, `app.js` calls `login("Your session has ended. Sign in again.")`, which creates `err = h("p", { class: "err", role: "alert" }, msg || "")` inside `form = h("form", { class: "card login" }, ..., err, ...)` off-DOM and mounts `form` into `<main id="app">` via `show(form)`. In `LIVE_OBSERVER_INIT_SCRIPT` (`test_assistant_panel_a11y_159.py:482-511`), `childList` handling passes `rec.target` (`#app`) and each `added` node (`form`) to `pushLive`, which only evaluates `el.closest('[aria-live], [role="status"], [role="alert"], [role="log"]')`. Because `Element.closest()` walks ancestors only and `err` already has its text before `form` enters `document.body`, `window.__a11yLiveEvents` records the `403` `workspaceStatus.textContent` update (`rec.target` is `p#workspace-status[role="status"]`) but never records the `401` `<p class="err" role="alert">` descendant inside `form`.
* Impact: `P01-T01`'s post-`401` `window.__a11yLiveEvents` assertion for `"Your session has ended. Sign in again."` on `role == "alert"` will fail in Chromium unless `LIVE_OBSERVER_INIT_SCRIPT` also inspects live-region descendants of `addedNodes`.
* Smallest useful change: Add one line to `P01-T01` instructing `LIVE_OBSERVER_INIT_SCRIPT`'s `childList` handler to also push matching descendants of each element `added` node (`for (const desc of added.querySelectorAll('[aria-live], [role="status"], [role="alert"], [role="log"]')) pushLive(desc, "addedSubtree");`).
* Action owner: planning parent
* Exact resolving evidence: Updated `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` (`P01-T01`) specifying descendant live-region scanning on `addedNodes` in `LIVE_OBSERVER_INIT_SCRIPT`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `Tab` on `Send` reaches the end of `document.body` (`BODY` blur) rather than directly entering `#app`; WCAG 2.1.2 no-trap proof also requires `Shift+Tab` from `Close chat`

* Related IDs: `FR-01`, `AC-01`, `P01`, `P01-T01`, `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` (`What You May Not Know`, `FR-01`), `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` (`P01-T01`, `P01-T02`), `src/api/src/zava_forward/api/web/index.html:12-46`, and `src/api/src/zava_forward/api/web/chat-widget.js:32-58`
* Concern: `ChatWidget.create` executes `document.body.append(launcher, root)` (`chat-widget.js:58`), placing `#employee-chat-launcher` and `#employee-chat` (`root`) at the end of `document.body` after `<main id="app">` (`index.html:44-45`). Inside `#employee-chat`, `<h2 id="employee-chat-title" tabindex="-1">` is skipped in sequential `Tab` order, making `Close chat` the first Tab-focusable control and `Send` the last Tab-focusable control in both `#employee-chat` and the document (`Attach` and `Voice` are `disabled`). In Chromium:
  * Pressing `Tab` once on `Send` hits the end-of-document boundary and blurs `document.activeElement` to `document.body` (`!panel.contains(document.activeElement)` is `True` and focus is not wrapped back to `Close chat`; pressing `Tab` a second time wraps to `a.skip-link` at the top of `document.body`, rather than stepping directly from `Send` into `#app`).
  * Pressing `Shift+Tab` from `Close chat` traverses backward out of `#employee-chat` directly into preceding page controls while `#employee-chat` stays open: when undocked, the first `Shift+Tab` lands on `#employee-chat-launcher` and the second `Shift+Tab` lands inside `<main id="app">`; when docked (`launcher.hidden == True`), the first `Shift+Tab` from `Close chat` lands directly inside `<main id="app">`.
  Testing only `Tab` on `Send` leaves the reverse dialog boundary (`Close chat` + `Shift+Tab`) unverified and makes the Plan's statement ("pressing `Tab` from `Send` moves focus out of `#employee-chat` into the underlying page") imprecise for 1-for-1 parity with `wcag-conformance-baseline.md`.
* Impact: Incomplete bidirectional focus-boundary coverage for WCAG 2.1.2 (No Keyboard Trap) and risk of introducing a new claim-vs-behavior discrepancy in `wcag-conformance-baseline.md`.
* Smallest useful change: Update `What You May Not Know`, `FR-01`, `P01-T01`, and `P01-T02` to assert both stay-open boundaries while `#employee-chat` remains visible: (1) forward `Tab` from `Send` exits `#employee-chat` without wrapping to `Close chat` (`!panel.contains(document.activeElement)` at document end `BODY`, with a subsequent `Tab` wrapping to `.skip-link`), and (2) reverse `Shift+Tab` from `Close chat` exits `#employee-chat` backward to `#employee-chat-launcher` (when undocked) and into `<main id="app">` (`#app.contains(document.activeElement)`), aligning `wcag-conformance-baseline.md` prose with both checks.
* Action owner: planning parent
* Exact resolving evidence: Updated `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` and `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` specifying both forward `Tab` past `Send` and reverse `Shift+Tab` from `Close chat` non-trapping exit assertions and matching baseline prose.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: `FR-02`, `AC-01`, and `P01-T02` specify unstaged `git diff --check` instead of `git diff --cached --check` and explicit single-`\n` EOF verification

* Related IDs: `FR-02`, `AC-01`, `P01`, `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` (`Executive Summary`, `FR-02`, `AC-01`), `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` (`P01-T02`), `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md` (`RV-002`, `Validation Evidence`), and `docs/reference/log.md`
* Concern: Although `Executive Summary` cites `git diff --cached --check` with single EOF newlines (matching `RV-002`), `FR-02`, `AC-01`, and `P01-T02` specify `git diff --check`. Unstaged `git diff --check` ignores untracked files (`src/api/tests/test_assistant_panel_a11y_159.py` and `.copilot-tracking/**`) and already returned exit code `0` in the parent review despite `docs/reference/log.md` missing its trailing `\n`. (Inspection confirms `docs/reference/log.md` is currently the only modified or untracked file lacking a trailing `\n`, and all existing historical critique/review files already end with a single `\n` and zero trailing whitespace.)
* Impact: Running only unstaged `git diff --check` in `P01-T02` will not validate staged new files or fail if a deliverable loses its single trailing `\n`.
* Smallest useful change: Update `FR-02`, `AC-01`, and `P01-T02` to run `git --no-pager diff --cached --check` on the staged index and an explicit single-newline EOF check (`endswith(b"\n") and not endswith(b"\n\n")`) across all modified and newly staged files, while keeping historical critique/review files untouched.
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-02`, `AC-01`, and `P01-T02` in `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` and `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` requiring `git --no-pager diff --cached --check` plus single-`\n` EOF verification.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strengths:
  * Keeps all production web assets (`src/api/src/zava_forward/api/web/*`) untouched, preserving every pinned baseline count in `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, and `src/api/tests/test_home_chat_regulatory_keyboard_provenance.py`.
  * Cleanly splits keyboard skill-selection `Enter` submission from `#employee-chat-question` (`article` count `4`) and `Send`-button `Enter` refusal submission (`article` count `6`), resolving the `PC-002` variance noted in `RV-001`.
  * Properly scopes `_SyntheticWorkbenchHarness.__init__` `try/except BaseException:` cleanup so partial initialization cannot leak temp directories, background workers, simulation handles, or SQLite connections (`RV-002`).
* Residual risk (explicitly accepted outside automated scope):
  * Optional Full-tier `.github/workflows/src-ci.yml` post-Chromium test execution step remains a separate Full-tier workflow change.
  * Named human desktop screen-reader (NVDA/Firefox, VoiceOver/Safari) and 320 px / 400% zoom acceptance remain open human-owned items under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Questions or Blocking Evidence Gaps

* None. All four findings are resolved by direct evidence in the supplied repository files and require no user input.

## Limitations

* Headless Linux host has Playwright Chromium installed for CDP Accessibility Tree and DOM live-region verification, with no desktop screen reader or audio output device; this critique evaluates engineering verification parity, not human assistive-technology sign-off.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md` and `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md` to incorporate `PC-001` through `PC-004`, finalize the plan without another critique pass, and proceed to `rpi-implement`.
* User response required: no
