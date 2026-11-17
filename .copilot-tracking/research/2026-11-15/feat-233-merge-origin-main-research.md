<!-- markdownlint-disable-file -->

# Task Research: feat-233-merge-origin-main

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | rpi-research (under RPI Agent automatic mode)                              |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md |

## Research Brief

* What to research: Exact three-way merge deltas, conflict hunks, semantic interactions across auto-merged files, scenario manifest hash dependencies, and focused validation contracts when merging `origin/main` into `feat/demo-233-same-home-tensions-0825` (`PR #1639`, Issue `#233` and 17 completed child issues).
* Why it matters: Both branches introduce dense, overlapping changes across `src/core` (`job_pack.py`, `projection.py`, `staff_intake.py`, `store.py`, `governance.py`, `taskqueues.py`, `workflows.py`) and `src/api` (`server.py`, `web/app.js`, `web/staff-intake.js`, `test_role_endpoint_inventory.py`, READMEs). Careless conflict resolution could drop `#1664`/`#1665`/`#1666`/`#1667` provenance/safeguarding/field-escalation controls from `origin/main` or `#233` same-home tension, cross-role exception queue, and WCAG 2.2 accessibility controls from `feat/demo-233-same-home-tensions-0825`.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases in this continuous automatic RPI run, plus downstream PR `#1639` reviewers.
* Scope: Three-way diff from merge-base `61e1917dd075a8307f0fd436c42cc41f47906846` to `HEAD` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`) and `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`), the 10 conflicting files, auto-merged files (`server.py`, `governance.py`, `taskqueues.py`, `workflows.py`, `test_taskqueues.py`, `docs/reference/log.md`), `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` (`SCENARIO_MANIFEST_RECIPE_SHA256`), and focused validation runners (`src/core` and `src/api` unit tests, `mypy`, `ruff`).
* Non-goals: Editing unrelated modules, running `tools/rpi-checks.py`, rebasing/rewriting branch history, or pushing to remote.
* Criteria: Every conflict region in all 10 files has line-level evidence from merge-base, `HEAD`, and `origin/main`; semantic cross-file interactions with auto-merged files and UX/WCAG/manifest invariants are verified; zero methods, routes, or fields are dropped from either branch.
* Requested outputs: Primary research artifact with `convergence` recommendation detailing exact reconciliation rules per file and verification steps.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                                             |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q6 covering branch commit verification, core Python conflict reconciliation, API/web/UX conflict reconciliation, test/README reconciliation, auto-merge semantic hazards, and manifest/tooling |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`, `docs/reference/research/ux/`                                                                  |
| External scope                   | none (internal repository reconciliation during research; Web Interface Guidelines fetched during web implementation/review per repository instructions)                                           |
| Initial internal candidate areas | 10 conflicting files under `src/core/` and `src/api/`, auto-merged `server.py`/`governance.py`/`taskqueues.py`/`workflows.py`, `scenario-manifest.json`, `test_scenario_manifest.py`              |
| Initial external candidate areas | none                                                                                                                                                                                              |
| Research posture                 | balanced                                                                                                                                                                                          |
| Posture provenance               | default (bounded internal merge with named 10-file conflict set plus adjacent auto-merge and manifest-hash interactions that could affect correctness)                                            |
| Explicit limits / deadline       | Focused validation tier (`src/core` and `src/api` unit tests, `ruff`, `mypy`; do NOT run `tools/rpi-checks.py`); do NOT push                                                                      |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across all 10 conflicts, adjacent auto-merged modules, manifest recipe hash, and test/type/lint runners                                             |
| Edits allowed during research?   | no, research-only                                                                                                                                                                                 |
| Resolved evidence root           | `.copilot-tracking/` default                                                                                                                                                                      |
| Known constraints / excluded sources | Preserve Fluent 2 design system, WCAG 2.2 AA baseline, plain-language content standard, human/resident approval boundaries; never read private datasets                                       |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                                                   | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|----------------------------------|------------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | Custom AMA Repository Instructions (`applyTo: "**"`) | Matches workspace root, `src/**`, `docs/**`                            | Enforces branch safeguards, Fluent 2/WCAG/plain-language UX rules, focused tier  | Selected: governs merge workflow, UX preservation, and validation boundaries              |
| Skill               | `rpi-research`                   | Active phase skill for read-only 3-wave investigation                  | Primary research artifact and `Ready` gate before `rpi-plan`                     | Selected: explicitly requested by caller for Phase 1                                      |
| Skill               | `web-design-guidelines`          | Matches `src/api/src/zava_forward/api/web/*.js` web changes            | External Web Interface Guidelines audit before web edits and before review       | Deferred to `rpi-implement` / `rpi-review`: research is read-only                         |
| Skill               | `redesign-existing-projects`     | Existing-app UI design upgrades                                        | Audits generic design patterns for visual redesigns                              | Skipped: task is surgical 3-way merge conflict preservation, not a visual redesign        |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered specialist for independent delegated research lanes    | Writes `.copilot-tracking/research/subagents/YYYY-MM-DD/*.md`                    | Selected for parallel deeper conflict-hunk inspection if needed, or inline when tightly coupled |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                                                  |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller directive to run full RPI loop continuously without stopping             | No interaction (CLI) | Proceed with `balanced` posture and `convergence` mode; verify actual `origin/main` SHA (`45cd2bd00`) vs prompt note |
| Direction change | None at intake                                                                                                            | N/A                  | Retain active scope across all 10 conflicts, auto-merged interactions, and manifest hash                         |
| Convergence      | Non-interactive CLI session; caller explicitly prohibited pausing between phases                                          | No interaction (CLI) | Complete full 3-wave cycle and transition automatically to `rpi-plan` once Planning Readiness is `Ready`         |

## Scope and Success Criteria

* Scope: Reconciling `feat/demo-233-same-home-tensions-0825` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`) with `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`) across all 10 conflicting files, auto-merged touchpoints, and `SCENARIO_MANIFEST_RECIPE_SHA256`.
* Assumptions:
  * Caller-cited SHA `89c8080cbfb1eb1c2b930c980cf3d73e0919c8e1` is not present on GitHub (`422 No commit found`); current `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`) contains `#1664`, `#1665`, `#1666`, `#1667`, and `#1672` and produces the exact 10 conflicting files listed in the prompt.
  * Auto-merged files (`server.py`, `governance.py`, `taskqueues.py`, `workflows.py`) might still contain subtle symbol/import/route collisions or count mismatches with `test_role_endpoint_inventory.py` and WCAG DOM checks.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect and plan resolution of the 10 merge conflicts from `git merge --no-commit origin/main`, preserve both `origin/main` (`#1664`, `#1665`, `#1666`, `#1667`) and `feat/demo-233-same-home-tensions-0825` (`#233` + 17 child issues / 49 commits) functionality without dropping methods, routes, or fields, check `SCENARIO_MANIFEST_RECIPE_SHA256` if `workbench_DomChecks.mjs` or manifest-tracked files changed, and validate with `src/core` + `src/api` unit tests, `mypy`, and `ruff`.
* Inferred research questions:
  * Why does `origin/main` resolve to `45cd2bd00` rather than `89c8080c`, and are all expected PRs present?
  * What exact dataclasses, methods, fields, and dict keys were added on each side of the 5 `src/core` conflicts (`job_pack.py`, `projection.py`, `staff_intake.py`, `store.py`, `test_job_pack.py`) and `src/core/README.md`?
  * What exact routes, DOM helpers, WCAG attributes, state cues, and endpoint inventories were added on each side of the 4 `src/api` conflicts (`app.js`, `staff-intake.js`, `test_role_endpoint_inventory.py`, `src/api/README.md`)?
  * Do auto-merged files (`server.py`, `governance.py`, `taskqueues.py`, `workflows.py`, `test_taskqueues.py`) or `workbench_DomChecks.mjs` / `test_wcag_*.py` / `test_scenario_manifest.py` break after naive union of the 10 conflicting files?
* Caller constraints and non-goals: Do NOT run `tools/rpi-checks.py`; do NOT push; preserve commit trailer and `Refs #233`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier only (`src/core` & `src/api` unit tests, `ruff`, `mypy`)      | User prompt / Intake | Exclude `tools/rpi-checks.py`; verify exact local Python/ruff/mypy runner paths    |
| exclude                                                  | Do not push merge commit to `origin`                                                  | User prompt / Intake | Keep final reconciled merge commit local in worktree                               |
| add                                                      | Preserve all methods, routes, and fields from both `origin/main` and `feat/demo-233`  | User prompt / Intake | Require contrarian check for accidental overwrites, duplicate keys, or count drift |

## Research Questions

|  # | Sub-question                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What commits diverge between `HEAD` (`a1d0be5f6`) and `origin/main` (`45cd2bd00`) from merge-base `61e1917dd`?                    | straightforward                          | H        | answered |
| Q2 | How should every conflict hunk in `src/core` (`job_pack.py`, `projection.py`, `staff_intake.py`, `store.py`, `test_job_pack.py`, `README.md`) be reconciled? | depth | H | answered |
| Q3 | How should every conflict hunk in `src/api` (`web/app.js`, `web/staff-intake.js`, `tests/test_role_endpoint_inventory.py`, `README.md`) be reconciled while preserving WCAG 2.2 cues? | depth | H | answered |
| Q4 | Do auto-merged files (`server.py`, `governance.py`, `taskqueues.py`, `workflows.py`, `test_taskqueues.py`) have hidden semantic conflicts? | breadth | H | answered |
| Q5 | Which files determine `SCENARIO_MANIFEST_RECIPE_SHA256` in `scenario-manifest.json`, and will this merge alter that digest?       | straightforward                          | H        | answered |
| Q6 | What exact Python/Node/mypy/ruff commands and environment paths run cleanly in this worktree?                                     | straightforward                          | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `.copilot-tracking/rpi-sessions/2026-11-15/228-procurement-wcag-c1-rebase-state.json`.
* Reused (verified) findings:
  * Child WCAG rebases on 2026-11-15 (`#227`, `#228`, `#229`, `#230`, `#231`, `#232`) and `#134`/`#135`/`#129` landed on `feat/demo-233-same-home-tensions-0825` up to `a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0` and maintain strict WCAG jump-link/table/state-cue counters in `src/api/tests/`.
  * Focused test execution in this environment uses `/usr/bin/python3` with `PYTHONPATH` across `src/core` and `src/api`, `/home/azureuser/.local/bin/ruff`, `/home/azureuser/.local/bin/mypy`, and Node v24.21.0.
* Superseded / stale:
  * Caller prompt noted `origin/main` as `89c8080cbfb1eb1c2b930c980cf3d73e0919c8e1`, which GitHub REST API reports as `422 No commit found`; actual fetched `origin/main` on GitHub is `45cd2bd00a593d28208f5b99053d854ababb5484` and produces the exact 10 conflicting files specified by the caller.

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier only (`src/core` & `src/api` unit tests, `ruff`, `mypy`); no push; zero dropped methods/routes/fields across `origin/main` and `feat/demo-233-same-home-tensions-0825`.
* Active research posture and completion basis: `balanced`; balanced scope coverage and adequate evidence across all 10 conflicts, adjacent auto-merged modules, manifest hashes, and test/type/lint runners.
* Explicit limits or deadline effect: `tools/rpi-checks.py` excluded per caller; all research executed read-only.

#### Wave 1: Wider

* Plan and independent lanes: Inline read-only sweep of branch divergence (`git log`, `git merge-tree --write-tree`), diff3 extraction of all 10 conflicting files against merge-base `61e1917dd075a8307f0fd436c42cc41f47906846`, scenario manifest locator scan, and tool availability probe (`python3`, `ruff`, `mypy`, `node`).
* Worker evidence relationships or inline fallback: Inline execution selected because all 10 conflicts share tightly coupled contracts (`job_pack` -> `staff_intake` -> `projection` -> `staff-intake.js`, and `taskqueues` -> `store` -> `app.js`). Mapped Q1 -> branch commits (`C1`), Q2/Q3 -> diff3 conflict hunks (`C2`-`C11`), Q5 -> `scenario_manifest.py` (`C15`).
* Reflection: `git merge-tree` confirmed the exact 10 conflicts and revealed two major parallel-feature overlaps needing deeper contract inspection: (1) Issue `#132` fieldwork variation escalation was implemented independently on `HEAD` (`#1682`/`#1725`) and `origin/main` (`#1666`), and (2) Issue `#76` hazard/safeguarding clocks were implemented independently on `HEAD` (`#1692`) and `origin/main` (`#1665`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Deep line-by-line comparison of Issue `#132` (`job_pack.py`, `staff_intake.py`, `projection.py`, `staff-intake.js`, `test_fieldwork_variation_owner_guard.py`, `test_staff_intake_api.py`, `test_job_pack.py`), Issue `#76` (`taskqueues.py`, `store.py`, `projection.py`, `app.js`, `test_workbench_hazard_clock_owner.py`, `test_safeguarding_clock_a11y.py`, `test_safeguarding_detail_boundary.py`), Issue `#82` (`GateError.rules` in `store.py` and `server.py`), and `scenario_manifest.py` `SOURCES`.
* Plan and independent lanes: Inline side-by-side analysis of every assertion in both branches' test suites against the conflicting modules and auto-merged files.
* Worker evidence relationships or inline fallback: Inline fallback (tightly coupled cross-branch Python/JS contracts). Mapped Q2 -> `C5`-`C10`, Q3 -> `C2`-`C4`, `C11`-`C13`, Q4 -> `C14`, Q5 -> `C15`, Q6 -> `C16`.
* Reflection: Uncovered exact dual-test constraints for `#132`: `test_fieldwork_variation_owner_guard.py` (`HEAD`) requires `acts_as_contract_instruction=False`, `is_contract_instruction=False`, `contract_notice`, `c["field_escalations"]`, `field_escalation_raised` audit row, staff-directory role check (`Pam Lead` cannot be `Building Safety Liaison`), `item["owner"] == {"name": ..., "role": ...}` when contact is unconfigured, and `staff-intake.js` form `aria-label="Raise a variation or concern"`; meanwhile `test_staff_intake_api.py` (`origin/main`) requires `named_owner()` placeholder/dotted-initial/role-word rejection, `assert_advisory()`, `note=ADVISORY_NOTE`, `advisory_only=True`, `owner_assigned`/`owner_status`, configured-env fallback with `owner["contact"]`, `c["escalations"]` with `id`/`case_id`/`named_owner`/`owner_role`/`escalation_kind`/`routed_by`/`routed_at`, and `field_escalation_routed` audit row.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether combining both `#132` representations or `#76`/`#135` web changes violates static WCAG counters (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`), plain-language blocked-word checks (`test_content_standard.py`), `projection.hold_notes` redaction (`assertNotIn(text, json.dumps(quil))`), `GateError` positional/optional args, or `scenario-manifest.json` SHA-256 checks.
* Plan and independent lanes: Inline verification of `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `taskqueues.py`, `GateError` call sites, and `git diff` on all 4 `scenario_manifest.py` `SOURCES`.
* Worker evidence relationships or inline fallback: Inline verification confirmed:
  1. Storing the escalation record in both `c["escalations"]` and `c["field_escalations"]` would leak `summary` on `GET /api/cases/ZF-3` for no-need roles UNLESS `projection.hold_notes` matches both shapes and skips overwriting both `"note"` and `"contract_notice"` (`C7`, `C12`). With that guard, `summary` becomes `NOTE_HELD` in both lists while both `note` and `contract_notice` survive intact.
  2. Unconditionally adding a second `screenTable` in `staff-intake.js` or using `"cannot"`/`"refused"` copy in `staff-intake.js` could violate `test_content_standard.py` (`BLOCKED_WORDS` check on `staff-intake.js`, `C13`); keeping `HEAD`'s conditional `screenTable` (`h("table", ...)` lives inside `role-screens.js`, keeping `test_accessibility_baseline.py` table count at `14`, `C11`) and `aria-invalid` site count at `9` preserves all WCAG baseline assertions.
  3. Setting `out["owner"]["contact"] = contact` ONLY when `contact` is non-empty avoids breaking `self.assertEqual(item["owner"], dict(name=OWNER, role=ROLE))` in `test_fieldwork_variation_owner_guard.py` while satisfying `self.assertEqual(out["escalation"]["owner"]["contact"], "pam@example.test")` in `test_staff_intake_api.py` (`C8`, `C12`).
  4. None of the 4 `scenario_manifest.py` `SOURCES` (`src/api/checks/workbench-manifest.json`, `src/api/checks/workbench_browser_check.py`, `src/core/tests/dataset.py`, `src/api/tests/test_workbench.py`) changed on either `HEAD` or `origin/main` since merge-base (`C15`), so `scenario-manifest.json` hashes remain valid unless touched; we will still run `test_scenario_manifest.py` and `test_generator_determinism_matrix.py` to confirm.
* Reflection: All contrarian hazards are resolved with concrete, testable invariants; zero unresolved contradictions remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Reconcile against `origin/main` (`45cd2bd00`) containing `#1664`, `#1665`, `#1666`, `#1667`, `#1672` | `C1` | accepted | GitHub REST API and `git fetch origin` confirm `45cd2bd00` is canonical `origin/main` and produces the exact 10 conflicts | Selected merge target in Recommendation |
| Unified `#132` escalation schema & dual-contract `job_pack.py` / `staff_intake.py` / `projection.py` / `staff-intake.js` | `C3`, `C5`, `C6`, `C7`, `C8`, `C10`, `C12`, `C13` | accepted | Preserves 100% of methods, fields, routes, and invariants tested by both `test_fieldwork_variation_owner_guard.py` and `test_staff_intake_api.py` | Core & web reconciliation specification |
| Keep both `hazard_clocks` (`#1692` accountable-owner/clock_text) and `safeguarding_clocks` (`#1665` allowlisted paragraph + raw `safeguarding_items` stripping) | `C2`, `C7`, `C9`, `C14` | accepted | `hazard_clocks` covers hazards (`c["hazards"]`) while `safeguarding_clocks` covers `c["safeguarding_items"]`; both render cleanly in `app.js` `workSummary` | `app.js`, `projection.py`, `store.py` specification |
| Combine `taskqueues.accountable_owner(active.get("owner"))` with `[gates.BOOKING_RULES["safety"]]` in `Store.require_safety_clear` | `C9`, `C14` | accepted | Preserves `#1692` fallback owner text and `#1667` structured `GateRule` provenance | `store.py` conflict resolution |
| Union `POST_ENDPOINTS` in `test_role_endpoint_inventory.py` (`field-escalate` + `/api/exceptions/recovery`) | `C4` | accepted | Covers all `server.py` routes from both `#1666`/`#1682` and `#1757` (`#135`) | `test_role_endpoint_inventory.py` resolution |
| Drop either `#1682` (`field_escalations`) or `#1666` (`escalations` / `route_escalation`) in favor of one side | `C8`, `C12` | rejected | Dropping either breaks existing regression tests and violates caller's zero-dropped-methods/fields constraint | Rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All 6 research questions and all 10 conflict files plus adjacent auto-merged files and manifest rules have complete line-level codebase evidence (`C1`-`C16`); contrarian checks surfaced and resolved every cross-branch interaction.
* Revised brief or revalidation required: none
* Readiness effect: `Ready` (`C1`-`C16`)

## Evidence Log

* Delegation: inline: all 10 conflicts form two tightly coupled cross-stack feature slices (`#132` field escalation and `#76`/`#82` clocks & gate rules) where direct 3-way diff3 comparison prevents cross-lane drift.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | `HEAD` is `a1d0be5f6` (56 commits ahead of merge-base `61e1917dd`); `origin/main` is `45cd2bd00` (20 commits ahead, including `#1664`, `#1665`, `#1666`, `#1667`, `#1672`), producing the exact 10 merge conflicts | `docs/reference/README.md:4` | bash (`git log`, `git merge-tree`, `gh api`) | high | Caller SHA `89c8080c` returned 422 on GitHub; `45cd2bd00` is live `origin/main` |
| C2  | `workSummary(work)` in `app.js` conflicts between `#1692` (`clock.clock_text` + `clock.accountable_owner` on `work.hazard_clocks`) and `#1665` (`(work.safeguarding_clocks \|\| []).map(...)` rendering `<p class="safeguarding-clock">`) | `src/api/src/zava_forward/api/web/app.js:833` | view / diff3 | high | Both map expressions belong inside `workSummary`'s `h("div", { class: "work-context" }, ...)` |
| C3  | `staff-intake.js` conflicts between `#1682` (`intakeNotInstruction`, `intakeEscalate(order, options, rerender)` with `aria-label="Raise a variation or concern"`, conditional `screenTable`) and `#1666` (per-order IDs `esc-${order}-*`, optional owner when configured, `Owner status` row) | `src/api/src/zava_forward/api/web/staff-intake.js:120` | view / diff3 | high | Tested by Node VM harness in `src/api/tests/test_fieldwork_variation_owner_guard.py:213` |
| C4  | `POST_ENDPOINTS` in `test_role_endpoint_inventory.py` adds `("/api/workorders/WO-0001/field-escalate", {})` on both sides plus `("/api/exceptions/recovery", {})` on `HEAD` (`#1757`) | `src/api/tests/test_role_endpoint_inventory.py:30` | view / diff3 | high | Keep single `field-escalate` entry plus `/api/exceptions/recovery` |
| C5  | `src/api/README.md` (`:5894`) and `src/core/README.md` (`:5308`) conflict only in the `#132` `field-escalate` prose description | `src/api/README.md:5894`, `src/core/README.md:5308` | view / diff3 | high | Combine non-contract-instruction / advice-only / named-owner / held-summary prose concisely |
| C6  | `job_pack.py` adds `NON_INSTRUCTION_NOTICE`, `INSTRUCTION_CLAIMS`, `is_contract_instruction=False`, `acts_as_contract_instruction=False`, `contract_notice`, and `reject_instruction_claim` on `HEAD`, while `origin/main` adds `_PLACEHOLDER_WORDS`, `_ROLE_WORDS`, `_NAME_ALLOWED`, `ADVISORY_NOTE`, `named_owner`, `assert_advisory`, and `note=ADVISORY_NOTE` | `src/core/src/zava_forward/core/job_pack.py:28` | view / diff3 | high | Retain `import re`, all constants, `named_owner`, `assert_advisory`, `reject_instruction_claim`, and stamp all non-instruction fields + `note` + `contract_notice` in `escalation()` |
| C7  | `projection.py` `hold_notes` pops `safeguarding_items` (`#1665`), redacts escalation `summary` to `NOTE_HELD`, and must skip overwriting both `note` (`#1666`) and `contract_notice` (`#1682`); `redact_staff_detail` also pops `safeguarding_items` | `src/core/src/zava_forward/core/projection.py:109` | view / diff3 | high | `contract_notice` is not in `NOTE_KEYS`, while `note` IS in `NOTE_KEYS` (`:30`), so skipping `k in ("note", "contract_notice")` when `advisory` preserves both |
| C8  | `staff_intake.py` needs `_valid_contact`, `_configured_owner`, `route_escalation`, `escalation_destination` (with `configured`, `owner_assigned`, `owner_status`, `advisory_only=True`, `contract_instruction=False`, `is_contract_instruction=False`, `acts_as_contract_instruction=False`, `note`), `escalation_options`, `_view_escalation`, and unified `escalate()` | `src/core/src/zava_forward/core/staff_intake.py:153` | view / diff3 | high | Validate `reject_instruction_claim`, text types, open case & non-withdrawn order, `route_escalation`, staff-directory role check when staff exist, store in `escalations` & `field_escalations`, emit `field_escalation_raised` & `field_escalation_routed` |
| C9  | `store.py` auto-merges `GateError(reasons, rules=())`, `_transition_rules`, `d.pop("safeguarding_items", None)`, and rule-bearing `GateError` raises, leaving 1 conflict in `require_safety_clear` where `HEAD` uses `taskqueues.accountable_owner(active.get('owner'))` and `origin/main` passes `[gates.BOOKING_RULES["safety"]]` | `src/core/src/zava_forward/core/store.py:608` | view / diff3 | high | Combine both on `require_safety_clear` |
| C10 | `test_job_pack.py` adds `test_instruction_claims_are_rejected` on `HEAD` and `test_placeholder_owner_names_are_rejected`, `test_real_names_are_accepted`, `test_every_kind_routes_to_named_owner_and_stays_advisory`, `test_assert_advisory_refuses_instruction_records` on `origin/main` | `src/core/tests/test_job_pack.py:140` | view / diff3 | high | Keep all 5 test methods; note line 157 tests `owner_name="Pam"`, which is accepted by `named_owner` |
| C11 | `test_accessibility_baseline.py` pins `sites == 9` (`aria-invalid`) and `tables == 14` (`h("table", {})`); `test_epic149_form_error_summary_associations.py` maps those exact 9 sites | `src/api/tests/test_accessibility_baseline.py:100`, `src/api/tests/test_epic149_form_error_summary_associations.py:16` | view | high | Do not add `aria-invalid` or raw `h("table", {})` in `app.js` or `staff-intake.js` |
| C12 | `test_fieldwork_variation_owner_guard.py` (`HEAD`) and `test_staff_intake_api.py` (`origin/main`) both subclass `ProcurementApiFixture` (`DATA["staff"][1]` is `Pam Lead`, `Retrofit Programme Manager`) and assert complementary HTTP, SQLite/JSON restart, projection, audit, and Node-VM screen properties | `src/api/tests/test_fieldwork_variation_owner_guard.py:21`, `src/api/tests/test_procurement_api.py:63` | view / git show | high | Setting `owner["contact"]` only when configured contact is non-empty satisfies both `assertEqual(item["owner"], {"name": OWNER, "role": ROLE})` and `owner["contact"] == "pam@example.test"` |
| C13 | `test_content_standard.py` audits string literals in `staff-intake.js` matching `BLOCKED_WORDS` (`cannot\|could not\|not available\|unavailable\|failed\|not valid\|switched off\|does not include\|refused\|not writable`) to require `intakeOwned` (`Owner:` + `Next action:`) | `src/api/tests/test_content_standard.py:242` | view | high | Avoid un-owned `BLOCKED_WORDS` literals in `staff-intake.js` |
| C14 | Auto-merged `server.py`, `governance.py`, `taskqueues.py`, and `workflows.py` combine cleanly without symbol collisions (`safeguarding_clocks` + `_text` in `taskqueues.py` do not collide with `hazard_clock` / `is_safeguarding` / `accountable_owner`) | `src/core/src/zava_forward/core/taskqueues.py:80`, `src/api/src/zava_forward/api/server.py:1660` | bash (`git diff`) | high | Verify with full `src/core` and `src/api` unit test discovery + `mypy` + `ruff` |
| C15 | `scenario_manifest.py` hashes 4 public files (`workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, `test_workbench.py`); `git diff` confirms zero changes to those 4 files on either `HEAD` or `origin/main` since merge-base | `src/core/src/zava_forward/core/synthetic/scenario_manifest.py:31`, `src/core/tests/test_scenario_manifest.py:20` | view / bash | high | `scenario-manifest.json` SHA-256 entries remain current; verify directly via `test_scenario_manifest.py` and `test_generator_determinism_matrix.py` |
| C16 | Environment provides Python 3.12.3 (`/usr/bin/python3`), `/home/azureuser/.local/bin/ruff`, `/home/azureuser/.local/bin/mypy`, and Node v24.21.0 (`/home/azureuser/.nvm/versions/node/v24.21.0/bin/node`) | `src/README.md:1` | bash (`which`) | high | Focused validation runners confirmed available |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* Prompt reference SHA vs remote `origin/main`: Prompt parenthetically cited `89c8080cbfb1eb1c2b930c980cf3d73e0919c8e1`, whereas GitHub REST API (`repos/jmservera/ama/branches/main`) and `git fetch origin` show `origin/main` at `45cd2bd00a593d28208f5b99053d854ababb5484` (`89c8080c` returns 422 on GitHub); resolved by primary repository state (`C1`) -> merge `origin/main` (`45cd2bd00`), which contains all cited PRs (`#1664`, `#1665`, `#1666`, `#1667`) and yields the exact 10 conflicting files.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `HEAD` (`a1d0be5f6`) has 56 commits and `origin/main` (`45cd2bd00`) has 20 commits since merge-base `61e1917dd`, conflicting in the exact 10 files | `C1` | high | Proceed with `git merge --no-commit origin/main` |
| Q2 | `job_pack.py`, `staff_intake.py`, `projection.py`, `store.py`, `test_job_pack.py`, and `src/core/README.md` require additive union of `#132` non-instruction/advisory-routing fields, dual `escalations`/`field_escalations` persistence with held-summary redaction, and `#76`+`#82` `GateError` safety owner + rule metadata | `C5`-`C10`, `C12` | high | Ready for exact file-by-file planning |
| Q3 | `app.js` renders both `#1692` `hazard_clocks` and `#1665` `safeguarding_clocks`; `staff-intake.js` keeps `#1682` `Raise a variation or concern` form & `intakeNotInstruction` fail-closed table while adding `#1666` per-order field IDs, `Owner status`, and optional configured-owner submission without `BLOCKED_WORDS` or WCAG count drift; `test_role_endpoint_inventory.py` keeps both `field-escalate` and `/api/exceptions/recovery` | `C2`-`C5`, `C11`-`C13` | high | Preserves WCAG 2.2 AA baseline and Node-VM screen tests |
| Q4 | Auto-merged `server.py`, `governance.py`, `taskqueues.py`, `workflows.py`, `test_taskqueues.py`, and `docs/reference/log.md` have zero symbol or logic collisions | `C14` | high | Verify post-merge via full unit, mypy, and ruff suites |
| Q5 | `scenario_manifest.py` hashes `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py`; none changed on either branch | `C15` | high | Verify via `test_scenario_manifest.py`; update hashes only if a tracked source changes |
| Q6 | `/usr/bin/python3`, `~/.local/bin/ruff`, `~/.local/bin/mypy`, and Node v24.21.0 are installed and ready | `C16` | high | Focused validation commands ready for `rpi-implement` |

## Key Discoveries

* Parallel Issue `#132` implementations landed on `feat/demo-233-same-home-tensions-0825` (`#1682`, `#1725`) and `origin/main` (`#1666`), leaving two active API test suites (`test_fieldwork_variation_owner_guard.py` and `test_staff_intake_api.py`) that must both pass simultaneously (`C6`, `C8`, `C12`).
* Setting `owner["contact"]` on routed escalations only when a configured contact is non-empty, persisting to both `escalations` and `field_escalations`, holding `summary` while preserving both `note` and `contract_notice` in `projection.hold_notes`, and recording both `field_escalation_raised` and `field_escalation_routed` audit entries satisfies every assertion in both `#132` test suites without dropping any method, field, or route (`C7`, `C8`, `C12`).
* Parallel Issue `#76` implementations (`#1692` hazard/safeguarding clock text on `hazards` vs `#1665` allowlisted `safeguarding_clocks` on `safeguarding_items` with raw-field stripping) compose cleanly in `taskqueues.py`, `projection.py`, `store.py`, and `app.js` (`C2`, `C7`, `C9`, `C14`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Execute `git merge --no-commit origin/main` on `feat/demo-233-same-home-tensions-0825` and apply an additive, contract-preserving union across all 10 conflicting files so every symbol, field, route, audit event, projection rule, and UI element from both `origin/main` (`#1664`, `#1665`, `#1666`, `#1667`) and `feat/demo-233-same-home-tensions-0825` (`#233` and 17 child issues) remains intact without altering `test_accessibility_baseline.py` or `test_content_standard.py` invariants.
* Rationale: Both branches contain merged, tested PR contracts with non-conflicting domain intent (named-owner non-instruction fieldwork escalations, safeguarding clock redaction, `GateRule` refusal metadata, cross-role exception recovery, and WCAG 2.2 role-screen accessibility). An additive union satisfies both branches' unmodified regression suites (`C2`-`C15`).
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `C13`, `C14`, `C15`
* Implementation impact: Resolves conflicts in the 10 listed files (`src/core/src/zava_forward/core/{job_pack,projection,staff_intake,store}.py`, `src/core/tests/test_job_pack.py`, `src/core/README.md`, `src/api/src/zava_forward/api/web/{app,staff-intake}.js`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/README.md`) and commits the merge alongside dated `.copilot-tracking/` artifacts.
* Confidence: high: Verified against diff3 hunks and every downstream test assertion on both branches.

File tree (conflicting files reconciled in merge commit, plus RPI artifacts):

```text
src/
  core/
    README.md
    src/zava_forward/core/
      job_pack.py
      projection.py
      staff_intake.py
      store.py
    tests/
      test_job_pack.py
  api/
    README.md
    src/zava_forward/api/web/
      app.js
      staff-intake.js
    tests/
      test_role_endpoint_inventory.py
.copilot-tracking/
  rpi-sessions/2026-11-15/feat-233-merge-origin-main-state.json
  research/2026-11-15/feat-233-merge-origin-main-research.md
  plans/2026-11-15/feat-233-merge-origin-main-plan.md
  details/2026-11-15/feat-233-merge-origin-main-phase-details.md
  reviews/plans/2026-11-15/feat-233-merge-origin-main-plan-critique.md
  changes/2026-11-15/feat-233-merge-origin-main-changes.md
  reviews/logs/2026-11-15/feat-233-merge-origin-main-review.md
```

### Alternative: Favor `origin/main` `#1666` schema and rewrite `HEAD`'s `test_fieldwork_variation_owner_guard.py`

* Approach: Take `origin/main` (`--theirs`) on `job_pack.py`, `staff_intake.py`, and `staff-intake.js`, dropping `acts_as_contract_instruction`, `is_contract_instruction`, `contract_notice`, `reject_instruction_claim`, `field_escalations`, and `escalation_options`, then rewrite `HEAD`'s `#1682`/`#1725` tests.
* Trade-offs: Slightly fewer keys on escalation dicts, at the cost of dropping explicit `#1725`/`#1682` fields (`is_contract_instruction`, `acts_as_contract_instruction`, `reject_instruction_claim`, closed-case/withdrawn-order guard, staff-directory role check) and mutating non-conflicting child-issue tests.
* Evidence refs: `C3`, `C6`, `C8`, `C12`
* Rejection rationale: Violates the explicit caller constraint to preserve BOTH `origin/main` and `feat/demo-233-same-home-tensions-0825` functionality without dropping any methods, routes, or fields.

### Alternative: Favor `HEAD` `#1682`/`#1725` schema and drop `origin/main` `#1666` helpers

* Approach: Take `HEAD` (`--ours`) on `job_pack.py`, `staff_intake.py`, and `staff-intake.js`.
* Trade-offs: Keeps `HEAD` tests green, at the cost of breaking `origin/main`'s `test_staff_intake_api.py` and dropping `named_owner`, `assert_advisory`, `route_escalation`, `_configured_owner`, `owner_assigned`/`owner_status`, and `advisory_only`.
* Evidence refs: `C6`, `C8`, `C10`, `C12`
* Rejection rationale: Breaks `test_staff_intake_api.py` on `origin/main` and violates the zero-dropped-methods/fields constraint.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Verify during `rpi-implement` whether any non-conflicting `origin/main` test (`test_generator_determinism_matrix.py`, `test_safeguarding_clock_a11y.py`, `test_safeguarding_detail_boundary.py`, `test_gates.py`, `test_discovery_parity` `#1627`) interacts with new tests or modules added on `feat/demo-233-same-home-tensions-0825`.
* Follow-up: Post-merge human assistive-technology (`#151`) and participant walkthrough (`#155`) gates remain open across `#233` role screens before merge to `main`.
* Residual uncertainty: Caller prompt cited `89c8080cbfb1eb1c2b930c980cf3d73e0919c8e1` for `origin/main`, which does not exist on GitHub (`45cd2bd00a593d28208f5b99053d854ababb5484` is live `origin/main`); documented explicitly in `Prior Knowledge Gate` and `Contradictions / Conflicts`.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Merge `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`) into `feat/demo-233-same-home-tensions-0825` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`) without pushing | confirmed | user / evidence | `45cd2bd00` is the live `origin/main` tip on GitHub with `#1664`-`#1667` and exact 10 conflicts | `C1` | Reconciles PR `#1639` locally |
| Use additive dual-contract reconciliation for `#132` across `job_pack.py`, `staff_intake.py`, `projection.py`, `test_job_pack.py`, `staff-intake.js`, and READMEs | confirmed | evidence / constraint | Preserves all methods/fields/routes from `#1666`, `#1682`, and `#1725` so both test suites pass | `C3`, `C5`-`C8`, `C10`, `C12`, `C13` | Zero dropped symbols or test rewrites outside the 10 conflicts |
| Preserve both `hazard_clocks` (`#1692`) and `safeguarding_clocks` (`#1665`) in `app.js` and combine accountable-owner fallback + `GateRule` in `store.py` | confirmed | evidence | Composes hazard clocks, allowlisted safeguarding clocks, and structured gate rules cleanly | `C2`, `C9`, `C14` | Passes `#76` and `#82` suites from both branches |
| Load and fetch `web-design-guidelines` before editing `app.js`/`staff-intake.js` and refresh before `rpi-review` | confirmed | constraint | Required by AMA Repository Instructions Web Development Guidance | `C2`, `C3`, `C11` | Ensures Web Interface Guidelines review with `file:line` findings |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Push reconciled merge commit to `origin/feat/demo-233-same-home-tensions-0825` (`PR #1639`) | Explicit owner/coordinator instruction after reviewing local merge commit | user | Remote PR `#1639` remains at `a1d0be5f6` until pushed | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Inspect opt-in Playwright/axe browser checks (`specialist_keyboard_browser_check.py`) on merged branch | Confirms rendered focus rings after merge | Separate full-gate run before PR `#1639` merge | deferred | `Q3`; `C2`, `C3`, `C11` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected — additive 3-way merge resolution across all 10 conflicting files preserving 100% of `origin/main` and `feat/demo-233-same-home-tensions-0825` contracts.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `C13`, `C14`, `C15`, `C16`
* Preconditions met: Clean worktree verified on `feat/demo-233-same-home-tensions-0825`; all 10 conflict blocks inspected with `--diff3`; adjacent auto-merged modules, WCAG counters, content-standard rules, and scenario manifest hashes verified; local runners confirmed.
* Blockers: none
* Smallest action to change readiness: none (`Ready` for automatic transition to `rpi-plan`).

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                                      |
| Lane evidence or inline fallback | Inline fallback: tightly coupled cross-branch `#132` and `#76`/`#82` contracts across Python core and JS web modules           |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`-`C16`)                                                                                                             |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent — automatic continuation to `rpi-plan`                                                           |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C16`)                                                                                           |
| Output mode and planning support | `convergence` — yes, supports planning when Planning Readiness is `Ready`                                    |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | 3-wave completion: passed; artifact self-check: passed; pre-transition state write to `Plan`: passed         |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md                                 |
| Notes for planning or re-entry   | Sequence merge initiation, `src/core` conflicts, `src/api` web/test/README conflicts (with `web-design-guidelines`), manifest/discovery verification, focused test/mypy/ruff suite, and merge commit |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All 10 conflict files, auto-merged modules, test contracts, and manifest hashes are completely mapped from primary codebase evidence; further research waves would be redundant.

## Sources

No external sources used.

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
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions/Risks, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none
