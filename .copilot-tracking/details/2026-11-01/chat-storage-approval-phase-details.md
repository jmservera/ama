<!-- markdownlint-disable-file -->
# Phase details: Chat storage approval

## P1 Decision record

Create `docs/reference/research/chat-demo-storage-approval-2026-11-01.md` with Decision, References, DPIA reference, Lawful basis, Notice, Retention, Prohibited use headings; index row; append-only log; DPIA Status pointer.

## P2 Infra

* `containerapps.bicep`/`main.bicep`: params chatDpiaRef, chatLawfulBasisRef, chatNoticeRef, chatRetentionRef (default ''), chatRetentionDays (default 0); api env appended when all four refs set.
* `main.test.bicepparam`: demo values; other bicepparam files untouched.
* `resident-demo.bicep`: five params with demo defaults, five env entries.
* Tests: `test_bicep_policy.py` (conditional, api-only, defaults empty, refs resolve to record headings, min replicas 0), `test_resident_demo_deploy.py` (env, defaults, scale, secrets).

## P4 Live

Backup `az containerapp show` JSON to the session folder (0600), `az containerapp update --set-env-vars` (names/values are non-secret refs), compare before/after env names, secrets, identity, registry, ingress, scale.

## P5 Verify

Playwright with test users read inside automation only.
