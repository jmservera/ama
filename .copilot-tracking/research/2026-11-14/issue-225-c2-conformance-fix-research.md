---
title: "Issue #225 Cycle-2 CI Conformance Fix Research"
description: "Root-cause analysis and cross-suite constraint synthesis for the RoleScreenConformance onclick failure on finance specialist screens (PR #1715)"
author: "GitHub Copilot"
ms.date: "2026-11-14"
---

## Research Brief

* Topic: Cycle-2 CI fix for Issue #225 (PR #1715: Add WCAG 2.2 keyboard jump nav and state labels to finance screens) on branch `feat/ux-225-finance-screens-wcag-1745` targeting `feat/demo-233-same-home-tensions-0825`.
* Purpose: Identify why `RoleScreenConformance.test_interactive_controls_are_native_and_keyboard_operable` failed in `src-ci.yml` (`src-api` job) and select a minimal, WCAG 2.2 AA-compliant fix that satisfies all role-screen conformance, finance screen, procurement, asset-board, and browser accessibility checks.
* Audience or intended use: Cycle-2 `rpi-plan`, `rpi-implement`, and `rpi-review` artifacts and local commit on `feat/ux-225-finance-screens-wcag-1745`.
* Output mode: `convergence`
* Scope:
  * `src/api/src/zava_forward/api/web/role-screens.js` (`screenJumpNav` and specialist screen jump delegation)
  * `src/api/tests/test_role_screens_conformance.py`, `src/api/tests/test_finance_screen_wcag.py`, `src/api/tests/test_finance_grants_screens.py`, `src/api/tests/test_finance_grants_screen_wcag.py`, and Cycle-2 regression coverage (`src/api/tests/test_finance_screens_wcag_225.py`)
  * Preservation of all existing `.copilot-tracking/` artifacts
* Non-goals:
  * Changing visual tokens, layout rules, or backend API routes
  * Weakening `test_role_screens_conformance.py` guardrails or read-only finance screen boundaries
  * Pushing commits or modifying PR state on GitHub
* Criteria:
  * `cd src/api && python3 -m mypy` passes with 0 errors
  * `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` passes
  * `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` passes
  * Full `src/api` finance and role-screen test discovery (`python3 -m unittest discover -s tests`) passes cleanly
* Requested outputs: Dated Cycle-2 research artifact under `.copilot-tracking/research/2026-11-14/` with verified `C#` evidence, evaluated alternatives, convergence recommendation, and planning readiness.
* Initial questions:
  * `Q1`: Why did `test_interactive_controls_are_native_and_keyboard_operable` fail on `feat/ux-225-finance-screens-wcag-1745`, and were there any other failures in CI run `43644186011`?
  * `Q2`: Which existing unit and browser checks constrain the HTML tag, `href`, attributes, and click handling of `screenJumpNav`?
  * `Q3`: How do other read-only specialist screens in `role-screens.js` implement keyboard-operable section jump links without violating `test_role_screens_conformance.py` or breaking hash routing?
  * `Q4`: Why do paths in the caller prompt (`static/role-screens.js`, `tests/test_finance_screens_wcag_225.py`, and `PYTHONPATH` without `:tests`) differ from the Cycle-1 filenames, and how should tests be structured so both CI discovery and direct CLI invocation succeed?
* Selected research posture: `focused`
* Posture provenance: Bounded internal Cycle-2 CI fix with an explicit failing test, line number, branch, and verification commands supplied by the caller.
* Explicit limits or deadline: Single worktree `/home/azureuser/source/ama-demo-wt/feat-225-finance-screens-wcag-1745`; local commit only (do not push).
* Resolved evidence root: `.copilot-tracking/research/2026-11-14/`
* Assumptions to verify:
  * `A1`: The prompt path `src/api/src/zava_forward/api/static/role-screens.js` refers to `src/api/src/zava_forward/api/web/role-screens.js` (verified true; no `static/` directory exists).
  * `A2`: `test_interactive_controls_are_native_and_keyboard_operable` was the sole failure in `src-ci.yml` on PR #1715 (verified true from run `43644186011`: 3,494 tests ran, 1 failure).

## Active Direction Controls

* Additions: None beyond initial Cycle-2 prompt.
* Changes: None.
* Narrowed scope: Focused to `screenJumpNav` conformance and finance jump-navigation regression tests in `src/api`.
* Exclusions: No remote `git push`, no deletion or modification of prior Cycle-1 or Cycle-3 `.copilot-tracking/` files.
* Discarded directions: Replacing jump links with `<button type="button">` (violates read-only finance screen rules) and relaxing `test_role_screens_conformance.py` (unnecessary guardrail weakening).
* Material direction checkpoints: Intake required no `vscode_askQuestions` checkpoint because non-interactive CLI mode applies and all scope, branch, and verification criteria are unambiguous.

## Extension Registry

| Kind | Name or path | Disposition | Provenance | Scoped authority or output contract |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` (custom instruction) | Selected | Repository root instructions (`applyTo: "**"`) | Enforces AMA knowledge-base reading, Fluent 2 / WCAG 2.2 AA / plain-language preservation, focused validation tier rules, and privacy-safe local commit conventions |
| Skill | `rpi-research` | Selected | Active RPI phase skill | Governs read-only three-wave research execution and primary evidence artifact structure |
| Skill | `redesign-existing-projects` | Selected (context read) | `.agents/skills/redesign-existing-projects/SKILL.md` | Confirms surgical usability fixes preserve existing design system and functionality without overhauls |
| Skill | `web-design-guidelines` | Deferred to Implement/Review | `.github/skills/web-design-guidelines/SKILL.md` | Web Development Guidance requires fetching live rules before web edits and before review; recorded for Phases 3 and 4 |
| Specialist | `hve-core-all:rpi-researcher` | Skipped (inline execution) | Host agent registry | Tightly coupled single-file JS/test trace completed in fewer than five direct reads; inline waves avoided subagent overhead without loss of coverage |

## Participation Record

* Checkpoint: Intake and post-cycle direction check
* Question summary: None issued
* Response or status: Non-interactive CLI session; caller instructions provided exact failure, branch, artifact directories, and verification commands
* Research effect: Proceeded directly through all three waves under `focused` posture

## Prior Knowledge and Starting Context

* Existing Cycle-1 research (`.copilot-tracking/research/2026-11-14-finance-screens-wcag-research.md`) and Cycle-3 rebase research (`.copilot-tracking/research/2026-11-14-225-cycle3-rebase-research.md`) established that `finance-invoices` and `finance-funding` are read-only specialist screens that forbid `<button>` elements inside `.screen-evidence`, and noted that finance WCAG tests live in `src/api/tests/test_finance_screen_wcag.py` and `src/api/tests/test_finance_grants_screen_wcag.py`.
* Commit `4d4d9aedc` switched `screenJumpNav` from `<button>` to `<a href="#${id}" ... onclick: ...>` to satisfy the read-only browser check, which inadvertently tripped the static `onclick:` conformance check in `test_role_screens_conformance.py`.
* UX baselines in `docs/reference/research/ux/wcag-conformance-baseline.md`, `design-system.md`, and `content-standard.md` require native keyboard-operable controls, visible two-tone focus indicators, non-colour text state prefixes, plain British English (`Go to ...`, no `gate` jargon), and preservation of `#/screens?...` SPA hash routing.

## Candidate Research Areas

| Area or uncertainty | Classification | Execution mode | Rationale |
| --- | --- | --- | --- |
| CI failure scope and `test_role_screens_conformance.py` contract | Tightly coupled internal check | Inline | Direct inspection of failing test and CI run `43644186011` log |
| Cross-suite specialist screen jump-navigation patterns in `role-screens.js` | Tightly coupled internal trace | Inline | Single file (`role-screens.js`) plus 5 sibling WCAG test modules |
| Test module naming and `PYTHONPATH` CLI invocation behavior | Bounded verification constraint | Inline | Direct reproduction of caller's `python3 -m unittest` command |

## Research Cycles

### Cycle 1

* Posture: `focused`
* Cycle goal: Verify exact CI failure scope, map every static/unit/browser constraint on `screenJumpNav`, and test candidate solutions against counter-evidence.

#### Wave 1: Wider

* Scope investigated: Branch commit log, GitHub Actions run `43644186011` on PR #1715, `src/api` layout (`pyproject.toml`, `web/`, `tests/`, `checks/`), and prior `.copilot-tracking/` artifacts for `#225`.
* Key observations:
  * All 9 non-API jobs on PR #1715 succeeded; `src-api` ran 3,494 unit tests and failed solely on `test_role_screens_conformance.RoleScreenConformance.test_interactive_controls_are_native_and_keyboard_operable` (`C2`).
  * `src/api/src/zava_forward/api/web/role-screens.js` is the canonical asset location (`C1`); no `static/` directory exists (`C9`).
  * Existing `#225` tests live in `test_finance_screen_wcag.py`, `test_finance_grants_screen_wcag.py`, `test_finance_grants_screens.py`, and `checks/finance_screens_browser_check.py` (`C3`–`C5`).
* Reflection: Breadth confirmed that no backend, CSS, or sibling project regressions exist; Wave 2 must inspect exact character-window and DOM-attribute assertions across all specialist screen tests.

#### Wave 2: Deeper

* Prioritized questions: `Q1`, `Q2`, `Q3`.
* Detailed investigation:
  * `test_role_screens_conformance.py:76-78` iterates over `re.finditer(r"onclick:", SCREENS)` and asserts `'h("button"' in window or 'h("a", { href: "#",' in window` on the 120 characters preceding `onclick:` (`C2`).
  * `screenJumpNav` at `role-screens.js:27-36` writes `h("a", { href: \`#${id}\`, class: "btn alt", "data-jump-target": id, onclick: (event) => { ... } }, \`Go to ${text}\`)` (`C1`). Because `href` is dynamic `` `#${id}` `` rather than literal `"#"`, the 120-char window fails line 78.
  * `role-screens.js:246-252` already installs a shared delegated listener: `document.addEventListener("click", (event) => { const link = event.target.closest?.("a[data-jump]"); if (!link) return; event.preventDefault(); document.getElementById(link.getAttribute("data-jump"))?.focus(); });` (`C6`).
  * `assetJumpNav` (`role-screens.js:268`), `residentJumpNav` (`role-screens.js:848`), and `procurementJumpNav` (`role-screens.js:1349`) all use `h("a", { href: \`#${id}\`, "data-jump": id }, \`Go to ${label}\`)` with zero inline `onclick:` handlers (`C7`), and `test_asset_exec_screen_wcag.py:64-67` explicitly pins the delegated listener source lines (`C8`).
  * `test_finance_grants_screens.py:100,242` exempts finance jump links via `"data-jump-target"` (`C5`), while `test_finance_screen_wcag.py:28-32` asserts `tag == "a"`, `href == "#" + attrs["data-jump-target"]`, `Go to ` prefix, and target `tabindex == "-1"` (`C4`).
* Reflection: Adding `"data-jump": id` alongside `"data-jump-target": id` on `screenJumpNav` and removing the inline `onclick:` satisfies every static, VDOM, and browser constraint without modifying the shared delegated listener.

#### Wave 3: Contrarian

* Challenged hypotheses and counter-evidence checked:
  1. *Could removing `target.scrollIntoView({ block: "start" })` break any test, browser check, or WCAG 2.4.11 behavior?*
     * Checked all `scrollIntoView` occurrences across `src/api/` (`C11`). Only `test_data_steward_screen_wcag.py` (which tests `data-operator` `<button>` jumps) and `test_safety_screen_wcag_keyboard.py` (which tests `hazardJump` `href: "#"` anchors) assert `scrollIntoView`. Neither `finance_screens_browser_check.py` nor `specialist_keyboard_browser_check.py` calls or mocks `scrollIntoView`. In browsers, `HTMLElement.focus()` without `{ preventScroll: true }` natively scrolls the focused `tabindex="-1"` container into view while honoring `html { scroll-padding-block-end: ... }` (`test_accessibility_baseline.py:121`), which is why `assetJumpNav`, `residentJumpNav`, and `procurementJumpNav` rely solely on `.focus()`.
  2. *What happens if the caller's exact Step 3 verification command runs verbatim?*
     * Executed `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_finance_screen_wcag.py -v` (`C10`). Two failure modes surfaced:
       1. `tests/test_finance_screens_wcag_225.py` did not yet exist under that module name (whereas sibling suites like `test_regulatory_ux_accessibility.py` and `test_alert_chat_accessibility.py` provide stable module entrypoints).
       2. Because `:tests` is omitted from `PYTHONPATH` in direct `python3 -m unittest tests/...` invocations (unlike `unittest discover -s tests` in `src-ci.yml`), bare `from test_finance_grants_screens import ...` raises `ModuleNotFoundError` unless imported via `tests.test_finance_grants_screens` (with fallback or package-qualified import, matching `test_resident_api.py:8`).
  3. *Could existing tests lack behavioral verification of delegated click handling on finance jump links?*
     * Confirmed: `test_finance_screen_wcag.py` inspected static VDOM attributes only. Without a behavioral test executing the `document` `"click"` listener registered by `role-screens.js`, removing `onclick:` without wiring `"data-jump": id` would pass `test_finance_screen_wcag.py` while silently breaking SPA hash preservation on click.
* Reflection: Contrarian testing uncovered a critical CLI invocation / import trap (`C10`) and a behavioral test gap. Addressing both in `test_finance_screen_wcag.py` and `test_finance_screens_wcag_225.py` makes the fix airtight across CI discovery and direct CLI runs.

#### Cycle 1 Synthesis and Re-entry Evaluation

* All four research questions (`Q1`–`Q4`) are answered with high-confidence primary codebase evidence (`C1`–`C11`).
* Re-entry decision: No second cycle needed; sources are complete and non-conflicting under `focused` posture.

## Questions and Findings

* `Q1` (CI failure scope): `src-ci.yml` (`src-api`) failed solely at `test_role_screens_conformance.py:78` because `screenJumpNav` used inline `onclick:` on `<a href="#${id}">` rather than `h("button"` or `h("a", { href: "#"` (`C1`, `C2`). All other 3,493 tests in `src-api` passed.
* `Q2` (Constraint intersection): Finance jump controls must be `<a>` tags (not `<button>`, `C3`, `C4`), keep `href="#<id>"` and `"data-jump-target": id` (`C4`, `C5`), carry no inline `onclick:` (`C2`), and keep targets as `<div id="<id>" tabindex="-1">` (`C1`, `C4`).
* `Q3` (Existing specialist-screen pattern): `role-screens.js:246-252` already handles `a[data-jump]` clicks via document event delegation (`event.preventDefault()` + `document.getElementById(... )?.focus()`), pinned by `test_asset_exec_screen_wcag.py:64-67` (`C6`–`C8`). Adding `"data-jump": id` to `screenJumpNav` reuses that exact mechanism cleanly.
* `Q4` (Test module & CLI compatibility): Updating `test_finance_screen_wcag.py` to support package-qualified import `tests.test_finance_grants_screens` when `tests/` is not on `sys.path`, and adding `src/api/tests/test_finance_screens_wcag_225.py` with behavioral delegated-click focus tests plus re-exported `FinanceScreenWcagTests`, satisfies both `unittest discover -s tests` and the caller's exact `python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` command (`C9`, `C10`).

## Codebase Evidence

| ID | Location | Tool category | Claim | Confidence | Provenance note |
| --- | --- | --- | --- | --- | --- |
| `C1` | `src/api/src/zava_forward/api/web/role-screens.js:26-36` | Code search | `screenJumpNav` renders `h("a", { href: \`#${id}\`, class: "btn alt", "data-jump-target": id, onclick: ... })` alongside `screenJumpTarget` (`tabindex: "-1"`). | High | Direct file read |
| `C2` | `src/api/tests/test_role_screens_conformance.py:74-78` | Code search | `test_interactive_controls_are_native_and_keyboard_operable` checks 120 chars before every `onclick:` in `role-screens.js` for `'h("button"'` or `'h("a", { href: "#",'`. | High | Direct file read and local/CI reproduction |
| `C3` | `src/api/checks/finance_screens_browser_check.py:150-154` | Code search | Finance browser harness asserts `evidence.locator("button, form, input, select, textarea").count() == 0` inside `Evidence for ZF-1`. | High | Direct file read |
| `C4` | `src/api/tests/test_finance_screen_wcag.py:17-33` | Code search | Asserts finance jump controls have `tag == "a"`, `href == "#" + data-jump-target`, `Go to ` label prefix, and matching `<div id=... tabindex="-1">` target. | High | Direct file read |
| `C5` | `src/api/tests/test_finance_grants_screens.py:100-105,241-246` | Code search | Legacy finance screen tests filter out jump anchors by `"data-jump-target"` and skip `<nav>` tags when checking cross-home links and tab order. | High | Direct file read |
| `C6` | `src/api/src/zava_forward/api/web/role-screens.js:246-252` | Code search | Document-level click listener intercepts `event.target.closest?.("a[data-jump]")`, calls `event.preventDefault()`, and focuses `document.getElementById(link.getAttribute("data-jump"))`. | High | Direct file read |
| `C7` | `src/api/src/zava_forward/api/web/role-screens.js:268,848,1349` | Code search | `assetJumpNav`, `residentJumpNav`, and `procurementJumpNav` all render `<a href="#${id}" data-jump="${id}">Go to ...</a>` without inline `onclick:`. | High | Direct grep and file read |
| `C8` | `src/api/tests/test_asset_exec_screen_wcag.py:64-67` | Code search | Pins `'closest?.("a[data-jump]")'` and `'event.preventDefault();\n    document.getElementById'` in `role-screens.js`. | High | Direct file read |
| `C9` | `src/api/pyproject.toml:30-60` | Code search | Configures `ruff` (`src = ["src", "tests"]`, `line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`) and `mypy` (`strict = true`, `files = ["src", "tests", "checks"]`), and packages `zava_forward.api` web assets from `web/*`. | High | Direct file read |
| `C10` | `src/api/tests/test_finance_screen_wcag.py:6` | Code search | Bare `from test_finance_grants_screens import ...` fails when invoked via `python3 -m unittest tests/...` without `:tests` in `PYTHONPATH`; `src/api/tests/test_regulatory_ux_accessibility.py:1-9` demonstrates stable test-module aliasing. | High | Direct test execution and file read |
| `C11` | `src/api/checks/specialist_keyboard_browser_check.py:42-60` | Code search | Specialist keyboard walk enumerates `finance-funding` (`Funding indicators and their state`) and `finance-invoices` (no-table gap) and checks `#workspace-status`, focus rings, handoff link, and reset link without requiring inline `onclick:`. | High | Direct file read |

## External Evidence

| ID | Source title | URL | Retrieval date | Version or date | Claim | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

## Sources

No external sources used

## Alternatives and Recommendation

| Option | Summary | Benefits | Trade-offs and risks | Evidence | Disposition |
| --- | --- | --- | --- | --- | --- |
| Option 1 (Selected) | Remove inline `onclick:` from `screenJumpNav` and add `"data-jump": id` alongside `"data-jump-target": id`; harden test imports and add `tests/test_finance_screens_wcag_225.py` with behavioral delegated-click assertions | Satisfies `test_role_screens_conformance.py`, preserves `<a href="#<id>">` and read-only zero-`<button>` finance invariants, reuses `role-screens.js:246-252` verbatim, and passes both CI discovery and caller CLI invocation | Adds both `data-jump` and `data-jump-target` attributes on the jump anchor (minimal, clean, explicit) | `C1`–`C11` | Selected |
| Option 2 | Change `screenJumpNav` to render `<button type="button">` | Matches `'h("button"'` in `test_role_screens_conformance.py` | Breaks `finance_screens_browser_check.py:153` (`button` forbidden in read-only finance evidence region) and `test_finance_screen_wcag.py:29` | `C2`, `C3`, `C4` | Rejected |
| Option 3 | Change `screenJumpNav` anchor to `h("a", { href: "#", ... onclick: ... })` | Matches `'h("a", { href: "#",' ` in `test_role_screens_conformance.py` | Loses meaningful `#<section-id>` fragment semantics and breaks `test_finance_screen_wcag.py:30` | `C2`, `C4` | Rejected |
| Option 4 | Broaden regex/window check in `test_role_screens_conformance.py:78` | Leaves `role-screens.js` unchanged | Weakens a cross-screen UX guardrail to accommodate duplicate inline click code that `role-screens.js:246-252` already handles via delegation | `C2`, `C6`, `C7` | Rejected |

## Decisions

### Current Decisions

| Decision | Status | Owner or source | Rationale | Evidence | Implications |
| --- | --- | --- | --- | --- | --- |
| Delegate `screenJumpNav` clicks via `"data-jump": id` instead of inline `onclick:` | `confirmed` | `evidence` | Aligns finance section jump links with `assetJumpNav`, `residentJumpNav`, and `procurementJumpNav` while satisfying `test_role_screens_conformance.py:78` and read-only zero-button rules | `C1`–`C8` | Single surgical edit in `src/api/src/zava_forward/api/web/role-screens.js` |
| Provide package-safe imports in `test_finance_screen_wcag.py` and add Cycle-2 behavioral regression suite in `src/api/tests/test_finance_screens_wcag_225.py` | `confirmed` | `constraint` | Ensures both `python -m unittest discover -s tests` (CI) and the caller's exact `python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` command pass under strict `mypy` and `ruff` | `C9`, `C10` | Covers delegated `click` `preventDefault()`, target `.focus()`, missing-target safety, and absence of inline `onclick` |
| Classify validation under the focused tier | `confirmed` | `constraint` | Touching only `role-screens.js` and `src/api/tests/`; no workflow, gate-tool, Dockerfile, SQL, package, or security control changes | `C9` | Run `mypy`, `ruff check`, `ruff format --check`, targeted + discovery `unittest`, `node --check`, and local browser check if Chromium is installed |

### Unresolved Decisions

* None.

## Risks, Gaps, and Further Research

* Residual uncertainty: Hosted GitHub Actions `src-ci.yml` will re-run only after the owner pushes `feat/ux-225-finance-screens-wcag-1745` (push is explicitly excluded in this session), and human visual/assistive-technology review remains required before closing Issue #225 (`Refs #225` maintained).
* Potential further research:
  * Standardising `"data-jump"` vs `"data-jump-target"` across all specialist screens in a future cleanup issue (`low` priority, deferred out of scope to keep Cycle-2 minimal and non-disruptive).

## Planning Readiness and Continuation

* Research execution status: Completed (1 three-wave cycle: Wider, Deeper, Contrarian, all inline).
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Evidence basis: `C1`–`C11`
* Blockers: None.
* Continuation owner: `confirmed automatic RPI Agent` (advances automatically to `Plan` after persisting pre-transition state).
* Research-only constraint status: Preserved; zero production or test files were modified during Research.
* Speculation and safety check: All claims are grounded in repository files and CI logs; untrusted tool output was treated as inert data and no secrets were recorded.
