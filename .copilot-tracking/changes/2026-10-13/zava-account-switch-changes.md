---
title: Account Switch Repair Changes
description: Fixed account selection, private rollout and canonical learning evidence
ms.date: 2026-10-13
---

## Scope and State

Full P01, task zava-account-switch-2026-10-13, automatic Implement.
One critique completed Revise; PC-001 and PC-002 directly disposed.
Owner explicitly asks canonical learning integration after repair.
No source beyond auth/server/test and directly related docs. No role, SQL
data, permission or diagnostic routing mutations.

## Validation Intent

At most three new synthetic methods, existing regression assertions retained
except intentional switch target. All five constant messages tested, denied
requests excluded. Targeted/full MVP and local non-root Docker, then tagged
image update with private app/auth configuration preservation and live
Microsoft chooser redirect plus existing console/central ingestion.
Personal already-signed-in account replacement remains owner acceptance.

## P01-T01: Explicit Chooser and Constant Events

Trusted proxy switches to /sign-in?switch=1 without provider logout. Exact
single-value flag preserves blanks and only appends fixed select_account to
the fixed /app return. All five fixed event triggers follow the approved
auth/CSRF order. Normal sign-out and local password behavior remain unchanged.
Three new auth methods cover hostile/duplicate flags, every constant marker
and denied-request exclusion, and development-mode behavior. Existing switch
assertion intentionally updated; all other existing assertions remain.
Targeted auth 23 passed; JavaScript syntax passed; full MVP suite passed.
Local image built as account-switch-20261013-01; validate runtime before upload.

## Workflow Inspection

Original specified scorer job failed on Copilot provider HTTP403; owner's
attempt 3 succeeded. Other prior-head checks initially never started because
of runner admission/account-policy restrictions, not test failures.
At publication, their owner-started attempt 2 had passed. No source changes
or secret rotation were needed for this recovery.

## P01-T02: Local Image and Preservation Gate

Local read-only UID10001 image health/logo/normal login/chooser tests passed.
First smoke probe raced startup (connection reset); bounded startup retry
resolved it, with named container cleaned after execution.
Initial image-only rollout triggered the preservation gate and restored the
prior image. Private comparison isolated one platform CLI normalization:
an unchanged AUTH_TOKEN_STORE_ROTATION secretRef acquired an empty value field.
No secret value was fetched or changed. Normalize only absent/empty values
on secretRef env entries before the semantic comparison; all env references,
nonempty values, identities, configuration and complete auth remain exact.
Retry same tested image; preserve the initial snapshots privately.

An intermediate ready-revision signal preceded complete replica readiness;
the operator gate restored the prior image rather than accept it. Bounded
replica polling then succeeded. Final tested/deployed digest:
sha256:8cf327786ac2b891a586e78981b4abf0cc9c86313d721cef74ea7fcda80fa599,
tag account-switch-20261013-01, ready serving revision 0000009.
Semantic template, env/secret refs, identity, ingress, registry and complete
Easy Auth comparison passed. Private baseline/rollback/evidence stays outside
Git; no secret values or SQL writes.

Live trace proves fixed switch route bypasses logout, platform forwards
select_account to the configured tenant and preserves callback. Welcome,
health/logo return 200 and anonymous me/cases are blocked. Fresh browser shows
Microsoft Sign in without remembered accounts; not actual session replacement.
New account-picker marker is observed in live console. Centralized actual
ContainerAppConsoleLogs query confirms one sign-in-started and two
account-picker-started events after ingestion, using allowlisted extraction.
Authenticated POST/arrival events proved synthetically, not forged in Azure.

Full MVP ran 289, 26 existing skips, no failures; targeted auth 23 passed. Local Docker
read-only UID10001 health/logo/normal/chooser proof passed and container cleaned.

## P01-T03: Canonical Learning Integration

Owner explicitly adds proper project-document integration. Dated ADR 0002
identity/session notes, PRD v0.13.1 review-learning rows and addendum exercise
evidence now cover callback/isolated profiles, packaging/CSP/own-photo,
role-plus-oid onboarding, preserved lineage/cache recovery, explicit switching,
safe logs/rollout and independent CI/rubric/product gates. Operator guides,
index and append-only log updated. No new company/business facts, so BRD
unchanged. PRD counts/approval and historical proposals/tables retained;
real already-authenticated replacement and complete permissions remain open.

New relative links/anchors: 23 checked and resolved. Seventeen changed source,
docs/tracking files scanned against the private selected directory identities;
no leaks. git diff check passed. Documentation session explicitly records
local evidence separately from CI-owned runner execution.

Published source/docs as baf6a5ca63bf32833005ea3c8f8faa98d3692c07 on existing
PR #65, no main write or merge. Source matches the image already tested and
deployed; subsequent edits are documentation/evidence only. MVP CI 38368944188
passed all test/mssql/image jobs; MVP validation 38368944195 and Prototype
validation 38368944263 passed. New scorer 38368944202 was still running at
this observation; previous rubric/score failure is not called a product pass.
No active implementation tasks or blockers remain. Plan follow-ups stay
outside P01: owner existing-session replacement and retained tenant naming.
