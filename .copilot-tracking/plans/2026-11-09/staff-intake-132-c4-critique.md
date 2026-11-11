<!-- markdownlint-disable-file -->
# Critique C4 (final candidate, executed once)

* Execution: executed once 2026-11-09, read-only rubber-duck sub-agent, before any test or source change. Verdict: Revise. Five blocking and one non-blocking finding. No user decision was needed. No second critique will run for C4.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | Existing unbound receipts stay stranded | Accepted in part. The branch is local and unpushed with synthetic data only, so no deployed unbound receipt exists. No new waiver or authority is added. The view shows an explicit blocker for any unbound receipt and a test covers it. Residual limit recorded in the handoff. |
| PC-002 | `current_context` can return None | Accepted. `_binding` returns 409 when there is no current scope; test by changing the design version. |
| PC-003 | Replay depends on the current pack | Accepted. Replay is matched against the stored receipt (its own measure and labels) before current-pack validation; tests for a removed measure case are covered by a changed pack and a lost-response retry. |
| PC-004 | Independence test cannot prove its claim | Accepted. Each contributor is tested on a fresh Submitted record using quality-role identities (pam, quil) and asserting the independence message; independent acceptance and replacement run separately. Worker identity is checked through `_independent` directly. |
| PC-005 | Cross-process stale-check race | Rejected for C4. It needs a shared persistence hook outside the 132 owned files and was already a recorded limit; in-process capture is atomic under the store lock. Remains an open limit. |
| PC-006 | Duplicate notice not order-scoped | Accepted. Notice is keyed by order and written into an always-present live region after paint. |
