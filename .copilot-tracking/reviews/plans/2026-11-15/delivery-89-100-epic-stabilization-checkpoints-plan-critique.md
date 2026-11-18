<!-- markdownlint-disable-file -->
# RPI Plan Critique: Scoped Stabilization Checkpoints for Epic #89 and Epic #100

## Metadata

* Task ID: delivery-89-100-epic-stabilization-checkpoints-2026-11-15
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Execute `#440` scoped stabilization checkpoints for Epic `#89` (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`) and Epic `#100` (`#101`, `#102`, `#103`) on `feat/epic-89-100-stabilization-checkpoints` under the Focused validation tier (no `tools/rpi-checks.py`), updating `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, and `docs/reference/log.md`, then committing locally after `Outcome: Conformant` review without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-research.md (`C1`..`C37`, `W1`..`W16`), docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md.
* Decisions, dependencies, and acceptance criteria considered: Automatic RPI mode, honest Git SHA reconciliation (`74273202817f9068f9c55cb325b39df7879cba7b` vs nominal prompt strings), ancestry exclusions (`PR #1666` on `origin/main` and sibling `feat/demo-233-same-home-tensions-0825` PRs), document-qualified BRD/PRD/ADR traceability, cross-cutting boundary matrix, exact local test observation, and Markdown/tracking hygiene rules.
* Assessment boundary: Evaluates plan credibility, command accuracy, test coverage completeness against `HEAD`, and sequencing against supplied research evidence without performing open-ended repository discovery.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, P01-T01, P01-T02, C21, C37         | Partial  | `PYTHONPATH` in `P01-T01` omits `src/api`, which is needed when running from the repository root so `from checks.asset_urls import asset_url` in `src/api/checks/script_retry.py` (`C21`) resolves (`PC-001`), and stacked `PR #1641` commits `#1745` and `#1770` (`W10`, `W16`) should explicitly include any dedicated core/agents test modules if present (`PC-003`). |
| FR-1, FR-2, P02, P04-T01, C34..C36       | Partial  | `test_live_doc_links.py` and `python3 tools/check-legacy-references.py` must be recorded in `cutover-evidence-pack.md` (`FR-1`), so `P04-T01` must ensure the recorded rows match the final post-edit execution with zero unverified post-run edits (`PC-002`). |
| FR-2, P02-T01, P02-T02, C1..C12, W1..W16 | Covered  | Provenance covers verified Git commit/tree SHAs, prompt nominal SHA disclosure, covered PRs/issues, ancestry exclusions, and Case Study / BRD / PRD / ADR versions, dates, blob SHAs, and draft/unsigned statuses. |
| FR-3, P02-T01, P02-T02, C4, C5, C15..C33 | Covered  | Traceability joins `BRD::`, `PRD::`, and `ADR-` IDs, flags `FR-*` numbering divergence, and verifies all six required cross-cutting boundaries. |
| FR-4, NFR-1, NFR-2, P03-T01, C31, C32    | Covered  | Preserves prior sections, updates `docs/reference/README.md` and EOF of `docs/reference/log.md`, enforces Markdown/tracking isolation, and preserves `#432` open/deferred residual wording for `tools/test_epic_child_disposition_audit.py` (`C36`). |

## Verdict

* Verdict: Revise
* Rationale: The plan's architecture, provenance honesty, traceability structure, and governance boundary coverage are strong and evidence-backed, but three direct planner-owned refinements (`PC-001`..`PC-003`) are needed before `Implement` so root-invoked `src/api` browser/retry tests resolve `checks.*` imports cleanly, post-edit documentation guard outputs match the recorded evidence rows without drift, and stacked `PR #1641` test additions (`#1745`, `#1770`) are explicitly swept into `P01`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Include src/api on PYTHONPATH for root-invoked API check imports

* Related IDs: FR-1, P01, P01-T01, C21, C37
* Evidence: .copilot-tracking/research/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-research.md (`C21`: `src/api/checks/script_retry.py:20` imports `from checks.asset_urls import asset_url`) and .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md (`P01-T01` `PYTHONPATH` string)
* Concern: `P01-T01` invokes `python3 -m unittest src/api/tests/...` from the repository root with `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests`, omitting `src/api` (the parent directory of `checks/`). Tests such as `test_workspace_scripts.py` and `test_staff_intake_browser.py` that import `checks.*` rely on `src/api` being on `sys.path`.
* Impact: Without `src/api` on `PYTHONPATH`, root-invoked `unittest` fails collection with `ModuleNotFoundError: No module named 'checks'`, causing avoidable runner failure or forcing ad-hoc command drift during `Implement`.
* Smallest useful change: Add `src/api` to `PYTHONPATH` (`PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/api:src/core/tests:src/agents/tests:src/api/tests`) in `Dependencies` and `P01` (`P01-T01`, `P01-T02`, `P04-T01`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `PYTHONPATH` in plan `Dependencies` and phase-details `P01`/`P01-T01`/`P01-T02`/`P04-T01` includes `src/api`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Lock two-step baseline and post-edit verification for doc guard rows

* Related IDs: FR-1, NFR-1, P01-T02, P02, P04-T01, C34, C35, C36
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md (`P02` vs `P04-T01`) and caller prompt Objective item 3 (`plus test_live_doc_links.py and python3 tools/check-legacy-references.py`)
* Concern: Caller Objective item 3 requires recording exact commands, exit codes, test counts, and skips for `test_live_doc_links.py` and `python3 tools/check-legacy-references.py` inside `docs/architecture/cutover-evidence-pack.md`, which is authored in `P02` before `P04-T01` runs post-edit verification.
* Impact: Recording doc-guard rows in `P02` without running them first risks count mismatch, while editing `cutover-evidence-pack.md` again in `P04-T01` without a final re-run would leave unverified edits.
* Smallest useful change: Specify in `P01-T02` and `P04-T01` that `test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, and `python3 tools/check-legacy-references.py` run in `P01-T02` to confirm deterministic test counts/commands and re-run in `P04-T01` on the finalized `docs/` tree with zero subsequent edits to `docs/`.
* Action owner: planning_parent
* Exact resolving evidence: `P01-T02` and `P04-T01` explicitly pair baseline execution and final zero-subsequent-edit post-doc verification for `test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, and `python3 tools/check-legacy-references.py`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Explicitly include stacked PR #1641 test modules for #133/#1745/#100 where present

* Related IDs: FR-1, P01-T01, P01-T02, C18, C29, W10, W16
* Evidence: .copilot-tracking/research/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-research.md (`W10`, `W16`: stacked commits `23b675164` `#1745`, `d8cb35d25` `#1770`, `4dc285ad2` `#1657`, `77c7bfb18` `#1674`, `08c36e4dc` `#1771`, `2fe7ff2e6` `#1792` in `HEAD`)
* Concern: While `P01-T01` and `P01-T02` list the primary `test_aftercare*.py`, `test_quality_procurement.py`, and `test_management_tokenomics_*_100.py` files, those recent stacked commits on `PR #1641` may also have added focused companion test modules in `src/core/tests/`, `src/agents/tests/`, or `src/api/tests/` (for example neutral-text or quality-AI grounding tests).
* Impact: Omitting a companion test file introduced by `#1745` or `#1770` would under-report local verification of stacked `HEAD` commits claimed in Provenance.
* Smallest useful change: Note in `P01-T01` and `P01-T02` to include any companion test files introduced by stacked commits `23b675164` (`#1745`), `d8cb35d25` (`#1770`), `4dc285ad2` (`#1657`), and `77c7bfb18` (`#1674`) present at `HEAD` (`git show --stat --name-only`).
* Action owner: planning_parent
* Exact resolving evidence: `P01-T01` and `P01-T02` explicitly cover companion test modules touched by stacked `HEAD` commits `#1745`, `#1770`, `#1657`, and `#1674`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong provenance integrity: The plan refuses to copy unresolvable 40-character SHA strings from the prompt (`C1`), binding verification to actual Git objects (`74273202817f9068f9c55cb325b39df7879cba7b` and `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`) while disclosing the nominal prompt strings and exact merge-base ancestry boundaries (`PR #1666` and sibling `feat/demo-233-*` PRs).
* Explicit BRD vs PRD requirement-ID disambiguation (`C4`, `C5`) and `#432` audit-guard preservation (`C36`) eliminate silent cross-document contradictions and regression risk.
* Residual risk (explicitly accepted): Browser tests in `src/api/tests/` depend on local Playwright Chromium binary presence; the plan already requires honest classification of any prerequisite-driven skip rather than masking or invoking `tools/rpi-checks.py`.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique did not execute tests or inspect files outside the supplied research, plan, and phase-details boundary.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply `PC-001`, `PC-002`, and `PC-003` directly to `.copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md`, record dispositions in `## Critique Disposition`, mark `Planning status: Ready`, and continue automatically to `rpi-implement`.
* User response required: no
