---
title: One-command Entra setup phase details
description: Implementation and evidence boundaries for issue 351
ms.date: 2026-10-16
---

## P01

Continuation boundary: validate planned membership conflicts during roster
resolution before any registration/SP writes. Probe selected vault metadata
without fetching values before addPassword. Require Succeeded provisioning
for clean no-op checks and reruns. Preserve PR #352's Custom X-Forwarded-Host/
Proto configuration while retaining linked-route callback discovery.

P01-T01: Keep orchestration synchronous and explicit, backed by one CLI runner
that suppresses raw failures. Reads may retry throttling/transient propagation;
no blind mutation retry. Fetch all Graph pages with fixed-host validation.
Validate public origins and same-group resource IDs. Derive edge callbacks from
origin-linked routes, not just a tagged profile. Preserve provider/token-store
settings and application role identifiers; reject incompatible matching roles.
Bind selected management tenant/subscription to isolated Graph tenant before
writes. Inspect token scopes/roles for planned operations, but never assert
that a token guarantees human directory authority. GET both control planes
is the authenticated network preflight.
Credential provisioning must not activate a new client against an old secret.
Stable app-bound credential/storage naming supports interruption recovery:
neither present -> create/store/verify then wire; both present -> reuse;
credential without storage -> block with portal remove-only-this-credential
instructions; storage without credential -> block for operator review.
No automatic deletion/rotation, no secret in argv or persistent repo file.
Exclusive profile lock prevents simultaneous local mutation; cross-host
execution must be serialized by the operator. Unknown POST outcomes require
rerun discovery rather than immediate retry.
Only enabled linked edge routes and validated/provisioned custom domains
produce callbacks; preserve bearer/browser action, exclusions and token store.
Users must be enabled members; groups must be security groups; direct group
membership only. Reject conflicting effective roles rather than elevate.
Report missing private roster as incomplete, never fabricate roles or people.
P01-T02: Keep callback-only imported API behavior available, route legacy CLI
to the supported tool, document changed broader CLI behavior. Tag only API,
edge profile and endpoint resources.

## P02

P02-T04: Use a private session venv and pip editable src/core, src/agents,
src/api. Run all infra tests and workflow Bicep/lint commands, mutation checks
for each routed finding, mypy and both local help launches. Repair the
secret-inventory assertion to check the parameter default and interpolated URI,
not require a hardcoded URI; retain compiled parameter forwarding/use checks.
No mvp/prototype edits or live tenant acceptance.

P02-T01: No live network tests. Stateful fake az covers creation then idempotent
rerun, drift mode, failure outputs and preservation of auth/roles/redirects.
P02-T02: README explains exact commands, fictional schema with placeholders,
Option A owner portal / Option B delegated administrator, polling/exit codes
and remaining SQL/private-network step. Knowledge log is append-only.
P02-T03: One independent post-implementation review, no review loop. Findings
route to follow-up, and material unresolved defects require draft/blocked PR
status, not a ready/conformant claim. Stage only this task's
files, configure authenticated noreply identity locally, push and open PR to main.
