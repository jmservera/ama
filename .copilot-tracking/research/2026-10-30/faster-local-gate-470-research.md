---
title: Faster local gate 470 research
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

Investigate the remaining acceptance criteria of issue #470, using its text
and comments as data. Audience: delivery coordinator. Output: convergence
for the explicitly requested full RPI loop, not a gate redesign.

## Research Parameters

Focused posture, selected for the bounded issue. Internal candidates:
`tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `src/README.md`,
existing gate evidence. External candidates: issue #470 and merged #475.
Resolved evidence root: `.copilot-tracking/`. No Azure, deployments, live
sign-in, credential files, secrets, push or PR creation. Heavy gates must hold
`/tmp/ama-rpi-heavy.lock`. Research edits are evidence/state only.

## Extension Registry and Provenance

Repository instructions and RPI research selected. Web skills skipped:
no web work is proposed. Research is inline because this is one continuous
implementation/evidence trace. Independent critique and final Review will
be separate bounded assessments as required by the RPI lifecycle.

## User Participation and Research Decisions

The user explicitly requests research, plan, implement, review in order.
This authorizes those phase advances without another mode-choice prompt.
Non-interactive execution; no widening or external publication authorized.

## Direction Controls

Reuse clean `ci/faster-local-gate-470` at the supplied base
`9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19`.
Implement only missing scope; preserve existing full/partial receipt rules.

## Research Questions

* Q1: Which requested features remain absent?
* Q2: Can comparable full serial/parallel measurements run safely here?
* Q3: What evidence proves acceptance without overstating a failed gate?

## Prior Knowledge Gate

Issue checkboxes and owner comment indicate #475 already delivered the
functional features. Verify against current source and tests before planning.

## Research Cycle Log

### Cycle 1, Wider

Issue #470 and its owner comment identify full before/after timing as the only
unticked criterion. Current source already imports the parallel executor and
provides changed/jobs/resume flags. Reflection: investigate benchmarking and
prerequisites, not duplicate previously merged functionality.

### Deeper

The owner comment and merged #475 PR agree that only a full timing comparison
remains. Existing tests cover selection, scope, parallel scheduling, cgroups
and resume. The runner isolates HOME, Azure config, synthetic data and package
environments, and performs only offline Bicep version checks. Every run already
holds the shared heavy lock; externally wrapping it in flock would deadlock
against its own independent lock acquisition.

All required full-gate executable paths and Docker are present. Python 3.12.3,
four Docker CPUs and approximately 15.6 GiB are observed. Root has 14 GiB and
`/mnt` has 28 GiB available. Ruff, mypy and project distributions are absent
from the active Python environment; restoration is allowed after these actual
missing-dependency results. A foreign process owns the heavy lock. A bounded
600-second admission wait is authorized by the current user, unlike the usual
nonqueued repository default.

Reflection: benchmark completed full runs only. Separate queued wall time from
lock-held elapsed time and record actual admitted workers, not requested jobs.

### Contrarian

Historical 23-26 minute command sums are not a controlled serial wall baseline.
The old 60.856-second result is partial and cannot satisfy full timing.
Use the same committed candidate/base, fresh external outputs, `--all
--jobs 1` versus `--all --jobs 3`; disclose order/cache effects and resource
capping. A failed gate, busy lock or single admitted worker does not prove a
speedup. Never weaken a failed check to manufacture benchmark completion.
The existing receipt's command timestamps and lock acquisition log permit
timing without changing the trusted gate implementation.

Reflection: source implementation already exists. The appropriate change is a
reproducible benchmark procedure and actual evidence or an explicit blocker.
No new cache/image reuse behavior is justified by the remaining criterion.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/470, retrieved 2026-10-30
  with `gh issue view 470` and `--comments`: features accepted; full timing missing.
* C1: `tools/rpi-checks.py:1`, current full/changed receipt runner.
* C2: `tools/rpi-checks.py:22`, existing parallel executor.
* C3: `src/README.md`, documented changed/jobs/resume and exact-head policy.
* C4: `tools/rpi-checks.py:1126`, isolated execution environment.
* C5: `tools/rpi-checks.py:1935`, shared-resource scheduler exclusions.
* C6: `tools/rpi-checks.py:2272`, fixed host-wide heavy lock.
* C7: `tools/test_rpi_checks.py:1`, focused gate regression suite.
* W2: https://github.com/jmservera/ama/pull/475, retrieved 2026-10-30:
  completed functionality, deferred caches, partial-only historical timing.

## Alternatives and Parent Synthesis

Accepted: benchmark the existing full runner, same commit/base and fresh
outputs, sequential serial/parallel attempts, preserve adverse evidence.
Rejected: duplicate merged implementation; compare partial versus full;
weaken scope/receipt checks; hold an outer flock around the self-locking runner.
Deferred: shared cache/image reuse, which #475 explicitly left outside its
delivered scope and which is not the remaining acceptance criterion.

## Open Questions and Residual Uncertainty

Full gates may fail on current inherited tests, downloads, disk capacity or
resource admission. A bounded lock wait does not grant interruption of its
foreign owner. Human/hosted approval and PR timing publication belong to the
coordinator.

## Current Decisions

Do not redesign merged gate features. Research disposition: executed.
Planning Readiness: Ready for the bounded benchmark/evidence work. Q1-Q3 are
answered; benchmark outcome belongs to Implement. One complete ordered cycle
suffices because further inspection would duplicate verified runner contracts.
Self-check: criteria, evidence, alternatives, constraints and gaps are recorded.
Parent continuation: Plan, explicitly authorized in the original request.
