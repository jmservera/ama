<!-- markdownlint-disable-file -->

# Task Research: governance-126-rai-prd-separation

| Field              | Value                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                              |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                                 |
| Status             | Complete                                                                                |
| Artifact path      | .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md     |

## Research Brief

* What to research: How to prove the three remaining engineering and documentation acceptance contracts on Issue #126 (RAI closure and PRD separation slice) across `src/core/src/zava_forward/core/governance.py`, `src/core/tests/test_governance.py`, and canonical documentation (`docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`) so the 2026-10-31 `PC-002` closure-audit rejections are completely resolved without claiming live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off.
* Why it matters: Issue #126 requires machine-verifiable separation of current PRD quality review and Product Owner acceptance from historical RAI baseline report acceptance (`baseline-assessment-and-remediation-planning only`) and constructed remediation claim completion (`dispositions_complete`), explicit runtime fields keeping live use blocked, affected dispatch disabled, and conditional EU assurance gated on qualified applicability review, plus synchronized repository documentation/index/log updates enforced by deterministic unit tests.
* Audience or intended use: Planning (`rpi-plan`), implementation (`rpi-implement`), independent exact-head review (`rpi-review`), and the delivery coordinator reviewing the frozen local commit on `feat/governance-126-rai-prd-separation` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Scope: `src/core/src/zava_forward/core/governance.py`, `src/core/tests/test_governance.py`, `src/core/README.md`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/reference/README.md`, `docs/reference/log.md`, and read-only compatibility verification against `src/api/tests/test_governance_evidence_api.py` and `src/core/tests/test_live_doc_links.py`.
* Non-goals: Claiming live pilot release, real OD-36 DPIA/lawful-basis sign-off, human Product Owner PRD sign-off, budget-owner confirmation, qualified EU AI Act applicability advice, web UI changes, new API endpoints or storage tables, modifying `docs/case_study_48_original.md`, `docs/reference/memory.md`, or the immutable 2026-10-14 RAI baseline report, or pushing/opening a PR.
* Criteria: Every contract in the caller prompt maps to exact production/test/documentation locations (`path:line`), preserves existing JSON and SQLite governance behavior, honors `src/core/pyproject.toml` formatting/typing configurations and container-image test skip guards, and prohibits `.copilot-tracking/` references in `src/` and `docs/`.
* Requested outputs: Primary research artifact selecting one convergent engineering and documentation approach ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q5 covering `PC-002` failure modes, `_rai_view`/`governance_view` separation schema, EU conditional guards, documentation invariants, and validation quirks     |
| Codebase scope                   | `src/core/`, `src/api/tests/test_governance_evidence_api.py`, `docs/case_study_48_*.md`, `docs/prds/`, `docs/adrs/0002-*.md`, `docs/reference/`, `.copilot-tracking/research/2026-10-31/` |
| External scope                   | GitHub repository metadata for `jmservera/ama` Issue #126 via `gh issue view 126`                                                                                  |
| Initial internal candidate areas | `src/core/src/zava_forward/core/governance.py`, `src/core/tests/test_governance.py`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/README.md`, `docs/reference/log.md` |
| Initial external candidate areas | GitHub Issue #126 (`https://github.com/jmservera/ama/issues/126`)                                                                                                  |
| Research posture                 | focused                                                                                                                                                            |
| Posture provenance               | default (bounded internal slice with named source targets and supplied closure-audit failure evidence)                                                             |
| Explicit limits / deadline       | Focused validation tier (`src/core` unit tests + `ruff` + `mypy` + documentation link/anchor checks); local commit only, no push or PR                             |
| Posture-specific completion basis| focused scope and materiality                                                                                                                                      |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Never read private datasets (`ZF_DATA`) or `support/`; never edit `docs/case_study_48_original.md` or `docs/reference/memory.md`; never put `.copilot-tracking/` paths in `src/` or `docs/` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                                    | Scoped authority or output contract                                              | Selected / skipped reason                                                                                   |
|---------------------|---------------------------------------|-------------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches all repository files and tracking inputs        | Enforces case-study/KB rules, Markdown ASCII/list rules, privacy-safe git email, and validation tiers | Selected: governs repository conventions, KB log/index updates, and non-claims of human/legal acceptance    |
| Skill               | `python-foundational` / `rai-standards` | Topic touches Python governance module and RAI baseline metadata       | Optional guidance for Python typing/testing and NIST/EU RAI terminology          | Skipped: existing `governance.py` conventions and recovered baseline report (`C1`, `C4`) already define exact domain rules |
| Skill               | `documentation`                       | Documentation updates across addendum, PRD, ADR, and KB index/log       | Markdown audit/author conventions                                                | Skipped: `.github/copilot-instructions.md` and `test_live_doc_links.py` (`C11`) already enforce exact repo rules |
| Research specialist | `hve-core-all:rpi-researcher`         | Available subagent for independent research lanes                       | Bounded lane artifact under `.copilot-tracking/research/subagents/`              | Skipped (inline): tightly coupled single-slice investigation across 8 known files completed directly in <=5 sweeps |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                                      |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------------------|
| Intake           | Caller prompt specifies exact branch, worktree, artifact date (`2026-11-15`), three acceptance contracts, and test commands; running in non-interactive autopilot mode | No question needed   | Proceed in focused posture with convergence output mode                                              |
| Direction change | No scope widening required; inspected `docs/adrs/0002-pilot-readiness-architecture.md` and `src/core/README.md` within Criterion 3's explicit "Update existing addendum/PRD/ADRs" scope | No question needed   | Include `docs/adrs/0002-pilot-readiness-architecture.md` and `src/core/README.md` alongside the 4 named docs |
| Convergence      | All 5 sub-questions answered with high-confidence codebase and GitHub issue evidence; remaining human/DPIA/PRD approvals are explicit non-goals | No question needed   | Converge on server-enforced read/write separation in `governance.py` plus repository doc-invariant tests |

## Scope and Success Criteria

* Scope: Prove Criteria 1, 2, and 3 on Issue #126 in `governance.py`, `test_governance.py`, `src/core/README.md`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Assumptions:
  * Verified: `src/api/tests/test_governance_evidence_api.py` asserts specific keys and claim payloads rather than closed top-level dict keys on `governance_view` or `_rai_view` (`C3`).
  * Verified: Shared editable install points to `/home/azureuser/source/ama/src/core/src`, so worktree test runs require `PYTHONPATH=src/core/src:src/core/tests` (`C12`).
* Success criteria:
  * Every research question is answered with exact `path:line` or URL + retrieval date evidence.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C1`-`C12`, `W1`).
  * Alternatives are compared with trade-offs and one convergent recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded honestly.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Expose and enforce in `_rai_view` and `governance_view` that `prd_quality_review` and `prd_owner_acceptance` remain separate from `baseline.acceptance_scope` (`baseline-assessment-and-remediation-planning only`) and from `dispositions_complete`, and cannot be satisfied or overwritten by RAI claim appends or report acceptance.
  2. Include `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` alongside `live_use` in `_rai_view`, and verify `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` preserve their unassessed/conditional guard until qualified applicability review.
  3. Update addendum, PRD, ADRs, knowledge index, and append-only log preserving historical versions and negative/insufficient outcomes, and add focused tests in `src/core/tests/test_governance.py` asserting all three contracts (`PC-002`).
* Inferred research questions: How `src/api` consumes `governance_view`, how container-image runs handle `docs/` absence, and how `src/core/pyproject.toml` configures `ruff` and `mypy` on `governance.py` and `test_governance.py`.
* Caller constraints and non-goals: No `.copilot-tracking/` references in `src/` or `docs/`; no claims of live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off; local commit only without push or PR.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                                |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|--------------------------------------------------------------------------------------------------|
| narrow                                                   | Restrict validation to focused tier (`src/core` unit tests, `ruff check .`, `ruff format --check .`, `mypy`, doc link/anchor checks) | User intake         | Keeps execution scoped to `src/core` and Markdown docs while checking coupled `src/api` test safety |
| exclude                                                  | Prohibit `.copilot-tracking/` paths in `src/` and `docs/`, and prohibit pushing or opening a PR          | User intake         | Enforced in documentation edits, unit-test assertions, and final git commit boundary             |
| exclude                                                  | Never claim live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off      | User intake         | Governs status strings in `governance.py` and wording across addendum, PRD, ADR, and KB log      |

## Research Questions

|  # | Sub-question                                                                                                                                         | Type            | Priority | Status   |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Why did the 2026-10-31 closure audit (`PC-002`) reject Issue #126 criteria 11 and 12, and what remained unproven on criterion 13?                    | straightforward | H        | answered |
| Q2 | How do `_rai_view`, `_rai_claim`, `rai_evidence_record`, and `governance_view` currently project and guard RAI baseline, claim, and governance state? | depth           | H        | answered |
| Q3 | How are `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` represented in `governance.py` and the 2026-10-14 RAI baseline report?                          | straightforward | H        | answered |
| Q4 | Which sections of the addendum, PRD, ADR 0002, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` hold #126 evidence and historical negative outcomes? | breadth         | H        | answered |
| Q5 | What build, lint, format, typecheck, `PYTHONPATH`, and container-image constraints govern `governance.py` and `test_governance.py`?                  | depth           | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `.copilot-tracking/research/2026-10-31/closure-audit-batch1-decisions.json` and `.copilot-tracking/research/2026-10-31/subagents/closure-audit-a.json`
  * `.copilot-tracking/reviews/2026-10-18/issue-126-rai-evidence-register-review.md`
  * `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/log.md`
* Reused (verified) findings:
  * Verified against current `HEAD` (`59dff61d82087defa72a3d76dc73e5d629352961`) that `governance.py` implements the 22-row baseline inventory (`RAI_RESIDUALS` + `RAI_UNASSESSED`), `RAI_BASELINE = "1cb398c7b90bec05a5700008a97d0cfac494144a"`, closed `RAI_CLAIM_FIELDS`, and detached read snapshots (`C2`).
* Superseded / stale:
  * The 2026-10-18 review relied on historical documentary inspection for PRD acceptance separation and documentation preservation rather than merged runtime fields and deterministic repository assertions, which caused the 2026-10-31 `PC-002` rejections (`C1`). Also, the PRD has since advanced from `0.17.0` (on 2026-10-18) to `0.21.0` (`Unsigned candidate`, 2026-10-27) (`C6`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier; no `.copilot-tracking/` references in `src/` or `docs/`; no live/approval overclaims; no push/PR.
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: None blocking; local git, `gh`, `python3`, `ruff`, and `mypy` are all available.

#### Wave 1: Wider

* Plan and independent lanes: Inline sweep of live GitHub Issue #126 (`W1`), 2026-10-31 closure audit artifacts (`C1`), mandatory repository context (`docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/log.md`), `governance.py`, `test_governance.py`, and API callers.
* Worker evidence relationships or inline fallback: Inline fallback (`<=5` direct read/search sweeps across tightly coupled governance and documentation files): Q1 -> `W1`, `C1`; Q2 -> `C2`, `C3`; Q4 -> `C5`, `C6`, `C7`, `C8`, `C9`.
* Reflection: Identified exact `PC-002` gaps: (1) neither `_rai_view` nor `governance_view` exposes `prd_quality_review` or `prd_owner_acceptance` as enforced runtime fields separate from `baseline.acceptance_scope` and `dispositions_complete`; (2) `_rai_view` has `live_use` and `RAI_EU_CONDITIONAL`, but `RAI_EU_CONDITIONAL` is unused at runtime and `_rai_view` lacks `affected_dispatch` and `conditional_eu_assurance`; (3) `test_governance.py` has zero assertions verifying documentation, ADR, index, or log invariants.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect exact line-by-line contracts in `governance.py` (`C2`), `rai-report-ama-20261014.md` (`C4`), `docs/case_study_48_addendum.md` (`C5`), `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`C6`), `docs/adrs/0002-pilot-readiness-architecture.md` (`C7`), `src/core/README.md` (`C8`), and `docs/reference/README.md` / `docs/reference/log.md` (`C9`).
* Plan and independent lanes: Inline deep read of all target sections, schema validators (`_rai_claim`, `_rai_assessment`, `_rai_view`, `governance_view`), and test suites (`test_governance.py`, `test_governance_evidence_api.py`).
* Worker evidence relationships or inline fallback: Inline: Q2/Q3 -> `C2`, `C3`, `C4`; Q4 -> `C5`-`C9`. Confirmed `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` is defined at `governance.py:67` as part of `RAI_UNASSESSED` (`NOT_ASSESSED`, `UNCHANGED`), and `_rai_claim` enforces strict key equality (`body.keys() != RAI_CLAIM_FIELDS`), rejecting any extra keys such as `prd_quality_review` or `prd_owner_acceptance`.
* Reflection: Designing `prd_quality_review` and `prd_owner_acceptance` as detached, immutable server-computed dictionaries on both `_rai_view` and `governance_view` (ignoring any injected keys in raw `governance` storage and remaining unchanged across all claim appends, `dispositions_complete == True`, protocol/benefits approvals, and release records) cleanly proves Criterion 1. Adding `affected_dispatch` and `conditional_eu_assurance` on `_rai_view` plus per-finding `conditional_eu` and `applicability_review` guards on `EU-COND-01/02/04` proves Criterion 2.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether adding keys to `_rai_view`, `findings` rows, or `governance_view` breaks `src/api` tests; whether repo-doc tests inside `src/core/tests/test_governance.py` break container-image test runs where `docs/` is absent; whether `ruff format` or `mypy` behaves unexpectedly on `governance.py`; and whether `python3` imports the wrong worktree.
* Plan and independent lanes: Inline contrarian inspection of `src/api/tests/test_governance_evidence_api.py`, `src/core/tests/test_live_doc_links.py`, `src/core/pyproject.toml`, and `python3 -c "import zava_forward.core.governance"`.
* Worker evidence relationships or inline fallback: Inline contrarian findings:
  1. `test_governance_evidence_api.py` (`C3`) asserts `view["rai_evidence"]["findings"][2]["claims"] == [record]` (stored claim dict, not finding wrapper) and accesses top-level keys selectively; adding keys to `_rai_view`, `findings` rows, and `governance_view` breaks zero API assertions.
  2. `test_live_doc_links.py:52-55` (`C11`) reveals that the hardened Docker image (`docker build -f src/api/Dockerfile src`) omits `docs/` and guards doc tests with `if not (ROOT / "docs").is_dir(): self.skipTest("repository docs are not in this image")`. Without that exact guard, running `test_governance.py` inside the container image would raise `FileNotFoundError`, whereas in a repository checkout `ROOT / "docs"` always exists so the test never skips in repo/CI runs!
  3. `src/core/pyproject.toml:30-66` (`C10`) excludes `src/zava_forward/core/governance.py` and `tests/test_governance.py` from `[tool.ruff.format]` and ignores mypy errors in `[[tool.mypy.overrides]]`. Running `ruff format <explicit-file>` would reformat untouched legacy lines and pollute the diff; running directory-mode `ruff check .`, `ruff format --check .`, and `python3 -m mypy` inside `src/core` preserves untouched lines cleanly.
  4. `python3 -c "import zava_forward.core.governance"` without `PYTHONPATH` resolves to `/home/azureuser/source/ama/src/core/src/...` (`C12`) in this shared host environment! Must run unit tests with `PYTHONPATH=src/core/src:src/core/tests` (and never run global `pip install -e` that would clobber shared worktrees).
* Reflection: All four contrarian hazards were caught before planning and converted into explicit engineering safeguards. No material uncertainty remains.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|--------------------|--------------------------|----------------------------|
| Expose immutable `prd_quality_review` and `prd_owner_acceptance` separation records in both `_rai_view` and `governance_view`, immune to stored-dict tampering, RAI claim appends (`dispositions_complete`), and governance approvals | `C1`, `C2`, `C5`, `C6` | accepted | Directly proves Issue #126 Criterion 1 and resolves `PC-002` index 11 rejection | Selected Recommendation (Contract 1) |
| Expose exact `affected_dispatch` and `conditional_eu_assurance` fields in `_rai_view` and bind `RAI_EU_CONDITIONAL` (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) to per-finding unassessed/conditional applicability guards | `C2`, `C3`, `C4`, `W1` | accepted | Directly proves Issue #126 Criterion 2 without breaking API consumers | Selected Recommendation (Contract 2) |
| Update `addendum`, `PRD`, `ADR 0002`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`, and add container-safe repository doc/link/anchor invariant tests in `test_governance.py` | `C1`, `C5`-`C9`, `C11` | accepted | Resolves `PC-002` index 12 rejection across all named document surfaces while keeping container test compatibility | Selected Recommendation (Contract 3) |
| Mutate `PRD` frontmatter `version` or mark PRD quality review / RAI findings accepted | `C4`, `C5`, `C6` | rejected | Violates non-goals and falsifies current `Unsigned candidate` (`0.21.0`) and `Open` / `Unknown` state | Recorded as explicit boundary |
| Run `pip install -e` in shared user site-packages or run `ruff format` on explicit excluded file paths | `C10`, `C12` | rejected | Would mutate shared multi-worktree environment or reformat untouched excluded lines | Recorded as validation safeguard |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope saturated; every acceptance criterion, closure-audit rejection, caller compatibility surface, and tooling constraint is verified from primary repository files.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`-`C12`, `W1`)

## Evidence Log

* Delegation: inline: bounded 8-file internal slice with tightly coupled contracts investigated directly in fewer than 5 search/read sweeps.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | 2026-10-31 closure audit rejected #126 criterion 11 (`PC-002: historical documentary Review is not a merged assertion preserving current PRD acceptance independently`) and criterion 12 (`PC-002: claim inventory tests do not assert all document/index/log updates and retained adverse outcomes`), leaving criterion 13 also open | `.copilot-tracking/research/2026-10-31/closure-audit-batch1-decisions.json:71-106` | view | high | Confirmed against `subagents/closure-audit-a.json:198-262` |
| C2  | `governance.py` defines `RAI_BASELINE`, `RAI_RESIDUALS` (11), `RAI_UNASSESSED` (11), unused `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, strict closed `_rai_claim` (`RAI_CLAIM_FIELDS`), `_rai_view` (missing `prd_quality_review`, `prd_owner_acceptance`, `affected_dispatch`, `conditional_eu_assurance`), and `governance_view` (missing top-level `prd_quality_review`, `prd_owner_acceptance`) | `src/core/src/zava_forward/core/governance.py:53-272` | view | high | `governance_view` is at `governance.py:965-983` |
| C3  | `src/api/tests/test_governance_evidence_api.py` checks `view["rai_evidence"]["findings"][2]["claims"] == [record]` and selective keys rather than closed dict equality on `_rai_view`, `findings` rows, or `governance_view` | `src/api/tests/test_governance_evidence_api.py:130-185` | view | high | Adding new keys to `_rai_view`, `findings` rows, and `governance_view` is backward-compatible with `src/api` |
| C4  | Recovered 2026-10-14 RAI baseline report records owner acceptance on 2026-10-15 for bounded baseline report and remediation planning only (`0.14.0` at `1cb398c7b90bec05a5700008a97d0cfac494144a`), 9 `DOWNGRADED` and 2 `CONFIRMED` `PARTIAL` residuals, 11 `NOT_ASSESSED` (`UNCHANGED`) checks including conditional EU screening (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`), and `All live use remains BLOCKED` | `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md:1-68` | grep / view | high | Immutable historical audit snapshot |
| C5  | `docs/case_study_48_addendum.md` records pre-merge resident draft `0.2.0` quality failure (`FAIL`, Validate `BLOCKED`, Finalize `NOT_EVALUATED`; `1.70 / 3.0`, not yet re-run on `0.21.0`), 2026-10-14 RAI baseline (`INVALID_PAYLOAD` reconciliation, 22 open checks), 2026-10-15 planning-only owner acceptance, and 2026-10-18 constructed RAI evidence register engineering | `docs/case_study_48_addendum.md:48-55` | view | high | RAI sections at `docs/case_study_48_addendum.md:977-1135` |
| C6  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`version: "0.21.0"`, `Unsigned candidate`) preserves `v0.12.0`, `v0.14.0`, `v0.16.0`, `v0.17.0`..`v0.21.0` history, constructed finding-evidence engineering (`L1740-1778`), and unsigned Product Owner handoff table (`L2957-2984`) | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1740-1778` | view | high | Sign-off and version history at `L2957-3105` |
| C7  | `docs/adrs/0002-pilot-readiness-architecture.md` documents `Finding-Evidence Register Engineering (2026-10-18, #126)` under the Responsible AI Audit Outcome and Live Release Gate section | `docs/adrs/0002-pilot-readiness-architecture.md:326-388` | view | high | ADR surface referenced by Criterion 3 ("Update existing addendum/PRD/ADRs") |
| C8  | `src/core/README.md` documents `Constructed RAI evidence claims (2026-10-18, #126)` and links to `src/api/README.md#constructed-rai-evidence-register-api-126` | `src/core/README.md:4610-4658` | view | high | Component guide for `zava_forward.core.governance` |
| C9  | `docs/reference/README.md` (`L697-706`, `L943`, `L1021-1035`) indexes the RAI baseline report, PRD, ADR 0002, and #126 register status; `docs/reference/log.md` is append-only (`L1810-1834`) | `docs/reference/README.md:697-706` | view | high | Append new `[2026-11-15]` entry at EOF of `docs/reference/log.md` without editing prior bytes |
| C10 | `src/core/pyproject.toml` places `src/zava_forward/core/governance.py` and `tests/test_governance.py` in `[tool.ruff.format] exclude`, `[tool.ruff.lint.per-file-ignores]`, and `[[tool.mypy.overrides]] ignore_errors = true` | `src/core/pyproject.toml:30-66` | view | high | Run `ruff check .`, `ruff format --check .`, and `python3 -m mypy` in directory mode inside `src/core` |
| C11 | `src/core/tests/test_live_doc_links.py` validates relative Markdown links across live docs and skips gracefully via `if not (ROOT / "docs").is_dir(): self.skipTest(...)` when executed inside the `src/`-only container image | `src/core/tests/test_live_doc_links.py:21-56` | view | high | Reuse this container-image guard pattern for doc-invariant tests in `test_governance.py`, plus explicit heading-anchor validation |
| C12 | Shared host Python resolves unprefixed `zava_forward.core.governance` to `/home/azureuser/source/ama/src/core/src/zava_forward/core/governance.py`, whereas `PYTHONPATH=src/core/src:src/core/tests` resolves to this worktree | `src/core/tests/test_governance.py:1-20` | bash | high | Always pass worktree `PYTHONPATH` during test runs; do not mutate shared editable installs |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Live GitHub Issue #126 lists 13 acceptance criteria; criteria 1-10 are checked `[x]` and the final 3 criteria (PRD quality review & owner acceptance separation; update addendum/PRD/ADRs & KB index/log preserving historical versions & negative/insufficient outcomes; live use blocked, affected dispatch disabled, conditional EU assurance after qualified applicability review) remain unchecked `[ ]` | GitHub Issue #126: Frozen protocol, benefits register and phase release gates | https://github.com/jmservera/ama/issues/126 | 2026-11-15 | OPEN (retrieved 2026-11-15) | high |

### Contradictions / Conflicts

* PRD version advancement since 2026-10-18: `.copilot-tracking/reviews/2026-10-18/issue-126-rai-evidence-register-review.md` refers to PRD `v0.17.0`, whereas `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`C6`) and `docs/case_study_48_addendum.md` (`C5`) are now at consolidated `v0.21.0` (`Unsigned candidate`, 2026-10-27); resolved by primary-source currentness -> preserve historical `0.12.0`, `0.14.0`, `0.16.0`, `0.17.0`..`0.20.0` references while accurately describing current `0.21.0` as an unsigned candidate without fresh full-PRD quality review or owner acceptance.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Closure audit `PC-002` requires merged runtime assertions proving current PRD quality review and owner acceptance remain separate from RAI report acceptance and remediation completion, plus deterministic tests asserting all doc/index/log updates and retained negative/insufficient outcomes; criterion 13 also needs explicit `affected_dispatch`, `conditional_eu_assurance`, and `EU-COND-01/02/04` guards. | `C1`, `W1` | high | Defines exact test and code scope for all 3 contracts |
| Q2 | `_rai_claim` already enforces a closed 11-field schema (`RAI_CLAIM_FIELDS`), rejecting PRD/acceptance override fields on write; adding detached immutable `prd_quality_review` and `prd_owner_acceptance` structures to both `_rai_view` and `governance_view` (computed purely from constants, never reading tampered `governance` keys or flipping when `dispositions_complete` is `True` or protocol/release actions run) enforces read/write separation end-to-end. | `C2`, `C3` | high | Ready for surgical implementation in `governance.py` |
| Q3 | `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` is already declared in `governance.py:67` within `RAI_UNASSESSED`. Exposing `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` on `_rai_view` and attaching `conditional_eu` + `applicability_review` guards to each finding row preserves their unassessed/conditional status across all claim tiers. | `C2`, `C4` | high | Ready for surgical implementation in `governance.py` |
| Q4 | All 6 documentation surfaces (`docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, `docs/reference/log.md`) already have dedicated `#126` subsections where concise `2026-11-15` updates can be integrated without rewriting historical entries or prior log bytes. | `C5`, `C6`, `C7`, `C8`, `C9` | high | Preserves historical versions (`0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`) and negative/insufficient outcomes |
| Q5 | Run tests with `PYTHONPATH=src/core/src:src/core/tests`, run `ruff check .`, `ruff format --check .`, and `python3 -m mypy` in directory mode inside `src/core`, and guard repository doc tests in `test_governance.py` with `if not (ROOT / "docs").is_dir(): self.skipTest("repository docs are not in this image")`. | `C10`, `C11`, `C12` | high | Prevents shared-worktree clobbering, excluded-file diff noise, and container test failures |

## Key Discoveries

* `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` already exists in `src/core/src/zava_forward/core/governance.py:67` (`C2`) but was never surfaced in `_rai_view` or finding rows; wiring it into `_rai_view` and per-finding rows directly grounds the conditional EU applicability guard in existing module constants.
* Shared host site-packages resolve `zava_forward.core` to `/home/azureuser/source/ama/src/core/src` (`C12`); explicit `PYTHONPATH=src/core/src:src/core/tests` is mandatory so tests validate this worktree without mutating shared editable installs.
* `src/core/tests/test_live_doc_links.py` (`C11`) establishes the exact container-compatible pattern (`if not (ROOT / "docs").is_dir(): self.skipTest(...)`) needed when `src/core/tests/test_governance.py` asserts repository documentation, index, and append-only log invariants.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach:
  1. In `src/core/src/zava_forward/core/governance.py`, define explicit immutable separation records (`PRD_QUALITY_REVIEW_STATE` and `PRD_OWNER_ACCEPTANCE_STATE`) and expose fresh `deepcopy` projections as `prd_quality_review` and `prd_owner_acceptance` in both `_rai_view` and `governance_view`, explicitly distinguishing them from `baseline["acceptance_scope"]` (`"baseline-assessment-and-remediation-planning only"`) and `dispositions_complete`, ignoring any tampered keys in raw `governance` storage, and rejecting any attempt to pass PRD review/acceptance fields into `rai_evidence_record`.
  2. In `_rai_view`, add `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` alongside `live_use`, and enrich finding rows with `conditional_eu` (`fid in RAI_EU_CONDITIONAL`) and `applicability_review` (`"Required before conditional EU assurance applies"` for `EU-COND-01`, `EU-COND-02`, `EU-COND-04`, else `"Not conditional EU check"`), keeping `baseline_status == "NOT_ASSESSED"`, `baseline_verdict == "UNCHANGED"`, `closure == "Open"`, and `acceptance == "Unknown"` invariant even after `independent-acceptance` claim appends.
  3. Update `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and append a `[2026-11-15]` entry to `docs/reference/log.md`, preserving historical versions and negative/insufficient outcomes without `.copilot-tracking/` references.
  4. Add focused unit tests in `src/core/tests/test_governance.py` covering JSON and SQLite stores for Contracts 1 and 2, plus deterministic repository documentation/ADR/index/log and relative Markdown link/anchor invariant tests for Contract 3 (`PC-002`).
* Rationale: Directly satisfies every clause of the three prompt contracts, closes both `PC-002` closure-audit rejections (`C1`), preserves backward compatibility with `src/api` (`C3`) and stripped container images (`C11`), and introduces zero new tables, endpoints, or unapproved authority claims.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `W1`
* Implementation impact: 1 production Python file (`governance.py`), 1 unit test file (`test_governance.py`), and 6 Markdown documentation/KB files.
* Confidence: high: all code paths, callers, doc targets, and lint/typecheck rules are directly verified in the worktree.

File tree:

```text
src/core/
  README.md                                              (update #126 contract fields)
  src/zava_forward/core/governance.py                    (expose/enforce PRD separation, affected_dispatch, conditional_eu_assurance, EU-COND guards)
  tests/test_governance.py                               (add Contract 1, 2, and 3 unit + doc/index/log invariant tests)
docs/
  case_study_48_addendum.md                              (update ms.date + 2026-11-15 #126 governance separation & EU guard note)
  adrs/0002-pilot-readiness-architecture.md              (extend #126 Finding-Evidence Register Engineering subsection)
  prds/zava-forward-retrofit-programme-demonstrator.md   (extend #126 Constructed Finding-Evidence Engineering subsection, keep v0.21.0 unsigned)
  reference/README.md                                    (update ms.date + #126 index summary)
  reference/log.md                                       (append [2026-11-15] update entry at EOF)
```

### Alternative: Mutable Stored Governance Fields for PRD Quality Review and Owner Acceptance

* Approach: Store `prd_quality_review` and `prd_owner_acceptance` inside `_governance_defaults(g)` as mutable dictionary entries persisted in `zavaforward.json` / SQL `documents` with new mutation methods.
* Trade-offs: Would allow state transitions inside the demonstrator database, but creates an unrequested mutation surface that could falsify human PRD sign-off or mutate source data on read.
* Evidence refs: `C2`, `C5`, `C6`
* Rejection rationale: Rejected because PRD quality review and Product Owner sign-off occur on the canonical repository PRD artifact through human governance, not via unverified demonstrator API writes, and mutating defaults would risk violating `_rai_view` / `governance_view` read-only snapshot semantics (`C2`) and the prompt's explicit prohibition against claiming owner sign-off.

### Alternative: Plain String Fields Only vs Structured Separation Dicts for `prd_quality_review` and `prd_owner_acceptance`

* Approach: Expose `prd_quality_review` and `prd_owner_acceptance` only as opaque strings without boolean flags (`accepted`/`satisfied`, `separate_from_report_acceptance`, `separate_from_remediation_completion`).
* Trade-offs: Slightly shorter code, but relies purely on prose substring matching rather than explicit boolean structural invariants alongside descriptive status strings.
* Evidence refs: `C1`, `C2`
* Rejection rationale: Rejected in favor of small immutable dicts containing clear `status` strings plus `accepted: False`, `separate_from_report_acceptance: True`, `separate_from_remediation_completion: True`, and `report_acceptance_scope: "baseline-assessment-and-remediation-planning only"`, while keeping `affected_dispatch` and `conditional_eu_assurance` to the exact literal strings specified in Criterion 2.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure no `.copilot-tracking/` string appears anywhere in modified `src/` or `docs/` files, and ensure `docs/reference/log.md` preserves every existing byte prior to the appended `## [2026-11-15]` entry.
* Follow-up: Fresh independent `prd-quality-reviewer` assessment on consolidated PRD `v0.21.0`, human Product Owner sign-off, OD-36 DPIA/lawful-basis approval, and qualified human/legal RAI acceptance remain separate downstream human governance gates.
* Residual uncertainty: none within this bounded engineering and documentation slice.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Expose detached immutable `prd_quality_review` and `prd_owner_acceptance` dicts in both `_rai_view` and `governance_view` | confirmed | evidence / user prompt | Enforces machine-checkable separation from `baseline.acceptance_scope` and `dispositions_complete` across JSON and SQLite stores and ignores raw storage tampering | `C1`, `C2`, `C5`, `C6` | Implemented in `governance.py` and tested in `test_governance.py` |
| Expose exact `affected_dispatch` and `conditional_eu_assurance` string constants in `_rai_view` and wire `RAI_EU_CONDITIONAL` per-finding guards | confirmed | user prompt / evidence | Matches exact prompt strings and binds `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` to conditional applicability review | `C2`, `C4`, `W1` | Implemented in `governance.py` and tested across all claim tiers |
| Update all 6 related doc/ADR/guide/KB files and verify invariants + relative links/anchors in `test_governance.py` with container `docs/` guard | confirmed | user prompt / repo instructions | Literal satisfaction of "addendum/PRD/ADRs and knowledge index/append-only log" plus `PC-002` closure and Docker image compatibility | `C1`, `C5`-`C9`, `C11` | Complete documentation traceability and regression protection |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Human Product Owner acceptance and fresh `prd-quality-reviewer` run on consolidated PRD `v0.21.0` | Independent full-PRD quality review pass, closure of `OD-35`..`OD-55`, and human owner sign-off | Product Owner (human) | Required before claiming an accepted PRD baseline; explicitly out of scope for #126 engineering slice | follow-up |
| Qualified human/legal RAI acceptance, EU AI Act applicability determination, and OD-36 DPIA sign-off | Named human legal/DPO/safety approvals and deployed operational evidence | Programme Manager / DPO-Legal / Safety Leads | Required before unblocking live use or enabling affected dispatch; explicitly out of scope here | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Audit remaining human-only governance sign-off gates across consolidated PRD `v0.21.0` (`OD-35`..`OD-55`) | Prepares human review packet once demonstrator code slices freeze | Owner request for live pilot readiness review | deferred | Q1, Q4; `C5`, `C6`, `W1` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected across `governance.py`, `test_governance.py`, and the 6 documentation/KB files.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `W1`
* Preconditions met: Clean worktree on `feat/governance-126-rai-prd-separation`, all target locations verified with exact line numbers, backward compatibility with `src/api` and container builds confirmed, and tooling commands verified.
* Blockers: none
* Smallest action to change readiness: none (already Ready for `rpi-plan`)

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wave 1 (Wider), Wave 2 (Deeper), and Wave 3 (Contrarian) completed in order                         |
| Lane evidence or inline fallback | Inline fallback: tightly coupled 8-file internal slice investigated directly without subagent overhead        |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C12`, `W1`)                                                                                     |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)                                 |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C12`, `W1`)                                                                                     |
| Output mode and planning support | `convergence`; yes, Planning Readiness is `Ready`                                                            |
| Acting owner                     | Confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness `Ready` (passed); pre-transition state write to `Plan` (passed) |
| Continuation result              | Automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md                          |
| Notes for planning or re-entry   | Preserve directory-mode `ruff`/`mypy` execution in `src/core`, `PYTHONPATH=src/core/src:src/core/tests`, container `docs/` guard, and zero `.copilot-tracking/` strings in `src/` or `docs/` |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All in-scope code, test, and documentation surfaces were inspected directly; further research would be redundant.

## Sources

* W1 - GitHub Issue #126: Frozen protocol, benefits register and phase release gates - https://github.com/jmservera/ama/issues/126 (retrieved 2026-11-15, OPEN)

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
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions, Risks, and Residual Uncertainty, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none (optional Complete Examples and Configuration Examples omitted per template rules).
