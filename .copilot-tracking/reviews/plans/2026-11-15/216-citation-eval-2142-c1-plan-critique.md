<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 PR #1774 CI Correction Cycle 1

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Resume RPI loop for issue `#216` PR `#1774` CI correction cycle 1 (`2026-11-15`), write `.copilot-tracking/reviews/plans/2026-11-15/216-citation-eval-2142-c1-plan-critique.md`, fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) and rebase onto it while preserving the `2026-11-15` `c1` tracking files, implement conditional `provision_ids` emission in `RegulatoryChat.bundle()` (`src/core/src/zava_forward/core/regulatory_chat.py`) and alias `compare_chat_against_deterministic_rule_cards` (`src/core/src/zava_forward/core/regulatory_eval_gates.py`), write `.copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md` and `.copilot-tracking/reviews/2026-11-15/216-citation-eval-2142-c1-review.md`, run exact focused verification commands in `src/core` and `src/agents`, and commit locally with `Refs #216` and Copilot trailer without `git push`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md (`C1`–`C10`), .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md, .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md, .copilot-tracking/rpi-sessions/2026-11-15/216-citation-eval-2142-c1-state.json.
* Decisions, dependencies, and acceptance criteria considered: `FR-1`–`FR-3`, `NFR-1`–`NFR-2`, `AC-1`–`AC-4`, phases `P01`–`P03` (`P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`), focused validation tier (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/agents`), no `tools/rpi-checks.py`, no `git push`, and open repository-level human governance gates (`OwnerGateAgreement`, staff paired trial, `BRD OD-51`) requiring `Refs #216`.
* Assessment boundary: Evaluates plan and phase-details credibility, git/rebase safety, contract parity across `src/core` and `src/agents`, and exact caller verification commands from supplied artifacts and caller instructions without running new codebase searches or mutating plan sources.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 (`C4`, `C5`, `C6`)                  | Covered  | `P02-T01` restores the frozen 10-field `regulatory-chat-v1` card envelope whenever `len(result["cards"]) <= 1` or every referenced `source_id` maps to a single provision in `sources`. |
| FR-2 (`C7`, `C8`)                        | Covered  | `P02-T01` mirrors `_active_cards_link_provisions` (`regulatory_eval_gates.py`) 1-for-1 by attaching `provision_ids` per card when `len(result["cards"]) > 1` and a card's base `source_id` maps to `>1` provision in `sources`. |
| FR-3 (`C9`)                              | Partial  | `P02-T01` aliases `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` in `regulatory_eval_gates.py`, but omits explicit `__all__` / `zava_forward.core` export parity (`PC-003`). |
| NFR-1 (`C10`)                            | Partial  | `P03-T01` covers `unittest`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/agents`, but references stale rebase SHA `243764945ea8f5b292eed0b73ea034b91c3b6e5f` (`PC-001`) and alters the caller's exact `src/agents` `PYTHONPATH` (`PC-002`). |
| NFR-2 (`C5`, `C8`)                       | Covered  | Bounded test discipline (`0` test removals, max `1` new regression test method `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias`) and preservation of `src/agents/evals/regulatory_gates_results.json` are well specified, subject to `PC-002` verification. |
| AC-1 / P01 / P01-T01 (`C1`, `C2`)        | Partial  | Plan and phase details hardcode older parent SHA `243764945ea8f5b292eed0b73ea034b91c3b6e5f` instead of caller-mandated `36aeddae345426fdf8ee53565fef1540979de967` (`PC-001`), and should verify post-fetch branch refs for `feat/ai-216-citation-eval-2142` vs `feat/demo-216-citation-eval-2142` (`PC-004`). |
| AC-2 / P02 / P02-T01 / P02-T02           | Covered  | Exact `src/core` verification command matches caller Required Step 5; `PC-003` closes explicit `__all__` export hygiene. |
| AC-3 / P03 / P03-T01 (`C10`)             | Partial  | `phase-details.md` adds `:tests:` to `PYTHONPATH` for direct file-path unittest invocation whereas caller Required Step 5 specifies `PYTHONPATH=../core/src:src:../core/tests` (`PC-002`). |
| AC-4                                     | Covered  | All `2026-11-15` `c1` RPI artifact paths, privacy-safe noreply git email, `Refs #216`, Copilot trailer, clean `git status --short`, and no `git push` are explicitly sequenced. |

## Verdict

* Verdict: Revise
* Rationale: The root-cause diagnosis (`C3`–`C8`) and selective `provision_ids` contract fix in `RegulatoryChat.bundle()` are technically sound, minimal, and fail-closed, but two High-severity direct planner corrections (`PC-001` updating target parent SHA from `243764945ea8f5b292eed0b73ea034b91c3b6e5f` to `36aeddae345426fdf8ee53565fef1540979de967`, and `PC-002` enforcing verbatim verification of the caller's exact `src/agents` `PYTHONPATH=../core/src:src:../core/tests` command) plus two Low-severity hygiene refinements (`PC-003`, `PC-004`) must be applied directly to the plan and phase details before transitioning to `Implement`. None conflict with user direction or require user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Target rebase SHA in plan and phase details lags caller-mandated parent commit

* Related IDs: AC-1, NFR-1, P01, P01-T01, C2
* Evidence: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md, .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md, and caller Required Step 2
* Concern: Both the plan (`Executive Summary`, `User Decisions and Requirements`, `Goals`, `In Scope`, `NFR-1`, `AC-1`, `P01`, `P01-T01`, `Dependencies`) and phase details (`P01`, `P01-T01`) hardcode `243764945ea8f5b292eed0b73ea034b91c3b6e5f` for `origin/feat/demo-164-chat-grounding-provenance-0900`, whereas caller Required Step 2 specifies `36aeddae345426fdf8ee53565fef1540979de967` and explicitly requires preserving the `2026-11-15` `c1` tracking files across the rebase.
* Impact: `P01-T01`'s exact SHA assertion (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`) will fail after fetching `origin/feat/demo-164-chat-grounding-provenance-0900`, and any commits between `243764945e` and `36aeddae34` must be inspected for conflict or file overlap (including `.copilot-tracking/` paths) before and during rebase.
* Smallest useful change: Update `plan.md` and `phase-details.md` (`AC-1`, `NFR-1`, `P01`, `P01-T01`, `Dependencies`) to require `origin/feat/demo-164-chat-grounding-provenance-0900` at `36aeddae345426fdf8ee53565fef1540979de967` (`git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD`), inspect `243764945e..36aeddae34` after fetch, and verify all `2026-11-15` `c1` tracking artifacts remain intact post-rebase.
* Action owner: planning_parent
* Exact resolving evidence: Updated `plan.md` and `phase-details.md` naming `36aeddae345426fdf8ee53565fef1540979de967`, plus `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` and `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exiting `0` in `changes.md`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P03 alters caller's exact src/agents PYTHONPATH verification command instead of ensuring verbatim pass

* Related IDs: AC-3, NFR-1, NFR-2, P03, P03-T01, C10
* Evidence: .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md (`P03` Context and Validation Expectations), .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md (`Non-Goals`, `NFR-2`, `AC-3`), and caller Required Step 5
* Concern: Caller Required Step 5 mandates verifying `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy` verbatim, yet `phase-details.md` (`P03`) asserts that direct path execution requires adding `tests` to `PYTHONPATH` (`PYTHONPATH=../core/src:src:tests:../core/tests`) because `src/agents/tests/` imports `regulatory_gate_fixture` as a top-level module, while `plan.md` unconditionally forbids any edit in `src/agents/`.
* Impact: If running the caller's exact Step 5 command without `:tests:` raises `ModuleNotFoundError: No module named 'regulatory_gate_fixture'`, substituting a custom `PYTHONPATH` in `P03` masks a failure of Required Step 5; conversely, if Python's file-path `unittest` invocation already puts `tests/` on `sys.path` (or if those two test files need a minimal `tests/` import fallback only when `regulatory_gate_fixture` is not on `sys.path`), the plan must verify the verbatim command first rather than bypassing it.
* Smallest useful change: Revise `AC-3`, `NFR-2`, and `P03`/`P03-T01` so the exact caller command (`PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy`) is a mandatory gate alongside `unittest discover -s tests`, keeping `src/agents/` completely untouched if the verbatim command already resolves imports (and permitting only a minimal non-behavioral `sys.path` / package import fallback in those two test files if and only if verbatim `PYTHONPATH=../core/src:src:../core/tests` fails with `ModuleNotFoundError`, never touching `regulatory_gate_fixture.py` or `evals/regulatory_gates_results.json`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `AC-3`, `NFR-2`, and `P03-T01` in `plan.md`/`phase-details.md`, and exit code `0` recorded in `changes.md` for the verbatim Step 5 `src/agents` command.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Alias export does not specify `__all__` and package re-export surface alignment

* Related IDs: FR-3, P02-T01, P02-T02, C9
* Evidence: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md (`FR-3`, `P02-T01`) and .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md (`P02-T01`)
* Concern: `P02-T01` specifies adding `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`, without checking whether `__all__` in `regulatory_eval_gates.py` or `src/core/src/zava_forward/core/__init__.py` explicitly enumerates `compare_chat_against_rule_cards` and `evaluate_citation_and_refusal_gates`.
* Impact: Under strict `mypy` (`no_implicit_reexport`) or `ruff` export checks, omitting `compare_chat_against_deterministic_rule_cards` from `__all__` (or package `__init__.py` if `compare_chat_against_rule_cards` is re-exported there) would leave export parity incomplete.
* Smallest useful change: Update `P02-T01` in `phase-details.md` to include `compare_chat_against_deterministic_rule_cards` in `__all__` wherever `compare_chat_against_rule_cards` is listed (`regulatory_eval_gates.py` and, if applicable, `zava_forward/core/__init__.py`).
* Action owner: planning_parent
* Exact resolving evidence: `compare_chat_against_deterministic_rule_cards` present in `__all__` parity with `compare_chat_against_rule_cards`, verified by `mypy`, `ruff check .`, and `test_c23`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Post-fetch branch ref verification between `feat/ai-216-citation-eval-2142` and caller-named `feat/demo-216-citation-eval-2142`

* Related IDs: AC-1, P01-T01, C1
* Evidence: .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md (`C1`), .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md (`What You May Not Know`, `P01-T01`), and caller Required Step 2
* Concern: Research `C1` established that PR `#1774`'s checked-out branch in worktree `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142` is `feat/ai-216-citation-eval-2142` and no `feat/demo-216-citation-eval-2142` ref existed previously, while caller Required Step 2 names `feat/demo-216-citation-eval-2142`. Since `origin/feat/demo-164-chat-grounding-provenance-0900` advanced since `C1`/`C2`, `P01-T01` should also confirm after fetching `origin` whether any `feat/demo-216-citation-eval-2142` ref was created or whether `feat/ai-216-citation-eval-2142` remains the sole PR `#1774` head branch.
* Impact: Re-verifying branch refs immediately upon fetch prevents rebasing the wrong ref if upstream created `feat/demo-216-citation-eval-2142` and documents clear branch provenance if `feat/ai-216-citation-eval-2142` remains PR `#1774`'s head.
* Smallest useful change: Specify in `P01-T01` (`phase-details.md`) to check `git show-ref` for `216-citation-eval-2142` alongside fetching `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), rebasing the checked-out PR `#1774` branch cleanly and recording exact branch/ref evidence in `changes.md`.
* Action owner: planning_parent
* Exact resolving evidence: Recorded `git branch --show-current` and `git log -n 3 --oneline` post-rebase in `changes.md`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Root-cause localization (`C3`–`C8`) accurately disproved the upstream false-positive hypothesis (`regulatory_assistant.py` / `"duty is satisfied"`) and proved that `RegulatoryChat.bundle()`'s unconditional `provision_ids` caused `actual.get("cards") != expected["cards"]` in `src/agents`, which cascaded into `refusal_accuracy.failed_case_ids` via `refusal_ok = answer_contract and citation_validity`.
* Per-card multi-provision disambiguation (`len(result["cards"]) > 1` with `>1` provision on a card's base `source_id`) aligns 1-for-1 with `_active_cards_link_provisions` in `regulatory_eval_gates.py`, preserving both frozen 10-field `regulatory-chat-v1` parity (`src/agents`) and `#216` `RV-023` fail-closed multi-card provenance checks (`src/core`).
* Residual risk (explicitly accepted): Repository-level human governance gates for `#216` (`OwnerGateAgreement` dual-capacity sign-off, live staff paired trial across `repairs`, `housing`, and `grants`, and `BRD OD-51` unit-cost ceiling ratification) remain outside executable offline code scope and are properly reflected by committing with `Refs #216` rather than a closing keyword.

## Questions or Blocking Evidence Gaps

* None. All four findings (`PC-001`–`PC-004`) are resolved by direct planner revision consistent with confirmed caller direction.

## Limitations

* Critique stayed strictly within supplied artifacts and caller instructions without fetching `origin` or running Python commands prior to `Implement`; `P01-T01` and `P03-T01` verify live remote SHA `36aeddae345426fdf8ee53565fef1540979de967` and verbatim `src/agents` command execution during `Implement`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, `PC-003`, and `PC-004` to `.copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md` and `.copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md`, finalize the plan without repeating critique, and transition automatically to `Implement`.
* User response required: no
