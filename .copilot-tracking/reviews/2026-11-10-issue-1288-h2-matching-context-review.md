<!-- markdownlint-disable-file -->
# Review: issue 1288 H2 matching-context observation

Readback `date -u` 2026-11-10T00:26Z. One Review, by the author; independent exact-head evidence assessment is still required before any publication. Changes: `.copilot-tracking/changes/2026-11-10-issue-1288-h2-matching-context-changes.md`.

## Outcome

* Execution: ONE admission, ONE H2 test, executed once, no retry. Outcome: H2 confirmed in this observation. With a matching independent provider context and a release active before construction, fresh stores and services (B, C) read the same persisted flag `review-suggested`, the same cited IDs, role projection and task state as the first service, and no release row changed.
* Discrimination: together with H1 (default `Ai` produced `release-denied`, and a later revoke), the evidence supports that the H0 status difference came from the missing release context of the default `Ai`, not from lost or changed persisted IDs. This is an inference from two separate observations on different bases (H0 and H1 on a859, H2 on main ddeebd01); H2 does not retroactively attribute the H0 or H1 cause.
* The H1 revoke of `fx-quality-evidence` was NOT reproduced under the matching context, and it was not triggered by `open_store`, `detail`, `release_reference` or `sensors` with the matching provider. Which call revoked it under the default `Ai` remains unestablished (H2 deliberately did not run that variant). Open finding for later user-selected work, not classified as a defect or as intended.

## Limits

* Same-process independent reopen, not an OS process restart; the first service stayed alive.
* Synthetic fixture and `CapturingProvider` only: not an actual model, not a release approval, not an authority holder (OQ-017 remains a gap). Real-provider simulation stays OFF.
* The 30 existing MSSQL cases are not a full class or gate; hosted CI runs no Quality MSSQL class.
* Excluded: unmerged 891 work; main after ddeebd01.
* Whole #1288, #440 and live-model criteria remain open. E11 success; E12 and E13 unused.

## Findings

* No material open finding against the plan execution; the harness prerequisites gate passed and the critique's three blocking items were applied.
