<!-- markdownlint-disable-file -->
# Critique: #111 sensor review draft plan (one pass)

Independent rubber-duck critique, 2026-11-10. Verdict: Revise, then proceed. Critique executed once, not repeated for this task. All findings applied directly; none conflicts with a confirmed owner decision.

| Finding | Severity | Disposition |
| --- | --- | --- |
| Role-only gate omits current staff row and `case_ids`/`areas` scope checks (`assistants.authorize`) | Blocking | Applied: gate 1 mirrors authorize; tests for revoked, malformed, out-of-scope users |
| Reads expose derived findings after consent withdrawal or unknown consent | Blocking | Applied: read rechecks consent and fails closed (`consent-withheld`); tests added |
| JSON audit/save ordering and SQL pending-audit or post-commit outcomes unspecified | Blocking | Applied: save then audit, backend-specific recovery, JSON non-atomic residual documented, `CommittedReloadError` treated as unknown and idempotent retry; failure tests added |
| Public write accepting caller signal and policy conflicts with "approval only in synthetic tests" | Blocking | Applied: production entry is `draft_from_retained` with server policy only; `_record_draft_synthetic` is a private test seam |
| POST dispatch performs `_case` before the act branch, leaking existence and returning case detail | Blocking | Applied: `sensor-draft` dispatched before `_case`, returns draft result directly; tests for existing and missing ids |
| Served replay `existing:true` impossible with unapproved policy; refusal precedence not always `NO_APPROVED_RULE` | Blocking | Applied: replay tested on the seam only; served refusals asserted per fixture by precedence |
| Future-dated readings after `as_of` can yield REVIEW | Blocking | Applied: `FUTURE_READINGS` guard inside new module; existing analysis unchanged; test added |
| MSSQL fixture keys off `ZF_SENSOR_MSSQL` | Blocking | Applied: set both flags, construct explicitly, assert backend type |
| Browser cannot know the flag without a request; conflicts with "no extra request when off" | Blocking | Applied: single GET from the sensor panel returning `disabled`; acceptance reconciled; no `/api/me` change |
| UI text-rendering test uses tampered summary that digest check withholds | Non-blocking | Applied: digest-valid fixture; tamper tested separately |

No significant or divergent issue needs a user decision.
