<!-- markdownlint-disable-file -->
# RPI Changes: AI metering publication remainder

## Metadata and Execution

* Task ID 432-publication; slug ai-metering-432-publication; date 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md
* Details: .copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md
* Scope: full child plan; status Partial, P01 complete; P02 pending.
* Approved targets: runner, runner tests (five methods maximum, removals none),
  related gate README and dated child evidence.
* Source-only boundary: no metering redesign, private data, paid calls or Azure.

## Starting Evidence and Critique Disposition

Read the caller-named previous correction changes first. Previous gate attempt
never started groups or produced a receipt; its original record is unchanged.
Focused research completed all three waves, Ready C1-C5/W1. The sole child
critique is Complete / Revise; PC-001/002/003 directly disposed before source
edits. In-tree evidence will freeze before final gate and sole exact-head
Review. Final result/state live externally and in the durable PR body.

## Validation Intent

P01-T01: existing runner tests and focused Ruff/format/mypy, plus actual
util-linux ownership/invalidity/closure/main-wiring tests on owned fixture locks.
P02: caller-authorised outer flock -w 1800 and full --all gate, fresh external
output/clean committed candidate/current main; per-group exception matrix.

## Remaining Work and Follow-ups

P02-T01, sole child Review and authorised push/main PR remain.
OD-51/prices/billing/batch, resident/historical joins and real pitch delivery
remain distinct parent RV-006 follow-ups. Hosted/human approval remains open.

## Completed Work: P01-T01 Inherited-lock Composition

tools/rpi-checks.py now validates an optional inherited descriptor against the
non-symlink regular shared path, duplicates it, asserts nonblocking exclusive
ownership and retains caller ownership through run/verify. Normal self-locking
admission is unchanged. src/README.md documents the explicit owner-authorised
queued composition; it grants no queue/publication authority.

tools/test_rpi_checks.py adds exactly five methods, removes none and leaves the
parent's two-module/35-method metering tests unchanged. Actual util-linux
composition, descendant FD exclusion, wrong/negative/closed/nonregular/symlink
inputs, contested ownership, pre-yield duplicate disposal, caller survival
through exceptions and main run/verify exclusion all pass.

Validation: 42 runner methods pass (11.661 seconds), with no skips; log
/tmp/ai432-publication-unit-final.log. Existing isolated E/F/I/B/UP Python 3.12
lint, isolated 100-column format and runner mypy pass; git diff --check passes.
An initial generic root Ruff invocation used unrelated repository-wide rules
and failed on inherited/new diagnostics; the repository's actual runner
isolated contract was then used. An initial new SPEC.origin narrowing error
was corrected with the actual test-file-relative runner path. These adverse
observations are retained, not evidence of a failed complete-gate group.

## Current Main and Candidate Preparation: P01-T02

Fetched main is a75bbdffa51ae34b1fcf779250f1f553d566ee93 and already an ancestor;
the explicitly requested git merge --no-edit origin/main returned Already up
to date. No rubric conflict or source merge was necessary. There is no observed
fix/gate-baseline-b023 PR yet; final fresh checks remain required.

This worktree contains inherited ignored developer caches. Do not delete them
or falsely call it a clean gate input: execute the full gate from a new owned
external clean clone of the final committed candidate. No private dataset or
foreign output is read/reused. Freeze committed preparation evidence, then
retain final gate/Review/state in an external dated tracking mirror and the PR
body to preserve matching exact candidate identity.

## Frozen Gate and Review Preparation

P01-T02 implementation/evidence commit:
cae4bba18d1800b571a2016638ef972e72d14559; all P01 tasks complete.
This subsequent preparation commit freezes in-tree evidence; final HEAD is
resolved externally to avoid self-reference. P02 is not yet complete and no
receipt or child Review outcome is claimed.

Owned clean clone: /tmp/ama-ai432-publication-clean-2026-10-31.
Full gate output: /tmp/ama-ai432-publication-gate-2026-10-31-a.
Gate log: /tmp/ama-ai432-publication-gate-2026-10-31-a.log.
Final Review/state/result root:
/home/azureuser/.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/
The PR body retains final identities, per-group evidence and review outcome;
final local files remain immutable/external, not unreviewed post-gate commits.

## First Full Gate: Preserved Adverse Result and Coupled Fixture Correction

At 2106ee22/base a75bbdff, outer flock acquired successfully and the runner
held continuous ownership; admitted jobs=1. Receipt sealed 2026-10-31T12:04:07Z
is full-selection / failed, not passing or verified. External output/log above
are preserved, never overwritten.

Known main B023: nine findings in unchanged
src/api/checks/case_journey_browser_check.py, 0070-browser.log; source SHA-256
ae5e2cf0998a2d439b73ec419333daa970d2f394774cac7221215337f1a17abd
matches main. Known chat-panel discovery: unchanged runner regression prints
two synthetic opt-in Chromium skip lines, so the outer static suite parser
fails despite all 42 runner tests passing; 0065-static.log. No actual browser
acceptance is inferred from those fixture lines.

Independent coupled failure: core discovery ran 1,634 tests/206 opt-in skips
but test_sensor_privacy.SensorPrivacyTests.test_actual_legacy_transport_body_is_closed
errored because financial admission prevented its mocked transport call;
0043-project-core.log. This is not covered by the baseline exception.
P01-T02 reopens for a surgical existing-test fixture correction, not a
production bypass; no new methods/modules or weakened privacy assertions.
Fresh full gate required after committing corrected source and evidence.

Agents 123, API 1,439 (321 enumerated skips), orchestrator 69 and importer 39
completed; namespace completed. Infra/migration/images/logo/SQL did not execute,
causally blocked by failed prerequisites. Pre-install namespace absence probes
were expected and followed by successful installations, not failure roots.
Main refetched after failure remains a75bbdff; no baseline-fix PR observed.
The final matrix must reflect the fresh run, not reuse this failed receipt.

## Coupled Privacy Fixture Validation and Fresh Candidate

The existing transport privacy method now supplies an explicit Mock financial
meter with an opaque reservation ID, preserving every request-body privacy
assertion and adding reserve, pre-network dispatch-check and exact transport
invocation assertions. It still mocks provider/token; no real call or applicable
price/authority is created. Exactly zero test methods/modules added or removed.
Production code and its fail-closed admission are unchanged.

All 17 sensor privacy tests pass in 2.008 seconds with one inherited SQL opt-in
skip; core Ruff/format (117 files) and strict mypy (170 files) pass. An initial
local namespace import failure was fixed by pip-installing core[dev] into the
new owned /tmp/ai432-publication-fixture-venv; failed gate environments remain
unchanged. This is an immediately relevant test-fixture reconciliation under
P01-T02, not a new significant decision or repeated critique/Review.

Fresh output /tmp/ama-ai432-publication-gate-2026-10-31-b and corresponding .log
will validate the new committed exact candidate. Preserve attempt a and its
4abc54f87e938ee8cd1174a53dbaecab4de143a7e9ccc2f2ab793480768ed1b7
receipt hash. All in-tree artifacts freeze again before the sole child Review.
