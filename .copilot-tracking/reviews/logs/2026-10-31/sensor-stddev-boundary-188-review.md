---
title: Sensor standard-deviation inclusive boundary Review
ms.date: 2026-10-31
---

## Scope and Evidence

Task ID: 188-pr-587-second-correction. Slug: sensor-stddev-boundary-188.
Original post-implementation Review, once only. Assessed boundary: bounded
second PR #587 correction, Refs #188; not full publication or live acceptance.

* Research: .copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md
* Plan: .copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md
* Details: .copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-31/sensor-stddev-boundary-188-changes.md

## Opening Review State

Goal: independently assess exact arithmetic, inclusive semantics, regression
coverage, retained metrics and requested local evidence. P01 complete; original
critique Complete / Pass. Plan/details/changes are reconciled, including final
full-core lint/format command refinement. First comparison: P01 requirements
versus actual comparator and regression. Source/evidence read-only; only this
Review record may change. P02 local commit intentionally follows Review.
No initial blocker for bounded assessment. Publication/live follow-ups remain
outside active correction; no whole-issue acceptance claim.

## Execution Status

Complete. This is the one independent original post-implementation Review of
the supplied task, not a second lifecycle or repeated assessment. P01 execution
is complete; full-plan persistence is still partial because P02-T01's local
commit intentionally follows this Review. Review completion does not establish
that commit, publication readiness or human approval.

## Outcome

Conformant for the bounded implemented correction and requested local evidence.
No implementation defect, significant decision gap or material research gap
was found. Critical 0; High 0; Medium 0; Low 2 non-blocking deferred follow-up
routes; Informational 3 conformance/continuation findings. No adverse outcome
or original opening state has been replaced or concealed.

## Compared Evidence and Reconciliation

The assessed source diff is against original HEAD 2f5685ce on
feat/sensor-ingestion-consistency-188. It changes only the comparator, its
existing external-package test file and directly related core README:
83 additions and 3 deletions. Dated RPI evidence is separately untracked at
Review time. Review did not stage, commit, change source or modify other
tracking artifacts.

| Boundary | Assessment |
| --- | --- |
| Research C1/C4 and exact inclusive requirement | Exact Fraction population variance and guarded squaring replace rounded-root acceptance, without epsilon or threshold widening. |
| Research C2 and retained behavior | Point/mean-step arithmetic, diagnostic calculations and public result shape remain unchanged against 2f5685ce. |
| Research C3/C5; P01-T01 | One new method outside packaged src owns exactly 32 cases. Independent execution confirms the specified fixture and original four acceptance differences. |
| Research C6 and non-goals | Documentation consistently limits evidence to synthetic ingestion parity; no physical calibration, live Hub/Azure SQL or whole-issue acceptance is claimed. |
| P01/P01-T01/P01-T02 markers and details | Checked completion agrees with changes, implementation and final requested validation evidence. |
| P02/P02-T01 and handoff | Unchecked remaining local persistence is intentional, not a stale assertion of full-plan completion. Parent must reconcile this Review and commit afterward. |
| Original critique | Complete / Pass, zero PC findings; its original disposition remains applicable and unchanged. No finding-specific correction or user decision was outstanding. |
| Implementation-time updates | Full-core ruff check/format strengthens the earlier changed-file command scope and matches the unqualified caller request. Added-test E501 formatting is ordinary execution cleanup. Current plan/details/changes record both changes and their evidence. |
| Material revision readiness | No material direction change, new requirement, dependency change or unresolved implementation decision occurred. No repeat critique or new user acceptance was needed. |
| Blockers and remaining work | No bounded implementation blocker. Local commit remains parent-owned; broader publication/live work is separately deferred. |

The research's original missing-package failure and subsequent isolated pip
installation are supplied evidence, not independently repeated. The current
pyproject still declares standard-library-only runtime dependencies,
Python >=3.12, ruff 0.17.1 and mypy 2.4.0. No manifest/tool configuration changed.

## Exact-Arithmetic and Semantic Assessment

For admitted nonnegative population variances a,b and finite nonnegative
tolerance t, the requested comparison is:
abs(sqrt(a)-sqrt(b)) <= t. Squaring that nonnegative difference yields
a+b-t*t <= 2*sqrt(a*b). If residual r=a+b-t*t is nonpositive, the inequality
already holds. Otherwise both sides are nonnegative and squaring is equivalent
to r*r <= 4*a*b. The implemented residual <= 0 short circuit is necessary:
without it, a=b=0 and t>0 would incorrectly fail. Both branches are inclusive.
Variance order is symmetric, so shrinking and expanding spread behave alike.

Fraction(value) preserves each Decimal reading exactly; pvariance over those
Fractions computes population, not sample, variance without recurring Decimal
division or rounded roots. Fraction(str(limit)) uses the same decimal-intent
interpretation as the former Decimal(str(tolerance.stddev)), not the binary
float ratio. Thus 0.1 means exactly 1/10, while
math.nextafter(0.1, 0.0) means 0.09999999999999999 and remains strictly smaller.
Tolerance validation still excludes negative, nonfinite and boolean inputs;
zero and admitted integer tolerances remain supported.

At t=0 the positive-residual comparison reduces to (a-b)^2 <= 0, accepting
exactly equal variances, including nonconstant data. With one variance zero,
acceptance reduces to the other variance <= t*t. The private helper receives
nonempty sides because report already requires at least two samples on each
side. No new public empty-input or negative-tolerance helper contract is needed.

Each channel applies the predicate independently to before and after, then
all combines their results. This is equivalent to bounding the maximum
per-side absolute stddev error; there is no side cancellation or averaging.
Existing per-channel point/mean checks, aggregate passed conjunction across
all homes/channels, metadata/coverage/cadence rejection and tolerance reporting
are retained. Short circuiting all affects only private pure computations.
Rounded pstdev, its subtraction and float conversion remain diagnostic-only;
their values need not be exact acceptance oracles.

The fixed reference has four extreme offsets of magnitude 29/20 in nine
samples, so variance = 4*(29/20)^2/9 = 841/900 and stddev = 29/30.
Outward delta 3/20 produces stddev 16/15; inward produces 13/15.
Both errors are exactly 1/10. Deltas 0.14 and 0.16 produce exact errors
7/75 and 8/75, respectively. The smaller-float tolerance rejects the exact
0.15 step without relying on a rounded error or changing the readings.

Fixture placement at split 3 puts the nine samples after handover; split 9
puts them before. The opposite side has three constant samples, requiring the
negative-residual guard at positive t. Paired signs preserve each side's mean;
point errors never exceed 0.16, below limit 1. The sibling channel stays
constant with all-zero tolerances. Two channels times two sides times two
directions times four cases equals 32, with explicit full checks dictionaries
and aggregate passed assertions. Existing two-home clean-report, zero-variance,
numeric isolation and invalid-input tests remain intact.

## Validation Evidence

Independent commands used the supplied installed environment Python:
/home/azureuser/.copilot/session-state/395184a9-e42b-4e9b-bed0-3e3e11ad5990/files/sensor-stddev-venv/bin/python.
Working directory was src/core; no install or PYTHONPATH workaround occurred.

| Validation | Provenance | Result and limit |
| --- | --- | --- |
| Original seven-method handover regression before production edit | Parent-supplied original changes/caller evidence | Failed four outward exact-limit cases, covering both channels and sides. Original failure preserved. |
| Final handover discovery | Independently rerun: -m unittest discover -s tests -p test_sensor_handover.py -q | Pass, exit 0; 7 methods including the 32-case regression. |
| Changed-source mypy | Independently rerun: -m mypy --cache-dir=/dev/null src/zava_forward/core/synthetic/sensor_consistency.py | Pass, exit 0; no issues in 1 source file. Cache output was disabled; no typing configuration changed. |
| Fixture cardinality and retained schema/metrics | Independent in-memory audit loading original source with git show 2f5685ce and wrapping the actual new test method | Pass, exit 0; exactly 32 report calls and exactly 4 changed aggregate outcomes. Removing only passed and per-channel stddev check booleans leaves complete reports identical to original source for all 32 cases. |
| Algebraic helper edge cases | Independent inline probe | Pass: equal nonzero variance at zero tolerance, unequal variance at zero, negative residual, zero-variance inclusive limit and above-limit rejection, each at Decimal precision 2 and 28. This verifies helper independence only, not an arbitrary-context contract for the entire report. |
| Final sensor discovery | Parent-supplied changes/caller evidence: -m unittest discover -s tests -p 'test_sensor_*.py' -q | Pass, 134 tests, 133 passed; 1 existing opt-in SQL skip. Not independently rerun. |
| Full-core lint | Parent-supplied: -m ruff check . | Pass, ruff 0.17.1. Initial two new-test E501 findings were formatted and final checks rerun. |
| Full-core formatting | Parent-supplied: -m ruff format --check . | Pass, 115 files already formatted. Not independently rerun. |
| Changed whitespace | Parent-supplied: git diff --check | Pass; not represented as an independent execution. |

The first independent in-memory baseline audit failed with
INVALID_HANDOVER_CONFIGURATION because its separately loaded original module
had a distinct Tolerance class. Translating the supplied tolerance fields into
that original class fixed the audit harness; the rerun above passed. This was
not a production failure or source correction.

Existing backfill ResourceWarnings are parent-supplied unrelated observations,
not suppressed or repaired. Actual opt-in SQL, Azure, hosted checks, scanners,
browser validation and the complete local publication gate were not executed
or claimed by this Review. They are not prerequisites for this bounded local
arithmetic verdict; publication retains its separate full gate.

## Findings and Routes

### RV-001: Exact inclusive predicate conforms

* Severity: Informational; closed conformance finding.
* Evidence: comparator helper, nonnegative admission, guarded inequality proof,
  independent edge-case execution and unchanged per-side/channel composition.
* Impact: Corrects exact-limit rejection without epsilon, binary-tolerance
  reinterpretation, loss of zero-tolerance semantics or cancellation.
* Destination: None; retain evidence. No rpi-implement, rpi-plan or
  rpi-research correction is indicated.

### RV-002: Regression and diagnostic preservation conform

* Severity: Informational; closed conformance finding.
* Evidence: actual 32-call fixture audit, independent seven-method suite,
  changed-source mypy and exact original-source report comparison.
* Impact: All four intended original acceptance failures are corrected;
  below/above/tiny-limit controls and all retained report data agree.
* Destination: None; retain original failure and final evidence. No new
  packaged tests or expanded active scope is required.

### RV-003: Local persistence remains an explicit parent continuation

* Severity: Informational; open planned continuation, not a defect.
* Evidence: P02-T01 remains unchecked across plan/details/changes, and current
  task changes/evidence are not yet committed at Review time.
* Impact: Review is complete, but full-plan local persistence must not yet be
  reported complete. This ordering is explicitly approved.
* Destination: Active parent completes P02-T01, preserves this original
  outcome, reconciles markers and commits only explicit task paths with
  privacy-safe identity and requested Copilot trailer. No push is authorized.

### RV-004: Publication prerequisites remain deferred

* Severity: Low; non-blocking residual route, not an implementation defect.
* Evidence: Plan Follow-Up Items, details P02 and changes explicitly defer
  complete publication receipt and hosted/human prerequisites.
* Impact: Local tests and this independent engineering Review cannot authorize
  publication or stand in for full exact-candidate/approval gates.
* Destination: Distinct coordinator-owned publication follow-up, only before
  a separately authorized push. No active correction scope is added.

### RV-005: Live handover acceptance remains separately unproven

* Severity: Low; non-blocking residual route, not a correction defect.
* Evidence: Second plan follow-up, changes and core README distinguish
  synthetic parity from live transport, actual Azure SQL and calibration.
* Impact: No whole #188 acceptance or issue closure is established; retain
  Refs #188 rather than a closing keyword.
* Destination: Distinct separately authorized live-handover evidence work,
  owned by the coordinator arranging that authorization. No Azure exercise,
  credentials, private-data access or operational activation is implied.

## Limits, Blockers and Next Owner

No blockers prevent acceptance of P01 or parent local-only continuation.
Performance of exact Fraction variance over large windows was not benchmarked;
research explicitly accepts the additional bounded arithmetic cost and claims
no live throughput. No new performance criterion is invented.

This reviewer used no nested agents, network writes, installation, commits,
push, Azure or private datasets. Only this canonical Review record was edited.
The verdict does not establish human approval, hosted approval, a current full
publication receipt or completed local persistence. Preserve all original
research, critique, failure and Review outcomes.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md](.copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md) | Compared original research C1-C6 |
| [.copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md](.copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md) | Compared scope, markers and two distinct follow-ups |
| [.copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md](.copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md) | Compared fixture, commands and local-only continuation |
| [.copilot-tracking/changes/2026-10-31/sensor-stddev-boundary-188-changes.md](.copilot-tracking/changes/2026-10-31/sensor-stddev-boundary-188-changes.md) | Supplied original/final validation and reconciliation |
| [.copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md) | Preserved original Complete / Pass critique |
| [src/core/src/zava_forward/core/synthetic/sensor_consistency.py](src/core/src/zava_forward/core/synthetic/sensor_consistency.py) | Independently assessed exact predicate and report semantics |
| [src/core/tests/test_sensor_handover.py](src/core/tests/test_sensor_handover.py) | Independently executed regression and 32-case audit |
| [src/core/README.md](src/core/README.md) | Compared diagnostic and acceptance boundaries |
| [src/core/pyproject.toml](src/core/pyproject.toml) | Unchanged runtime, tool and package contract |
| [.copilot-tracking/reviews/logs/2026-10-31/sensor-stddev-boundary-188-review.md](.copilot-tracking/reviews/logs/2026-10-31/sensor-stddev-boundary-188-review.md) | One original complete Review and routed findings |

## Next Steps

The active parent may record this Complete / Conformant Review and finish
P02-T01's authorized local-only persistence. No second Review or user action is
required. RV-004 and RV-005 remain distinct deferred follow-ups, not active
defects. Do not push or claim full publication, live acceptance or human approval.
