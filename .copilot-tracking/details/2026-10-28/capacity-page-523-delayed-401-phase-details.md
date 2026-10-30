---
title: Capacity delayed sibling 401 phase details
description: Implementation and verification boundaries for issue 523
ms.date: 2026-10-28
---

Task 523-delayed-401 / capacity-page-523-delayed-401.
Research C1-C4 and plan share this identity; previous artifacts remain unchanged.

<!-- P01 -->
## P01: Implement and verify

<!-- P01-T01 -->
### P01-T01: Red regression

Use the existing synthetic manager and supplied contract fixture. Capture real
successful packages/workorders payloads before intercepting. For each endpoint,
save threshold configuration once, hold both resulting refresh GETs, fail the
selected endpoint with 503 while retaining its sibling. Wait for Try again,
click it and hold its two new GETs. Fulfill the original sibling with 401;
observe sign-in, session alert and focus. Retain the exact clicked retry button
ElementHandle and observe disabled/aria-busy while its two requests are held.
Fulfill the retry GETs with actual successful payloads. Wait on this same
detached button for disabled=false and absence of aria-busy, proving go finally
completed after awaiting capacityView, before asserting
sign-in, no capacity heading/retry controls, focus and exactly one POST plus
one persisted configuration. Reauthenticate between orderings.
For unguarded red proof, record both stale-render failures in separate runs,
reversing the endpoint iteration for the second via an external in-memory
launcher if fail-fast prevents reaching it. Keep committed green assertions
strict; no production test hook is required.

<!-- P01-T02 -->
### P01-T02: Green and focused validation

After Promise.all, call captured signal.throwIfAborted and return if !me.
Rendering is synchronous thereafter. Preserve go/load and draft behavior.
Describe delayed-sibling expiry coverage in API README.
Use existing installed /tmp/ama-capacity-523-venv interpreter. Browser script
itself acquires /tmp/ama-rpi-heavy.lock with LOCK_NB before any heavy work.
Retry only its explicit lock-busy exit every 60 seconds, deadline 40 minutes;
do not rerun actual failures automatically. Run owned --mssql browser.
Run test_procurement_api, test_auth and test_ui_support with documented shared
fixture paths; Node --check ops.js and app.js; strict isolated Ruff E/F/I/B/UP
and format at 100 on harness, repository API Ruff check, API mypy. Diff check.

<!-- P02 -->
## P02: Review and publication

<!-- P02-T01 -->
### P02-T01: Original Review

Reconcile plan/details/changes and actual command evidence. Fresh independent
Review assesses exact source changes, regression synchronization and red/green
results. Refresh web rules for ops.js review, preserve original verdict and route
findings rather than repeat Review. Leave human approval/live acceptance open.

<!-- P02-T02 -->
### P02-T02: Publish and resolve

Resolve gh api user, configure repository-local privacy-safe author/committer.
Commit implementation and dated original evidence with required trailer.
Normal push only after scoped tests and Review. No complete gate invocation:
az is barred. Owner explicitly requested scoped push with that limitation.
Retain PR body history while clearly marking old receipt historical for this
new head; use Refs #523, never a closing keyword.
Reply to PRRT_kwDOUU8JX86xSi-Q with pushed SHA and results, then invoke
GraphQL resolveReviewThread. Verify remote head and resolved state. Post-commit
publication evidence may live externally to avoid a self-referential SHA commit.
