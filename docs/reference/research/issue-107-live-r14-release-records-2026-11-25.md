---
title: Issue 107 five demo release records recorded; capped real-AI batch blocked by private endpoint (Refs #107)
description: The five release records were recorded on the demo API after correcting the approver identity, the harness now recognises an in-force release, and the live batch spent no tokens because the AI account is reachable only through a private endpoint
ms.date: 2026-11-25
---

Scope: synthetic demo, desktop only. Tier FULL (a one-line change under `src/api/checks` plus its test); `rpi-checks.py --all` was not run. Builds on the [thirteenth pass](./issue-107-live-r13-real-ai-harness-2026-11-25.md). Evidence and redacted scripts are in `.copilot-tracking/evidence/107-live-r14/`; no credential or token was printed or stored.

## Release records

* Prior failure: 403 "not an appointed approver". Cause: the demo API runs behind the trusted-proxy provider, which derives the caller's app identity (`email_for(tid, oid)`, a `@entra.invalid` key) and ignores the sign-in UPN. The approver variable held the UPN, so no caller matched. A header check (`X-ZF-CSRF: 1`) is also required for POSTs.
* Fix on the demo estate: the app identity of the demo user was appended to `ZF_ASSIST_RELEASE_APPROVERS` on `ca-cutover-test-demo-api` (new revision `0000076`, healthy, 100% traffic; the UPN entry was kept). No other setting changed.
* Result: `POST /api/assistants/releases` returned 201 for all five assistants (stock-prioritisation, assessment-preparation, funding-evidence, works-resident-coordination, quality-evidence), each `evidence_class: actual`, bound to the live 13-field binding (serving model `gpt-4.1-nano-2025-04-14`), expiry 30 days, owner named as approver. A fresh `GET /api/assistants` shows all five as `"in force"` (`post_releases.json`).
* Limit: the approval attribution is the owner's demo decision of 2026-11-18 and 2026-11-25, not OQ-017/018/019 clearance. The live gate checks for authority holders, fairness and Legal/DPO stay blocked, and nothing here is a real approval.

## Harness

* The harness treated a release as admitted only when it was an object with an `id`. The live listing shows the string `"in force"`, so every assistant would have been blocked. `admitted()` now accepts exactly that marker; the test was updated. `python3 -m unittest tests/test_assistant_real_ai_acceptance.py` (8 tests), `ruff check`, `ruff format --check` and `python3 -m mypy` in `src/api` are clean.
* Live run (`run_harness.py`, hard cap 200000 tokens, 5 calls, 400 prompt and 200 completion tokens per call, USD 1, az-cli token): attempt 1 and attempt 2 each stopped after the first call as `stopped-bad-usage`. Direct status probes show why: first `401 PermissionDenied` (the az login principal had no data-plane role), then, after a temporary `Cognitive Services OpenAI User` assignment propagated, `403 Public access is disabled. Please configure private endpoint.`
* Tokens per assistant: none were consumed. No call reached the model; the harness charged its worst case (600 tokens, USD 0.00012) only in its own accounting, which is not measured usage. Per assistant: all five 0 measured tokens.
* Cleanup: the temporary role assignment was deleted. I did not enable public network access on the AI account or set an operator allowance, because both change a security control or the estate beyond this goal.

## Per-criterion result

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Unproven beyond [r12](./issue-107-live-r12-endpoint-deployment-2026-11-25.md); nothing new here | No real older packaged image run; constructed fixtures and local disposable SQL only |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Partly proven: five actual release records exist on the deployed build with the matching binding and the 201 note says bounded proposals only; real-AI evidence is not produced (zero tokens) | AI account has public access disabled and the VM has no private path; the app's own invoke path is also off until an operator allowance is set. Both need an owner decision |

## Next step

Run the harness from inside the private network (or with an owner-approved temporary network or allowance change) using `run_harness.py`; the five releases are in force and expire in 30 days.
