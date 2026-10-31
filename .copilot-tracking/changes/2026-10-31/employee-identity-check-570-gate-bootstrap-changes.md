---
title: Employee acceptance gate bootstrap changes
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Opening Scope

Task 570-gate-bootstrap, employee-identity-check-570-gate-bootstrap.
P01 declared. Research Complete/Ready, exactly one critique Complete/Pass.
Direct coupled bootstrap child, not a repeat of original RV correction Review.
Only test launch handling, CLI strict reduction and owning guide permitted.
No BINDING/observer/matrix/Azure/credential changes or new/removed test methods.

## Original Evidence

Fresh absent-browser reproduction: three launch errors in 1.561 seconds.
First aa531930 complete gate timed out at shared lock (600 seconds), no groups.
Fresh-output retry acquired lock and is running aa531930 independently;
it remains an immutable historical candidate attempt. Any later commit requires
a fresh full current-base gate; no running gate/environment is edited.

## Remaining Work

P01-T01/P01-T02, then one child Review, candidate/evidence commit and fresh
complete gate/current-base receipt/exact-head assessment before push/PR.
Independent expected identity and original live criterion remain unmet.

## P01 Completed and Validation

Reused exact narrow missing-executable catch from existing browser asset test;
all other BrowserError values propagate. CLI now requires wasSuccessful,
testsRun equal three and no skips. Observer and BINDING bodies unchanged.
No methods added/removed. API guide explicitly separates approved discovery
skips from mandatory CLI/integration execution.

| Check | Result | Evidence |
| --- | --- | --- |
| Absent-browser three-test discovery | Qualified discovery success | Three exact existing approved skips, 2.586 seconds; zero actual Chromium executions |
| Absent-browser maintained CLI | Correct refusal | Exit 1 despite unittest skip-success, 3.098 seconds; no passing acceptance |
| Installed-browser identity/acceptance module | Passed | 16 tests, 18.510 seconds, zero skips |
| Installed-browser maintained CLI | Passed | Three actual Chromium executions, 13.074 seconds, zero skips |
| Non-missing launch fault | Correct failure | Injected synthetic launch error produces one unittest error, no skip |
| API Ruff/format/mypy | Passed | 66 formatted files, explicit runner formatter, 125 typed files |
| tools/test_rpi_checks.py | Passed | 37 tests, 10.907 seconds |
| Git diff / guide | Passed | No whitespace errors; missing-browser qualification explicit |

Plan/details/changes/source are reconciled; P01 complete and child Review ready.
Original correction's full API 1439/320-skip evidence remains historical exact
pre-bootstrap source; fresh complete gate will rerun whole final API discovery
with the expected qualified absent-browser skips and subsequently execute all
three required Chromium extras with zero skips.
No mandatory gate or live acceptance is claimed before that run.

## Original Child Review

Exactly one independent child Review Complete / Residual work, no substantive
findings. Original artifact:
.copilot-tracking/reviews/logs/2026-10-31/employee-identity-check-570-gate-bootstrap-review.md.
Reviewer independently confirmed absent-browser CLI refusal, installed-browser
execution, non-missing error propagation, strict synthetic zero/incomplete/
excess/skipped/failed CLI result refusals and unchanged observer/BINDING/matrix
and test-method boundaries. Prior correction Review remains unchanged.
Task's bounded implementation/Review complete; explicit parent publication
still requires new committed-head full gate, verified receipt and exact-head
assessment. Original live criterion is unmet; Refs #570 only.
