<!-- markdownlint-disable-file -->
# Plan Critique: Issue #163 Proposal-Route Privacy Gate and Pre-Scheduled Memory Expiry Enforcement (Cycle 5)

## Inputs and Criterion Boundary

* Task ID: issue-163-chat-privacy-region-c5
* Parent Task ID: issue-163-chat-privacy-region-c4
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c5-phase-details.md
* Evidence considered:
  * .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c4-review.md (`RV-001`, `RV-002`)
  * src/api/src/zava_forward/api/server.py (`POST /api/chat/threads/<tid>/proposals` and adjacent `/api/chat/*` routes)
  * src/core/src/zava_forward/core/chat_privacy.py (`memory_status`, `prompt_memory`, `purge_expired`, `purge_retention`, `decision`)
  * src/core/src/zava_forward/core/chat_isolation.py (`memory_for`, `build_prompt`)
  * src/api/tests/test_chat_panel.py, src/core/tests/test_chat_privacy.py, and src/core/tests/test_chat_memory.py
* Criterion boundary: Focused validation tier (`src/core` and `src/api` unit tests, `ruff`, `mypy`, `git diff --check`; `tools/rpi-checks.py --all` and `infra/` Bicep changes excluded by caller direction; Issue #163 criterion 2 remains gated on human DPO/Legal sign-off).

## Execution Status and Verdict

* Critique execution status: Complete
* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 1 Medium (`PC-001`), 0 Low

## Coverage Assessment and Limitations

* `RV-001` coverage: `P01-T01` and `P01-T02` accurately gate `POST /api/chat/threads/<tid>/proposals` on `c.privacy._require()` before `app.assistants.invoke(...)` and `s.chat_add_message(...)`, matching `POST /api/chat/threads` and `POST /api/chat/threads/<tid>/messages` / `ask`. Data-subject rights and cleanup routes (`archive`, `delete`, `opt-out`, `memory/<id>/delete`, `memory/erase`, `global`, `task`) appropriately remain accessible without `_require()`, and `memory/<id>/edit` already calls `self._require()`.
* `RV-002` coverage: `P01-T01` and `P01-T02` accurately restore per-row `expires_at` enforcement in `ChatPrivacy.purge_expired()` while keeping `expires_at IS NULL` rows untouched, keeping `decision()["retention_days"] = None` and `purge_retention()["applied"] = False` when unapproved or under invalid provider settings, and respecting `PortabilityTests` SQL-keyword bans.
* Adjacent memory-prompt seam (`PC-001`): Inspection of `ChatPrivacy.memory_status()` and `ChatPrivacy.prompt_memory()` (called by `ChatIsolation.build_prompt()`) surfaced one adjacent gap when previously opted-in memory is read after provider/privacy approval becomes invalid.
* Limitations: Static/read-only inspection of supplied candidate plan, phase details, and source files.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: `ChatPrivacy.memory_status()` and `prompt_memory()` remain active for previously opted-in users after privacy or model-provider approval becomes invalid

* Related IDs: `FR-01`, `P01-T01`, `P01-T02`
* Evidence: In `src/core/src/zava_forward/core/chat_privacy.py`, `memory_status(user, task="")` computes `active` solely from `gl and opted and tk` without checking `self.decision()["approved"]`, and `prompt_memory(user, task="")` checks `self.memory_status(user, task)["active"]`. If a user opted in and saved memory while approved, and `CHAT_PROVIDER_REGION="eastus"` or `CHAT_DPIA_REF=""` subsequently invalidates `self.decision()["approved"]`, `GET /api/chat/memory/status` still reports `active=True` and `ChatIsolation.build_prompt()` / `privacy.prompt_memory()` still returns stored preference items for prompt construction.
* Impact: Direct callers of `prompt_memory()` / `ChatIsolation.build_prompt()` and UI consumers of `GET /api/chat/memory/status` see memory as active for model prompt injection even when model-provider residency or privacy approval has failed closed.
* Smallest useful change: In `ChatPrivacy.memory_status(user, task="")`, evaluate `d = self.decision()` and require `d["approved"]` for `active=True` after preserving existing switch-reason precedence (`not gl` -> `"disabled by an administrator"`, `not opted` -> `"not opted in"`, `not tk` -> `f"disabled for task {task}"`, `not d["approved"]` -> `"chat and memory privacy or provider position is not approved"`), so `prompt_memory()` automatically returns `[]` whenever `not d["approved"]`; add a deterministic assertion in `src/core/tests/test_chat_privacy.py`.
* Action owner: Primary planner / implementer (`direct planner correction`)
* Resolving evidence: `ChatPrivacy.memory_status()` returns `active=False` and `ChatPrivacy.prompt_memory()` returns `[]` for a previously opted-in user when `CHAT_PROVIDER_REGION="eastus"` or `CHAT_DPIA_REF=""`, while `test_chat_memory.py` switch-reason tests continue to pass.
* User decision required: No (compatible direct planner correction aligned with confirmed fail-closed requirement).

## Closeout

* Highest-impact finding: `PC-001` (Medium)
* Action owner: Primary planner (`rpi-plan`)
* Smallest next action: Apply `PC-001` directly to `P01-T01` and `P01-T02` in `c5-plan.md` and `c5-phase-details.md`, record disposition in `## Critique Disposition`, mark plan `ready`, and advance to `rpi-implement` without repeating critique.
* User response required: No
