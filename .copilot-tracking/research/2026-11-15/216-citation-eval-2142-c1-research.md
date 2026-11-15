<!-- markdownlint-disable-file -->

# Task Research: 216-citation-eval-2142-c1

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | rpi-research (RPI Agent automatic loop)                                  |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md |
| Research Disposition | executed                                                               |
| Planning Readiness | Ready                                                                    |

## Research Brief

* What to research: Diagnose the `src-agents` CI failure on PR `#1774` (Issue `#216`) when merged/rebased against `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), specifically how `REFUSAL_PATTERNS` / refusal classification and `evaluate_citation_and_refusal_gates` / `compare_chat_against_deterministic_rule_cards` interact across `src/core` and `src/agents`, and verify the exact branch/rebase mechanics in worktree `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142`.
* Why it matters: Normal regulatory answers include the standard human-authority disclaimer ("decide whether a duty is satisfied"), so matching `"duty is satisfied"` as a refusal pattern misclassifies grounded answers (`automated-source`, `lookup-hazard`, `lookup-home`, `lookup-emergency`, `source-injection`, `stale-source-label`) as refusals in `src/agents` tests while `#216` gates must still pass in both `src/core` and `src/agents`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases of the `#216` PR `#1774` correction cycle 1 (`2026-11-15`).
* Scope: `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), PR `#1774` head commit `61ba873dc`, `src/core/src/zava_forward/core/` (`regulatory_assistant.py`, `regulatory_chat.py`, `regulatory_eval_gates.py`), `src/core/tests/`, and `src/agents/` (`tests/test_regulatory_citation_card_gates.py`, `tests/test_regulatory_gates.py`, and related regulatory modules).
* Non-goals: Running `tools/rpi-checks.py`, pushing to `origin` (`git push`), changing unrelated packages (`infra`, `orchestrator`, `importer`), or claiming live human governance sign-off (`OwnerGateAgreement`, live staff trial, OD-51 policy ratification).
* Criteria: Identify exact root cause (`path:line`) on both current `HEAD` and target base `origin/feat/demo-164-chat-grounding-provenance-0900`, confirm rebase compatibility, and select a minimal, fail-closed fix that preserves all `src/core` and `src/agents` unit tests, `ruff`, and `mypy`.
* Requested outputs: Complete primary research artifact with convergence recommendation and planning handoff.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | Why did `src-agents` fail on PR `#1774` against `origin/feat/demo-164-chat-grounding-provenance-0900`, where do `regulatory_assistant.py` / `regulatory_chat.py` / `regulatory_eval_gates.py` reside across the two branches, and what exact change preserves answer-vs-refusal classification and `#216` gates in both `src/core` and `src/agents`? |
| Codebase scope                   | `src/core/`, `src/agents/`, `.github/workflows/`, and git ancestry of `feat/ai-216-citation-eval-2142` and `origin/feat/demo-164-chat-grounding-provenance-0900` |
| External scope                   | none (codebase and local/GitHub CI run inspection only)                 |
| Initial internal candidate areas | `src/core/src/zava_forward/core/`, `src/core/tests/`, `src/agents/src/`, `src/agents/tests/test_regulatory_citation_card_gates.py`, `src/agents/tests/test_regulatory_gates.py` |
| Initial external candidate areas | none                                                                    |
| Research posture                 | focused                                                                 |
| Posture provenance               | default (bounded internal regression fix with named targets and CI failure evidence) |
| Explicit limits / deadline       | Focused validation tier only; do NOT run `tools/rpi-checks.py`; do NOT `git push` |
| Posture-specific completion basis | focused scope and materiality: all affected modules, tests, and rebase conflicts/interactions across `HEAD` and `origin/feat/demo-164-chat-grounding-provenance-0900` verified with exact `path:line` evidence |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                    |
| Known constraints / excluded sources | Read-only during `rpi-research`; no source edits or git branch mutations until `rpi-implement` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches repository and tracking paths | Adds AMA validation tier, branch/PR, Markdown style, and regulatory safety boundaries | Selected: mandatory repository instruction |
| Skill               | `rpi-research`                   | Explicit phase skill for RPI loop step 1          | Owns three-wave research cycle and primary research artifact | Selected: active phase contract |
| Skill               | `python-foundational`            | Matches Python unit tests / typing in `src/core` and `src/agents` | Python implementation and testing conventions | Skipped during Research: read-only phase requires no code authoring |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered specialist for independent research lanes | Bounded lane artifact under `.copilot-tracking/research/subagents/` | Skipped (inline preferred): tightly coupled 5-file git-ancestry + Python contract trace fits faster and cleaner inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller brief naming issue `#216`, PR `#1774`, target parent `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), exact failing test cases, and verification commands. | Not applicable (non-interactive; inputs sufficient) | Proceed in `focused` posture with `convergence` output mode; inspect branch naming (`feat/ai-216-citation-eval-2142` vs prompt text `feat/demo-216-citation-eval-2142`) during Wave 1. |
| Direction change | Caller triage attributed `src-agents` `refusal_accuracy` failures to `"duty is satisfied"` in `regulatory_assistant.py`; Wave 1/2 proved `regulatory_assistant.py` does not exist on either branch and the exact CI failure is caused by `provision_ids` in `RegulatoryChat.bundle()`. | Not applicable (non-interactive; code evidence unambiguous) | Keep caller's exact contract goal (fix PR `#1774` `src-agents` CI failure while keeping `#216` evaluation gates and rule-card comparator passing in both `src/core` and `src/agents` after rebasing onto `243764945ea8f5b292eed0b73ea034b91c3b6e5f`). |
| Convergence      | Evidence across all three waves converged on one minimal, backward-compatible contract fix in `src/core` with zero changes needed in `src/agents`. | Not applicable (non-interactive; single clear convergence option) | Advance to `Plan` (`Planning Readiness: Ready`). |

## Scope and Success Criteria

* Scope: Git commits and file tree differences between `HEAD` (`61ba873dc` on `feat/ai-216-citation-eval-2142`) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), PR `#1774` `src-agents` CI failure logs, `regulatory_assistant.py`, `regulatory_chat.py`, `regulatory_eval_gates.py`, and `src/core` + `src/agents` regulatory tests.
* Assumptions:
  * Assumption A1: PR `#1774`'s actual head branch in this worktree is `feat/ai-216-citation-eval-2142` (while the worktree directory is `feat-216-citation-eval-2142` and the prompt referred to `feat/demo-216-citation-eval-2142`); verify whether `feat/demo-216-citation-eval-2142` exists anywhere or if `feat/ai-216-citation-eval-2142` is the sole branch for PR `#1774`.
  * Assumption A2: `src/core/src/zava_forward/core/regulatory_assistant.py` exists on `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`) or in the PR `#1774` merge commit tested by GitHub Actions.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, git commits, or CI logs, with `path:line` locations.
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Diagnose and plan the fix for the `src-agents` CI failure on PR `#1774` caused by `"duty is satisfied"` in `REFUSAL_PATTERNS` inside `src/core/src/zava_forward/core/regulatory_assistant.py`.
  * Verify rebase target `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`) and compatibility of `#216`'s `evaluate_citation_and_refusal_gates` and `compare_chat_against_deterministic_rule_cards` across `src/core` and `src/agents`.
* Inferred research questions:
  * Why does `HEAD` (`61ba873dc`) currently modify `regulatory_chat.py` and `regulatory_eval_gates.py` while the CI failure references `regulatory_assistant.py`, `evaluate_citation_and_refusal_gates`, and `compare_chat_against_deterministic_rule_cards`?
  * What commits exist on `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`) vs `HEAD` (`61ba873dc`), and how will rebasing merge or conflict?
* Caller constraints and non-goals: Focused validation tier (`src/core` and `src/agents` unit tests, `ruff`, `mypy`); do NOT run `tools/rpi-checks.py`; do NOT `git push`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused validation tier (`src/core` + `src/agents` tests, `ruff`, `mypy` only) | User prompt (Intake) | Excludes `tools/rpi-checks.py` and unrelated packages |
| exclude                                                  | Do NOT run `git push` | User prompt (Intake) | Keeps rebased/fixed commit local in worktree |
| add                                                      | Write `2026-11-15` dated `c1` artifacts across `research`, `plans`, `details`, `changes`, `reviews` | User prompt (Intake) | Establishes `216-citation-eval-2142-c1` artifact paths under `2026-11-15/` |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | What is the exact git ancestry and file diff between `HEAD` (`61ba873dc`), `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), and PR `#1774`'s tested merge commit, and what is the exact branch name in this worktree? | straightforward | H | answered (`C1`, `C2`) |
| Q2 | What caused `src-agents` to fail on PR `#1774` (`failed_case_ids: ['automated-source', 'lookup-hazard', 'lookup-home', 'lookup-emergency', 'source-injection', 'stale-source-label']`), and how does `regulatory_assistant.py` classify answers vs refusals? | depth | H | answered (`C3`, `C4`, `C5`, `C6`) |
| Q3 | How are `#216`'s `evaluate_citation_and_refusal_gates` and `compare_chat_against_deterministic_rule_cards` implemented across `regulatory_assistant.py` / `regulatory_eval_gates.py` / `regulatory_chat.py`, and how do both `src/core` and `src/agents` test them after rebasing onto `243764945ea8f5b292eed0b73ea034b91c3b6e5f`? | depth | H | answered (`C7`, `C8`, `C9`, `C10`) |
| Q4 | Could removing or narrowing `"duty is satisfied"` in `REFUSAL_PATTERNS` weaken any legitimate refusal detection or adversarial gate case in `src/core` or `src/agents`? | depth | H | answered (`C5`, `C7`, `C8`) |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-14/216-citation-eval-2142-state.json`, `.copilot-tracking/rpi-sessions/2026-11-14/216-citation-eval-2142-c22-state.json`, `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md`
* Reused (verified) findings: `61ba873dc` on `feat/ai-216-citation-eval-2142` added `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py` (`ship_gated`/`surface`), `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md` (`#216` section), and `src-core` CI passed on PR `#1774` while `src-agents` CI failed (`job/132718061819`).
* Superseded / stale: Prior `2026-11-14` `c1..c22` artifacts addressed `src/core`-only pre-PR review iterations before PR `#1774` ran `Source projects CI` against base `feat/demo-164-chat-grounding-provenance-0900`.

## Research Execution — Cycle 1

### Wave 1: Wider (Inline)

* Investigated git branch topology, PR `#1774` metadata (`gh pr view 1774`), GitHub Actions CI run `43683167651` / job `132718061819`, and module layout across `src/core`, `src/agents`, and `src/api`.
* Verified Assumption A1 (branch naming): worktree `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142` is checked out on `feat/ai-216-citation-eval-2142` (`61ba873dc38ba2e19a67253988940b976fbc223a`), which is PR `#1774`'s exact `headRefName` targeting `baseRefName` `feat/demo-164-chat-grounding-provenance-0900` (`C1`). No local or remote ref named `feat/demo-216-citation-eval-2142` exists; keeping and rebasing `feat/ai-216-citation-eval-2142` preserves PR `#1774`'s head branch (`C1`).
* Verified parent branch tip on GitHub (`feat/demo-164-chat-grounding-provenance-0900` = `243764945ea8f5b292eed0b73ea034b91c3b6e5f`): two commits landed after `61ba873dc`'s parent `08c36e4dc8` — `71f5c9f9b6` (`#154`, `#1772`) and `243764945e` (`#116`, `#1766`) (`C2`).
* Refuted Assumption A2 (`regulatory_assistant.py`): neither `HEAD` (`61ba873dc`) nor `feat/demo-164-chat-grounding-provenance-0900` (`243764945e`) contains any `regulatory_assistant.py` file (`C3`). In `src/core`, `#216` lives in `src/core/src/zava_forward/core/regulatory_chat.py` and `src/core/src/zava_forward/core/regulatory_eval_gates.py`; in `src/agents`, regulatory evaluation gates live in `src/agents/src/zava_forward/agents/regulatory_chat.py`, `src/agents/src/zava_forward/agents/regulatory_gates.py`, and `src/agents/src/zava_forward/agents/citation_card_gates.py` (`C3`, `C4`, `C7`).

### Wave 2: Deeper (Inline)

* Retrieved exact CI failure logs for `src-agents` (`job/132718061819`) and reproduced all 4 failures across the 40 regulatory tests in `src/agents`:
  1. `test_comparator_reports_lift_and_ships_chat_when_gates_pass` (`src/agents/tests/test_regulatory_citation_card_gates.py:63`): `report["ship_mode"] == 'cards_only' != 'chat_with_cards'`.
  2. `test_gates_have_owners_and_cover_both_sets` (`src/agents/tests/test_regulatory_citation_card_gates.py:23`): `refusal_accuracy` failed on `['automated-source', 'lookup-hazard', 'lookup-home', 'lookup-emergency', 'stale-source-label']` (graded) and `['source-injection']` (adversarial), while `citation_validity` passed on all 7 cases!
  3. `test_development_cases_are_independently_graded_and_no_overall_pass` (`src/agents/tests/test_regulatory_gates.py:39`): `answer_contract` failed (`18/24`, `failed_case_ids: ['automated-source', 'lookup-hazard', 'lookup-home', 'lookup-emergency', 'source-injection', 'stale-source-label']`), and `refusal_accuracy` failed on the same 6 answer cases (`18/24`).
  4. `test_recorded_60000_home_report_matches_exact_rerun` (`src/agents/tests/test_regulatory_gates.py:298`): live evaluation report diverged from committed `src/agents/evals/regulatory_gates_results.json`.
* Traced field-by-field why `answer_contract` failed on all 6 `kind == "answer"` cases while `actual["kind"]` was still `"answer"` (NOT `"refused"`):
  * `src/agents/src/zava_forward/agents/regulatory_gates.py:124` evaluates `answer_contract` on `"answer"` turns with `actual.get("cards") == expected["cards"]` (`C4`).
  * `src/agents/src/zava_forward/agents/regulatory_gates.py:157-160` defines `refusal_ok = r["answer_contract"] and r["citation_validity"]` for `expected["kind"] == "answer"`, so any `answer_contract` mismatch on an answer case is also reported in `refusal_accuracy.failed_case_ids` (`C4`). That explains why upstream failure triage misread the 6 answer case IDs in `refusal_accuracy.failed_case_ids` as a refusal-pattern false positive!
  * `src/agents/tests/regulatory_gate_fixture.py:161-172` (`expected_card`) defines the frozen 10-field `regulatory-chat-v1` card oracle (`id`, `status`, `approved_by`, `approved_on`, `effective`, `exercise`, `link`, `safe_default`, `clock`, `source_freshness`) WITHOUT `provision_ids` (`C5`).
  * In commit `61ba873dc`, `src/core/src/zava_forward/core/regulatory_chat.py:410` unconditionally added `provision_ids=list(card["provisions"])` to every card dictionary in `RegulatoryChat.bundle()` (`C6`). Every other field of `actual` matched `expected` identically, and all 13 tests in `src/api/tests/test_regulatory_chat_api.py` passed (`C6`).
* Inspected how `src/core/src/zava_forward/core/regulatory_eval_gates.py` consumes `provision_ids`:
  * Every validator in `regulatory_eval_gates.py` (`_cards_reference_bundle_sources` at line `785`, `_active_cards_link_provisions` at lines `1043-1077`, `_card_provenance_valid` at line `1615`, and `grade_chat_turn` at line `1862`) ALREADY treats `"provision_ids"` on card dicts as optional whenever card-to-provision linkage is unambiguous (`len(cards) == 1` or each referenced `source_id` has a single provision in the bundle's `sources`) (`C7`).
  * `"provision_ids"` is ONLY required to disambiguate multi-card bundles (`len(cards) > 1`) where multiple provisions in `sources` share the same unversioned `source_id` (`provs_per_base_sid[sid] > 1`), as tested by `test_c11_exact_card_provision_ids_unflagged_version_conflicts_and_expected_refusal_guards` (`src/core/tests/test_regulatory_eval_gates_216.py:2429-2509`) (`C8`).

### Wave 3: Contrarian (Inline)

* Challenged three potential failure modes against the proposed selective `provision_ids` design:
  1. **Could `refuse_question` / `_REFUSAL_PATTERNS` in `regulatory_eval_gates.py` actually misclassify disclaimers or normal regulatory questions?** Checked `src/agents/src/zava_forward/agents/regulatory_chat.py` and `src/core/src/zava_forward/core/regulatory_eval_gates.py`: `src/agents` passes its own `regulatory_chat.refusal` callback into `RegulatoryChat(...)` (`regulatory_gate_fixture.py:224`), NOT `regulatory_eval_gates.refuse_question`, and `refuse_question` only inspects user prompts (never rendered answer disclaimers) and passed all 22 cycles of positive/negative linguistic refusal tests in `test_regulatory_eval_gates_216.py` (`C5`, `C8`). Touching `_REFUSAL_PATTERNS` would weaken `#216` adversarial refusal gates without fixing `src-agents` at all!
  2. **What about symbol naming (`compare_chat_against_deterministic_rule_cards` vs `compare_chat_against_rule_cards`)?** Checked `src/core/src/zava_forward/core/regulatory_eval_gates.py:3999`: the module defines `compare_chat_against_rule_cards` (alongside `evaluate_citation_and_refusal_gates` at line `2443` and `deterministic_rule_cards`), while the caller prompt refers to `compare_chat_against_deterministic_rule_cards` (`C9`). Exporting `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` as a module-level alias preserves all existing callers while directly satisfying callers or scripts importing `compare_chat_against_deterministic_rule_cards` (`C9`).
  3. **What about `PYTHONPATH` when running `src/agents` tests directly by file path vs `unittest discover`?** Checked `src/agents/pyproject.toml:34-43` and `.github/workflows/src-ci.yml:88`: `src/agents` configures `src = ["src", "tests"]` and `mypy_path = ["src", "tests", "../core/tests"]`, and CI runs `python -m unittest discover -s tests -v` (which adds `tests/` to `sys.path`) so all 40 test files import `from regulatory_gate_fixture import ...` (`C10`). Modifying `src/agents/tests/` is unnecessary and out of scope for `#216`; during local validation, verify both `unittest discover -s tests` (CI's exact runner) and direct module execution with `tests` on `PYTHONPATH` (`PYTHONPATH=../core/src:src:tests:../core/tests`) (`C10`).
* Re-entry assessment: All 4 research questions (`Q1`–`Q4`) are answered with direct `path:line` and CI evidence; no unresolved uncertainties remain, so no Cycle 2 is warranted.

## Evidence Log

| ID  | Source (`path:line`) | Summary | Confidence |
|-----|----------------------|---------|------------|
| C1  | `.git/HEAD:1` (worktree branch `feat/ai-216-citation-eval-2142` at `61ba873dc`, PR `#1774` `headRefName`) | Worktree branch for PR `#1774` is `feat/ai-216-citation-eval-2142` targeting `feat/demo-164-chat-grounding-provenance-0900`; `feat/demo-216-citation-eval-2142` does not exist. | High |
| C2  | `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`) | Parent branch advanced by 2 non-overlapping commits (`71f5c9f9b6` `#154`, `243764945e` `#116`) above `61ba873dc`'s base `08c36e4dc8`. | High |
| C3  | `src/core/src/zava_forward/core/regulatory_chat.py:1` & `src/core/src/zava_forward/core/regulatory_eval_gates.py:1` | No `regulatory_assistant.py` exists in the repository; `#216` core implementation resides in `regulatory_chat.py` and `regulatory_eval_gates.py`. | High |
| C4  | `src/agents/src/zava_forward/agents/regulatory_gates.py:116-160` | `grade_answer` requires exact `actual.get("cards") == expected["cards"]` for `answer_contract`, and `evaluate_answers` requires `answer_contract and citation_validity` for `refusal_accuracy` on `answer` cases. | High |
| C5  | `src/agents/tests/regulatory_gate_fixture.py:161-172` & `src/agents/evals/regulatory_gates_results.json:1` | Frozen `regulatory-chat-v1` single-card oracle in `src/agents` expects exact 10 card keys without `provision_ids`. | High |
| C6  | `src/core/src/zava_forward/core/regulatory_chat.py:399-428` | Commit `61ba873dc` unconditionally added `provision_ids=list(card["provisions"])` at line `410` in `RegulatoryChat.bundle()`, causing all 4 `src-agents` CI test failures. | High |
| C7  | `src/core/src/zava_forward/core/regulatory_eval_gates.py:785-793`, `1043-1077`, `1615-1635`, `1861-1865` | `regulatory_eval_gates.py` already resolves single-card and single-provision-per-source card linkage without `provision_ids`, requiring `provision_ids` only when `len(cards) > 1` and a referenced `source_id` has multiple provisions in `sources`. | High |
| C8  | `src/core/tests/test_regulatory_eval_gates_216.py:2429-2509` | `test_c11` tests `provision_ids` specifically on a 2-card bundle sharing multi-provision source `"synthetic"` (`synthetic@v1#0001` and `synthetic@v1#0002`) and verifies mid-loop `>2`-card refusal clearing. | High |
| C9  | `src/core/src/zava_forward/core/regulatory_eval_gates.py:2443`, `3999` | `evaluate_citation_and_refusal_gates` and `compare_chat_against_rule_cards` are exported; aliasing `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` supports both names cleanly. | High |
| C10 | `src/agents/pyproject.toml:34-43` & `.github/workflows/src-ci.yml:88` | `src-agents` CI executes `python -m unittest discover -s tests -v` with `tests/` as an import root; `src/agents` needs zero file edits. | High |

## Synthesis and Convergence Recommendation

### Alternatives Evaluated

1. **Selected Recommendation — Emit `provision_ids` in `RegulatoryChat.bundle()` only when disambiguating multi-card shared-source bundles (`len(result["cards"]) > 1` with `>1` provision for a referenced `source_id`), plus export `compare_chat_against_deterministic_rule_cards` alias in `regulatory_eval_gates.py`**:
   * Preserves the exact frozen 10-field `regulatory-chat-v1` card envelope (`id`, `status`, `approved_by`, `approved_on`, `effective`, `exercise`, `link`, `safe_default`, `clock`, `source_freshness`) across all single-card and distinct-source bundles (`C4`, `C5`, `C6`), restoring 100% pass rate across `src/agents` (including byte-for-byte parity with `src/agents/evals/regulatory_gates_results.json`) with zero edits to `src/agents`.
   * Preserves exact per-card `provision_ids` linkage (`RV-023` / `test_c11`) whenever `len(result["cards"]) > 1` and multiple provisions in `sources` share a card's `source_id`, matching `_active_cards_link_provisions` (`regulatory_eval_gates.py:1062-1065`) 1-for-1 (`C7`, `C8`).
   * Adds `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` in `regulatory_eval_gates.py` and regression coverage in `test_regulatory_eval_gates_216.py` verifying both single-card envelope compatibility (`"provision_ids" not in card`) and multi-card shared-source `provision_ids` disambiguation (`C9`).
2. **Rejected Alternative A — Modify `src/agents` (`expected_card` in `regulatory_gate_fixture.py` and `evals/regulatory_gates_results.json`) to expect `provision_ids`**:
   * Rejected because it mutates an independent downstream regression oracle and a committed 60,000-home evaluation snapshot (`src/agents/evals/regulatory_gates_results.json`), widens the PR footprint into `src/agents`, and weakens backward compatibility of the `regulatory-chat-v1` card contract (`C4`, `C5`).
3. **Rejected Alternative B — Weaken `_REFUSAL_PATTERNS` around `"duty is satisfied"` in `regulatory_eval_gates.py`**:
   * Rejected because `src-agents` does not call `regulatory_eval_gates.refuse_question`, none of the 6 failing `src-agents` cases had `actual["kind"] == "refused"`, and weakening `"duty is satisfied"` would introduce false negatives on compliance-determination prompts (`C3`, `C4`, `C8`).

### Current Decisions, Risks, and Planning Readiness

* **Accepted decisions**:
  * D1: Keep PR `#1774`'s checked-out branch `feat/ai-216-citation-eval-2142` and rebase it onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`) (`C1`, `C2`).
  * D2: Update `RegulatoryChat.bundle()` in `src/core/src/zava_forward/core/regulatory_chat.py` to attach `provision_ids` on cards only when `len(result["cards"]) > 1` and a card's base `source_id` maps to multiple provisions in `sources`, keeping standard `regulatory-chat-v1` cards free of `provision_ids` (`C5`, `C6`, `C7`, `C8`).
  * D3: Export `compare_chat_against_deterministic_rule_cards` alias in `src/core/src/zava_forward/core/regulatory_eval_gates.py`, update `src/core/README.md`, and add focused regression assertions in `src/core/tests/test_regulatory_eval_gates_216.py` verifying exact `src/agents` single-card contract compatibility alongside multi-card disambiguation (`C8`, `C9`).
* **Unresolved decisions / blockers**: None for implementation (`OwnerGateAgreement`, live staff trial, and `BRD OD-51` remain explicit repository-level human governance boundaries for `#216` as a whole, so the commit uses `Refs #216`).
* **Potential further research**: None required.
* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`

## Self-Check

* [x] Research brief, parameters, extension provenance, participation, and direction controls recorded.
* [x] Complete three-wave cycle (Wider, Deeper, Contrarian) executed in read-only mode before synthesis.
* [x] Every research question (`Q1`–`Q4`) answered with `C1`–`C10` `path:line` evidence.
* [x] Alternatives evaluated with explicit rejection rationale and one convergence recommendation selected.
* [x] Zero production/test files or git branches modified during `rpi-research`.

