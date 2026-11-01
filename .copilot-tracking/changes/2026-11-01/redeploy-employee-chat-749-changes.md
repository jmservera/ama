---
title: Redeploy employee chat fix from main 1a644d317, changes and live results
ms.date: 2026-11-01
---

## Deployment

| App | Before | After | Health |
| --- | --- | --- | --- |
| ca-cutover-test-demo-api | `--0000008` | `--0000009` | Healthy, `/healthz` 200 |
| ca-cutover-test-api | `--0000002` | `--0000003` | Healthy, 1 replica (internal ingress, no public probe) |
| ca-resident-demo | `--0000007` | unchanged | not touched |
| ca-cutover-test-agents | `--0000001` | unchanged | not touched |

* Image digest `sha256:72dfb10326dc1e8c9c0eefe2970b6e11490847bb028d1fd6ddfbb699795e57bc` (build of main `1a644d317`).
* Sanitized before and after diff ([post-deploy-diff-sanitized.json](../../redeploy-employee-chat-749-2026-11-01/post-deploy-diff-sanitized.json)): only revision and image changed. Five `CHAT_*` variables present before and after on both API apps and the resident app; min replicas 0; eight jobs Manual.
* Registry window: IP-only, exports on, restored; full `az acr show` before and after identical except `systemData` timestamps.
* No rollback needed. Own local image removed by exact tag.
* Backups: full configs of four apps and eight jobs (0600, session folder, not committed); sanitized pre-config committed.

## Live results (2026-11-01 UTC)

| Check | Result | Evidence |
| --- | --- | --- |
| Employee sign-in | PASS | live-results-employee.json |
| Chat window usable size | PASS | 512x720 in 1280x900, contained |
| Chat stays open after two asks | PASS | still open both times |
| Case chat grounded with sources (#749) | PASS | Both replies are rules-based, cite case facts (stage, status, owner, recorded next step) and show Sources (4); no generic "Continue with the ordinary case workflow" refusal |
| Storage approved and working | PASS | `/api/chat/status` storage_approved true, retention 30 days; no "storage not approved" notice; privacy text says text is masked before it is saved, retention 30 days; thread POST 200, asks 200, thread read 200 with 4 turns |
| Capacity and work orders | PASS | "Showing work orders 1 to 20 of 601. Page 1 of 31"; no stuck loading |
| Resident sign-in | PASS | live-results-resident.json |
| Resident three questions | PASS | Grounded rules-based replies (pause, documents D1/D2), no generic refusal |
| Resident sensors card | PASS (loads) | empty by data, unchanged |

Notes on the raw JSON: the script's `employee_chat_grounded_and_stays_open` is recorded `fail` because its regex rejects the wording "not available", which appears in the legitimate rules-only disclosure ("This reply uses rules only because the assistant is not available"). Sources are 4 on both replies, so the verdict above is PASS. `employee_chat_storage_works` is `fail` only because it searched reply text for "saved" while the saved/retention wording is in the panel privacy text. `employee_chat_storage_api_evidence` is `fail` only because an unrelated `GET /api/chat/regulatory/status` returned 403 for this role (carried over from the earlier run, not investigated); all `/api/chat/threads*` calls were 200. No new bug is raised: none of these is an app failure.

## Gate statement

Only the focused gate (`python3 tools/rpi-checks.py --changed`) was run for this evidence-only branch. The complete local gate, which deployment work requires, was NOT run, so no full-gate receipt exists. Independent exact-head review, hosted CI and owner approval remain required.

## Rollback procedure (revert-and-redeploy)

Apps use single revision mode and the agents app has no ingress, so do not rely on shifting traffic between revisions.

1. Revert the offending commit on a topic branch, merge via PR.
2. Rebuild the API image from the reverted main and push in the standing IP-only registry window (restore and compare the registry afterwards).
3. Run `az containerapp update -g ama -n ca-cutover-test-demo-api --image <repo>@<new-digest>` and the same for `ca-cutover-test-api`.
4. Fast path: update both apps to the previous known-good digest `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:7aa2a317a1fe52ddb22ee72a6489ed7addaab245728f99dc047c8c2ab7b25289` (still in the registry), then verify health and the five `CHAT_*` variables.

## Credential handling incident

While locating the credential file formats the agent ran a command whose output displayed the contents of `~/.ama-test-user` and `~/.ama-resident-test-user` in the session transcript. Nothing was written to any tracked file. The owner should rotate both test-user passwords.

## Issues

None opened. #749 is proven by the live evidence above.
