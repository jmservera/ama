---
title: Setup API selection phase details
description: Bounded implementation gates
ms.date: 2026-10-17
---

Task360/setup-api-selection-360, research Ready; one critique complete PC001-003
accepted by parent, revised plan Ready. No second critique.

<!-- rpi:phase id=P01 -->
## P01: Regression and narrow implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Red-first

Extend stateful fake to show requested container by exact name where needed,
not fixed default app. Use legacy workload-only old API plus direct-ingress/
workload-only intended API (actual observed tags) and reverse order. Test
explicit old path via discover/main with valid old ID; modern/legacy conflicts
and duplicate/unmarked ambiguities fail. Existing direct tests cover modern.
Test check --run-in-azure and local failure/candidate fallback with transport
mock raising if reached; no calls/requests/tag_writes/sql apply/restart.
Fixture no private data. New methods maximumsix/removalsnone.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Compatibility and no-write guard

Direct preference accepts canonical roleapi, or absent role plus workloadapi,
AND explicit ingressdirect. Modern role authority within each resource preserved;
more than one eligible direct candidate (including mixed modern/legacy) refuses
before generic choose can hide the legacy candidate; no name/order/
environment-only inferred intent. Explicit name bypasses preference. Existing
external/environment/subscription/origin validation still applies after selection.
azure_staff central guard refuses args.check/dry_run/list_staff before payload
preparation and execute; accurate private-host handoff text.
Explicit --check Azure and automatic candidate/check fallback report incomplete/
blocked, no job/secret creation. Existing local read-only helper remains and
mutation-mode Azure transport preserved. No silent fallback to wrong target.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validate and document

Restore dependencies only after chosen test fails missing import; worktree-local
.venv pip source packages and requirements as existing infra guide. TMPDIR task
owned, exact cleanup. Run selected red/green then combined relevant tests.
No generic whole-script formatter; F-only lint plus compile and scoped mypy.
Update runbook discovery priority and --check transport limitation, remove stale
advice permitting cloudwrites undercheck; retain historical transport evidence.
Existing KB index/additive log, all prior ACR artifacts byte-identical.
Critique PC001: modify both existing Azure listing/fallback tests to require no
attempted cloud writes and blocked handoff, preserve local success and
mutation-mode generated roster transport. PC003: existing
test_arm_generated_and_legacy_kv_reuse_retains_upstream_expiry_boundaries
keeps all credential reuse/rotation assertions, but check overall incomplete
and no additional writes relative to initialized fixture baseline.

<!-- rpi:phase id=P02 -->
## P02: Review/publication

<!-- rpi:task id=P02-T01 -->
### P02-T01: Independent Review

One fresh generic independent reviewer activates rpi-review, only canonical
review output writable. Full new scope, original ACR Review not rerun.
Findings complete and routed; corrections only concrete root defect up to2cycles.
No fabricated Pass/acceptance. Reconcile completed markers/results before review.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Publish same topic

Fresh gh user privacy-safe local author/committer and Copilot trailer. Normal
source push to existing openPR385, update title/body Refs #360 only. Fresh main
already verified ancestorbbbc924, no integration needed at intake. If later
authorized rebase necessary preserve entire upstream log prefix/all entries/
routes and exact lease topiconly. Never merge/close/delete or touchgroupama.

## Completion Reconciliation

P01 complete: five canonical test additions/no removals, red-first then164
combined passes, scoped lint/format/types/compile. Integration main d400eb8,
reviewed source f48cc9b, exact executable fingerprints in Changes and Review.
One critique PC001-003 resolved; one independent Review Complete/Residual work,
source conformant/no defects, zero correction cycles. P02 complete: verified
publication03d90083447fbbb71d48ecc0413235561c9b0ff5 to existing open PR385/main,
updated title/body, authorized expected-remote lease d11c273 only for rebase.
Final completion metadata follows normal push; no source byte change or new Review.
No Azure writes this continuation; all live/image/retirement follow-ups unperformed.
