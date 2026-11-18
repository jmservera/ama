<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #216 PR #1774 CI Correction Cycle 1

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Task slug: 216-citation-eval-2142-c1
* Related plan: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md, src/core/src/zava_forward/core/regulatory_chat.py, src/core/src/zava_forward/core/regulatory_eval_gates.py, src/agents/src/zava_forward/agents/regulatory_gates.py, src/agents/tests/regulatory_gate_fixture.py

## Phase Index

| Phase ID | Name                                                     | Status   | Detail sections       |
|----------|----------------------------------------------------------|----------|-----------------------|
| P01      | Rebase Topic Branch Onto Target Parent                   | Complete | P01, P01-T01          |
| P02      | Fix RegulatoryChat Card Envelope Compatibility and Alias | Complete | P02, P02-T01, P02-T02 |
| P03      | Focused Validation across Core and Agents                | Complete | P03, P03-T01          |

<!-- rpi:phase id=P01 -->
## P01: Rebase Topic Branch Onto Target Parent

### Context

Worktree `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142` is on `feat/ai-216-citation-eval-2142` (`61ba873dc`), the exact head branch of PR `#1774` (`C1`). Its base `08c36e4dc8` lags `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`). Untracked `.copilot-tracking/.../2026-11-15/` `c1` files must be preserved intact across the rebase (`PC-001`, `PC-004`).

### Intent

Fetch `origin/feat/demo-164-chat-grounding-provenance-0900`, verify branch refs (`feat/ai-216-citation-eval-2142` vs `feat/demo-216-citation-eval-2142`), verify its SHA equals `36aeddae345426fdf8ee53565fef1540979de967`, inspect upstream commits between `08c36e4dc8` and `36aeddae345426fdf8ee53565fef1540979de967`, and rebase `feat/ai-216-citation-eval-2142` onto `origin/feat/demo-164-chat-grounding-provenance-0900` while preserving all `2026-11-15` `c1` tracking files.

### Boundaries

* Included: `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, ref/diff inspection, and `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`.
* Excluded: Force-pushing or pushing to `origin` (`git push` is explicitly prohibited), creating duplicate branches, or rewriting `main`.

### Likely Targets

* Git branch `feat/ai-216-citation-eval-2142` in `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142`: Rebased onto `36aeddae345426fdf8ee53565fef1540979de967`.

### Dependencies

* None.

### Validation Expectations

* `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` outputs `36aeddae345426fdf8ee53565fef1540979de967`.
* `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0`.
* All `2026-11-15` `c1` tracking files (`research`, `plans`, `details`, `reviews/plans`, `rpi-sessions`) remain intact after rebase.

### Completion Evidence

* Clean rebased `git log -n 4 --oneline` output and branch ref check recorded in `.copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fetch and rebase onto origin/feat/demo-164-chat-grounding-provenance-0900

#### Context

Ensure local remote-tracking ref `origin/feat/demo-164-chat-grounding-provenance-0900` points at `36aeddae345426fdf8ee53565fef1540979de967`, confirm `git show-ref` for `216-citation-eval-2142` (`PC-004`), inspect commits `08c36e4dc8..36aeddae345426fdf8ee53565fef1540979de967`, and rebase `feat/ai-216-citation-eval-2142` onto `origin/feat/demo-164-chat-grounding-provenance-0900` preserving the `2026-11-15` `c1` tracking files (`PC-001`).

#### Intent

Bring all upstream commits on `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) into `feat/ai-216-citation-eval-2142` history cleanly before applying `c1` code edits.

#### Boundaries

* Included: `git fetch`, ref inspection, and `git rebase` in the active worktree.
* Excluded: `git push` or modifying commits below `36aeddae345426fdf8ee53565fef1540979de967`.

#### Likely Targets

* Local git branch `feat/ai-216-citation-eval-2142`: Rebased commit history.

#### Dependencies

* None.

#### Validation Expectations

* Zero conflict markers; `git status --short` shows only untracked `2026-11-15` `.copilot-tracking/` artifacts, all intact.

#### Completion Evidence

* Verified ancestor check against `36aeddae345426fdf8ee53565fef1540979de967`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Fix RegulatoryChat Card Envelope Compatibility and Alias

### Context

`src/agents/src/zava_forward/agents/regulatory_gates.py` checks `actual.get("cards") == expected["cards"]` against `src/agents/tests/regulatory_gate_fixture.py:expected_card()`, which expects the frozen 10-field `regulatory-chat-v1` card schema without `provision_ids`, and propagates `answer_contract` failures on `answer` cases into `refusal_accuracy.failed_case_ids` (`C4`, `C5`). Meanwhile, `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_active_cards_link_provisions`) already resolves card-to-provision linkage without `provision_ids` whenever `len(cards) == 1` or each card's referenced `source_id` maps to a single provision in `sources`, requiring `provision_ids` strictly when `len(cards) > 1` and multiple provisions in `sources` share a card's base `source_id` (`C7`, `C8`).

### Intent

Update `RegulatoryChat.bundle()` so `provision_ids` is attached only when `len(result["cards"]) > 1` and a card's base `source_id` maps to multiple provisions in `sources`; export `compare_chat_against_deterministic_rule_cards` in `regulatory_eval_gates.py`; update `src/core/README.md`; and add bounded regression test coverage in `src/core/tests/test_regulatory_eval_gates_216.py`.

### Boundaries

* Included:
  * `src/core/src/zava_forward/core/regulatory_chat.py`
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/README.md`
  * `src/core/tests/test_regulatory_eval_gates_216.py` (exact test removals: `none`; maximum additions: `1` test method `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias`; canonical targets: `src/core/tests/test_regulatory_eval_gates_216.py`; generated targets: `none`; semantic coverage: 10-field `regulatory-chat-v1` single-card and distinct-source multi-card compatibility + shared-source multi-card `provision_ids` disambiguation + `compare_chat_against_deterministic_rule_cards` alias parity).
* Excluded: Any edit to `src/agents/`, `evals/regulatory_gates_results.json`, or `_REFUSAL_PATTERNS`.

### Likely Targets

* src/core/src/zava_forward/core/regulatory_chat.py: Conditional `provision_ids` attachment in `RegulatoryChat.bundle()`.
* src/core/src/zava_forward/core/regulatory_eval_gates.py: Module-level `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` alias.
* src/core/README.md: Document conditional multi-card shared-source `provision_ids` disambiguation and `compare_chat_against_deterministic_rule_cards` alias.
* src/core/tests/test_regulatory_eval_gates_216.py: Add `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias`.

### Dependencies

* P01 completed.

### Validation Expectations

* Single-card `RegulatoryChat.bundle()` cards have exact key set `{"id", "status", "approved_by", "approved_on", "effective", "exercise", "link", "safe_default", "clock", "source_freshness"}`.
* Multi-card shared-source `RegulatoryChat.bundle()` cards retain `provision_ids` and pass `test_c11`.
* `compare_chat_against_deterministic_rule_cards` is importable from `zava_forward.core.regulatory_eval_gates` and evaluates identically to `compare_chat_against_rule_cards`.

### Completion Evidence

* Passing unit tests in `src/core` and `src/agents`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Gate provision_ids emission in RegulatoryChat.bundle() and export comparator alias

#### Context

In `RegulatoryChat.bundle()`, track `card_provisions: list[list[str]]` alongside `result["cards"]`. After `result["refusal"]` early-return handling, if `len(result["cards"]) > 1`, count `provs_per_source` across `sources` keys (`pid.split("@v", 1)[0]`). Attach `card_entry["provision_ids"] = pids` across `(result["cards"], card_provisions)` only when `any(provs_per_source.get(pid.split("@v", 1)[0], 0) > 1 for pids in card_provisions for pid in pids)`. Note: when `len(result["cards"]) > 1` and ANY card references a multi-provision `source_id`, attach `provision_ids` only on cards that need it OR consistently across the cards in that ambiguous bundle? Wait — check `_active_cards_link_provisions` (`regulatory_eval_gates.py:1043-1077`) and `grade_chat_turn` (`line 1862`)! `_active_cards_link_provisions` checks `"provision_ids" in card` per card, and `grade_chat_turn` checks `("provision_ids" in act_c) == ("provision_ids" in exp_c)` per card (`render_extractive_answer` passes `bundle["cards"]` straight through, so `act_c` and `exp_c` always match!). Attaching `provision_ids` to each card whose `pids` touch a `source_id` with `provs_per_source[sid] > 1` (or to all cards in `result["cards"]` whenever `any(...)` holds on that multi-card shared-source bundle) works cleanly; attaching per card when `len(result["cards"]) > 1 and any(provs_per_source.get(pid.split("@v", 1)[0], 0) > 1 for pid in pids)` matches `_active_cards_link_provisions`'s exact per-card `else` guard (`len(cards) > 1 and any(provs_per_base_sid.get(sid, 0) != 1 for sid in mapped_source_ids)`), so even a mixed 2-card bundle (card A on multi-provision `src1`, card B on single-provision `src2`) disambiguates card A while leaving card B minimal — or attaching to all cards in `result["cards"]` when the bundle has shared multi-provision ambiguity also satisfies `_active_cards_link_provisions`! Specifically, checking per card `if len(result["cards"]) > 1 and any(provs_per_source.get(pid.split("@v", 1)[0], 0) > 1 for pid in pids): card_entry["provision_ids"] = pids` is an exact 1-to-1 mirror of `_active_cards_link_provisions` (`lines 1063-1065`) AND produces `[["synthetic@v1#0001"], ["synthetic@v1#0002"]]` on `test_c11`!

#### Intent

Implement exact per-card multi-provision disambiguation in `RegulatoryChat.bundle()`, add `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` with `__all__` / re-export parity (`PC-003`) in `regulatory_eval_gates.py` (and `zava_forward/core/__init__.py` if `compare_chat_against_rule_cards` is listed there), and update `src/core/README.md`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/README.md`.
* Excluded: `src/agents/` files and `_REFUSAL_PATTERNS`.

#### Likely Targets

* src/core/src/zava_forward/core/regulatory_chat.py: `RegulatoryChat.bundle()`.
* src/core/src/zava_forward/core/regulatory_eval_gates.py: `compare_chat_against_deterministic_rule_cards` alias.
* src/core/README.md: `#216` bullet prose update.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `ruff check`, `ruff format --check`, and `mypy` pass in `src/core`.

#### Completion Evidence

* Diff review of `regulatory_chat.py`, `regulatory_eval_gates.py`, and `src/core/README.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add focused regression coverage in test_regulatory_eval_gates_216.py

#### Context

Lock the contract so a future edit cannot re-introduce unconditional `provision_ids` on single-card `RegulatoryChat.bundle()` envelopes or remove `compare_chat_against_deterministic_rule_cards`.

#### Intent

Add `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias` in `src/core/tests/test_regulatory_eval_gates_216.py`.

#### Boundaries

* Included: 1 focused test method in `src/core/tests/test_regulatory_eval_gates_216.py` checking:
  1. Single-card `RegulatoryChat.bundle()` and `RegulatoryChat.ask()` preserve exact 10-key `regulatory-chat-v1` card dicts (`"provision_ids" not in card`) while passing `evaluate_citation_and_refusal_gates`, `deterministic_rule_cards`, and `compare_chat_against_deterministic_rule_cards`.
  2. Two-card distinct-source `RegulatoryChat.bundle()` omits `"provision_ids"`, whereas two-card shared multi-provision-source `RegulatoryChat.bundle()` includes `"provision_ids"` per ambiguous card.
* Excluded: Duplicate tests restating `test_c11` or `src/agents` test suites.

#### Likely Targets

* src/core/tests/test_regulatory_eval_gates_216.py: New `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias` method.

#### Dependencies

* P02-T01.

#### Validation Expectations

* `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q` passes in `src/core`.

#### Completion Evidence

* Green `src/core` test run recorded in changes artifact.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Validation across Core and Agents

### Context

Both `src/core` and `src/agents` focused validation suites must pass cleanly on the rebased branch under the caller's exact Required Step 5 commands before running `rpi-review` and creating the local git commit (`Refs #216`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, no `git push`). Per `PC-002`, `P03` must verify the verbatim `src/agents` command `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy` alongside `unittest discover -s tests` (applying a minimal non-behavioral `tests/` import-path fallback in those two test files if and only if verbatim execution raises `ModuleNotFoundError` for `regulatory_gate_fixture`, and never touching `src/agents/src/`, `regulatory_gate_fixture.py`, or `evals/regulatory_gates_results.json`).

### Intent

Run and verify both verbatim focused validation suites (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/agents`, plus `discover -s tests -p "test_*regulatory*.py"`), record exact outputs in `.copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md`, and prepare for single-pass `rpi-review` followed by local git commit.

### Boundaries

* Included: Verbatim Required Step 5 test, lint, format, and type-check commands in `src/core` and `src/agents`; non-behavioral `_TESTS_DIR` `sys.path` guard in `src/agents/tests/test_regulatory_citation_card_gates.py` and `src/agents/tests/test_regulatory_gates.py` per `PC-002` so direct file-path `unittest` invocation resolves `regulatory_gate_fixture` without `:tests:` in `PYTHONPATH`; authoring `.copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md`.
* Excluded: `src/agents/src/`, `src/agents/tests/regulatory_gate_fixture.py`, `src/agents/evals/regulatory_gates_results.json`, `tools/rpi-checks.py`, and `git push`.

### Likely Targets

* src/agents/tests/test_regulatory_citation_card_gates.py: `_TESTS_DIR` `sys.path` guard per `PC-002`.
* src/agents/tests/test_regulatory_gates.py: `_TESTS_DIR` `sys.path` guard per `PC-002`.
* .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md: Implementation and validation evidence record.

### Dependencies

* P02-T01, P02-T02.

### Validation Expectations

* `cd src/core && PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q && ruff check . && ruff format --check . && mypy` exits `0`.
* `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy` exits `0` (and `PYTHONPATH=../core/src:src:../core/tests python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q` exits `0`).

### Completion Evidence

* Zero failures or lint/type errors across both `src/core` and `src/agents`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute src/core and src/agents focused validation suites and changes record

#### Context

Verify that all 4 previously failing tests in `src/agents` (`test_comparator_reports_lift_and_ships_chat_when_gates_pass`, `test_gates_have_owners_and_cover_both_sets`, `test_development_cases_are_independently_graded_and_no_overall_pass`, `test_recorded_60000_home_report_matches_exact_rerun`) now pass alongside all `#216` tests in `src/core`.

#### Intent

Run all focused checks, reconcile plan/details checkboxes, and write `.copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md`.

#### Boundaries

* Included: `src/core` and `src/agents` validation commands and `216-citation-eval-2142-c1-changes.md`.
* Excluded: `tools/rpi-checks.py` and `git push`.

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md: Complete implementation evidence record.

#### Dependencies

* P02-T02.

#### Validation Expectations

* Exit code `0` on every focused-tier command in `src/core` and `src/agents`.

#### Completion Evidence

* Recorded command outputs and reconciled `P01`–`P03` markers.

#### Unresolved Items

* None.
