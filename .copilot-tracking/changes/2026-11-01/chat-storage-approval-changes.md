<!-- markdownlint-disable-file -->
# Changes: Chat storage approval (synthetic-data demo)

* Task slug: chat-storage-approval
* Date: 2026-11-01
* Branch: chore/chat-storage-approval

## Repository changes

* New `docs/reference/research/chat-demo-storage-approval-2026-11-01.md` (owner demo-only decision, refs, 30-day retention); index row, append-only log entry, DPIA Status pointer.
* `infra/modules/containerapps.bicep`, `infra/main.bicep`: five scalar chat parameters, default empty; api env added only when all four refs are set. Agents app unchanged.
* `infra/main.test.bicepparam`: demo values. `infra/resident-demo.bicep`: parameters with demo defaults and five env entries.
* Tests: `test_bicep_policy.py` (2 new), `test_resident_demo_deploy.py` (1 new).

## Validation

* `az bicep build` main, resident-demo, main.test.bicepparam: ok.
* `infra/tests` full discover in a venv with the src distributions: 502 tests, only `test_pipeline` fails to import (pre-existing, unrelated to this change; the same module failed to import on the base). `test_chat_privacy`, `test_regulatory_privacy`: 34 pass.
* Focused gate `tools/rpi-checks.py --changed`: BLOCKED twice, first by a dirty/ignored scratch tree (cleaned), then by the global heavy-resource lock held by another session's `--all` run (timeout 600 s, then a queued run that was stopped). Not passed; no receipt exists.

## Live (resource group ama; nothing deleted)

Private backups (0600) in the session folder: full `az containerapp show` and revisions for the two apps, all jobs.

* Dry run: offline diff of the exact backup against the five settings. Both apps: adds only the five CHAT_* names, changes none. `az containerapp update` has no what-if; `resident_demo_deploy.py` needs an interactive terminal and was not used.
* Applied `az containerapp update --set-env-vars` (non-secret refs and 30) on `ca-cutover-test-demo-api` (new revision `--0000007`) and `ca-resident-demo` (`--0000006`). Not changed: `ca-cutover-test-api`, `ca-cutover-test-agents`.
* After versus before: only the five env entries added. Ingress, registries, secret names, image digest, identity, min replicas 0 (max 4 and 1) unchanged. The resident app's two secretRef env entries gained an empty `value` field in the API representation; secretRef is unchanged. All eight jobs still Manual.
* Playwright (headless Chromium, test users read inside automation, no secret printed):
  * Employee: unauthenticated `/api/chat/status`, `/api/chat/threads`, `/api/me` return 302 to sign-in (the app is configured to redirect, not 401). Signed in: `/api/chat/status` storage_approved true, retention "30 days"; threads 0 to 1 after one UI message; owner reads it (200, 2 messages); the same thread id unauthenticated returns 302; no "Chat storage is not approved" text in the panel or reply. Chat tables exist (a thread was stored).
  * Resident: login 200; no "not approved" text; the app has no chat storage routes (404), so no thread is stored there.
* Not verified: cross-user isolation on the live site. Only one employee Entra identity is available and the resident test user cannot sign in to the employee app, so a second signed-in user could not be tested. Isolation remains covered by `src/api/tests/test_chat_isolation.py`. The UI notice text (warning and retention line) was not asserted in the DOM.
* One synthetic thread remains in the demo database (expires per the 30-day retention).
