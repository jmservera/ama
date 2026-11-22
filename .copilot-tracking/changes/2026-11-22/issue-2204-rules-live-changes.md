# Changes: issue 2204 rule actions live (2026-11-22)

Status: implemented. Tier: focused (no source change). Refs #2204.

## Added

* `docs/reference/research/issue-2204-rule-actions-law-store-live-2026-11-22.md` (evidence note), index row in `docs/reference/README.md`, entry in `docs/reference/log.md`.
* Evidence under `.copilot-tracking/evidence/2026-11-22/issue-2204-rules-live/` (script, JSON, two masked screenshots, run log).
* RPI artifacts for task `2204-rules-live-20261122T134010Z`.

## Azure changes (az only)

* Container `law-snapshots` in `stcutovertestrzsrg` (kept).
* Env vars `ZF_LAW_STORE=mssql`, `ZF_LAW_BLOB_ACCOUNT_URL`, `ZF_LAW_BLOB_CONTAINER` on `ca-cutover-test-demo-api`, revision 0000050 (kept). Revision 0000048 failed activation; 0000049 was the rollback. The API was unreachable for about eight minutes.
* Law tables created by the app in the demo SQL database; synthetic draft card `exercise-rules-live-2204` v1 (append-only, remains).
* Throwaway Entra user created and deleted three times (diagnosis of MFA block); Graph shows none. Test account restored to ProgrammeManager only (verified).

## Divergences

* A second identity for a distinct-owner approval could not sign in (MFA registration blocked, TAP refused, resident account in another tenant), so the plan's B-author phase became a single-account proof.

## Per-criterion table

| Criterion | Proven | Unproven |
| --- | --- | --- |
| 503 cause found and law store enabled | Yes: missing `ZF_LAW_STORE`; GET `/api/law/cards` 200 | First failed start's message unread (Log Analytics blocked) |
| RuleAuthor action live | Yes: propose 201, draft v1, role `rule_author` | |
| RuleOwner action live | Reaches domain gates; 409 refusals | Successful approve, activate, hold, release, retire (needs a distinct second identity) |
| Each role sees only permitted views; admin sees all | Prior notes plus this note for capability roles | Successful RuleOwner action |
| One wrong-role denial; no credentials printed or stored | Yes: three 403 denials; literal scan clean | |
| Evidence recorded | Yes | |
