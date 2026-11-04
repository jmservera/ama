<!-- markdownlint-disable-file -->
# Issue 120 research: staff time capture gated on DPIA (2026-11-04)

Task slug: `issue-120-notice-version`. Research disposition: executed (read-only, base `640342230`).

## Already delivered (merged PRs and code)

* PR #408 (merged): bare yes/true/on/1 DPIA values refused; reference gate across request, activation, acknowledgement and recording.
* Earlier work (#267 and the flag-gated module): consultation and notice references, manager request plus different-role enabling, audit events `time_capture_enable_requested`, `time_capture_enabled`, acknowledgement audit, own-entry only, aggregate report with `ZF_TIME_MIN_GROUP` (default 5, floor 2), screens at `#/time` (`web/timecapture.js`).
* Issue ticks: C1 (DPIA reference) and C2 (minimum group). C3 unticked after the 2026-10-31 closure audit.

## Unmet criterion C3: what is code and what is human

* Human/legal and out of reach for code: actual staff notice wording approval, consultation, DPO/administrator ratification. The notice text is a draft (`NOTICE_VERSION = "draft-1"`).
* Code gap found: `ZF_TIME_NOTICE_APPROVED` is a free reference with no link to the wording. The wording and `NOTICE_VERSION` can change in code while an earlier enabling record stays valid, so staff could acknowledge, and be monitored under, wording the approver never saw. The enabling record and audit event name the approval reference but not which wording it covers.

## Smallest coherent slice

Bind the notice approval to the notice version without schema change: require `ZF_TIME_NOTICE_VERSION` to equal `NOTICE_VERSION` (trimmed, exact). The approver states the version they approved; a reworded notice turns capture off until re-confirmed. No SQL, DDL, infrastructure, deployment or security-control change, so the focused tier applies.

## Boundaries kept

* Reference/version presence is not authenticity or approval; human approval stays outside code.
* Off by default; no new data, no per-person reporting, no AI feature, no web UI change (JS reads `notice_approved`, now version-aware, so the existing checklist shows "Missing" with the reason).
