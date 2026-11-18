<!-- markdownlint-disable-file -->

# Task Research: ux-76-hazard-clock-owner-c2-rebase

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                            |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                               |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-research.md  |
| Planning Readiness | Ready                                                                                 |
| Disposition        | executed                                                                              |

## Research Brief

* What to research: Verify branch/PR topology, commit-by-commit 3-way merge conflicts across `6e9eb39de`, `8f8d85342`, and `941806d9d`, AST-level semantic overlap in `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py`, cross-feature visibility interactions between `#116` (`PR #1766`, `243764945`) and `#76` (`PR #1768`), and exact validation selector coverage when rebasing onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`).
* Why it matters: Target parent `origin/feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) advanced from `08c36e4dc` by two commits (`71f5c9f9b` `PR #1772` / Issue `#154`, and `243764945` `PR #1766` / Issue `#116`). Both `#116` and `#76` enforce security/safety projection invariants in `projection.py` and `store.py`; mechanical conflict resolution without inspecting raw-case visibility rechecks could silently weaken `#116`'s Entra/field-level AI output gate on `#76`'s standalone safeguarding items.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` for `ux-76-hazard-clock-owner-c2-rebase`.
* Scope: `08c36e4dc..243764945`, `08c36e4dc..941806d9d`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/taskqueues.py`, and focused test/lint/typecheck runners in `src/core` and `src/api`.
* Non-goals: Pushing to `origin`, running `tools/rpi-checks.py`, or renaming the open `PR #1768` head branch (`feat/ux-76-hazard-clock-owner`).
* Criteria: Every merge-tree conflict mapped with exact `path:line` evidence; semantic vs formatting diffs separated; `#116` + `#76` cross-feature visibility behavior proven on both projected `store.detail()` dicts and raw `store.cases` dicts; focused validation coverage verified.
* Requested outputs: Compact 3-wave synthesis (`C1`–`C8`), convergence recommendation, and planning readiness record.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                          |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1: What are the exact active branch/file paths in this worktree vs prompt shorthand, and which commits conflict on rebase onto `243764945`? Q2: How do `projection.py` and `store.py` conflict, and is there any cross-feature semantic seam between `#116` and `#76`? Q3: What do the caller validation selectors match, and what targeted `#76` + `#116` unit tests must also run? |
| Codebase scope                       | `src/core/`, `src/api/`, `.copilot-tracking/*/2026-11-15/ux-76-hazard-clock-owner*`                            |
| External scope                       | none                                                                                                           |
| Research posture                     | focused                                                                                                        |
| Posture provenance                   | default (bounded rebase continuation with exact parent SHA `243764945ea8f5b292eed0b73ea034b91c3b6e5f` and caller criteria) |
| Explicit limits / deadline           | Focused validation tier (`unittest`, `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`); do NOT run `tools/rpi-checks.py`; do NOT `git push` |
| Edits allowed during research?       | no, research-only                                                                                              |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                   |
| Known constraints / excluded sources | Preserve prior `ux-76-hazard-clock-owner-*`, `c1-*`, and `c1-rebase-*` commits and artifacts intact            |

## Extension Registry and Provenance

| Kind        | Candidate                         | Match and provenance                        | Scoped authority or output contract                   | Selected / skipped reason                                                |
|-------------|-----------------------------------|---------------------------------------------|-------------------------------------------------------|--------------------------------------------------------------------------|
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"`                             | Focused validation tier, noreply author, RPI tracking | Selected automatically                                                   |
| Skill       | `web-design-guidelines`           | Web UI changes only                         | Pre-edit and review checklist for web files           | Skipped: rebase continuation modifies Python `core` modules/tests only   |
| Specialist  | `hve-core-all:rpi-researcher`     | Registered general RPI research lane worker | Independent subagent lane artifact                    | Skipped: tightly coupled 2-file merge-tree + AST inspection fits inline  |

## User Participation and Research Decisions

| Checkpoint  | Questions or no-interaction rationale                                                   | Answers / unanswered | Resulting decision or selected further research       |
|-------------|-----------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------|
| Intake      | Non-interactive session with exact parent tip (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), conflict preservation rules, and validation commands | N/A | Proceed with `focused` posture and `convergence` mode |
| Convergence | All questions answered via read-only `git merge-tree`, AST comparison, and codebase inspection | N/A | Converge on Option A and advance to `rpi-plan` |

## Research Questions

|  # | Sub-question                                                                                                    | Type     | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------|----------|----------|----------|
| Q1 | What are the exact branch and module paths in this worktree, and which commits conflict when rebasing onto `243764945`? | internal | High     | Answered |
| Q2 | What is formatting-only vs semantic in `projection.py` and `store.py`, and how do `#116` and `#76` interact at runtime? | internal | High     | Answered |
| Q3 | What tests match `-p "test_*case_workbench*.py"` vs actual `#76` and `#116` test modules in `src/core` and `src/api`? | internal | High     | Answered |

## Cycle 1 Execution (Wider -> Deeper -> Contrarian)

### Wider Wave

* Verified worktree `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` is checked out on `feat/ux-76-hazard-clock-owner` (`941806d9d`), which is the actual head branch of open `PR #1768` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`, remote tip `243764945ea8f5b292eed0b73ea034b91c3b6e5f`); no branch named `feat/demo-76-hazard-clock-owner-1208` or subpackage `case_workbench/` exists in the repository (`C1`). The actual flat module paths are `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py`.
* Inspected `08c36e4dc..243764945` (`71f5c9f9b` `PR #1772` for `#154` representative expiry views; `243764945` `PR #1766` for `#116` AI output role-visibility recheck and document derivative gating) against `08c36e4dc..941806d9d` (`6e9eb39de` `feat(queues)`, `8f8d85342` `fix(queues)`, `941806d9d` `chore(queues)`).
* Verified `git merge-tree --write-tree 243764945ea8f5b292eed0b73ea034b91c3b6e5f 941806d9d` and `git merge-tree --write-tree 243764945ea8f5b292eed0b73ea034b91c3b6e5f 6e9eb39de` conflict strictly in `src/core/src/zava_forward/core/projection.py` (1 hunk) and `src/core/src/zava_forward/core/store.py` (6 hunks), while `8f8d85342` and `941806d9d` touch neither file and will replay conflict-free (`C2`).

### Deeper Wave

* Ran AST-normalized per-function comparisons across `08c36e4dc`, `243764945`, and `HEAD` (`C3`, `C4`):
  * In `src/core/src/zava_forward/core/store.py`, upstream (`08c36e4dc..243764945`) semantically modified `_clean_doc_ai_metadata`, `_rec_view`, `_visible_cid`, `add_document`, `ai_live_report`, `ai_priority`, `ai_run`, `draft`, `funding_draft`, `publish`, `read_document`, `row`, and `valid`, and applied `ruff format` across the file. Local `#76` (`6e9eb39de`) semantically modified `_open_safety_items`, `_work_context`, `counts`, `detail`, `focus`, `gate_reasons`, `require_safety_clear`, `status_line`, and `summary` (`C4`). The two function sets are completely disjoint: all 6 conflict hunks (`gate_reasons`, `summary`, `_work_context`, `focus`, `counts`, `require_safety_clear`) result from `#116`'s `ruff format` line-wrapping colliding with `#76`'s safety-item edits, while `detail()` and `status_line()` auto-merged cleanly (`C4`, `C5`).
  * In `src/core/src/zava_forward/core/projection.py`, upstream (`243764945`) added `_collect_case_strings`, `_is_high_sensitivity_path`, `_is_plain_iso_date`, `_skip_ai_generated_path`, `contains_withheld_value`, `normalize_visibility_text`, `project_case_visibility`, `withheld_case_values`, and `withheld_scope_values`, updated `redact_staff_detail`, and formatted `hold_notes`. Local `#76` (`6e9eb39de`) updated `hold_notes` so `is_safety_dict` matches both legacy hazards (`"category" in c and "released" in c`) and projected safety views (`c.get("item_kind") in ("hazard", "safeguarding")`), holding `("source", "job", "summary", "reason")` (`C3`).

### Contrarian Wave

* Tested whether simply resolving the single conflict hunk in `projection.hold_notes` is sufficient when `#116` and `#76` execute together (`C6`):
  * **Material cross-feature finding (`C6`):** In `#76`, `Store.detail()` transforms raw `c["safeguarding_items"]` / `c["safeguarding"]` via `workflows.safeguarding_view(...)`, which injects `item_kind="safeguarding"` before `redact_staff_detail(user, d)` calls `hold_notes(d)`. However, `#116`'s `projection.project_case_visibility(user, raw_case)` and `projection.withheld_scope_values(store, user, case_ids)` run `redact_staff_detail(user_dict, deepcopy(dict(raw_case)))` **directly on `raw_case`** from `store.cases` without running `safeguarding_view(...)`. Raw standalone safeguarding items (such as `{"id": "SG-76-1", "priority": "Urgent", "response_due_at": "...", "note": "PRIVATE-SG-NOTE", "summary": "PRIVATE-SG-SUMMARY", "source": "PRIVATE-SG-SOURCE"}` in `test_hazard_safeguarding_clock_owner_76.py:249-258`) lack both `"released"` and `"item_kind"`. If `hold_notes` only checks `("category" in c and "released" in c) or c.get("item_kind") in ("hazard", "safeguarding")`, then `project_case_visibility` leaves `summary`, `source`, `job`, and `reason` unheld on raw standalone safeguarding dicts for non-reason staff (`not can_see_reason(user)`), causing `withheld_case_values` and `withheld_scope_values` to misclassify private safeguarding summaries/sources as visible rather than withheld during `#116` AI output and document-summary gating!
  * **Exact resolution (`C6`, `C7`):** Extending `hold_notes` to also hold `("source", "job", "summary", "reason")` on raw safeguarding item dicts inside `c["safeguarding_items"]` (list) and `c["safeguarding"]` (list, or dict intersecting `SAFEGUARDING_ITEM_KEYS`, without touching passive note-only `{"note": "..."}` canaries or `documents[*]["summary"]`) AND treating `("hazards" | "safeguarding_items" | "safeguarding", ..., "summary")` as high-sensitivity in `_is_high_sensitivity_path` preserves both `#116` field-level Entra/role visibility gating and `#76` safeguarding redaction across raw and projected paths.
* Checked validation test discovery (`C8`): neither `src/core/tests` nor `src/api/tests` contains files matching `test_*case_workbench*.py` (`unittest discover -p "test_*case_workbench*.py"` runs `0` tests because flat modules are named `test_hazard_safeguarding_clock_owner*.py`, `test_data_protection.py`, `test_ai_tasks.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_task_queue_api.py`, `test_workbench.py`). Running BOTH the exact caller command lines AND the targeted `#76` + `#116` `unittest` modules ensures literal step-4 compliance plus real unit-test verification.

## Evidence Register

* `C1`: `src/core/src/zava_forward/core/projection.py:1` and `src/core/src/zava_forward/core/store.py:1` — Worktree `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` tracks `feat/ux-76-hazard-clock-owner` (`PR #1768` targeting `feat/demo-164-chat-grounding-provenance-0900` at `243764945ea8f5b292eed0b73ea034b91c3b6e5f`); `projection.py` and `store.py` live directly under `zava_forward/core/`.
* `C2`: `src/core/src/zava_forward/core/projection.py:130-142` and `src/core/src/zava_forward/core/store.py:165-664` (`6e9eb39de` vs `243764945`) — `git merge-tree` reports conflicts only in Commit 1 (`6e9eb39de`) across `projection.py` (1 hunk) and `store.py` (6 hunks); Commits 2 (`8f8d85342`) and 3 (`941806d9d`) modify disjoint files.
* `C3`: `src/core/src/zava_forward/core/projection.py:133-141` (`HEAD`) vs `243764945:src/core/src/zava_forward/core/projection.py:251-257` — `#76` widened `hold_notes` `private_hazard` to cover `item_kind in ("hazard", "safeguarding")` and keys `("source", "job", "summary", "reason")`; `#116` reformatted `hold_notes` and added `withheld_case_values`, `project_case_visibility`, `withheld_scope_values`, `contains_withheld_value`, and AI summary/draft rechecks in `redact_staff_detail`.
* `C4`: `src/core/src/zava_forward/core/store.py:168-664` (`HEAD`) vs `243764945:src/core/src/zava_forward/core/store.py:260-988` — AST diff confirms zero overlapping function logic in `store.py`: `#116` modified AI/document methods while `ruff format` wrapped `gate_reasons`, `summary`, `_work_context`, `focus`, `counts`, and `require_safety_clear` where `#76` wired `_open_safety_items`, `insights.has_hazard`, `taskqueues.has_open_safeguarding`, `taskqueues.has_open_safety`, and `staff=staff_list`.
* `C5`: `src/core/src/zava_forward/core/store.py:528-540` (`HEAD`) — `#76`'s `Store.detail()` `safeguarding_items` and `hazards` projection auto-merges cleanly alongside `#116`'s changes in `store.py`.
* `C6`: `243764945:src/core/src/zava_forward/core/projection.py:438-505` and `src/core/src/zava_forward/core/taskqueues.py:12-43,157-169` — `project_case_visibility` and `withheld_scope_values` pass `raw_case` directly to `redact_staff_detail` -> `hold_notes` without `safeguarding_view`, so raw standalone safeguarding dicts in `raw_case["safeguarding_items"]` / `raw_case["safeguarding"]` (matching `SAFEGUARDING_ITEM_KEYS` without `"item_kind"` or `"released"`) need safety-field holding in `hold_notes` and high-sensitivity `summary` path classification in `_is_high_sensitivity_path`.
* `C7`: `src/core/tests/test_hazard_safeguarding_clock_owner_76.py:249-319` and `243764945:src/core/tests/test_data_protection.py:451-505` — Existing `#76` tests verify `store.detail()` redaction and passive note-only `{"note": "..."}` canary preservation; `#116` tests verify `redact_staff_detail` role-based AI summary/funding-draft withholding.
* `C8`: `src/core/pyproject.toml:90-100` and `src/api/pyproject.toml:115-123` (`243764945`) — `test_*case_workbench*.py` matches 0 files in both packages; strict `mypy` and `ruff` cover all `src` and `tests` files, and targeted `#76` + `#116` test modules (`test_hazard_safeguarding_clock_owner*.py`, `test_data_protection.py`, `test_ai_tasks.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_task_queue_api.py`, `test_workbench.py`) directly cover the merged code.

## Alternatives and Convergence Recommendation

* **Option A (Selected):** Fetch `origin feat/demo-164-chat-grounding-provenance-0900` (`243764945ea8f5b292eed0b73ea034b91c3b6e5f`), rebase `feat/ux-76-hazard-clock-owner` (`6e9eb39de`, `8f8d85342`, `941806d9d`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` resolving Commit 1's `projection.py` and `store.py` conflicts in `ruff format` style while preserving all `#116` and `#76` logic, harden `projection.py` (`hold_notes` + `_is_high_sensitivity_path`) with a focused regression test in `test_hazard_safeguarding_clock_owner_76.py` so `#116`'s raw-case `project_case_visibility` / `withheld_scope_values` and AI summary/draft gating also withhold `#76` raw standalone safeguarding fields (`summary`, `source`, `job`, `reason`) for non-reason roles, run both the literal step-4 validation commands and the targeted `#76` + `#116` `unittest` suites, and commit the `c2-rebase` changes and dated `.copilot-tracking/` artifacts with `Refs #76` and the Copilot trailer without pushing.
* **Option B (Rejected — Mechanical hunk merge only, ignoring `project_case_visibility` on raw `safeguarding_items`):** Would pass pre-existing isolated tests while leaving raw standalone safeguarding `summary`/`source` values unredacted in `projection.project_case_visibility` and unwithheld in `projection.withheld_scope_values`, creating a subtle cross-feature bypass between `#116` and `#76`.

## Readiness and Self-Check

* Research execution status: Complete (1 full Wider -> Deeper -> Contrarian cycle).
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check:
  * All questions `Q1`–`Q3` answered with `C1`–`C8` `path:line` evidence: pass.
  * Research-only constraint honored (zero tracked source files modified during Research): pass.
  * Ready for parent RPI Agent automatic transition to `rpi-plan`.
