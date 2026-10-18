<!-- markdownlint-disable-file -->
# RPI Phase Details: Scoped consultation hold

## Metadata

Task ID 92; slug issue-92-scoped-consultation-hold; date 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-92-scoped-consultation-hold-plan.md.
Research: .copilot-tracking/research/2026-10-18/issue-92-scoped-consultation-hold-research.md.
No blockers to safe scoped service restoration; true let/renew and Legal remain unmet.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Scoped service behavior | Complete | P01-T01 |
| P02 | Validation and documentation | Complete | P02-T01 |

P01 completion evidence: five blanket calls removed; one replacement lifecycle
method plus two new scoped methods and one new HTTP method. No method coverage
removed beyond obsolete blanket-guard expectations. Five individual reintroduced
guard mutants are killed by the unmocked lifecycle. Existing scoped building,
appointment and SQL validation code is unchanged.

<!-- rpi:phase id=P01 -->
## P01: Scoped service behavior

<!-- rpi:task id=P01-T01 -->
### P01-T01: Failing-first probes and implementation

Context: unmocked test_mvp/test_workflows fail at unrelated issue before independent
gates; same selectors with verbatim original-main procurement pass 40/40.
First adapt consultation tests to require normal lifecycle success without clearing
effective status. Use existing supplied appointment helper for main's new commitment.
Run before implementation and retain error evidence. Remove the five blanket
guard calls, not any existing building/hazard/resident/provider/appointment gate.
Keep direct consultation guard always denying; make its text explicitly about
consultation-dependent actions. Audit wording must not imply ordinary work held.

Exact scope test: reuse building_fixture.add_building and existing hold schema
if appropriate; source-backed Unknown/Open hold explicitly binds case and package.
Issue/reissue/correct/book/final advance each must honor existing building checks.
Different cases must not inherit explicit case scope; another package on the held
case can perform package-aware instructions but final case advance retains its
existing case-wide hold. PC-001 test matrix: matching P1 denials; P2 package-aware
success; different-case lifecycle success; same-case final advance denied with
one otherwise eligible P2 appointed order, current genuine synthetic appointment/
capacity/resident bindings and unchanged case/order/audit. Null scope remains
fail-closed. A record label is descriptive only, never a parser.
Capacity and contract-source relations must not confer consultation authority.
Keep existing transaction fault/current-source/current-recorder version tests.
Completion: focused semantic/HTTP checks pass unmocked and exact original
source control deltas contain only removed blanket calls plus truthful wording.

<!-- rpi:phase id=P02 -->
## P02: Validation and documentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute local checks and evidence reconciliation

Dependencies: P01; critique findings disposed once. Run selected installed-package
tests first, then actual failed CI API discovery and needed core regression coverage.
Run configured core/API ruff check, format --check and mypy. No blanket formatting.
Manifest/source hash remains untouched; its checker must prove parity.

Persistence seam applicability changes justify actual SQL parity. Create a unique
task-owned loopback SQL Server container using an already available image; never
connect to active #76 server or inspect its credentials. Run existing new-feature,
provider/HTTP/workflow adapters and relevant optimistic/recovery tests; retain
failed probes as evidence, close connections, remove only owned resources.
Non-root installed API HTTP suites satisfy local execution; no image/deployment
acceptance is inferred. Record optional browser/cloud/human checks unperformed.

Update src/core/README.md, src/api/README.md, existing UX synthesis and index; append
new log entry after both historical task entries without rewriting upstream body.
Verify old artifact SHA256 values and upstream prefix, no server/SQL/queue/export
implementation changes, clean diff, and exact main hash before publication.
Reconcile plan markers, details, changes and state before one original Review.

Completion evidence: combined 519 run/95 skips; core1117/133; API794/252;
actual SQL136/one; configured core/API ruff check/format/mypy; migration25pass;
five adverse guard mutants killed; old artifact digests and upstream log prefix
match. No independent control source or fixture/schema changed. Source/tests/
docs completed one original Review: Residual work, no bounded defects.

## Authorized integration/publication continuation

Coordinator cleared the moved-main blocker on 2026-10-18: rebase only owned
branch from local 7e4aa6eca3a65dd9fe5a403a57f63b3edf62cb5c onto exact
a86282c4badebc58eabbf9e441410d930a201ac2. Preserve PR407 production/tests,
recorder controls, additive README sections and both original assessments.
No source correction or policy change. Prove normalized exact patch parity and
full inventory; run fresh consultation/provider/workflow/API and queue smoke,
plus configured core/API quality. Actual 135 SQL passes and hardened-image
evidence remain historical unless a production conflict/persistence change
requires rerun. Publish initial exact lease 9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7;
normal push only afterward. Update PR389 with Refs #92 only, empty closing refs,
exact head/base and unmet Legal/genuine let-renew/human/live acceptance.
Stop after publication for independent coordinator review. The later exact-base
authorization below supersedes the prior main-movement wait.

Rebase completed without conflicts at source candidate
adc9ad984cd9cd6bcfbd30db6d52485d9506ab47. Both README additions auto-merged
and inspected; owned source blobs and protected upstream production/tests are
exact. Normalized zero-context patches compare exactly after removing only
index and hunk-position metadata. Complete tree inventories and original
assessment hashes accompany the separate integration receipt.
Fresh focused run: 212 executions, 199 passed, 13 explicit skips, 80.599s.
Fresh combined run including queue selectors: 553 executions, 458 passed,
95 explicit skips, 151.838s. Configured core/API quality passes: Ruff check,
format (72/24 files) and mypy (125/56 source files). Historical 135 actual SQL
passes and upstream hardened-image evidence were not rerun or promoted.

Publication preflight at candidate ae2bc36b14025f833d449bc12c18873ee65e4b0d
found main ab0613f3336109ff9b96560a16758ee842232715. The exact-main guard
stopped before push; remote topic remains 9fb84836. Read-only PR389 inspection:
open, unchanged remote head, closingIssuesReferences empty. No initial lease,
normal push, PR update or further rebase performed. Integration onto authorized
a86282c4 is complete locally; publication is blocked pending coordinator direction.

## Exact ab0613f3 continuation

2026-10-18 coordinator authorizes rebase from a86282c4 onto exact fetched
ab0613f3336109ff9b96560a16758ee842232715, expected local c6732027. Preserve
PR408 timecapture.py/test_timecapture.py byte-exact and additive API README;
retain all queues, recorder controls, own scoped intent and old/new assessments.
No source correction, policy change, second original Review or critique.
Keep existing receipts unchanged and add a new integration receipt. Preserve
/tmp/rpi-92-scoped-hold.log and /tmp/rpi-92-final-integration.log; exact copies
and hashes are saved in this worker's permitted session files.

Minimal fresh selectors: consultation/procurement API/quality procurement/
mvp/workflows/timecapture. Configured core/API Ruff check/format/mypy.
No broad rerun for unchanged source; prior integration smoke remains inherited.
SQL/image remain historical unless packaging/persistence conflict changes source.
Publish only exact topic lease 9fb84836; stop if topic advanced. Later main
movement does not block this exact-base publication, but must be reported.
Update PR389 with Refs #92 only, exact head/base and unmet acceptance gates;
no review checkbox or independent acceptance claim. Stop for coordinator review.
