---
description: "Primary research artifact for Issue #133 remaining locally verifiable acceptance criteria in src/core"
---
<!-- markdownlint-disable-file -->

# Task Research: 133-aftercare-concern-2142

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                          |
| Researcher / agent | RPI Agent (`rpi-research`)                                                          |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md        |

## Research Brief

* What to research: How `src/core` (`aftercare.py`, `aftercare_intake.py`, `aftercare_store.py`, and `tests/test_*aftercare*.py`) implements and verifies the two target Issue #133 criteria: (1) a household or representative can raise an aftercare concern through an accessible route including a non-digital one, and (2) no causation, blame or savings promise appears in any generated or templated text, plus why bare `unittest discover` in this worktree requires local `src` resolution.
* Why it matters: Issue #133 (`FR-049`, `AC-063`) requires an accessible concern intake for both households and representatives across digital and non-digital channels without jargon, medical gatekeeping, causation claims, household blame, or savings promises, verified locally in `src/core`.
* Audience or intended use: Planning, implementation, and exact-head review in the current automatic RPI loop for branch `feat/quality-133-aftercare-concern-2142`.
* Scope: `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/aftercare_store.py`, `src/core/tests/test_aftercare*.py`, and `src/core/README.md`, with read-only compatibility checks against `src/api/src/zava_forward/api/web/aftercare.js` and `src/api/tests/test_aftercare_screen.py`.
* Non-goals: Editing `src/api`, modifying GitHub issue checkboxes, running `pip install -e` against shared `~/.local` site-packages, pushing to remote, or claiming human assistive-technology / DPO / evaluator sign-off from code alone.
* Criteria: Every codebase claim cites `path:line`; backward compatibility with existing `zf-aftercare-intake/1` persisted documents and `src/api` screen contract is preserved; exact verification command in `src/core` passes cleanly.
* Requested outputs: Convergence recommendation for `rpi-plan` covering `src/core` code, tests, and documentation updates.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q4 covering AC1 route/accessibility gaps, AC5 neutral-text/template gaps, API/snapshot compatibility, and bare `unittest` import |
| Codebase scope                   | `src/core/`, `src/api/` (read-only compatibility), `docs/` (case study, PRD, UX content standard, journey atlas), `.copilot-tracking/` |
| External scope                   | none                                                                                                                                |
| Initial internal candidate areas | `src/core/src/zava_forward/core/aftercare*.py`, `src/core/tests/test_aftercare*.py`, `src/core/README.md`                           |
| Initial external candidate areas | none                                                                                                                                |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | caller-specified bounded `src/core` delivery scope                                                                                  |
| Explicit limits / deadline       | Changes restricted to `src/core`, `src/core/README.md`, and `.copilot-tracking/`; do not push                                       |
| Posture-specific completion basis| focused scope and materiality: all target modules, tests, downstream consumers, and verification behaviors inspected directly       |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Shared non-sandboxed environment; do not mutate shared `~/.local` editable `.pth` files; keep Focused validation tier honest    |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                   | Scoped authority or output contract                            | Selected / skipped reason                                                       |
|---------------------|---------------------------------------|--------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches repository and tracking files  | AMA docs-first read, validation tiering, privacy-safe git user | Selected: mandatory repository governance                                       |
| Skill               | `rpi-research`                        | Explicit RPI loop phase 1                              | Three-wave read-only research artifact with `C#` evidence IDs  | Selected: active RPI phase skill                                                |
| Skill               | `web-design-guidelines` / UX skills   | Web UI design and review                               | Applies only to web edits                                      | Skipped: task scope is backend `src/core` only; `src/api` is read-only context  |
| Research specialist | `hve-core-all:rpi-researcher`         | Independent delegated research lanes                   | Compact subagent lane artifact                                 | Skipped (inline): all 3 target modules and 3 test suites fit direct inspection  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                                  |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive automatic RPI run with explicit branch, worktree, target files (`src/core`), ACs, and verify command.  | N/A (autonomous)     | Proceed in confirmed automatic mode with focused posture; absorb interrupted worktree diff safely |
| Direction change | Pre-existing uncommitted diff in `aftercare.py` and `aftercare_intake.py` inspected and verified as interrupted run.   | N/A (autonomous)     | Retain valid partial additions (`SUPPORT_OPTIONS`, `_variants`, `intake_error_summary`) and extend |
| Convergence      | All four research questions answered from direct code and test execution evidence; no external ambiguity remains.      | N/A (autonomous)     | Advance to `rpi-plan` under convergence recommendation                                           |

## Scope and Success Criteria

* Scope: `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/aftercare_store.py`, `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/core/tests/test_aftercare_store.py`, and `src/core/README.md`.
* Assumptions:
  * Verified: Household free-text (`statement` and `representative_basis`) must remain verbatim in the resident's or representative's own words and must not be filtered through `neutral_text` (`C11`), whereas every system-generated or templated string must pass `neutral_text` (`C4`, `C11`).
  * Verified: Existing staff-assisted routes (`GET /api/aftercare/form`, `POST /api/aftercare/concerns`) must keep rejecting `channel="digital"` and unauthorized staff roles (`C10`, `C12`).
* Success criteria:
  * Every research question is answered with exact `path:line` citations.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C1`-`C16`).
  * Alternatives are compared with trade-offs and a single convergence recommendation is selected.
  * Open questions, governance boundaries, and residual uncertainty are recorded honestly.

## Task Research Requests

* Explicit requests:
  * Deliver in `src/core`: "A household or representative can raise an aftercare concern through an accessible route including a non-digital one" and "No causation, blame or savings promise appears in any generated or templated text".
  * Write all 4 `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`).
  * Pass exact verification in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*aftercare*.py' -v`.
* Inferred research questions:
  * How to support both accessible household/representative self-service digital intake and staff-assisted non-digital intake (plus persisted accessibility support adjustments) in `src/core` without breaking existing `AftercareService` role/channel/snapshot invariants or `aftercare.js`.
  * Which clause-boundary, paraphrase, Unicode/punctuation, or unguarded template/generated-text gaps remain in `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py`.
  * Why bare `python3 -m unittest discover` in `src/core` imports stale code without `PYTHONPATH=src` and how to resolve it cleanly inside `src/core/tests`.
* Caller constraints and non-goals: Do not touch `src/api`, do not push, and leave `git status --short` empty after commit.

## Direction Controls

| Control type | Direction or boundary                                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|--------------|-------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow       | Deliver locally verifiable engineering criteria in `src/core` only                                    | User prompt         | Keep `src/api` untouched while verifying payload compatibility with `aftercare.js` |
| add          | Verify with bare `python3 -m mypy`, `ruff`, and `python3 -m unittest discover` without `PYTHONPATH`   | User prompt         | Investigate `sys.path` shadowing from shared `~/.local` editable `.pth` files      |
| exclude      | Do not push to remote; commit locally with Copilot trailer and clean working tree                     | User prompt         | Stop git actions after local commit verification                                   |

## Research Questions

|  # | Sub-question                                                                                                                               | Type            | Priority | Status   |
|---:|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What gaps prevent `src/core` from fully supporting household and representative concern raising across accessible digital and non-digital routes? | depth           | H        | answered |
| Q2 | Where can causation, blame, or savings promises still appear in generated or templated text across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py`? | depth           | H        | answered |
| Q3 | How do persisted `zf-aftercare-intake/1` snapshots and `src/api/src/zava_forward/api/web/aftercare.js` constrain schema and form changes?  | breadth         | H        | answered |
| Q4 | Why does bare `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` fail in this worktree when `PYTHONPATH=src` is omitted?  | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`
  * `docs/prd-zava-north-homes-retrofit-demonstrator.md` (`FR-049`, `AC-063`)
  * `docs/reference/research/ux/content-standard.md` and `docs/reference/research/ux/customer-journeys/customer-journey-atlas.md` (`O13`, `O14`)
  * `.copilot-tracking/research/2026-11-13/133-aftercare-ac-audit-1416-research.md` and `.copilot-tracking/changes/2026-11-13/133-aftercare-ac-audit-1416-changes.md`
* Reused (verified) findings:
  * PR #1708 (`f6d13c953`) expanded `neutral_text` with `PARAPHRASE_PATTERNS`, `_UNCERTAIN`, `_NEGATED_CLAIM`, `strip_unsafe_sentences`, and `assert_templates_neutral` (`C4`, `C5`).
  * Plain-language standard requires everyday words, no system jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), per-field plain guidance, and non-digital equivalence without requiring medical justification (`C1`, `C15`).
* Superseded / stale:
  * `src/core/README.md:4971` still claims persistence in stores and API/UI wiring are "Not delivered" (`C16`), predating `DocumentStateStore` and `aftercare.js`; documentation for `src/core` aftercare capabilities should accurately state what `src/core` delivers versus external human/governance gates.

## Research Cycle Log

### Cycle 1

* Active direction controls: `src/core`-only implementation scope; bare verification command; no push.
* Active research posture and completion basis: `focused`; complete inspection of all three aftercare modules, their test suites, downstream API screen test contract, and local test runner behavior.
* Explicit limits or deadline effect: Inline execution selected because total target surface is ~1,650 LOC across 3 source files and 3 test files.

#### Wave 1: Wider

* Plan and independent lanes: Map Issue #133 criteria, PRD `FR-049`/`AC-063`, UX content standard, prior #133 audit (`133-aftercare-ac-audit-1416`), current worktree diff, and all `aftercare*` modules and tests.
* Worker evidence relationships or inline fallback: Inline inspection mapped `FR-049`/`AC-063` and UX plain-language rules (`C1`) to `aftercare.py` (`C3`-`C7`), `aftercare_intake.py` (`C8`-`C10`), `aftercare_store.py` (`C13`), and prior audit gaps (`C2`).
* Reflection: Identified that `AftercareRegister` supports `digital` and `staff_recorded` routes (`C6`), whereas `AftercareService` only supports `staff_recorded` (`C8`, `C9`) and discards accessibility support options (`C5`, `C6`). Also observed partial uncommitted edits in `aftercare.py` and `aftercare_intake.py` adding `SUPPORT_OPTIONS`, `SUPPORT_NOTE`, `_variants()`, and `intake_error_summary()`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Q1 (accessible digital + non-digital intake and `support_needed` persistence), Q2 (every template, error string, and dynamic text path across all 3 modules), Q3 (`_validate` snapshot invariants and `aftercare.js` form rendering).
* Plan and independent lanes: Line-by-line audit of `aftercare.py`, `aftercare_intake.py`, `aftercare_store.py`, `aftercare.js`, `test_aftercare*.py`, and `test_aftercare_screen.py`.
* Worker evidence relationships or inline fallback:
  * Q1/Q3: `aftercare.js` renders every entry in `form.fields` with `options` as a labelled `<select id="ac-<name>">` (`C15`), and `AftercareService._validate` currently hardcodes `rec["route"] != "staff_recorded"` and requires `recorded_by` and `channel` (`C8`). Supporting both `staff_recorded` (assisted non-digital) and `digital` (household/representative direct route via `household_form()` and `submit_household_concern()` + `/api/aftercare/household-form` and `/api/aftercare/household-concerns`) while keeping `form()` / `record_concern()` unchanged preserves all existing staff-role and non-digital channel tests (`C10`, `C12`).
  * Q1: Adding optional `support_needed` (validated against `SUPPORT_OPTIONS` codes `large_print`, `interpreter`, `call_back`, `support_person`, accepting omitted/empty, single code, or list of codes) on `intake_form()`, `intake_errors()`, `AftercareRegister.raise_concern()`, and `AftercareService` concerns/receipts preserves requested accessibility adjustments end-to-end without requiring explanation (`C5`, `C6`, `C9`).
  * Q2: Audited every string constant, f-string, and exception message across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py`, finding unguarded error/status templates in `intake_errors`, `evaluator_view` unknowns, `propose_pack` owner interpolation, `review_pack` approval labels, `_assisted_errors`, `_context_errors`, `_free_text`, `_flagged`, `_date`, `_staff`, `owner_label`, `_comparison` unknown reason, and `aftercare_store.py` messages (`C5`-`C9`, `C13`).
* Reflection: Need contrarian adversarial probing of `neutral_text` regexes (`_UNCERTAIN`, `_NEGATED_CLAIM`, `PARAPHRASE_PATTERNS`) and investigation of why bare `unittest discover` failed without `PYTHONPATH=src`.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. Challenge whether `neutral_text` (`aftercare.py:107-140`) can still be bypassed via clause punctuation, newlines, hyphenation, or unguarded paraphrases.
  2. Challenge whether adding `support_needed` or digital receipts breaks existing `zf-aftercare-intake/1` snapshots or SHA-256 request fingerprints.
  3. Challenge why bare `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` failed while `PYTHONPATH=src` passed 123/123 tests (`15` MSSQL skipped).
* Plan and independent lanes: Probe regex behavior on adversarial strings; inspect `~/.local` site-packages `.pth` resolution and `src/core/pyproject.toml`.
* Worker evidence relationships or inline fallback:
  * Adversarial regex finding (`C4`): `_variants()` collapses `\n` into `" "` before `_UNCERTAIN` and `_NEGATED_CLAIM` run, and both regexes only stop at `\s(?:and|but|or)\s|[.;,]|$`. Consequently, `"Unknown whether draughts changed: the tenant is at fault."`, `"Unknown whether draughts changed! Bills will fall."`, `"Unknown whether draughts changed\nBills will drop."`, and `"No promise of savings — the tenant is at fault."` all swallow the second clause and bypass `neutral_text()`!
  * Adversarial paraphrase finding (`C4`): `"because of the tenant/household/occupant/retrofit"`, `"attributable to"` / `"attributed to"`, `"guarantee savings"` / `"promised savings"`, `"save on your bills"` / `"pay less on bills"`, `"blamed"` / `"blaming"`, and hyphenated `"mis-use"` / `"resident-error"` bypass `BANNED_PHRASES` and `PARAPHRASE_PATTERNS`.
  * Snapshot compatibility finding (`C8`): If `_fingerprint` preserves the existing 7-tuple `[raised_by, basis, home, kind, statement, channel, next_update]` whenever `route == "staff_recorded"` and `support_needed` is empty, and `from_state` / `_validate` treat absent `support_needed` as `[]`, all pre-existing snapshots remain 100% valid without migration.
  * Worktree import finding (`C14`): Shared `~/.local/lib/python3.12/site-packages/__editable__.zava_forward_core-0.1.0.pth` points to `/home/azureuser/source/ama/src/core/src` (an older checkout). Because `python3 -m mypy` sets `mypy_path = ["src", "tests"]` (`C14`) and `ruff` sets `src = ["src", "tests"]`, bare `mypy` and `ruff` check the worktree, whereas bare `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` imports stale `/home/azureuser/source/ama/src/core/src` unless the test suite prepends its own sibling `../src` to `sys.path` (and `zava_forward` namespace `__path__` if already loaded).
* Reflection: Every contrarian challenge revealed a concrete defect that would otherwise have broken either AC5 adversarial safety, snapshot compatibility, or the caller's exact bare verification command.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                   | Evidence IDs   | Parent disposition | Evidence-based rationale                                                                                      | Primary-artifact treatment |
|--------------------------------------------------------------------------------------------------------------------|----------------|--------------------|---------------------------------------------------------------------------------------------------------------|----------------------------|
| Persist optional `support_needed` adjustments across `intake_form`, `intake_errors`, `AftercareRegister`, and `AftercareService` | C1, C5, C6, C9 | accepted           | Turns `SUPPORT_OPTIONS` into an actionable, non-gatekept accessibility adjustment on both digital and non-digital routes | Selected recommendation    |
| Add household/representative self-service digital intake (`household_form`, `submit_household_concern`, `/api/aftercare/household-form`, `/api/aftercare/household-concerns` + receipt readback) alongside staff-assisted non-digital `record_concern` | C2, C6, C8, C9, C10 | accepted | Gives households and representatives both an accessible digital route and all four non-digital channels in `AftercareService` without altering `record_concern` staff-only semantics | Selected recommendation |
| Fix `_UNCERTAIN` / `_NEGATED_CLAIM` clause terminators (newlines, `:`, `?`, `!`, dashes, parentheses), expand causal/blame/savings paraphrases & separator folding, and guard all templates/generated strings across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py` | C4, C5, C7, C9, C13 | accepted | Closes real bypasses in generated/AI text and guarantees import-time + runtime neutrality across every template and generated message | Selected recommendation |
| Ensure `test_aftercare*.py` resolves sibling `src/core/src` ahead of shared `~/.local` editable `.pth`             | C14            | accepted           | Allows bare `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` to test this worktree without mutating shared `~/.local` site-packages | Selected recommendation |
| Filter household `statement` or `representative_basis` through `neutral_text`                                      | C11            | rejected           | Households must be free to report e.g. "I was told I would save money" in their own words; AC5 governs generated/templated text | Explicit non-goal / guard  |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All four research questions (Q1-Q4) are answered with verified line-level codebase evidence and baseline test runs; no external dependencies or unresolved ambiguities remain within `src/core`.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: all three `src/core` aftercare modules and their test suites fit direct read-only inspection within focused scope.

### Codebase Evidence

| ID  | Claim / finding                                                                                                                         | Location (`path:line`)                                                    | Tool | Confidence | Notes |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|------|------------|-------|
| C1  | `FR-049` / `AC-063` and UX content standard require accessible digital + non-digital concern routes, plain language without jargon, and zero causation/blame/savings promises | `docs/reference/research/ux/content-standard.md:1-95`                     | view | high       | Also `docs/prd-zava-north-homes-retrofit-demonstrator.md:1424,2159` |
| C2  | Prior #133 audit found `AftercareService` lacked household self-service digital submission and `neutral_text` missed paraphrases         | `.copilot-tracking/changes/2026-11-13/133-aftercare-ac-audit-1416-changes.md:27-125` | view | high | Baseline before PR #1708 and this slice |
| C3  | `ROUTES`, `NON_DIGITAL_CHANNELS`, `RAISED_BY`, `SUPPORT_OPTIONS`, `SUPPORT_NOTE`, `ACCESSIBLE_ROUTE`, `PROTECTION`, `EVALUATOR_NOTICE`  | `src/core/src/zava_forward/core/aftercare.py:19-60`                       | view | high       | Core route, channel, support, and protection constants |
| C4  | `_UNCERTAIN` and `_NEGATED_CLAIM` stop only at `\s(?:and|but|or)\s\|[.;,]\|$`, after `_variants` collapses `\n` to space, allowing `:`, `!`, `?`, `—`, and `\n` second-clause bypasses; `PARAPHRASE_PATTERNS` misses `"because of the tenant/retrofit"`, `"attributable to"`, `"guarantee/promised savings"`, `"save/pay less on bills"`, `"blamed/blaming"` | `src/core/src/zava_forward/core/aftercare.py:75-142` | view | high | Verified contrarian bypasses |
| C5  | `intake_form()` and `intake_errors()` expose `support_options` and `intake_error_summary()` but do not validate/accept `support_needed` or assert neutrality on `title` and `intake_errors` templates | `src/core/src/zava_forward/core/aftercare.py:185-275` | view | high | Partial diff left from interrupted run |
| C6  | `AftercareRegister.raise_concern` and `from_state` support `digital` and `staff_recorded` routes but do not store/validate `support_needed` or check `owner` neutrality | `src/core/src/zava_forward/core/aftercare.py:300-415` | view | high | `owner` later flows into `propose_pack` facts |
| C7  | `evaluator_view`, `propose_pack`, and `review_pack` leave `unknowns` and pack approval status strings outside `assert_templates_neutral` | `src/core/src/zava_forward/core/aftercare.py:504-602`                     | view | high       | `PACK_TASK` registered disabled/unapproved in `ai_registry` |
| C8  | `AftercareService._validate`, `_fingerprint`, and `_receipt_fingerprint` hardcode `rec["route"] != "staff_recorded"` and mandatory `channel`/`recorded_by` | `src/core/src/zava_forward/core/aftercare_intake.py:175-240`              | view | high       | Blocks digital route records in `AftercareService` |
| C9  | `AftercareService` exposes only staff-gated `form()` and `record_concern()`; several error/status templates, `owner_label`, `_flagged`, and `_comparison` unknown reason are not passed through `neutral_text` / `assert_templates_neutral` | `src/core/src/zava_forward/core/aftercare_intake.py:53-122,386-565,805-922` | view | high | Route table at lines 861-922 |
| C10 | `test_aftercare_intake.py` asserts `record_concern` refuses `channel="digital"`, enforces `RECORD_ROLES`/`VIEW_ROLES`, and returns 404/405 for pack routes | `src/core/tests/test_aftercare_intake.py:362-595`                         | view | high       | Must preserve exact `form()` and `record_concern()` behavior |
| C11 | `NeutralTextTests` explicitly skips verbatim household `original`, `statement`, and `representative_basis` fields when scanning payloads | `src/core/tests/test_aftercare_intake.py:525-545`                         | view | high       | Confirms user free-text is data, not generated/templated text |
| C12 | `test_aftercare.py` checks `set(af.intake_errors({})) == {"raised_by", "home_ref", "kind", "statement"}`                                | `src/core/tests/test_aftercare.py:399-409`                                | view | high       | `support_needed` must remain optional (`required: False`) |
| C13 | `aftercare_store.py` defines user-facing `UNCONFIRMED`, conflict, and persistence error messages without `assert_templates_neutral`      | `src/core/src/zava_forward/core/aftercare_store.py:29-34,135-145`         | view | high       | Guard at import time |
| C14 | `pyproject.toml` sets `mypy_path = ["src", "tests"]` and `ruff` `src = ["src", "tests"]`, while `~/.local` editable `.pth` points to `/home/azureuser/source/ama/src/core/src` | `src/core/pyproject.toml:26-41` | view | high | Explains bare `unittest` failure vs `PYTHONPATH=src` 123-test pass |
| C15 | `aftercare.js` renders `form.fields` entries with `options` as native `<select>` controls and checks all static JS literals with `neutral_text` + `JARGON` regex | `src/api/src/zava_forward/api/web/aftercare.js:89-135` | view | high | Also `src/api/tests/test_aftercare_screen.py:130-260` |
| C16 | `src/core/README.md` documents `AftercareRegister`, `AftercareService`, and `DocumentStateStore` along with undelivered external gates  | `src/core/README.md:4935-5048`                                            | view | high       | Update to document accessible household/staff routes, support adjustments, and tightened neutral-text guard |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `src/core/README.md:4971` states store persistence and API/UI wiring are "Not delivered", while lines `5026-5047` document `DocumentStateStore` runtime hook integration (`C16`); resolved by updating the `src/core/README.md` aftercare section to match current delivered `src/core` functionality while keeping human/WCAG, evaluator-role, DPO, and pack-screen gates clearly marked undelivered.

## Findings Mapped to Questions and Evidence

| Question | Finding                                                                                                                                                              | Evidence IDs         | Confidence | Decision or readiness implication |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|------------|-----------------------------------|
| Q1       | `AftercareRegister` supports `digital` and `staff_recorded` routes (`phone`, `in_person`, `paper`, `assisted_visit`) for `household` and `representative`, while `AftercareService` lacked a self-service household/representative digital intake and neither layer persisted `support_needed` accessibility adjustments. | C1, C3, C5, C6, C8, C9 | high | Add optional `support_needed` across both layers plus `household_form()`, `submit_household_concern()`, `household_receipt()`, and `/api/aftercare/household-*` routes on `AftercareService`. |
| Q2       | `_UNCERTAIN` and `_NEGATED_CLAIM` allowed second-clause bypasses after `:`, `!`, `?`, `—`, or `\n`; several causal/blame/savings paraphrases and hyphenated tokens bypassed `neutral_text`; multiple fixed error/unknown/status templates and dynamic strings lacked `assert_templates_neutral` or `neutral_text`. | C4, C5, C7, C9, C13 | high | Harden `_variants`, `_UNCERTAIN`, `_NEGATED_CLAIM`, `PARAPHRASE_PATTERNS`, and `strip_unsafe_sentences`, and enforce `assert_templates_neutral` + `neutral_text` across all 3 aftercare modules. |
| Q3       | Keeping `support_needed` optional (`[]` default when omitted), preserving the 7-field SHA-256 fingerprint for `staff_recorded` concerns without `support_needed`, and keeping `form()`/`record_concern()` contracts intact preserves 100% snapshot and `aftercare.js` compatibility. | C8, C10, C12, C15 | high | Zero breaking changes to persisted state or `src/api` tests. |
| Q4       | Bare `unittest discover` in `src/core` loads stale `/home/azureuser/source/ama/src/core/src` from `~/.local` `.pth`; prepending the local worktree `src` path in a small `tests/aftercare_fixture.py` imported by `test_aftercare*.py` ensures local worktree code is tested without mutating shared user site-packages. | C14 | high | Bare verification command works deterministically in any worktree. |

## Key Discoveries

* Collapsing newlines in `_variants()` before applying `_UNCERTAIN` and `_NEGATED_CLAIM` created a subtle multiline/colon/dash clause-injection hole where an uncertainty prefix (`"Unknown whether X:\nBills will fall."`) masked a subsequent prohibited claim (`C4`).
* `AftercareService._validate()` rejected any concern whose `route` was `"digital"` (`C8`), preventing `AftercareService` from serving a direct household or representative accessible digital submission alongside the staff-recorded non-digital channels (`phone`, `in_person`, `paper`, `assisted_visit`).
* Shared `~/.local` editable `.pth` files point to `/home/azureuser/source/ama/src/core/src`, causing bare `python3 -m unittest discover` in linked git worktrees to test stale installed modules unless the test module resolves its sibling `../src` (`C14`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach:
  1. Complete and harden `neutral_text()`, `strip_unsafe_sentences()`, and `assert_templates_neutral()` in `aftercare.py`: split/terminate `_UNCERTAIN` and `_NEGATED_CLAIM` at newlines and clause punctuation (`[.!?;,:\n\u2013\u2014()]`), fold invisible characters and hyphen separators, cover remaining causal/blame/savings paraphrases (`because of`, `attributable/attributed to`, `guarantee/promised savings`, `save/pay less on bills`, `blamed/blaming`, `wastes/wasted heat/energy`, `fault/error of the household`), and guard every fixed template and dynamically generated string across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py` (excluding verbatim household/representative `statement` and `representative_basis`).
  2. Complete accessible concern routes for households and representatives in `aftercare.py` and `aftercare_intake.py`:
     * Add `SUPPORT_OPTION_CODES` and optional `support_needed` validation/normalization (`normalize_support_needed`) across `intake_form()`, `intake_errors()`, `AftercareRegister.raise_concern()` / `from_state()`, and `AftercareService` (`record_concern`, `submit_household_concern`, receipts, and concern views), plus plain-language `intake_error_summary()` with non-digital staff fallback and zero jargon.
     * Add `AftercareService.household_form()`, `AftercareService.submit_household_concern(values)` (setting `route="digital"`, default `next_update` 7 days ahead in plain language when omitted, idempotent `request_id` replay, durable receipt `RC-AC-nnn`, and `support_needed`), `AftercareService.household_receipt(concern_id, request_id)` (safe receipt/status readback bounded by matching `request_id` without exposing sensor context or other homes), and corresponding HTTP-agnostic routes (`GET /api/aftercare/household-form`, `POST /api/aftercare/household-concerns`, `GET /api/aftercare/household-concerns/<id>?request_id=...`) while keeping staff-assisted `form()` and `record_concern()` 100% intact.
  3. Add `src/core/tests/aftercare_fixture.py` imported by `test_aftercare.py`, `test_aftercare_intake.py`, and `test_aftercare_store.py` to prepend the worktree's `src/core/src` ahead of stale `~/.local` `.pth` paths, add focused unit/contract tests for AC1 and AC5 edge cases, and update `src/core/README.md`.
* Rationale: Directly satisfies both target acceptance criteria in `src/core` with complete adversarial guard coverage, backward-compatible persistence, zero jargon, and deterministic bare verification in linked worktrees.
* Evidence refs: C1, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16
* Implementation impact: `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/aftercare_store.py`, `src/core/tests/aftercare_fixture.py`, `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/core/tests/test_aftercare_store.py`, and `src/core/README.md`.
* Confidence: high

```text
src/core/
├── README.md
├── src/zava_forward/core/
│   ├── aftercare.py
│   ├── aftercare_intake.py
│   └── aftercare_store.py
└── tests/
    ├── aftercare_fixture.py
    ├── test_aftercare.py
    ├── test_aftercare_intake.py
    └── test_aftercare_store.py
```

### Alternative: Overload `AftercareService.record_concern` to accept unauthenticated `channel="digital"`

* Approach: Allow `user=None` and `channel="digital"` inside existing `AftercareService.record_concern()` and `POST /api/aftercare/concerns`.
* Trade-offs: Mixes staff-only audit semantics with household self-service submissions on a single endpoint.
* Evidence refs: C9, C10
* Rejection rationale: Breaks existing contract tests (`test_every_channel_is_accepted_and_digital_is_not` and `test_only_existing_staff_roles_can_record_or_view`, `C10`) and weakens role-gating on the staff-recorded endpoint. Separate `household_form` / `submit_household_concern` methods and `/api/aftercare/household-*` routes preserve explicit staff role boundaries.

### Alternative: Run `pip install --no-deps -e .` in shared `~/.local` site-packages

* Approach: Overwrite `~/.local/lib/python3.12/site-packages/__editable__.zava_forward_core-0.1.0.pth` to point to this worktree.
* Trade-offs: Makes bare `unittest` pass in this worktree temporarily without touching test imports.
* Evidence refs: C14
* Rejection rationale: Unsafe in a shared multi-worktree host environment because mutating user-global `~/.local` `.pth` files silently redirects concurrent worktrees and `ama` main checkouts. Resolving sibling `../src` in `aftercare_fixture.py` is self-contained, repo-local, and CI-safe.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Human assistive-technology/WCAG acceptance (`AC1`), named real owners (`AC2`), evaluator role & DPO lawful-basis sign-off (`AC4`), and a served pack review UI + model release evidence (`AC6`) remain external/cross-package gates and must not be overclaimed in `src/core/README.md` or commit messages.
* Follow-up: Wire `/api/aftercare/household-form` and `/api/aftercare/household-concerns` into `src/api` resident-facing UI once resident authentication and WCAG assistive-technology checks are scheduled.
* Residual uncertainty: Pattern-based `neutral_text` guards in `src/core` deterministically block literal phrases, Unicode/separator evasions, clause-masking bypasses, and broad causal/blame/savings paraphrases, while `ai_registry` keeps live model generation disabled (`aftercare-concern-pack` unapproved) until human/release gates are met.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Deliver separate household/representative digital route alongside staff-assisted non-digital channels + optional `support_needed` in `src/core` | confirmed | evidence / user scope | Proves accessible digital + non-digital intake for households and representatives without breaking existing staff route contracts | C1, C5, C6, C8, C9, C10, C12 | Update `aftercare.py` and `aftercare_intake.py` with backward-compatible state validation |
| Harden `neutral_text` clause boundaries and paraphrases, and guard all templates/generated messages across all 3 aftercare modules | confirmed | evidence / user scope | Closes contrarian multiline/colon/dash bypasses and unguarded error/status/unknown templates while keeping household free-text verbatim | C4, C5, C7, C9, C11, C13 | Update `aftercare.py`, `aftercare_intake.py`, `aftercare_store.py`, and tests |
| Resolve worktree `src` in `tests/aftercare_fixture.py` | confirmed | evidence / constraint | Makes bare `python3 -m unittest discover` test this worktree safely without mutating shared `~/.local` site-packages | C14 | Imported at top of `test_aftercare*.py` |
| Validation classification: Focused tier | confirmed | `.github/copilot-instructions.md` | Scoped `src/core` domain/guard enhancement and documentation update with no infra, SQL schema, workflow, dependency, or deployment change | C14, C16 | Run `mypy`, `ruff check`, `ruff format --check`, `test_*aftercare*.py`, plus `test_dependency_rule.py` and read-only `src/api` `test_aftercare_screen.py` compatibility check |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Evaluator role access & DPO outcome-data position | Named governance and DPO sign-off | Project owner / DPO | Required before closing all of Issue #133 | follow-up (outside `src/core` scope) |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L        | Resident-facing UI wiring and assistive-technology harness for `/api/aftercare/household-*` | Connects the new `src/core` household concern route to a served WCAG-verified resident screen | Follow-up `src/api` slice on #133 | deferred | Q1, Q3; C2, C15 |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected for `src/core` implementation.
* Evidence basis: C1-C16
* Preconditions met: All target files, invariants, contrarian edge cases, downstream `aftercare.js` expectations, and bare verification behavior are verified.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                 |
|----------------------------------|----------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                               |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                              |
| Lane evidence or inline fallback | Inline inspection across `src/core`, `src/api` (read-only), and `docs/`                |
| Research disposition             | executed                                                                               |
| Planning Readiness               | Ready (C1-C16)                                                                         |
| Blockers                         | none                                                                                   |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic transition to `Plan` (`rpi-plan`)             |

## Advisory Next Step

| Field                            | Record                                                                                 |
|----------------------------------|----------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                               |
| Planning Readiness               | Ready (C1-C16)                                                                         |
| Output mode and planning support | convergence; yes, single evidence-backed design selected                               |
| Acting owner                     | confirmed automatic RPI Agent                                                          |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); state persisted (passed) |
| Continuation result              | automatic continuation to `rpi-plan`                                                   |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md           |
| Notes for planning or re-entry   | Preserve backward-compatible `zf-aftercare-intake/1` fingerprints for existing `staff_recorded` records; do not run `neutral_text` on household verbatim `statement` or `representative_basis` |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All target `src/core` modules, tests, and compatibility boundaries are completely mapped; further research would be redundant.

## Sources

* Internal codebase and documentation sources recorded in Evidence Log `C1`-`C16`. No external web sources used.
