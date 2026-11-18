<!-- markdownlint-disable-file -->
# Implementation Details: Issue #163 Proposal-Route Privacy Gate and Pre-Scheduled Memory Expiry Enforcement (Cycle 5)

* Task ID: issue-163-chat-privacy-region-c5
* Parent Task ID: issue-163-chat-privacy-region-c4
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan.md
* Date: 2026-11-15

<!-- rpi:phase id=P01 -->
## P01: Enforce Proposal-Route Privacy Gate, Restore Per-Row Memory Expiry Purging, and Verify (`RV-001`, `RV-002`)

* Initial phase direction: Apply the two surgical fixes in `server.py` and `chat_privacy.py` and verify across both memory and SQLite store implementations plus HTTP routes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Gate `/api/chat/threads/<tid>/proposals` on `c.privacy._require()` and honour recorded `expires_at` in `ChatPrivacy.purge_expired()` (`RV-001`, `RV-002`)

* Context and evidence:
  * In `src/api/src/zava_forward/api/server.py`, `if parts[2] == "proposals":` currently resumes `tid`, checks `if not t["case_id"]:`, calls `app.assistants.invoke(...)`, and calls `s.chat_add_message(...)` without checking `c.privacy._require()`. Calling `c.privacy._require()` before `app.assistants.invoke(...)` and `s.chat_add_message(...)` raises `ChatNotApproved` (caught by `except (ChatForbidden, ChatNotApproved, PermissionError) as e: return self._json(403, {"error": str(e)})`) whenever DPO/Legal references or model-provider settings become invalid, matching `POST /api/chat/threads` and `POST /api/chat/threads/<tid>/messages` / `ask`.
  * Wait — check error ordering on `if parts[2] == "proposals":`:
    * Note that `thread = s.chat_resume(u, tid)` already ran immediately above (checking thread ownership and case visibility, and regulatory thread access). Inside `if parts[2] == "proposals":`, calling `c.privacy._require()` right at the top ensures unapproved privacy/provider posture fails closed with HTTP `403` before capability validation, proposal queueing, or message persistence.
  * In `src/core/src/zava_forward/core/chat_privacy.py`, `ChatPrivacy.purge_expired(self, now=None)` calls `repo.purge_memory(now or self._now())`, which runs `DELETE FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?`. Removing `if not self.decision()["retention_days"]: return 0` restores `HEAD`'s storage-limitation invariant:
    * Items created without an approved retention period (`retention_days is None`) have `expires_at = None`, so `purge_expired` never deletes them.
    * Items created under an approved retention period carry a concrete `expires_at` timestamp, and `purge_expired` deletes them once `expires_at < now` even if `CHAT_PROVIDER_REGION`, `CHAT_MODEL_TRAINING`, `CHAT_DPIA_REF`, or `ZF_DATA_PROCESSING` subsequently blocks creating new data.
    * Update the docstring of `purge_expired` to clarify both invariants clearly (`"Delete memory past its recorded expires_at timestamp. Items created before a retention period is approved have no expiry and are untouched."`), and align `src/core/README.md` if needed.
* Completion expectations:
  * `server.py` enforces `c.privacy._require()` in `if parts[2] == "proposals":` before `app.assistants.invoke` and `s.chat_add_message`.
  * `chat_privacy.py` `memory_status()` requires `self.decision()["approved"]` after preserving `not gl` / `not opted` / `not tk` reason precedence so `prompt_memory()` returns `[]` when unapproved (`PC-001`).
  * `chat_privacy.py` `purge_expired()` purges rows with `expires_at < now` regardless of current write-approval state, while leaving `expires_at IS NULL` rows untouched and keeping `PortabilityTests` green (no SQL keywords in `chat_privacy.py` — note: keep SQL words like `SELECT`/`DELETE FROM`/`INSERT INTO`/`UPDATE` followed by `chat_` out of `chat_privacy.py` code/docstrings per `PortabilityTests.test_chat_privacy_has_no_own_sql_or_connection`!).

<!-- rpi:task id=P01-T02 -->
### P01-T02: Update deterministic unit assertions in `test_chat_panel.py` and `test_chat_privacy.py` and run Focused validation (`RV-001`, `RV-002`)

* Context and evidence:
  * In `src/api/tests/test_chat_panel.py`, expand `test_proposal_request_uses_the_assistants_path_and_checks_role`:
    * On the existing case thread `tid`, patch `os.environ` with `{"CHAT_PROVIDER_REGION": "eastus"}` and separately `{"CHAT_DPIA_REF": ""}`, call `self.api(ROLE, f"/api/chat/threads/{tid}/proposals", {"capability": "assessment-preparation"})`, assert HTTP `403`, and verify `self.api(ROLE, f"/api/chat/threads/{tid}")[1]["messages"] == []` and `self.app.assistants.listing(self.user(ROLE), "ZF-1")["proposals"] == []` (or proposal count unchanged before vs after).
  * In `src/core/tests/test_chat_privacy.py`:
    * In `test_no_expiry_without_retention`: verify that a memory item added without retention (`expires_at is None`) is NOT purged by `c.purge_expired("9999-01-01T00:00:00+00:00")` (`0`), whereas a memory item added while retention WAS approved (`expires_at` recorded) IS purged once past `expires_at` even when called via an unapproved or invalid-provider `ChatPrivacy` instance (`CHAT_PROVIDER_REGION="eastus"`, `CHAT_DPIA_REF=""`, or `ZF_DATA_PROCESSING="actual"`), leaving the `expires_at is None` item intact (`len == 1`).
* Completion expectations:
  * Focused unit suites (`src/core` privacy/provider tests, `src/api` `test_chat_panel.py`, `test_assistants.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, `tools/rename-zava-tests.py`), `ruff check`, `ruff format --check`, `mypy`, and `git --no-pager diff --check` all exit `0`.
