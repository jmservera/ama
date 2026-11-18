---
description: "Primary evidence artifact for Epic #89 and Epic #100 scoped #440 stabilization checkpoints"
---
<!-- markdownlint-disable-file -->

# Task Research: delivery-89-100-epic-stabilization-checkpoints

| Field              | Value                                                                                                  |
|--------------------|--------------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                             |
| Researcher / agent | rpi-research (RPI Agent, automatic mode)                                                               |
| Status             | Complete                                                                                               |
| Artifact path      | .copilot-tracking/research/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-research.md       |

## Research Brief

* What to research: Exact Git/GitHub provenance, BRD/PRD/ADR metadata and blob SHAs, requirement-to-code/test/journey traceability, governance/boundary invariants, test suite inventory and runner setup, and residual/closure disposition for the `#440` scoped stabilization checkpoints of Epic `#89` (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`) and Epic `#100` (`#101`, `#102`, `#103`).
* Why it matters: Merged child issues alone do not satisfy the `#440` epic stabilization criterion; an evidence-backed, honest reconciliation and local-first regression record in `docs/architecture/cutover-evidence-pack.md` (indexed in `docs/reference/README.md` and logged in `docs/reference/log.md`) is required before epic closure.
* Audience or intended use: Project owner, coordinator, independent reviewer, and downstream `rpi-plan` / `rpi-implement` / `rpi-review` phases.
* Scope: `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/*.md`, `src/core/`, `src/api/`, `src/agents/` (tokenomics/boundaries), `tools/check-legacy-references.py`, and live GitHub issue/PR metadata via `gh`.
* Non-goals: No source code edits unless an actual bug or required refactoring is uncovered; no `tools/rpi-checks.py` invocation; no ticking or closing of GitHub issues; no `git push` or `gh pr create`; no fabricated Azure/human/legal approvals.
* Criteria: Accurate SHA/blob provenance (resolving any prompt vs repository SHA discrepancy honestly), complete document-qualified traceability (`BRD`, `PRD`, `ADR`), explicit boundary verification (package/identity, persistence, auth/roles, resident consent, human review/approval, AI unavailable/failure and manual paths), runnable focused regression plan, and honest bug/residual/recommendation disposition.
* Requested outputs: Primary research artifact supporting convergence on the exact documentation structure, traceability tables, and focused local test execution matrix.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                      |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q6 covering Git/PR/issue provenance, BRD/PRD/ADR status & blobs, Epic #89 traceability, Epic #100 traceability, cross-cutting boundaries, and local test runner matrix |
| Codebase scope                   | `docs/`, `src/core/`, `src/api/`, `src/agents/`, `tools/`                                                                                  |
| External scope                   | GitHub repository `jmservera/ama` issues, PRs, and branches via `gh` CLI                                                                   |
| Initial internal candidate areas | `docs/architecture/cutover-evidence-pack.md`, `docs/brds/`, `docs/prds/`, `docs/adrs/`, `src/core/src/zava_forward/core/`, `src/api/src/zava_forward/api/` |
| Initial external candidate areas | GitHub issues `#89`, `#100`, `#440`, `#90-#92`, `#132-#133`, `#1384`, `#1402`, `#101-#103`, PR `#1641`                                      |
| Research posture                 | balanced                                                                                                                                   |
| Posture provenance               | default (bounded internal stabilization task with named epics, child issues, and target docs)                                              |
| Explicit limits / deadline       | Do NOT invoke `tools/rpi-checks.py`; do NOT push or open a PR; no `.copilot-tracking/` references in `docs/` or `src/`                     |
| Posture-specific completion basis| balanced scope coverage and adequate evidence across all #440 checkpoint dimensions                                                        |
| Edits allowed during research?   | no, research-only                                                                                                                          |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                       |
| Known constraints / excluded sources | Never read private datasets; preserve existing sections of `cutover-evidence-pack.md`; append-only at EOF for `docs/reference/log.md`  |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches all repository paths | Enforces KB conventions, Markdown style (`*` lists, ASCII punctuation, no em dashes), focused tier rules, and no `.copilot-tracking/` leaks in `docs/` | Selected: mandatory repository governance |
| Skill               | `rpi-research`                   | Explicit caller RPI loop phase 1                  | Produces dated research artifact with three-wave cycle | Selected: active phase skill |
| Skill               | `documentation`                  | Documentation authoring/audit plugin skill        | General doc drift/authoring guidance         | Skipped: repository instructions and existing `#440` checkpoint conventions in `cutover-evidence-pack.md` already define exact schema |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered subagent for independent research lanes | Lane artifact under `.copilot-tracking/research/subagents/` | Skipped (inline preferred): tightly coupled cross-artifact SHA, requirement ID, code module, and test file reconciliation takes fewer direct calls inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Caller supplied complete scope, worktree, branch, target files, child issue lists, validation tier, and commit rules in autopilot mode | No interactive prompt required | Proceed in `balanced` posture and verify exact Git/GitHub SHAs against caller-stated SHAs |
| Direction change | None at intake                                              | N/A                       | N/A                                                |
| Convergence      | All 6 research questions answered with `C#` and `W#` evidence; contrarian SHA and ancestry check resolved | No interactive prompt required in automatic mode | Converge on two dated 2026-11-15 `#440` checkpoint sections in `docs/architecture/cutover-evidence-pack.md` plus KB index/log updates (`Planning Readiness: Ready`) |

## Scope and Success Criteria

* Scope: Verify every `#440` stabilization requirement for Epic `#89` and Epic `#100` on worktree HEAD (`feat/epic-89-100-stabilization-checkpoints`).
* Assumptions:
  * Caller-stated SHAs (`7427320280f68fd91f91df37a108892c3e97101f` and `c1ef91e23df56947b6ce1313684b587ff03dc134`) must be verified against actual Git and GitHub remote refs rather than copied blindly.
  * All listed child issues of Epic `#89` and Epic `#100` are closed on `main`, which must be verified via `gh`.
* Success criteria:
  * Every research question is answered with `C#` / `W#` evidence IDs.
  * Exact Git commit/tree/blob SHAs and live GitHub issue/PR states are verified.
  * Every child issue and BRD/PRD/ADR requirement for Epic `#89` and Epic `#100` maps to concrete `src/core` / `src/api` / `src/agents` modules, tests, and journeys.
  * Local Python environment and exact focused test commands are identified for Implement.

## Task Research Requests

* Explicit requests: Reconcile provenance, BRD/PRD/ADR intent, code/test/journey traceability, governance boundaries, local regression commands, bug/refactoring disposition, and Azure/human residuals for Epic `#89` and Epic `#100` `#440` checkpoints.
* Inferred research questions: How has Epic `#89` evolved since its partial 2026-11-03 checkpoint (including `#92`, `#132`, `#133`, `#1384`, `#1402` and FR-016/FR-017 numbering divergence), what changed in `cutover-evidence-pack.md` conventions up to 2026-11-14, and why do local Git SHAs differ from the prompt's 40-char strings?
* Caller constraints and non-goals: Research-only in this phase; do not run `tools/rpi-checks.py`; do not push or open PR; no `.copilot-tracking/` paths inside `docs/`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| exclude                                                  | Do NOT invoke `tools/rpi-checks.py` | Caller prompt | Use focused `pytest`/`unittest`, `test_live_doc_links.py`, and `tools/check-legacy-references.py` |
| narrow                                                   | Focused validation tier; leave frozen local commit without push/PR | Caller prompt | Restricts Implement/Review closeout to local verification and local commit |
| exclude                                                  | No `.copilot-tracking/` references in `docs/` or `src/` | Caller prompt & repo instructions | Unlike older sections in `cutover-evidence-pack.md` that linked `.copilot-tracking/`, our new checkpoint sections in `docs/` must contain zero `.copilot-tracking/` strings |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status |
|---:|------------------|------------------------------------------|-----------|--------|
| Q1 | What are the exact Git commit/tree SHAs (worktree HEAD, parent branch/PR #1641, `origin/main`, live remote `main`), and how do they reconcile with the caller prompt's stated SHAs? | straightforward | H | answered (`C1`, `W1`, `W2`) |
| Q2 | What are the exact live GitHub states, closing PRs, and acceptance criteria of `#440`, Epic `#89` (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`), and Epic `#100` (`#101`, `#102`, `#103`)? | breadth | H | answered (`W3`..`W15`) |
| Q3 | What are the exact paths, versions/dates, git blob SHAs, and approval statuses of Case Study 48 original/addendum, BRD, PRD, and relevant ADRs in `docs/adrs/`? | straightforward | H | answered (`C2`..`C12`) |
| Q4 | How do Epic `#89` requirements (`BRD`, `PRD`, `ADR`) map to `src/core` and `src/api` modules, tests, journeys, and cross-cutting boundaries (including updates since the 2026-11-03 partial checkpoint)? | depth | H | answered (`C4`, `C5`, `C11`, `C12`, `C13`..`C23`) |
| Q5 | How do Epic `#89` and Epic `#100` requirements (`BRD`, `PRD`, `ADR`) map to `src/core`, `src/agents`, and `src/api` modules, tests, journeys, and cross-cutting boundaries? | depth | H | answered (`C4`, `C5`, `C7`..`C11`, `C24`..`C33`) |
| Q6 | Which Python environment and focused test commands cleanly execute Epic `#89`, Epic `#100`, `test_live_doc_links.py`, and `tools/check-legacy-references.py`, and what existing caveats/residuals apply? | depth | H | answered (`C34`..`C37`) |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/log.md` (tail), and `docs/architecture/cutover-evidence-pack.md` (lines 1-260, 760-892, 2475-2560, 8495-8560).
* Reused (verified) findings:
  * `docs/architecture/cutover-evidence-pack.md` already contains a partial `Epic #89 scoped stabilization checkpoint (2026-11-03)` at line 2477 (when `#92`, `#132`, `#133` were open) and recent `#440` checkpoints up to `Stabilization checkpoint (2026-11-14, Refs #440 #104 #149 #165)` at line 8498.
  * Earlier Epic `#89` checkpoint flagged the `FR-016` / `FR-017` numbering divergence between BRD and PRD.
* Superseded / stale:
  * The 2026-11-03 Epic `#89` checkpoint recorded `#92`, `#132`, `#133` as open/unmerged and predated `#1384` and `#1402`; it explicitly required rerunning the checkpoint once children resolved.
  * Some older sections in `cutover-evidence-pack.md` mention `.copilot-tracking/` paths, which is now explicitly prohibited by caller rules ("no `.copilot-tracking/` references in `docs/` or `src/`").

## Cycle 1: Three-Wave Execution

### Wave 1: Wider (Breadth Discovery)

* Execution mode: Inline fallback (tightly coupled repository, Git object graph, and GitHub issue/PR metadata inspection).
* Breadth findings:
  * Git branch `feat/epic-89-100-stabilization-checkpoints` is stacked on `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`, `OPEN` targeting `main`) (`C1`, `W1`).
  * Live GitHub issue `#440`, Epic `#89`, and Epic `#100` are `OPEN`, while all 7 Epic `#89` children (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`) and all 3 Epic `#100` children (`#101`, `#102`, `#103`) are `CLOSED` (`W3`..`W15`).
  * Existing `docs/architecture/cutover-evidence-pack.md` contains an earlier partial `Epic #89 scoped stabilization checkpoint (2026-11-03)` (`C13`) when `#92`, `#132`, `#133` were open and before `#1384` and `#1402` existed, and has no dedicated Epic `#100` `#440` stabilization checkpoint section (`C14`).
  * All normative specification documents (`case_study_48_original.md`, `case_study_48_addendum.md`, `agentic-retrofit-programme-brd.md`, `zava-forward-retrofit-programme-demonstrator.md`, and `docs/adrs/0001..0007`) exist in-tree with deterministic Git blob SHAs and explicit draft/proposed/bounded-exercise approval statuses (`C2`..`C12`).

### Wave 2: Deeper (Code, Contract, Test, and Boundary Verification)

* Execution mode: Inline fallback across `docs/brds/`, `docs/prds/`, `docs/adrs/`, `src/core/`, `src/agents/`, `src/api/`, and `tools/`.
* Key technical findings:
  * **BRD vs PRD Requirement ID Divergence (`C4`, `C5`)**:
    * In `BRD-2026-AMA48-001` (`v0.21.0`), `FR-016` and `FR-017` define exception-stop (`AC-022`) and human-handoff (`AC-023`) rules; `FR-020..FR-022` cover supplier capacity loss, supplier scorecards, and channel-neutral contract data schedules; `FR-029..FR-031` cover defect reopen, defect tracking, and resident handover; `FR-035` covers cohort/building bundling; `FR-047` preserves open remedies/defects/disputes across closure; and `NFR-012` / `FR-052` / `OD-51` / `Required Management Views` govern AI Tokenomics and management oversight.
    * In `PRD-2026-AMA48-001` (`v0.21.0`), `FR-016` defines the versioned provider-package record (`AC-022`) and `FR-017` defines per-measure quality disposition (`AC-023`); `FR-020..FR-024` define the coordinator heatmap, lifecycle funnel, event-based progression history, scenario delivery forecasts, and stakeholder progress views/exports; `FR-030` defines portable AI-independent case/evidence export; `FR-035` defines the versioned constructed-scenario manifest (`AC-043`); `FR-049` preserves open remedies/disputes across closure (`AC-063`); and `FR-061` / `NFR-017` / `OQ-027` govern AI Tokenomics consumption economics.
  * **Epic `#89` Implementation & Test Coverage (`C15`..`C23`)**:
    * Provider packages, committed capacity, work orders, and leaseholder Section 20 consultation let/renew guard (`#90`, `#92`): `src/core/src/zava_forward/core/procurement.py` (`CONSULTATION_STATUSES`, `record_consultation`, `let_package`, `renew_package`, `create_order`, `transition_order`) and `src/api/src/zava_forward/api/app.py` (`/api/provider-packages*`, `/api/work-orders*`, `/api/procurement-summary`), tested by `test_quality_procurement.py`, `test_consultation_controls.py`, `test_procurement_api.py`, and `test_procurement_screens.py`.
    * Per-measure quality acceptance, defect reopen, and handover boundary (`#91`): `src/core/src/zava_forward/core/quality.py` (`checklist_for`, `TRANSITIONS`, per-measure acceptance/rejection/defect states, non-closure on open defects) and `/api/cases/{cid}/quality*`, tested by `test_quality_procurement.py` and `test_technical_quality_screens.py`.
    * Staff-mediated contractor job pack and field evidence capture (`#132`, `ADR-0007`): `src/core/src/zava_forward/core/job_pack.py` (`build_job_pack` closed allowlist excluding resident/vulnerability/health notes, `worker_receipt` `Submitted by worker - awaiting independent review`, non-acceptance receipt boundary) and `/api/work-orders/{oid}/job-pack` + `/api/cases/{cid}/field-evidence*`, tested by `test_job_pack.py`, `test_staff_intake_api.py`, and `test_staff_intake_browser.py`.
    * Aftercare concern route, lived-performance evaluator view, neutral-text guard, and blank `FileStateStore` refusal (`#133`, `#1402`): `src/core/src/zava_forward/core/aftercare.py`, `aftercare_intake.py` (`StateInvalid` fail-closed validation, privacy/PII redaction guard, sensor-context non-dismissal), `aftercare_store.py` (refusing blank existing `FileStateStore` documents), and `/api/aftercare*`, tested by `test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`, `test_aftercare_screen.py`, and `test_aftercare_served.py`.
    * Bounded workspace script-retry exhaustion oracle (`#1384`): `src/api/checks/script_retry.py` (`SCRIPT_RETRY_DELAYS` derived from `web/app.js`, mutation self-tests) and `src/api/tests/test_workspace_scripts.py`.
  * **Epic `#100` Implementation & Test Coverage (`C24`..`C33`)**:
    * Coordinator area/building/archetype heatmap, lifecycle funnel, and drill-down (`#101`): `src/core/src/zava_forward/core/coordinator.py` (staff-only RBAC, current authorized population vs partial event flow, explicit `unknown_history`, `missing_geocode`, `filtered_out` denominators, non-inferred conversion) and `/api/coordinator`, tested by `test_coordinator.py` and `test_coordinator_api.py`.
    * Event-based progression history, declared scenario delivery forecasts, and stakeholder progress/evidence exports (`#102`): `src/core/src/zava_forward/core/progress.py`, `src/core/src/zava_forward/core/insights.py`, `src/core/src/zava_forward/core/list_export.py` (formula-injection neutralization via `safe_cell`, deterministic CSV/JSON packs without AI dependency), and `src/api/src/zava_forward/api/progress.py` (`/api/progress`, `/api/progress/report`, `/api/progress/export`, `/api/cases/{cid}/export`), tested by `test_progress_event_capture.py`, `test_progress_reports.py`, `test_list_export.py`, `test_progress_dashboard.py`, `test_progress_report_api.py`, `test_list_export_api.py`, `test_list_export_inventory.py`, and `test_asset_board_screen.py`.
    * Versioned constructed-scenario manifest and synthetic needs inventory (`#103`): `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` (`v0.2.1`) and `needs-inventory.json` (`v1.3.0`), SHA-256 bound to public fixture/workbench files without reading private datasets, tested by `test_scenario_manifest.py` and `test_needs_inventory.py`.
    * AI Tokenomics consumption economics across management views (`#100`, `#432`, `PR #1792`): `src/core/src/zava_forward/core/tokenomics.py` (`UNPRICED_PROVISIONAL_TARIFF`, `NO_ACCEPTED_OUTCOMES`, `NOT_CONFIGURED_WITH_DEFAULT_ZERO`, per-capability token breakdown, deterministic non-AI fallback parity) wired into `core/progress.py`, `api/progress.py`, and `/api/ai-consumption*`, tested by `test_ai_consumption.py`, `test_ai_consumption_safety.py`, `test_ai_consumption_skill_breakdown.py`, `test_management_tokenomics_invariant_100.py`, `test_ai_consumption_api.py`, and `test_management_tokenomics_api_100.py`.

### Wave 3: Contrarian (Counter-Evidence, SHA Discrepancy, and Ancestry Boundaries)

* Execution mode: Inline contrarian audit against Git object graph, remote GitHub API, and repository guard tests (`C1`, `C34`..`C37`, `W1`, `W2`, `W16`).
* Contrarian findings that refine the plan:
  1. **Prompt SHA Discrepancy (`C1`, `W1`, `W2`)**: The caller prompt stated parent head `7427320280f68fd91f91df37a108892c3e97101f` and `origin/main` SHA `c1ef91e23df56947b6ce1313684b587ff03dc134`. `git cat-file -t` confirms neither 40-char string exists in the repository object database. Actual worktree `HEAD` and live GitHub `PR #1641` (`feat/demo-164-chat-grounding-provenance-0900`) `headRefOid` is `74273202817f9068f9c55cb325b39df7879cba7b` (matching the 9-char prefix `742732028`, tree `545efe335ef470272cd61ac6cde573764186a737`), actual `origin/main` (and live GitHub `branches/main`) SHA is `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, and `git merge-base HEAD origin/main` is `61e1917dd075a8307f0fd436c42cc41f47906846`. Recording fabricated/unresolvable SHAs as verified commits would violate `#440` honesty rules; we must record the verified Git object IDs as authoritative AND explicitly disclose the caller brief's nominal strings (`7427320280f68fd91f91df37a108892c3e97101f` / `c1ef91e23df56947b6ce1313684b587ff03dc134`) as unresolvable dispatch strings.
  2. **Branch Ancestry Split (`C1`, `W16`)**: `HEAD` (`74273202817f9068f9c55cb325b39df7879cba7b`) branches from `origin/main` at merge-base `61e1917dd075a8307f0fd436c42cc41f47906846`. Therefore:
     * All primary child deliveries merged to `main` at or before `61e1917dd075a8307f0fd436c42cc41f47906846` (`#380`, `#384`, `#387`, `#389`, `#390`, `#394`, `#396`, `#528`, `#869`, `#900`, `#911`, `#1076`, `#1080`, `#1090`, `#1150`, `#1169`, `#1390`, `#1392`, `#1400`, `#1425`, `#1432`, `#1441`, `#1456`, `#1458`, `#1527`, `#1564`) PLUS stacked parent-branch commits on `PR #1641` (`#1657` `4dc285ad2`, `#1674` `77c7bfb18`, `#1745` `23b675164`, `#1770` `d8cb35d25`, `#1771` `08c36e4dc`, `#1792` `2fe7ff2e6`) ARE inside `HEAD`'s verified tree.
     * Post-merge-base `origin/main` commit `4629e3e5c` (`PR #1666`, field escalation routing) and sibling-stack `feat/demo-233-same-home-tensions-0825` merges (`PR #1682`, `#1706`, `#1725`, `#1758`) are NOT in `HEAD`'s tree prior to rebasing `PR #1641` onto latest `origin/main`. They must be listed honestly under Exclusions / Post-Merge-Base Sibling Deltas rather than claimed as locally executed in `74273202817f9068f9c55cb325b39df7879cba7b`.
  3. **Guard Compatibility (`C34`..`C36`)**:
     * `src/core/tests/test_live_doc_links.py` checks every relative Markdown link across `docs/` (excluding `docs/reference/log.md` and `docs/capstone/`).
     * `tools/check-legacy-references.py` checks relative links and retired path/package tokens across tracked files.
     * `tools/test_epic_child_disposition_audit.py` scans `docs/architecture/cutover-evidence-pack.md` for `#104`, `#149`, `#165` children (including `#432`, which is `DEFERRED` under `#104`!). Crucial contrarian catch: if our Epic `#100` section mentions `#432`, `test_epic_child_disposition_audit.py` (`test_non_closed_children_carry_an_explicit_residual`) already passes as long as `#432` carries residual language (`deferred`, `open`, `unapproved`, `draft`, `pending`) within 9 lines — which it naturally does because `#432` / `OD-51` / `OQ-027` remains an unapproved tariff/budget governance item! We should also run `python3 -m unittest tools/test_epic_child_disposition_audit.py` during Implement to guarantee zero regression!

## Evidence Log

### Codebase Evidence (`C#`)

| ID  | Path and line anchor | Fact established |
|-----|----------------------|------------------|
| C1  | `.git/HEAD:1` (verified via `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git merge-base HEAD origin/main`) | Worktree `HEAD` is `74273202817f9068f9c55cb325b39df7879cba7b` (tree `545efe335ef470272cd61ac6cde573764186a737`), `origin/main` is `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, and merge-base is `61e1917dd075a8307f0fd436c42cc41f47906846`; prompt strings `7427320280f68fd91f91df37a108892c3e97101f` and `c1ef91e23df56947b6ce1313684b587ff03dc134` do not exist in Git object storage |
| C2  | `docs/case_study_48_original.md:1-15` | `ms.date: 2026-09-10`, blob `0aec2d8070117a647574b1fadc8cfbdd2af68598`, immutable initial case specification |
| C3  | `docs/case_study_48_addendum.md:1-35` | `ms.date: 2026-11-08`, blob `49f9c21b0c6cfda92e10a640596f6ad2b3b5d11a`, executive proposal and exercise research baseline; unsigned for live operations |
| C4  | `docs/brds/agentic-retrofit-programme-brd.md:1-60` | `BRD-2026-AMA48-001`, `version: 0.21.0`, `ms.date: 2026-10-24`, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`, `status: draft` (`business_goal_smart_status: fail`, unsigned, 55 open decisions including `OD-51`) |
| C5  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1-45` | `PRD-2026-AMA48-001`, `version: 0.21.0`, `ms.date: 2026-10-25`, blob `a385d27481f831d21a467259808a125f48226dd8`, `status: in-review` (`author-complete-unsigned-pending-review-and-owner-acceptance`; v0.12.0 exercise-accepted 2026-10-10; v0.21.0 unsigned) |
| C6  | `docs/adrs/0001-azure-architecture.md:1-25` | `ADR-0001`, `ms.date: 2026-10-24`, blob `dd93aaf4c673bfa3bbe74fec781d78d17af2e8ad`, `Proposed` non-production demonstrator target design |
| C7  | `docs/adrs/0002-pilot-readiness-architecture.md:1-30` | `ADR-0002`, `ms.date: 2026-10-24`, blob `96d6db89780976b4f2a2d5528527a8d4658075fe`, `Proposed` overall (bounded Entra staff-access decision accepted 2026-10-24) |
| C8  | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:1-35` | `ADR-0003`, `ms.date: 2026-10-29`, blob `d60645397b20fb70ac3d1dc47c7a6c8671201306`, `Accepted with amendment` on 2026-10-15 for exercise runtime fit only |
| C9  | `docs/adrs/0004-per-user-agent-chat-and-memory.md:1-30` | `ADR-0004`, `ms.date: 2026-10-15`, blob `9406c2e747ced91e5ba7be4072f9482293c0c38f`, `Accepted as written` on 2026-10-15 for staged exercise direction (`OD-44`); live gates (`OD-45..49`) open |
| C10 | `docs/adrs/0005-regulatory-compliance-assistant.md:1-30` | `ADR-0005`, `ms.date: 2026-10-16`, blob `4d610335a5a18bb282e29c6cb3053404beda995d`, `Accepted for synthetic development only` on 2026-10-16 |
| C11 | `docs/adrs/0006-src-layout-and-cutover.md:1-30` | `ADR-0006`, `ms.date: 2026-10-27`, blob `956da1a3b804c803041fe2e8a312bd9f400273ae`, `Accepted` on 2026-10-15 (`src/` package isolation and 2026-10-27 cut-over, archive `v0.21.0`) |
| C12 | `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md:1-40` | `ADR-0007`, `ms.date: 2026-11-11`, blob `541e0f72dd2c1b5ae6feb2439a9223331bcdd783`, `Proposed` overall (2026-11-09 relayed owner direction for staff-mediated synthetic demonstrator intake only; provider portal and `#116` B2B identity unapproved) |
| C13 | `docs/architecture/cutover-evidence-pack.md:2477-2558` | Partial `Epic #89 scoped stabilization checkpoint (2026-11-03)` recorded when `#92`, `#132`, `#133` were open and before `#1384`, `#1402` |
| C14 | `docs/architecture/cutover-evidence-pack.md:8498-8558` | Latest `#440` checkpoint (`2026-11-14`, Refs `#440 #104 #149 #165`); EOF at line 8558 |
| C15 | `src/core/src/zava_forward/core/procurement.py:32-355` | Versioned provider packages, committed capacity tracking, work-order state machine, and `CONSULTATION_STATUSES` leaseholder Section 20 let/renew guard (`#90`, `#92`) |
| C16 | `src/core/src/zava_forward/core/quality.py:1-220` | Per-measure quality checklists, pass/fail/defect states, reopen transitions, and handover gate (`#91`) |
| C17 | `src/core/src/zava_forward/core/job_pack.py:45-120` | Staff-mediated contractor job pack closed allowlist (`build_job_pack`) and non-accepting `worker_receipt` (`Submitted by worker - awaiting independent review`, `#132`) |
| C18 | `src/core/src/zava_forward/core/aftercare.py:1-120` | Digital and non-digital (`phone`, `in_person`, `paper`, `assisted_visit`) aftercare concern register, neutral-text/no-blame/no-savings guard, sensor non-dismissal, and separate handover/financial closure (`#133`) |
| C19 | `src/core/src/zava_forward/core/aftercare_intake.py:245-315` | Fail-closed `StateInvalid` verification, receipt fingerprint integrity, and NFKC/invisible-folded PII guard (`#133`) |
| C20 | `src/core/src/zava_forward/core/aftercare_store.py:1-95` | `FileStateStore` persistence refusing blank existing aftercare state documents (`#1402`) |
| C21 | `src/api/checks/script_retry.py:1-80` | `SCRIPT_RETRY_DELAYS` workspace script-retry exhaustion oracle derived directly from `web/app.js` with mutation verification (`#1384`) |
| C22 | `src/api/src/zava_forward/api/app.py:988-1071` | FastAPI endpoints for provider packages, work orders, job packs, field evidence, quality acceptance, and aftercare with staff RBAC and human-review gates (`#90`, `#91`, `#92`, `#132`, `#133`) |
| C23 | `src/core/src/zava_forward/core/dependencies.py:1-60` | Package dependency rule (`core` depends on stdlib only; `agents` on `core`; `api` on `core` and `agents`) verified by `test_dependency_rule.py` |
| C24 | `src/core/src/zava_forward/core/coordinator.py:1-120` | Read-only coordinator heatmap and lifecycle funnel over `STAFF_ROLES` with explicit `unknown_history`, `missing_geocode`, `filtered_out`, and non-inferred conversion (`#101`) |
| C25 | `src/core/src/zava_forward/core/progress.py:1-120` | Prospective event-based progression history, declared scenario delivery forecasts, and provenance status tags without inferred clocks (`#102`) |
| C26 | `src/core/src/zava_forward/core/insights.py:1-90` | Canonical `STAGE_ORDER`, cohort/tenure/archetype aggregations, and deterministic baseline calculations (`#101`, `#102`) |
| C27 | `src/core/src/zava_forward/core/list_export.py:1-45` | AI-independent, one-way CSV export with formula-injection neutralization (`safe_cell`) and role-scoped visibility (`#102`, `PRD::FR-030`) |
| C28 | `src/api/src/zava_forward/api/progress.py:1-110` | Synthetic-guarded management progress, closed-case archive, stakeholder report, and export views integrating `tokenomics` (`#100`, `#102`) |
| C29 | `src/core/src/zava_forward/core/tokenomics.py:1-140` | AI consumption economics (`UNPRICED_PROVISIONAL_TARIFF`, `NO_ACCEPTED_OUTCOMES`, `NOT_CONFIGURED_WITH_DEFAULT_ZERO`, per-capability breakdown, deterministic fallback parity) (`#100`, `PR #1792`) |
| C30 | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:1-55` | Version `0.2.1` constructed-scenario manifest bound to `needs-inventory.json` (`v1.3.0`) and SHA-256 hashes of public fixture/workbench sources (`#103`) |
| C31 | `docs/reference/README.md:1-120` | Knowledge base index listing `docs/architecture/cutover-evidence-pack.md` and architecture evidence navigation |
| C32 | `docs/reference/log.md:1665-1695` | Append-only knowledge base change log (latest entries dated `2026-11-15`) |
| C33 | `src/core/tests/test_management_tokenomics_invariant_100.py:1-90` | Core invariant tests proving management views report honest provisional AI consumption economics and preserve manual/non-AI parity (`#100`, `PR #1792`) |
| C34 | `src/core/tests/test_live_doc_links.py:1-65` | Live Markdown relative-link resolver across `docs/` (excluding `docs/reference/log.md` and `docs/capstone/`) |
| C35 | `tools/check-legacy-references.py:1-120` | Deterministic `#203` legacy path/package token and changed-doc link checker |
| C36 | `tools/test_epic_child_disposition_audit.py:1-120` | `#440` audit test over `cutover-evidence-pack.md` requiring explicit residual wording near non-closed `#104`/`#149`/`#165` children (including `#432`) |
| C37 | `/usr/bin/python3` & `/home/azureuser/.local/bin/pytest` | Local Python 3.12 runtime resolving `zava_forward.{core,agents,api}` cleanly via `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests` |

### External / Live GitHub Evidence (`W#`)

| ID  | URL and retrieval date | Fact established |
|-----|------------------------|------------------|
| W1  | `https://github.com/jmservera/ama/pull/1641` (retrieved 2026-11-15 via `gh pr view 1641`) | Parent PR `#1641` (`feat/demo-164-chat-grounding-provenance-0900` -> `main`) is `OPEN` at `headRefOid` `74273202817f9068f9c55cb325b39df7879cba7b` |
| W2  | `https://github.com/jmservera/ama/commits/main` (retrieved 2026-11-15 via `gh api repos/jmservera/ama/branches/main`) | Live `main` branch tip is `5e0c7f74432ffce73cfeaa672e4e40a605ca6274` |
| W3  | `https://github.com/jmservera/ama/issues/440` (retrieved 2026-11-15 via `gh issue view 440`) | `#440` (`OPEN`) defines mandatory scoped stabilization checkpoint gates before epic closure |
| W4  | `https://github.com/jmservera/ama/issues/89` (retrieved 2026-11-15 via `gh issue view 89`) | Epic `#89` (`OPEN`) has all feature criteria ticked except the `#440` scoped stabilization checkpoint criterion |
| W5  | `https://github.com/jmservera/ama/issues/100` (retrieved 2026-11-15 via `gh issue view 100`) | Epic `#100` (`OPEN`) has all feature criteria ticked except the `#440` scoped stabilization checkpoint criterion |
| W6  | `https://github.com/jmservera/ama/issues/90` (retrieved 2026-11-15 via `gh issue view 90`) | `#90` `CLOSED` (provider packages, committed capacity, work orders; PR `#384`) |
| W7  | `https://github.com/jmservera/ama/issues/91` (retrieved 2026-11-15 via `gh issue view 91`) | `#91` `CLOSED` (per-measure quality acceptance, defects, handover; PRs `#387`, `#528`) |
| W8  | `https://github.com/jmservera/ama/issues/92` (retrieved 2026-11-15 via `gh issue view 92`) | `#92` `CLOSED` (Section 20 leaseholder consultation check before contract let/renewal; PRs `#389`, `#900`, `#1090`) |
| W9  | `https://github.com/jmservera/ama/issues/132` (retrieved 2026-11-15 via `gh issue view 132`) | `#132` `CLOSED` (staff-mediated contractor job pack and fieldwork evidence capture; PRs `#1080`, `#1150`, `#1425`, `#1432`, `#1441`) |
| W10 | `https://github.com/jmservera/ama/issues/133` (retrieved 2026-11-15 via `gh issue view 133`) | `#133` `CLOSED` (aftercare concern route and lived-performance review; PRs `#869`, `#1076`, `#1400`, `#1456`, `#1527`, `#1564`, plus `#1770` on parent `#1641`) |
| W11 | `https://github.com/jmservera/ama/issues/1384` (retrieved 2026-11-15 via `gh issue view 1384`) | `#1384` `CLOSED` (workspace script-retry exhaustion oracle; PRs `#1390`, `#1392`) |
| W12 | `https://github.com/jmservera/ama/issues/1402` (retrieved 2026-11-15 via `gh issue view 1402`) | `#1402` `CLOSED` (refuse existing blank `FileStateStore` documents in aftercare; PR `#1458`) |
| W13 | `https://github.com/jmservera/ama/issues/101` (retrieved 2026-11-15 via `gh issue view 101`) | `#101` `CLOSED` (coordinator heatmap and lifecycle funnel; PR `#396`) |
| W14 | `https://github.com/jmservera/ama/issues/102` (retrieved 2026-11-15 via `gh issue view 102`) | `#102` `CLOSED` (historical progression, scenario forecasts, stakeholder progress packs; PRs `#390`, `#394`) |
| W15 | `https://github.com/jmservera/ama/issues/103` (retrieved 2026-11-15 via `gh issue view 103`) | `#103` `CLOSED` (constructed-scenario manifest and exercise test data; PR `#380`) |
| W16 | `https://github.com/jmservera/ama/pull/1792` & `pull/1666` (retrieved 2026-11-15 via `gh pr view`) | `PR #1792` (`2fe7ff2e6`) merged into parent `#1641` (`HEAD`); `PR #1666` (`4629e3e5c`) merged to `main` after merge-base `61e1917dd075a8307f0fd436c42cc41f47906846` and sibling PRs `#1682`/`#1706`/`#1725`/`#1758` merged to `feat/demo-233-same-home-tensions-0825` |

## Cycle 1 Synthesis and Convergence

### Selected Recommendation (`convergence` mode)

* Append two clearly structured, dated `2026-11-15` `#440` scoped stabilization checkpoint sections at the end of `docs/architecture/cutover-evidence-pack.md` (preserving all existing sections, including the historical 2026-11-03 partial Epic `#89` checkpoint, and cross-referencing how the 2026-11-15 Epic `#89` checkpoint supersedes its open-child blockers now that `#92`, `#132`, `#133`, `#1384`, and `#1402` are delivered), update `docs/architecture/cutover-evidence-pack.md` `ms.date` to `2026-11-15`, update `docs/reference/README.md` (`ms.date: 2026-11-15` + architecture index description), and append one dated `[2026-11-15]` EOF entry to `docs/reference/log.md` with zero `.copilot-tracking/` references in `docs/`.
* Run the complete focused unit, API, screen/served, browser-retry, dependency-rule, live-doc-link, legacy-reference, and `#440` child-disposition test suites locally during `Implement`, capturing exact commands, exit codes, test counts, and skips before writing the observed verification rows.

### Alternatives Evaluated and Rejected

* **Alternative A (Overwrite the 2026-11-03 Epic `#89` section in place)**: Rejected because the caller prompt explicitly instructs to preserve all existing sections in `docs/architecture/cutover-evidence-pack.md` and append/update cleanly (`C13`, `C14`).
* **Alternative B (Copy caller-stated SHA strings `7427320280f68fd91f91df37a108892c3e97101f` and `c1ef91e23df56947b6ce1313684b587ff03dc134` without git verification)**: Rejected because `git cat-file -t` proves neither exists in Git (`C1`); `#440` requires exact reproducible Git commits, so recording verified SHAs alongside an explicit note on the dispatch prompt's nominal strings is both accurate and auditable.
* **Alternative C (Invoke `tools/rpi-checks.py`)**: Rejected per explicit caller constraint ("Do NOT invoke `tools/rpi-checks.py` (avoid heavy lock contention)").

### Current and Unresolved Governance Decisions / Risks

* BRD (`v0.21.0`, `draft`) and PRD (`v0.21.0`, `in-review`) remain unsigned for live operations (`C4`, `C5`), and `ADR-0001`, `ADR-0002`, and `ADR-0007` remain `Proposed` (`C6`, `C7`, `C12`).
* Post-merge-base `origin/main` commit `4629e3e5c` (`PR #1666`) and sibling-branch PRs (`#1682`, `#1706`, `#1725`, `#1758`) will converge when parent `PR #1641` rebases/merges onto `main` (`C1`, `W16`); this must be stated explicitly in Exclusions.
* Azure live SQL/Container Apps/Entra B2B/IoT deployment and named human legal/DPO/commercial/tariff approvals remain authorized external residuals tracked on `#116`, `#136`, `#144`, `#432`, and `#440` (`continue` recommendation gates epic closure on merge + owner sign-off, without ticking or closing `#89` or `#100` prematurely).

### Research Disposition and Planning Readiness

* Research disposition: `executed`
* Cycle re-entry decision: No Cycle 2 needed; all 6 research questions have direct codebase (`C1`..`C37`) and live GitHub (`W1`..`W16`) evidence with no unresolved investigation gaps.
* Planning Readiness: `Ready`

## Self-Check

* [x] Research brief, parameters, extension registry, participation, direction controls, questions, and prior-knowledge gate are recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order before parent synthesis.
* [x] Every codebase finding has a `C#` ID with `path:line` and every external GitHub finding has a `W#` ID with URL and retrieval date.
* [x] Research remained strictly read-only over repository source and documentation files.
* [x] `Research disposition: executed` and `Planning Readiness: Ready` are explicitly recorded.
