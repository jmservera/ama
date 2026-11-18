<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #117 Document Scan Fix (`test_resident_decisions`) and Rebase onto 0358b9ad5

## Metadata

* Task ID: issue-117-doc-scan-fix-rebase-0358b9ad5
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements:
  1. Rebase `feat/demo-117-doc-scan` (`PR #1781`, `5c5370a4a`) onto the latest parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`).
  2. Fix the `src-core` CI failure (`JsonResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates` and `SqlResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates` at `src/core/tests/test_resident_decisions.py:2526`) while keeping all `#117` tests (`test_technical_evidence_usability.py`, `test_document_rescan.py`, `test_resident_documents.py`, `src/api/tests/test_document_controls.py`) passing 100%.
  3. Run focused validation matching `src-ci.yml` in `src/core` and `src/api` (`unittest`, `ruff check src tests`, `ruff format --check src tests`, and `mypy`).
  4. Update `.copilot-tracking/` RPI artifacts for `#117` and commit cleanly with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing, leaving a clean worktree for the coordinator.
* Research and evidence considered:
  * .copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md (`C1`-`C8`)
  * .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md
  * .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md
  * .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-state.json
  * .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md
  * .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md
  * .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json
  * src/core/tests/test_resident_decisions.py
  * src/core/src/zava_forward/core/doc_controls.py
  * src/core/tests/test_technical_evidence_usability.py
  * src/core/tests/dataset.py
  * src/core/pyproject.toml
  * src/api/pyproject.toml
* Decisions, dependencies, and acceptance criteria considered:
  * Confirmed caller and research decisions in .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-state.json: preserve fail-closed `is_available_case_document` for `generated=False` documents missing `scan` metadata, align `test_resident_decisions.py` synthetic `Store.EVIDENCE` pre-state setup with `dataset.py:113-115`, rebase cleanly onto `0358b9ad5`, isolate module imports via worktree `PYTHONPATH`, preserve original parent `#117` `Residual work` (`RV-001`) review outcome, configure privacy-safe noreply git identity, and do not push.
  * Functional and non-functional requirements `FR-FIX-01` through `FR-FIX-03`, `NFR-FIX-01`, `NFR-FIX-02`, and acceptance criteria `AC1` through `AC4`.
* Assessment boundary:
  * Single-pass read-only verification of plan completeness, technical accuracy, security-invariant preservation, `ruff`/`mypy` compatibility, worktree import isolation, and git/tracking hygiene against the supplied workspace artifacts and source files. Live hosted GitHub Actions execution after rebase remains outside local unpushed execution scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / `FR-FIX-01` / `AC1` / `C1`, `C2`, `C7` | Covered | `P01-T01` configures privacy-safe noreply `user.email` before rebasing, keeps tracked files clean prior to rebase, replays `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`) where `doc_controls.py` (`#109`) and `assistants.py` (`#146`) auto-merge without conflict, and verifies `git merge-base --is-ancestor 0358b9ad5 HEAD` plus empty `server.py` diff. |
| Caller Req 2 / `FR-FIX-02` / `AC2` / `C3`, `C4`, `C5`, `C6` | Covered | `P01-T02` updates the sole un-scanned `generated=False` setup comprehension at `src/core/tests/test_resident_decisions.py:2522-2524` to add `scan=dict(status="clean", scanner="Synthetic metadata fixture")` matching `src/core/tests/dataset.py:113-115`. Both `JsonResidentDecisions` and `SqlResidentDecisions` inherit that test method (`src/core/tests/test_resident_decisions.py:4870`), while `is_available_case_document` (`src/core/src/zava_forward/core/doc_controls.py:183-190`) and `src/core/tests/test_technical_evidence_usability.py:29-67` remain untouched and fail-closed. |
| Caller Req 3 / `NFR-FIX-01` / `AC3` / `C8` | Covered | `P02` / `P02-T01` first asserts PEP 420 namespace `__path__[0]` resolution inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`, then runs both exact caller `src-ci.yml` commands (`src/core` and `src/api` `unittest`, `ruff check src tests`, `ruff format --check src tests`, `mypy`) plus full `src/core` `unittest discover -s tests -q`, `ruff check . && ruff format --check .`, `src/api/tests/test_role_endpoint_inventory.py`, and `python3 tools/rename-zava-tests.py`. |
| Caller Req 4 / `FR-FIX-03` / `NFR-FIX-02` / `AC4` | Covered | `P03` / `P03-T01` cleanly separates pre-Review `rpi-implement` reconciliation (6 parent and child artifacts, preserving original parent `#117` `Outcome: Residual work` and `RV-001`) from post-Review parent `RPI Agent` closeout commit (all 10 updated `.copilot-tracking/` files committed locally with noreply email, `Refs #117`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, no `.copilot-tracking/` path mentions in commit messages, no `git push`, and empty `git status --short`). |
| `P01` (`P01-T01`, `P01-T02`) | Covered | Sequencing (`P01-T01` rebase before `P01-T02` test edit and commit), change budget lock (`0` manual production edits, `1` test file), `ruff format` 100-char compliance, and `mypy` (`strict = true`, `disallow_untyped_calls = false` on `test_resident_decisions` in `src/core/pyproject.toml:106-116`) are verified against source. |
| `P02` (`P02-T01`) | Covered | Covers semantic `#117` suites, the fixed `test_resident_decisions` suite, full `src/core` regression discovery across the 6 newly rebased upstream PRs (`#1775`, `#1777`, `#1778`, `#1779`, `#1780`, `#1782`), endpoint inventory, static checks, and rename regression tests without mutating shared `~/.local` packages. |
| `P03` (`P03-T01`) | Covered | Matches the established 10-file child continuation commit pattern (`5c5370a4a`), validates JSON syntax on both state files, enforces `git diff --check`, and guarantees a clean unpushed worktree at closeout. |

## Verdict

* Verdict: Pass
* Rationale: Ready for implementation. Every caller requirement, research finding (`C1`-`C8`), repository governance rule, and static/runtime CI gate is accurately addressed with zero substantive gaps or security regressions. Updating `src/core/tests/test_resident_decisions.py:2522-2524` to carry `scan=dict(status="clean", scanner="Synthetic metadata fixture")` resolves both `JsonResidentDecisions` and `SqlResidentDecisions` failures at their synthetic fixture source while preserving `#117` fail-closed missing-scan quarantine in `src/core/src/zava_forward/core/doc_controls.py:183-190`.

## Findings

* None. Zero actionable `PC-xxx` findings were identified across requirements, research, phases, tasks, acceptance criteria, dependencies, formatting/typing rules, or git/tracking boundaries.

## Strengths and Residual Risk

* Strengths:
  * Preserves `#117` fail-closed security invariants (`is_available_case_document` and `TechnicalEvidenceUsability`) rather than weakening production quarantine checks for synthetic test stubs.
  * Explicitly verifies `src/core/pyproject.toml` lint, format (100-char line length), and `mypy` rules for `tests/test_resident_decisions.py`, avoiding formatting or typing regressions in `src-core` CI.
  * Guards against shared-host `~/.local` editable install shadowing via an explicit `zava_forward.{core,agents,api}.__path__` worktree assertion prior to test execution, and adds full `src/core` `unittest discover -s tests -q` alongside the targeted `#117` suites.
  * Cleanly sequences pre-rebase working-tree cleanliness (untracked child RPI files do not collide with `fa6f8d1dd..0358b9ad5` or `5c5370a4a`), pre-Review tracking reconciliation in `P03-T01`, and post-Review 10-file local tracking commit at parent closeout.
* Residual risk (explicitly accepted within plan boundaries):
  * If `origin/feat/demo-164-chat-grounding-provenance-0900` advances past `0358b9ad5` during `git fetch`, `P01-T01` explicitly verifies the fetched SHA (`0358b9ad5`) and `git merge-base --is-ancestor 0358b9ad5 HEAD` so any unexpected upstream drift is immediately visible rather than silently assumed.
  * Prior parent `#117` non-blocking follow-ups (`RV-001` direct `SqlStore.rescan_pending()` reopen/counter unit test, Azure Storage Defender Bicep wiring, and DPO/Legal retention schedule sign-off) remain tracked outside active `P01`-`P03` scope per caller brief.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* This critique is strictly read-only and did not execute `git rebase` or mutate source, test, or tracking files beyond writing this critique artifact.
* Hosted GitHub Actions execution on `PR #1781` will occur only after the coordinator pushes the rebased branch (`git push` is excluded from this task).

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning parent (confirmed automatic `RPI Agent` / `rpi-plan`)
* Smallest next action: Finalize the candidate plan and phase details as Ready without another critique pass and proceed directly to `rpi-implement` (`P01` -> `P02` -> `P03`).
* User response required: no
