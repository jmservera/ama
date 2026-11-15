---
title: "Task Research: 228-procurement-wcag-c1-rebase"
description: "Primary evidence artifact for Issue #228 Cycle 1 parent rebase onto feat/demo-233-same-home-tensions-0825 (fe6398197)"
ms.date: 2026-11-15
---

| Field              | Value                                                                                      |
|--------------------|--------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                 |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                                    |
| Status             | Complete                                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md           |

## Research Brief

* What to research: Exact commit divergence, overlapping file hunks, shared helper signatures (`statusBadge` / `statusText` / `screenJumpNav` / `scope="row"` / route aliases), counted baseline assertions, and content-standard guardrails between `feat/ux-228-procurement-wcag` (`0486e2ca1`) and updated parent `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, containing merged PRs `#1759` (`#134`), `#1762` (`#230`), `#1763` (`#232`), `#1757` (`#135`), and `#1764` (`#229`)).
* Why it matters: PR `#1765` (`#228`) must rebase cleanly onto `fe6398197` while preserving every upstream merged change (`#134`, `#230`, `#232`, `#135`, `#229`) and every `#228` procurement/supplier/contractor WCAG 2.2 accessibility improvement, reconciled accessibility baseline counts, and zero forbidden content-standard terms.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases of the automatic RPI session for `228-procurement-wcag-c1-rebase`.
* Scope: Git commit range `5536c3907..fe6398197` vs `5536c3907..0486e2ca1`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and the sibling role/feature unit test suites (`#228`, `#229`, `#230`, `#232`, `#135`, `#134`).
* Non-goals: Pushing to remote, altering unrelated backend/infra behavior, changing human accessibility acceptance claims (`#151` / `#155`), or modifying historical `.copilot-tracking/` records.
* Criteria: Identify every conflicting or semantically interacting hunk across code, docs, and tests; determine exact combined counts if `test_accessibility_baseline.py` or `wcag-conformance-baseline.md` assert exact totals; confirm Python/virtualenv test runner setup without `uv`.
* Requested outputs: Evidence-backed rebase conflict analysis, exact reconciliation map, and planning readiness verdict.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                   |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | What commits and hunks diverge between `0486e2ca1` and `fe6398197`, where do `#228` and `#134/#230/#232/#135/#229` conflict or interact semantically, do accessibility baseline counts shift, and what focused validation commands verify all six issues together? |
| Codebase scope                   | `src/api/`, `docs/reference/research/ux/wcag-conformance-baseline.md`, git refs `0486e2ca1` and `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`                             |
| External scope                   | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                                                |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `docs/reference/research/ux/wcag-conformance-baseline.md` |
| Initial external candidate areas | Vercel Web Interface Guidelines (`command.md`)                                                                                                                          |
| Research posture                 | focused                                                                                                                                                                 |
| Posture provenance               | caller-specified bounded rebase scope with explicit commit pins and Focused Tier validation                                                                             |
| Explicit limits / deadline       | Focused Tier validation (`ruff`, `mypy`, targeted `unittest` suites with `pip` only, no `uv`); commit locally with trailer; do NOT push                                 |
| Posture-specific completion basis| focused scope and materiality: every diverging file, conflict hunk, shared JS helper, baseline counter, and sibling test suite inspected across all three waves         |
| Edits allowed during research?   | no, research-only                                                                                                                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                                    |
| Known constraints / excluded sources | Preserve Fluent 2, WCAG 2.2 baseline, plain-language content standard (never `'human-approved'`), and exact local freeze without remote push                           |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                                   | Scoped authority or output contract                                                             | Selected / skipped reason                                                                                 |
|---------------------|---------------------------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches all repository and tracking files              | Enforces Fluent 2, WCAG 2.2 baseline, plain-language content standard, Focused Tier validation  | Selected: governs web guidance, validation tier, noreply git config, and non-overclaim evidence rules      |
| Skill               | `rpi-research`                        | Explicit RPI loop phase 1                                              | Governs three-wave cycle, `C#`/`W#` evidence log, synthesis, and readiness gates                | Selected: primary research phase contract                                                                 |
| Skill               | `web-design-guidelines`               | Required by repository Web Development Guidance before web edits       | Fetches live Vercel Web Interface Guidelines (`command.md`) for web code implementation/review  | Selected: fetched `W1` to guide web conflict resolution and review                                        |
| Skill               | `accessibility`                       | Matches WCAG 2.2 jump links, row headers (`scope="row"`), state cues   | Canonical WCAG 2.2 and ARIA APG accessibility contract                                          | Selected: guides `scope="row"`, landmark/heading focus, and non-colour state cue verification             |
| Skill               | `redesign-existing-projects`          | Existing-app visual overhaul skill                                     | Visual redesign patterns                                                                        | Skipped: task is a deterministic parent-branch rebase and accessibility reconciliation, not a visual redesign |
| Research specialist | `hve-core-all:rpi-researcher`         | General delegated research lane worker                                 | Bounded independent lane artifact                                                               | Skipped (inline fallback): tightly coupled git merge-tree and single-worktree file comparison (<10 files) |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                             | Answers / unanswered | Resulting decision or selected further research                                                                 |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------|-----------------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive confirmed automatic RPI run with explicit worktree, branch, parent SHA (`fe6398197`), objectives, and validation tier | Not needed           | Execute focused Cycle 1 inline across git topology, merge conflicts, row-header parity, and baseline assertions |
| Direction change | Wave 3 Contrarian found `#228` tables in `0486e2ca1` used `screenTable` (`rowHeader=false`) while upstream `#232` added `screenRecordTable` (`scope="row"`) and Objective 2 explicitly requires `#228` row headers (`scope="row"`) | Not needed (explicitly covered by Objective 2) | Adopt `screenRecordTable` across all 6 `#228` procurement/contractor tables in `role-screens.js` during rebase  |
| Convergence      | All 5 research questions answered with `high` confidence in Cycle 1                                                               | Not needed           | Mark Planning Readiness `Ready` and hand off to `rpi-plan` in automatic mode                                    |

## Scope and Success Criteria

* Scope: Rebase `feat/ux-228-procurement-wcag` (`0486e2ca1`) onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`) preserving upstream `#134`, `#230`, `#232`, `#135`, `#229` and `#228` procurement/supplier/contractor WCAG 2.2 jump links, `scope="row"` row headers, and textual state cues (`procurementBadge` / `stateCue`), with passing Focused Tier checks and no push.
* Assumptions:
  * Verified: `origin/feat/demo-233-same-home-tensions-0825` resolves to `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` (`C1`).
  * Verified: Untracked `.copilot-tracking/*228-procurement-wcag-c1-rebase*` paths do not collide with any tracked path in `5536c3907..fe6398197` (`C1`, `C2`).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Fetch `origin/feat/demo-233-same-home-tensions-0825` and inspect rebase of `feat/ux-228-procurement-wcag` (`0486e2ca1`) onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`.
  2. Identify all merge conflicts and semantic interactions across `role-screens.js`, `app.js`, `ops.js`, `test_accessibility_baseline.py`, and `wcag-conformance-baseline.md`, preserving `#134`, `#230`, `#232`, `#135`, `#229`, and `#228` jump links, `scope="row"` row headers, and textual state cues.
  3. Determine whether counted accessibility baseline assertions shift after rebasing onto `fe6398197`.
  4. Confirm `test_content_standard.py` constraints (never `'human-approved'`, no banned internal jargon, `Owner:` before `Next action:` in `OWNED_FILES`) and Focused Tier test runner configuration (`pip` only, no `uv`).
* Inferred research questions:
  * Do upstream `src/core` changes in `#134` (`profile_journey_contract.py`) or `#135` (`exception_feeds.py`, `exception_queue.py`, `exception_register.py`) require editable package installation or `PYTHONPATH` ordering when running `src/api` tests?
  * Do any top-level JS declarations collide across `app.js`, `ops.js`, and `role-screens.js` once `fe6398197` and `0486e2ca1` are combined?
* Caller constraints and non-goals: Focused Tier validation only; use `/usr/bin/python3` or `/tmp` virtualenv with `pip` only (no `uv`); commit locally with Copilot trailer; do NOT push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                                 |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------------------------|
| narrow                                                   | Target exact parent `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`) | User intake         | Scopes git divergence analysis to `5536c3907..fe6398197` vs `5536c3907..0486e2ca1`                |
| exclude                                                  | Do not use `uv`; do not push to `origin`; never introduce forbidden phrase `'human-approved'`           | User intake         | Constrains Python environment setup, content copy, and post-implementation git state              |
| add                                                      | Preserve `#228` jump links, row headers (`scope="row"`), and textual state cues alongside `#134/#230/#232/#135/#229` | User intake / Wave 3 | Requires upgrading the 6 `#228` tables in `role-screens.js` from `screenTable` to `screenRecordTable` |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What exact commits and files diverge between merge-base `5536c3907`, parent `fe6398197`, and branch HEAD `0486e2ca1`, and what conflicts arise?    | straightforward                          | H        | answered |
| Q2 | How do `#228` helpers in `app.js`, `ops.js`, and `role-screens.js` interact semantically with `#134`, `#230`, `#232`, `#135`, and `#229`?          | depth                                    | H        | answered |
| Q3 | Do `#228` procurement and contractor tables emit `<th scope="row">` row headers via `screenRecordTable`, and do DOM badge cells stay compatible?  | depth                                    | H        | answered |
| Q4 | Do counted baseline assertions in `test_accessibility_baseline.py` or `wcag-conformance-baseline.md` shift when `0486e2ca1` rebases onto `fe6398197`? | straightforward                          | H        | answered |
| Q5 | What `test_content_standard.py` invariants and Python test-runner settings (`pip` only, no `uv`) govern Focused Tier validation across all 6 issues? | breadth                                  | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/changes/2026-11-15/procurement-contractor-wcag-228-changes.md` (`0486e2ca1`), `fe6398197:.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, and `docs/reference/research/ux/wcag-conformance-baseline.md`.
* Reused (verified) findings: Commit `0486e2ca1` implemented `#228` jump navigation, `#/role/procurement` and `#/role/contractor` hash routing, and non-colour `procurementBadge` cues across `role-screens.js`, `app.js`, `ops.js`, and `test_procurement_contractor_screen_wcag.py` (`C2`).
* Superseded / stale: Branch `feat/ux-228-procurement-wcag` was rooted at `5536c3907` (`#227`), predating 5 parent merges (`bcaec70f9` `#134`, `efe14ef3d` `#230`, `321a22960` `#232`, `7989f1394` `#135`, `fe6398197` `#229`) including `#232`'s shared `screenRecordTable` (`scope="row"`) helper and `#135`'s updated WCAG baseline counters (`sites == 9`, `tables == 14`) (`C1`, `C5`, `C9`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `fe6398197`; exclude `uv`, remote push, and `'human-approved'`; preserve all upstream `#134/#230/#232/#135/#229` and `#228` WCAG 2.2 capabilities.
* Active research posture and completion basis: `focused`; focused scope and materiality across all diverging commits, conflict hunks, shared helpers, baseline counters, and sibling test suites.
* Explicit limits or deadline effect: Focused Tier validation only (`ruff`, `mypy`, targeted `unittest` suites via `pip`/python3 without `uv`); frozen local commit without push.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth sweep over git commit topology (`5536c3907..fe6398197` vs `5536c3907..0486e2ca1`), read-only 3-way merge simulation (`git merge-tree --write-tree`), changed file inventory, sibling test module names, and live Vercel Web Interface Guidelines (`W1`).
* Worker evidence relationships or inline fallback: Inline fallback (single-worktree git object inspection across 11 `#228` files and 5 upstream merge commits); mapped `Q1 -> C1, C2, C3, C4` and web review rules `-> W1`.
* Reflection: `git merge-tree --write-tree fe6398197 0486e2ca1` proved that ONLY two text conflict hunks occur across the entire repository (`app.js` `isRoleScreensDestination` and `role-screens.js` `ROLE_HASH_SCREENS`), while `ops.js`, `test_accessibility_baseline.py`, `wcag-conformance-baseline.md`, and `docs/reference/log.md` have zero git text conflicts. Prioritized deeper inspection of auto-merged hunks in `app.js` and `role-screens.js` plus baseline counters for Wave 2.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Auto-merged hunks in `app.js` (`route()`, delegated `a[data-jump]` click handler, contractor views) and `role-screens.js` (`screenNodeValue`, `screenFields`, `screenTable`, `screenRecordTable`, `screenWithheld`, `screenTension`, `procurement-packages`, `contractor-job-pack`), plus `test_accessibility_baseline.py` and `test_content_standard.py`.
* Plan and independent lanes: Inline line-by-line diff inspection of `5536c3907..fe6398197` and `5536c3907..0486e2ca1` across `app.js`, `ops.js`, `role-screens.js`, `test_accessibility_baseline.py`, `wcag-conformance-baseline.md`, and `test_content_standard.py`.
* Worker evidence relationships or inline fallback: Inline investigation mapped `Q2 -> C3, C4, C5, C6`, `Q4 -> C9, C10`, and `Q5 -> C11, C12`.
* Reflection: Found three critical details: (1) `screenWithheld(items, anchor = null)` and `screenTension(kind, anchor = null)` were upgraded identically on both sides and auto-merge cleanly; (2) `app.js` `route()` has both `#228`'s `const hashBase = hash.split("?")[0];` and `#135`'s `const baseHash = hash.split("?")[0];` four lines apart, which should be unified on `baseHash` (`C3`); (3) `#228` added zero `aria-invalid` sites, zero `h("table", {},` literals, and zero `position:fixed` rules, so `fe6398197`'s baseline counts (`sites == 9`, `tables == 14`, `fixed == 2`) remain exact (`C9`, `C10`). Prioritized contrarian testing of `scope="row"`, `#134` same-home contract assertions, and JS top-level identifier disjointness for Wave 3.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge the assumption that clean git auto-merge of `procurement-packages` and `contractor-job-pack` satisfies Objective 2 (`row headers (scope="row")`), challenge whether `#228` badge prefixes break `#134`'s `test_same_home_profile_journey_acceptance.py` or `test_procurement_screens.py`, and challenge whether upstream top-level JS symbols break `test_top_level_identifiers_disjoint_and_no_sys_modules_deletion`.
* Plan and independent lanes: Inline inspection of `role-screens.js` lines 51-76 and 1488-1585, `fe6398197:src/api/tests/test_same_home_profile_journey_acceptance.py`, `fe6398197:src/core/src/zava_forward/core/profile_journey_contract.py`, `test_procurement_screens.py`, `fe6398197:.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`, and Python AST/regex disjointness check across combined `app.js`, `ops.js`, and `role-screens.js`.
* Worker evidence relationships or inline fallback: Inline contrarian checks disproved passive auto-merge sufficiency on table row headers (`Q3 -> C5, C7, C8`): in `0486e2ca1` (authored before `#232` landed), all 6 `#228` tables in `role-screens.js` called `screenTable(...)` (`rowHeader = false`, emitting `<td>` in column 0), whereas `#232` introduced `screenRecordTable` (`rowHeader = true`, emitting `<th scope="row">`) and `#229`'s Cycle 1 rebase (`fe6398197`) upgraded its tables to `screenRecordTable`. Verified `screenRecordTable` delegates `cell = undefined` to `screenTable`'s default `(value) => screenNodeValue(value)`, so DOM badge nodes (`procurementBadge(...)`) work seamlessly while column 0 becomes `<th scope="row">`, and `test_procurement_screens.py` `cells()` already handles `node.get("tag") in ("td", "th")` (`C8`). Also verified `#134` checks substring `"Needs notice"` in `cview["evidenceText"]` (satisfied by `"Visit notice required: Needs notice"`, `C11`) and top-level JS declarations across `app.js`, `ops.js`, and `role-screens.js` have empty pairwise intersections (`C6`).
* Reflection: Contrarian wave caught a substantive WCAG 2.2 gap that git conflict markers alone would have missed: upgrading all 6 `#228` tables in `role-screens.js` from `screenTable` to `screenRecordTable` directly fulfills Objective 2's `row headers (scope="row")` requirement and matches `#232` and `#229` on the parent branch. No unresolved gaps remain.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                           | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale                                                                                                               | Primary-artifact treatment                                 |
|----------------------------------------------------------------------------------------------------------------------------|---------------------------------|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| Resolve `app.js` `isRoleScreensDestination` and `role-screens.js` `ROLE_HASH_SCREENS` by unioning all 6 `#/role/*` aliases  | `C3`, `C4`                      | accepted                                            | Preserves `#227` (`building_safety_lead`, `repairs`), `#232` (`housing_officer`, `resident_engagement`), and `#228` (`procurement`, `contractor`) | Core rebase resolution decision                            |
| Unify duplicate `hashBase` / `baseHash` in `app.js` `route()` onto `baseHash`                                              | `C3`                            | accepted                                            | Eliminates redundant `hash.split("?")[0]` introduced independently by `#135` and `#228`; no test greps literally for `hashBase`        | Included in `app.js` rebase cleanup                        |
| Upgrade all 6 `#228` tables in `role-screens.js` (`procurement-packages` x4, `contractor-job-pack` x2) to `screenRecordTable` | `C5`, `C7`, `C8`, `W1`          | accepted                                            | Emits `<th scope="row">` on first-column record identifiers per Objective 2 and `#232`/`#229` convention while keeping `screenNodeValue` badges | Core `#228` post-rebase semantic alignment + unit test pin |
| Keep `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` counts at `sites == 9`, `tables == 14`, `fixed == 2` | `C9`, `C10`                     | accepted                                            | `#228` adds 0 `aria-invalid` sites, 0 `h("table", {},` literals (`screenRecordTable` reuses existing `screenTable`), and 0 `position:fixed` rules | Verified post-rebase; no artificial count bump             |
| Run Focused Tier tests with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src` or `/tmp` `pip` venv  | `C11`, `C12`                    | accepted                                            | Ensures updated `src/core` modules from `#134`/`#135` (`profile_journey_contract`, `exception_*`) and `dataset.py` resolve locally without `uv` | Recorded for `rpi-implement` validation                    |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: focused scope saturated; every diverging commit, file, conflict hunk, semantic interaction, baseline counter, content guardrail, and test suite is verified with line-level evidence.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: bounded single-worktree rebase analysis across 2 conflict hunks and 6 sibling test suites did not warrant subagent context fan-out.

### Codebase Evidence

| ID  | Claim / finding                                                                                                                                                 | Location (`path:line`)                                                   | Tool | Confidence | Notes                                                                                     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|------|------------|-------------------------------------------------------------------------------------------|
| C1  | Merge-base of `0486e2ca1` and `fe6398197` is `5536c3907`; parent has 5 commits (`bcaec70f9` `#134`, `efe14ef3d` `#230`, `321a22960` `#232`, `7989f1394` `#135`, `fe6398197` `#229`) | `.git/refs/remotes/origin/feat/demo-233-same-home-tensions-0825:1`       | bash | high       | Verified via `git fetch`, `git merge-base`, and `git log --oneline`                       |
| C2  | Commit `0486e2ca1` touches only `.copilot-tracking/*procurement-contractor-wcag-228*`, `app.js`, `ops.js`, `role-screens.js`, and `test_procurement_contractor_screen_wcag.py` | `src/api/tests/test_procurement_contractor_screen_wcag.py:1`             | bash | high       | Verified via `git show --stat 0486e2ca1`; did not touch `docs/reference/log.md`           |
| C3  | Conflict #1 in `app.js` is `isRoleScreensDestination(destination)` (`housing_officer`/`resident_engagement` vs `procurement`/`contractor`), plus adjacent `hashBase`/`baseHash` in `route()` | `src/api/src/zava_forward/api/web/app.js:370`                            | view | high       | Verified via `git merge-tree --write-tree fe6398197 0486e2ca1`; `route()` at lines 433-455 |
| C4  | Conflict #2 in `role-screens.js` is `ROLE_HASH_SCREENS` (`#/role/housing_officer` & `#/role/resident_engagement` vs `#/role/procurement` & `#/role/contractor`) | `src/api/src/zava_forward/api/web/role-screens.js:94`                    | view | high       | Verified via `git merge-tree --write-tree`; union has 6 `#/role/*` entries                |
| C5  | `screenTable` uses default `cell = (value) => screenNodeValue(value)` and `rowHeader = false`; `#232` added `screenRecordTable` passing `cell = undefined, rowHeader = true` (`<th scope="row">`) | `src/api/src/zava_forward/api/web/role-screens.js:51`                    | view | high       | Lines 51-76; `screenNodeValue` preserves DOM badge nodes in `screenFields`, `screenTable`, and `screenRecordTable` |
| C6  | Top-level JS declarations across merged `app.js`, `ops.js`, and `role-screens.js` (`fe6398197` U `0486e2ca1`) are pairwise disjoint (`set()`)                   | `src/api/tests/test_procurement_contractor_screen_wcag.py:900`           | bash | high       | Verified with `TOP_LEVEL_DECL` regex over union of symbols from both refs                 |
| C7  | All 6 tables in `procurement-packages` (4 tables) and `contractor-job-pack` (2 tables) currently call `screenTable(...)` without `rowHeader = true`             | `src/api/src/zava_forward/api/web/role-screens.js:1491`                  | view | high       | Lines 1491, 1505, 1509, 1514, 1545, 1554; column 0 in each table names the record/item    |
| C8  | `test_procurement_screens.py` helper `cells()` already extracts text from both `td` and `th` (`if node.get("tag") in ("td", "th")`)                             | `src/api/tests/test_procurement_screens.py:95`                           | view | high       | Switching `#228` tables to `screenRecordTable` (`<th scope="row">`) preserves all existing row-text tests |
| C9  | On `fe6398197`, `test_accessibility_baseline.py` pins `sites == 9` (`aria-invalid`), `tables == 14` (`h("table", {},`), and `len(fixed) == 2` (`position:fixed`) | `src/api/tests/test_accessibility_baseline.py:96`                        | bash | high       | Lines 96, 141, 162 on `fe6398197`; `#228` adds 0 to any of the three static inventories    |
| C10 | On `fe6398197`, `wcag-conformance-baseline.md` (`ms.date: 2026-11-15`) already records all 9 `aria-invalid` sites and all 14 script-built tables (`#135`)        | `docs/reference/research/ux/wcag-conformance-baseline.md:54`             | bash | high       | Lines 54 and 57 on `fe6398197`; remains accurate when `#228` rebases onto `fe6398197`     |
| C11 | `#134`'s `test_same_home_profile_journey_acceptance.py` renders `procurement-packages` and `contractor-job-pack` in Node and asserts `"Needs notice"` substring and redaction | `src/api/tests/test_same_home_profile_journey_acceptance.py:616`         | bash | high       | Lines 616-660 on `fe6398197`; `"Visit notice required: Needs notice"` satisfies `assertIn("Needs notice", ...)` |
| C12 | `test_content_standard.py` audits `AUDITED_FILES` (forbidding internal jargon and `'human-approved'`) and `OWNED_FILES` including `ops.js` (`Owner:` before `Next action:`) | `src/api/tests/test_content_standard.py:18`                              | view | high       | Verified `#228` strings in `app.js`, `ops.js`, and `role-screens.js` introduce zero banned terms |

### External Evidence

| ID | Claim / finding                                                                                                                               | Source (title)                         | URL                                                                                | Retrieved  | Version/date | Confidence |
|----|-----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|------------------------------------------------------------------------------------|------------|--------------|------------|
| W1 | Native semantic links (`<a href="...">`) must be used for navigation, headings/landmarks require accessible names, focus rings must stay visible | Vercel Labs - Web Interface Guidelines | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-15 | main         | high       |

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding                                                                                                                                                                                                 | Evidence IDs         | Confidence | Decision or readiness implication                                                                                 |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|------------|-------------------------------------------------------------------------------------------------------------------|
| Q1       | Only 2 git conflict hunks occur when rebasing `0486e2ca1` onto `fe6398197`: `isRoleScreensDestination` in `app.js` and `ROLE_HASH_SCREENS` in `role-screens.js`.                                        | `C1`, `C2`, `C3`, `C4` | high     | Rebase conflict resolution is deterministic: union all 6 `#/role/*` destinations/screens.                         |
| Q2       | `screenWithheld` and `screenTension` anchor parameters auto-merge identically; `app.js` `route()` has duplicate `hashBase`/`baseHash` (`hash.split("?")[0]`) to unify onto `baseHash`; top-level JS symbols stay disjoint. | `C3`, `C5`, `C6`     | high       | Unify `baseHash` in `app.js` `route()` during rebase cleanup and preserve delegated `a[data-jump]` deduplication. |
| Q3       | Upgrading all 6 `#228` tables in `role-screens.js` (`procurement-packages` x4, `contractor-job-pack` x2) from `screenTable` to `#232`'s `screenRecordTable` emits `<th scope="row">` while preserving DOM badge cells via `screenNodeValue`. | `C5`, `C7`, `C8`, `W1` | high     | Plan an explicit post-rebase refinement in `role-screens.js` + row-header assertions in `test_procurement_contractor_screen_wcag.py`. |
| Q4       | `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` counts on `fe6398197` (`sites == 9`, `tables == 14`, `fixed == 2`) remain unchanged after rebasing `0486e2ca1`.                     | `C9`, `C10`          | high       | Preserve `fe6398197`'s `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` unchanged and verify by running the test. |
| Q5       | `test_content_standard.py` passes so long as no banned jargon or `'human-approved'` copy is added; sibling suites (`#228`, `#229`, `#230`, `#232`, `#135`, `#134`) require updated `src/core` on `PYTHONPATH` or editable `pip` install in `/tmp` venv without `uv`. | `C11`, `C12`         | high       | Install/configure `/tmp` venv with `pip install --no-build-isolation --no-deps -e` (or explicit local `src/*` `PYTHONPATH`) and run all targeted suites + `ruff` + `mypy`. |

## Key Discoveries

* Only two conflict hunks exist between `0486e2ca1` and `fe6398197`, both caused by parallel additions to `#/role/*` hash routing (`housing_officer` + `resident_engagement` from `#232` vs `procurement` + `contractor` from `#228`) (`C3`, `C4`).
* Upstream `#232` introduced `screenRecordTable` (`rowHeader = true` -> `<th scope="row">`) and `#229` (`fe6398197`) adopted it across its specialist tables; switching `#228`'s 6 tables in `role-screens.js` to `screenRecordTable` seamlessly combines `#232`'s `scope="row"` row headers with `#228`'s `screenNodeValue` DOM status badges (`C5`, `C7`, `C8`).
* Upstream `#135` (`7989f1394`) already incremented `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` to `9` `aria-invalid` sites and `14` `h("table", {},` tables; `#228` adds zero new instances of either, so no baseline counter edits are required after rebase (`C9`, `C10`).
* Sibling test module for `#232` is named `tests.test_housing_resident_screen_wcag` (singular `screen`), `#230` is `tests.test_programme_screen_wcag`, `#229` is `tests.test_data_steward_screen_wcag`, `#135` is `tests.test_exception_queue_ui` + `tests.test_epic149_form_error_summary_associations` + `tests.test_list_export_inventory`, and `#134` is `tests.test_same_home_profile_journey_acceptance` (`C1`, `C11`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Rebase `feat/ux-228-procurement-wcag` (`0486e2ca1`) onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`), union the 6 `#/role/*` entries in `app.js` (`isRoleScreensDestination`) and `role-screens.js` (`ROLE_HASH_SCREENS`), unify `hashBase`/`baseHash` in `app.js` `route()`, upgrade all 6 `#228` tables in `role-screens.js` (`procurement-packages` and `contractor-job-pack`) from `screenTable` to `screenRecordTable` (`<th scope="row">`), extend `test_procurement_contractor_screen_wcag.py` to assert `scope="row"` row headers and all 6 `#/role/*` route aliases, validate with Focused Tier checks (`ruff`, `mypy`, `node --check`, and targeted `unittest` suites across `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, and `test_content_standard`), and create a clean local commit with the Copilot trailer without pushing.
* Rationale: Preserves 100% of upstream `#134/#230/#232/#135/#229` functionality and 100% of `#228` accessibility work while closing the `scope="row"` row-header parity gap surfaced in Wave 3 Contrarian.
* Evidence refs: `C1`, `C3`, `C4`, `C5`, `C7`, `C8`, `C9`, `C11`, `C12`, `W1`
* Implementation impact: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_procurement_contractor_screen_wcag.py`, plus dated `2026-11-15` `.copilot-tracking/` artifacts (`ops.js` carries forward cleanly via rebase).
* Confidence: `high`: every conflict hunk and test contract has been inspected directly against `fe6398197`.

File tree:

```text
src/api/src/zava_forward/api/web/
  app.js                                            (rebase conflict resolution + baseHash cleanup)
  ops.js                                            (carried forward cleanly from #228 commit)
  role-screens.js                                   (rebase conflict resolution + screenRecordTable scope="row" on 6 #228 tables)
src/api/tests/
  test_procurement_contractor_screen_wcag.py        (extended with scope="row" and 6-alias coexistence assertions)
.copilot-tracking/
  research/2026-11-15/228-procurement-wcag-c1-rebase-research.md
  plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md
  details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md
  reviews/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan-critique.md
  changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md
  reviews/logs/2026-11-15/228-procurement-wcag-c1-rebase-review.md
  rpi-sessions/2026-11-15/228-procurement-wcag-c1-rebase-state.json
```

### Alternative: Resolve Text Conflicts Only Without Upgrading `#228` Tables to `screenRecordTable`

* Approach: Resolve only the two git conflict markers in `app.js` and `role-screens.js` and leave `#228`'s 6 tables calling `screenTable(...)` (`<td>` in column 0).
* Trade-offs: Minimizes diff lines beyond `0486e2ca1`, but leaves `#228` tables without `<th scope="row">` row headers even though `#232` landed `screenRecordTable` on the parent branch and Objective 2 explicitly calls for preserving `#228` row headers (`scope="row"`).
* Evidence refs: `C5`, `C7`, `C8`
* Rejection rationale: Fails Objective 2 parity (`scope="row"`) and creates an avoidable inconsistency with `#232` and `#229` on `feat/demo-233-same-home-tensions-0825`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: `none`
* Important: Ensure `src/core`, `src/agents`, and `src/api` resolve from the rebased working tree (via `/tmp` `pip` venv editable install or explicit local `PYTHONPATH`) so new modules from `#134` (`profile_journey_contract.py`) and `#135` (`exception_feeds.py`, `exception_queue.py`, `exception_register.py`) are imported rather than stale pre-rebase distributions.
* Follow-up: Live browser Playwright checks and human assistive-technology / participant walkthrough validation (`#151`, `#155`) remain tracked follow-ups outside Focused Tier unit validation.
* Residual uncertainty: `none` within Focused Tier scope.

## Current Decisions

| Decision                                                                                         | Status    | Owner / source      | Rationale                                                                                                       | Evidence IDs         | Implications                                                                                       |
|--------------------------------------------------------------------------------------------------|-----------|---------------------|-----------------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------------|
| Rebase `feat/ux-228-procurement-wcag` onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` without pushing | confirmed | user                | Aligns PR `#1765` with merged `#134`, `#230`, `#232`, `#135`, and `#229` on parent `#1639`                      | `C1`, `C2`           | Leaves clean local HEAD for coordinator review and `--force-with-lease` push                       |
| Union all 6 `#/role/*` destinations in `app.js` and `role-screens.js` and unify `baseHash`        | proposed  | evidence            | Resolves both git conflicts cleanly while removing duplicate `hash.split("?")[0]` in `route()`                  | `C3`, `C4`           | Preserves `#227`, `#232`, `#135`, and `#228` routing                                               |
| Upgrade all 6 `#228` tables in `role-screens.js` from `screenTable` to `screenRecordTable`       | proposed  | evidence / constraint | Delivers `<th scope="row">` record headers required by Objective 2 while keeping `screenNodeValue` DOM badges   | `C5`, `C7`, `C8`, `W1` | Add explicit `scope="row"` and 6-route coexistence assertions in `test_procurement_contractor_screen_wcag.py` |
| Keep `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` counters at `9 / 14 / 2` | confirmed | evidence            | `#228` adds zero `aria-invalid` sites, zero `h("table", {},` literals, and zero `position:fixed` CSS rules      | `C9`, `C10`          | Upstream `#135` files carry through rebase untouched and pass `test_accessibility_baseline.py`     |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| `none`   | `none`                             | `n/a` | `none` | `none`         |

## Potential Next Research

| Priority | Research item                                                                 | Expected value                                                       | Trigger                                                     | Selected? | Related questions / evidence |
|----------|-------------------------------------------------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------|-----------|------------------------------|
| L        | Chromium Playwright + axe runtime check across rebased `#/role/*` surfaces    | Browser-rendered focus and axe evidence beyond Node VM unit tests    | Scheduled browser-tier or pre-release UX gate (`#151`)      | deferred  | `Q2`, `Q3`; `C3`, `C4`, `W1` |

## Planning Readiness

* Status: `Ready`
* Decision state: Convergence recommendation selected with high confidence.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `W1`
* Preconditions met: Every research question answered; all three waves completed in order; exact conflict hunks, row-header upgrade sites, baseline counters, content-standard rules, and sibling test suites identified.
* Blockers: `none`
* Smallest action to change readiness: `none` (already `Ready`).

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                       |
| Lane evidence or inline fallback | Inline fallback: tightly coupled single-worktree git merge-tree and diff analysis across <10 files           |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C12`, `W1`)                                                                                     |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic transition to `Plan`                                                |

## Advisory Next Step

| Field                            | Record                                                                                                                                      |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                                                    |
| Planning Readiness               | Ready (`C1`–`C12`, `W1`)                                                                                                                    |
| Output mode and planning support | `convergence`; yes — supports direct transition to `rpi-plan`                                                                               |
| Acting owner                     | confirmed automatic RPI Agent                                                                                                               |
| Required gates or confirmations  | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), all 3 waves complete (`passed`), state write (`passed`)    |
| Continuation result              | automatic continuation to `Plan` (`rpi-plan` + single-pass `rpi-plan-critique`)                                                             |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md                                                            |
| Notes for planning or re-entry   | Plan 3 bounded phases: P01 Git Rebase & Conflict Resolution, P02 `screenRecordTable` Row-Header Parity & Coexistence Tests, P03 Focused Validation & Local Commit |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All diverging commits and files between `0486e2ca1` and `fe6398197` were inspected directly; further research would be redundant.

## Sources

* W1 - Vercel Labs Web Interface Guidelines (`command.md`) - https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-11-15, `main`)

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
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Cycle 1 (Wider, Deeper, Contrarian, Synthesis, Re-entry), Evidence Log (`C1`–`C12`, `W1`), Findings Mapped, Key Discoveries, Alternatives and Selected Recommendation, Open Questions/Risks, Current/Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none.
