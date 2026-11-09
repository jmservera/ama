# Research: assistant release/serving integrity and independent-worker race coverage (#107)

Task `assistant-release-integrity-107`, base add72cc9013ab84a36a240e635cc4417dae714d3, branch `fix/assistant-release-integrity-107`, target main. Research disposition: executed (code, tests, issue and PR history read; no live, provider or Azure action). Planning Readiness: Ready.

## Owner scope and priority (2026-11-07)

Maximise demo throughput: employees get real AI assistance with a clear visible line between model draft/recommendation, deterministic rule and human decision. The five proposed L2/L3/L4 responsibilities are proposals, not operationally accepted. Parent #104 integration PR1170 already merged; this is a scoped #107 follow-up. No attestation, authority, approval or real-platform evidence may be manufactured.

## Issue 107 state read (gh issue view 107, 2026-11-07)

Open. Unticked: C6 (actual release record/approver), C8 (authoritative serving attestation), C10 (independent SQL worker/race/restart), C13 (delivered-build CON-009/AC-057), plus tokenomics C16 (usage attribution). Ticked by earlier merged work: registry/allowlist/trigger, role denial, purpose principal off by default, SQL ownership of identity/dedupe/leases, no controlled writes, denial with zero calls, recheck through claim/dispatch/completion/list/export, routine-vs-material change, default-off authority, metadata is not inference authorization, C15 per-assistant call bounds, C17 forecast.

Linked merged PRs: #287 (release admission, legacy dispatch gating, returned-model check), #301 (dispatch worker), #315, #863 (per-assistant call bounds), #915 (forecast), #1095 (per-assistant usage attribution), #913/#1170 (controlled records unchanged), #1166 (status record). Closure audit comment 2026-10-31 lists C10 as unmet because "the complete old-image rollback/restart/finite-allowance and authoritative material-mismatch bundle is not demonstrated".

## Already delivered (proved by reading code and running tests on this base)

Release module `src/core/src/zava_forward/core/assistant_release.py` (admission, record, change, invalidation, events). Tests in `src/api/tests/test_assistant_release.py` (45 pass before this task):

| Control | Existing test |
| --- | --- |
| Absent/expired/suspended/revoked deny, zero calls, revoked terminal | `test_absent_release_denies_with_zero_calls_and_retains_denial`, `test_expired_suspended_revoked_deny_and_revoked_is_terminal` |
| Material mismatch denies, routine case edit only stales | `test_material_mismatch_denies_but_routine_case_edit_only_stales`, `test_each_binding_mismatch_denies_reactive_and_proactive_with_no_calls` |
| Revocation on an independent connection, then restart | `test_revocation_on_independent_connection_blocks_dispatch_and_reliance` |
| Revocation between claim and completion quarantines | `test_revocation_between_claim_and_completion_quarantines` |
| Returned model differs: quarantine and suspend | `test_unexpected_serving_model_quarantines_and_suspends_release` |
| Live provider needs actual authorisation with serving proof | `test_live_provider_needs_actual_release_with_serving_proof` |
| Endpoint rollback does not revive history | `test_endpoint_rollback_does_not_revive_historical_release` |
| Allowance: no restart reset, no expiry extension, last-reservation race | `src/api/tests/test_assistants.py` `test_allowance_no_restart_daily_reset_or_expiry_extension`, `test_last_budget_reservation_race` |
| Suspend/review/restart overlaps | `src/api/tests/test_continuity*.py` |

Disposable-SQL-Server variants of the assistant classes exist in `test_assistants.py` (gated on `ZF_SQL_SERVER`) and are skipped here: they are not run and SQLite results are not counted as SQL Server acceptance.

## Confirmed gap

No single test combined, on genuinely independent connections/workers: release revoked after a claim consumed finite allowance, concurrent post-revocation dispatch/invoke by several independent workers, completion of the in-flight claim, and a restart with a larger configured allowance and later expiry. Each piece existed separately; the combined C10 bundle (no revived approval, no replenished allowance, no unauthorised call, in-flight result quarantined) was not asserted anywhere.

## Not engineering gaps (human/live gates, no code change)

* C8 attestation: `response.model` and the deployment alias are not attestation; the code correctly requires `actual` evidence class and denies live use otherwise. An authoritative platform attestation source and an authorised approver are external. No code added.
* C6, C13: actual approver (`ZF_ASSIST_RELEASE_APPROVERS` unset), real AI, actual SQL Server and Azure evidence under CON-009/AC-057.
* C16 residual: historical/resident joins and accepted-output evidence are separate metering work, already covered by merged PRs; not redone.

## Planning Readiness

Ready: add one regression test only; no production change.
