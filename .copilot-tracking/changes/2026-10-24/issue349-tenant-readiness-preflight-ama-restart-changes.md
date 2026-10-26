<!-- markdownlint-disable-file -->
---
title: Issue 349 ama-restart changes
description: Changes evidence and owner intervention plan, 2026-10-24
ms.date: 2026-10-24
---

## Changes

Added only dated tracking files for 2026-10-24 (research, plan, details,
changes, review, state). No change to infra/, src/, tools/ or tests; no live
write. Prior reviews, critiques, state files and log entries are untouched.
Focused tests: 35 passed. Critique findings applied as recorded in the plan.

## Readiness result (2026-10-24)

Blocked, not feedback-ready. Preflight overall blocked (exit 1): API audience
is the literal systemAssignedIdentity, no credential setting, Graph read denied
for the az session; m365 Graph reads return 403. Public URL returns Envoy
"RBAC: access denied" 403 consistent with ingress Deny 0.0.0.0/0. Replicas 0.
All live #349 criteria remain unticked.

## Smallest exact next action (owner/coordinator, not performed)

1. Owner decision on the ingress Deny rule: it is tied to #360 private
   transport (owner-blocked, untouched). A feedback path needs either an
   owner-approved allow rule or the #360 route; also needs #126 headroom and
   tranche approval for any running replicas.
2. A tenant authority holder (Application Administrator or equivalent) creates
   or designates the single-tenant API app registration with the manifest roles
   (Entra write, human consent), then the deployment points audience at it.
3. Credential creation and delivery by the authorized human; staff binding
   separately.
4. Re-run: python3 infra/scripts/tenant-readiness-preflight.py -g ama -n
   ca-cutover-test-demo-api --public-url <https origin> --json; expect ready
   for audience and graph-* checks only after steps 2 to 3.
