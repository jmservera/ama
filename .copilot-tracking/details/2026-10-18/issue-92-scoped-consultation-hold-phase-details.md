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
docs are review-ready. Remote main moved to a86282c4, so publication and further
integration wait for coordinator direction as explicitly required.
