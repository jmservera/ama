<!-- markdownlint-disable-file -->
# RPI Changes: Complete local gate baseline repair

## Metadata

* Task ID: a81da11b-4af4-4c2c-bd8a-ca8a765c6fd4
* Related plan: .copilot-tracking/plans/2026-10-31/gate-baseline-repair-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md
* Implementation date: 2026-10-31

## Execution Status

* Status: Complete for P01
* Declared invocation scope: P01; P02 Review/publication owned by automatic parent
* Completed scope markers: P01, P01-T01, P01-T02, P01-T03
* Remaining markers: P02-T02 publication; P02-T01 original Review complete
* Starting boundary: two Python files and directly related API README

## Execution Summary

Research reproduced the full clean a75bbdff baseline failure after waiting for
the shared lock. Exact chat-panel Chromium test passes unchanged. Implement
iteration-specific closure binding and fixture-only transcript capture.

## Completed Work

### Keyword-only iteration binding

P01-T01: src/api/checks/case_journey_browser_check.py now binds the nine
references. Defaults are keyword-only because Playwright passes both Route and
Request positionally; its wrapper counts positional parameters. Ordinary
positional defaults would be overwritten by Request. Confirmed in installed
Playwright's ImplToApiMapping.wrap_handler and RouteHandler._handle_internal.
Mutable list identity and registered callback identity are preserved.
Ruff 0.17.1 isolated E,F,I,B,UP/py312/100 and isolated formatter pass.
Existing strict formatter required formatting the already-unformatted file;
no behavioral changes introduced. Actual three-check browser group passes.

### Fixture transcript isolation

P01-T02 complete: tools/test_rpi_checks.py captures only the two intentional
Runner.command skip transcripts, asserts the captured text, and retains row
skip counts and browser integration rejection. Full tooling suite: 39 passed
in 12.762 seconds. No synthetic chat skip result lines leak into outer output.
No added test methods, production parser changes or skip allowances.

### API validation and documentation

P01-T03: API unit discovery passes, 1430 tests in 604.827 seconds, 320 recorded
expected opt-in skips. Ruff passes; format checks 65 files; mypy passes 123
source files. Exact unchanged chat Chromium executed earlier with zero skips.
API README records the repair, unchanged wiring and local-only evidence.
Real design-system/workbench, case-journey and regulatory checks pass.
Journey: Chromium 156.0.8078.4, axe 4.10.3, 87 scans, zero violations;
regulatory: outcome passed, axe executed, 21 scans, zero violations.
Browser output /tmp/ama-gate-baseline-browser-a81da11b/checks.log includes
actual 200% zoom, keyboard, reduced motion, fallback and reflow evidence.

### Finite own-output cleanup

Only the 15 named fresh pip-generated egg-info files in core/agents/api were
selected. Full tracking snapshot including untracked evidence and opaque
symlinks was archived with metadata: 5078 members. Full archive readback,
selected-member restoration and hash comparison passed; all protected tracking
inputs were checked before and after pruning. Pending/removed journal retained.
Archive SHA-256: 11325bb25a2e79fbe9b2c690d44f2fb7c2319f8b08c1f2b0c7882dd6b510afb8.
Manifest, archive, restore and receipt:
/tmp/ama-gate-baseline-cleanup-a81da11b/.
No historical/foreign files or original RPI evidence removed.
Own empty .venv browser marker removed; all caches and browser outputs external.
git ls-files --others --ignored --exclude-standard now returns no ignored inputs.

## Implementation-Time Plan and Detail Updates

### Current-main reconciliation

Ordinary fast-forward incorporated e64c6e6c (#600), preserving the original
a75bbdff failed reproduction. #600 strengthens exact-chat success parsing;
it does not repair the nine browser closures or artificial discovery-skip
transcript leakage. No history rewrite, remote write or foreign file movement.
Plan/details reflect current base; critique remains one original Revise with
PC-001/PC-002 directly disposed. User's scope and test budget unchanged.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Original complete gate | clean a75bbdff/main | Failed | /tmp/ama-gate-baseline-20261031-repro-wait-a81da11b/receipt.json |
| Exact unchanged Chromium | chat-panel selector | Passed | /tmp/ama-gate-baseline-chat-repro-a81da11b.log; 1 executed, 0 skipped |
| Repairs | P01 | Passed | external dev venv /tmp/ama-gate-baseline-dev-a81da11b |
| Strict Ruff and isolated formatter | three gate browser files and tooling | Passed | pinned Ruff 0.17.1; E,F,I,B,UP/py312/100 |
| Full tooling suite | static gate regressions | Passed | /tmp/ama-gate-baseline-tooling-a81da11b.log; 39 tests |
| API unit suite | src/api | Passed | /tmp/ama-gate-baseline-api-a81da11b.log; 1430, skipped 320 |
| API Ruff/format/mypy | src/api | Passed | 65 formatted files; 123 typed source files |
| Actual three browser checks | design-system, journey, regulatory | Passed | /tmp/ama-gate-baseline-browser-a81da11b/checks.log; shared lock; 87/21 axe scans, zero violations |
| Archive/readback/restore/protected cleanup | finite 15 own metadata files | Passed | /tmp/ama-gate-baseline-cleanup-a81da11b/receipt.json |

## Pre-Review Reconciliation

Ready. P01 markers/details, completed-work evidence, validation and handoff
agree. No source blocker. Original Review and final committed full gate remain
pending P02 work, not claimed as completed implementation.

## Blockers

None in source repair. Publication requires full clean committed gate and
non-adverse independent Review/exact-head assessment.

## Remaining Work

Final committed gate/exact-head assessment and PR.

### Original Review outcome

One independent original Review executed Complete, outcome Conformant for P01.
No source defects. RV-001 Low retains broader #572 acceptance with its owner;
RV-002 Low routes unrelated exempt-harness closure debt to separate maintenance.
Original findings are preserved without a repeat Review or implementation loop.
Current main advanced to 5198a1ff while reviewing. Its API README overlap
prevents a dirty fast-forward; commit our own assessed work before ordinary
merge. Do not stash, force-push or rewrite history.

The final complete gate, exact-head assessment and publication evidence will
remain external; this committed original record intentionally does not claim
that post-commit work already passed.

### Exact command-context validation correction

Final candidate 1ee35aa3641480b654389eea5f7dbce27d979339 against main
f11d29e41cd40c1be2b81b111f6189340df84bdd failed its browser lint at
0151-browser.log with I001 only. Original failure retained:
/tmp/ama-gate-baseline-20261031-final-1ee35aa3-a81da11b/receipt.json.
Fifteen other required groups passed; browser and dependent MSSQL did not.

The earlier strict lint ran from repository root, causing Ruff's isolated
first-party import inference to put checks before playwright. The actual gate
runs inside src/api and requires the original playwright-before-checks order.
Restore that original order, then validate from the exact gate working directory.
This is an immediately relevant command-context/formatter correction in P02,
not a runtime change, new Review or disposition rewrite. Original Review and
failed receipts remain unchanged. Fresh full committed gate required.
Main f11d29e4 was incorporated by ordinary merge with the Copilot trailer;
this repair still changes no workflow or gate production code relative to main.
Exact src/api working-directory strict lint and formatter now pass on all
three gate browser files. Current tooling suite passes 42 tests in 12.727
seconds: /tmp/ama-gate-baseline-tooling-current-a81da11b.log.

## Follow-Up Items

Canonical plan Follow-Up Items: #572 acceptance remains owner-owned; unrelated
exempt browser harness findings are outside this repair.

## Return-to-Caller State

Automatic parent running, P01 and original Review complete. Review execution
Complete and outcome Conformant for P01. Final publication remains pending
with binding controls; original full gate failure remains preserved.
