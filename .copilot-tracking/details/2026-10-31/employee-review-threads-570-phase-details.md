---
title: Employee acceptance review-thread phase details
description: Task-level boundaries and evidence expectations for PR 601 corrections
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: 570-review-threads. Slug: employee-review-threads-570.
Plan: .copilot-tracking/plans/2026-10-31/employee-review-threads-570-plan.md.
Research: .copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete | P02-T01, P02-T02 |
| P03 | Publication active | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct acceptance contracts

Only consumer containment and hosted invocation change. Core and browser
qualification remain unchanged. No live data, UI or dependency changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Cluster tolerance and regressions

C1 shows accumulated centroid roundoff; C2 uses exact comparisons. Use 1e-9
degree cluster-only slack in containment after existing coordinate and bounds
validity. Strict point containment, finite/geographic range, ordered bounds,
counts and duplicate-link checks stay intact.

Two new methods maximum, zero removals. Construct 501 public fictional cases
with unique IDs and original (54.9, -1.6), pass to real map_view with default
cap 500. Assert cluster mode/counts, nonzero overshoot and accepted projection,
not merely a hand-authored centroid. A table-driven test covers both axes,
both sides, in/out-of-tolerance, strict points, geographic boundaries, booleans
and nonfinite coordinates/bounds. Existing module owns coverage.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Hosted browser enforcement

C3-C5 show legitimate discovery skip but missing execution after installation.
Place CLI after Chromium install with
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests
from the existing API guide. No sign-in env or secrets. Keep discovery and
maintained CLI's exactly-three/zero-skips checks. Hash exact workflow bytes;
update only src-ci.yml entry in WORKFLOW_HASHES. Document tolerance and hosted
enforcement in src/api/README.md.

<!-- rpi:phase id=P02 -->
## P02: Verify and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validation

Run acceptance/identity selectors and maintained CLI from src/api using test
import paths; verify three Chromium executions and zero skips. Run API discovery,
configured Ruff/format/mypy and isolated changed adapter lint/format retaining
the pre-existing embedded-JavaScript E501 exemption. Run requested
gate-tool tests from root and strict tool lint/format/type checks. Record real
outcomes, not full-gate or live acceptance. Workflow pin and parsed command
order/environment must agree. Missing Chromium is a validation blocker until
pip-installed Playwright's Chromium setup succeeds.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review

One fresh worker activates rpi-review, reads current research/plan/details/
changes and source diff, and writes only
.copilot-tracking/reviews/logs/2026-10-31/employee-review-threads-570-review.md.
Check both exact requirements and preserve original Review execution/outcome.
Parent reconciles markers and routes genuine residual work; no second Review.

<!-- rpi:phase id=P03 -->
## P03: Publish and resolve

<!-- rpi:task id=P03-T01 -->
### P03-T01: Publication

Same-commit workflow/hash pin, original dated evidence and requested trailer.
Use repository-local privacy-safe identity from gh api user, no private email.
Push existing branch with git push -u origin HEAD, never force; rejected push
requires git pull --no-rebase before retry. Reply to and resolve exact threads
PRRT_kwDOUU8JX86yQ7KW and PRRT_kwDOUU8JX86yQ7Kg after push.
Verify remote SHA and thread resolution. CI gate remains hosted/pending;
original #570 live criterion and owner PR merge stay unclaimed.

## Completion Evidence

P01 implemented. Producer regression failed before the fix, then all 18
acceptance/identity tests passed including all three Chromium tests. Strict
negative matrix covers both modes/axes/sides and geographic/schema guards.
Workflow CLI inserted after install; paired digest
9964408b3a69e4bbc01955dcab15612e8794280f1170e6b2d67ec75672224262.
P02-T01 validation complete; no outstanding ordinary decision. All focused checks,
maintained CLI, gate-tool tests and configured API static checks passed;
full API discovery passed, 1441 tests in 613.621 seconds, 320 skips. Quiet
discovery output does not enumerate aggregate skip reasons; the selected
acceptance/identity modules and maintained CLI had zero skips. Knowledge
index/log updated with the
owning API guide; no old evidence or unrelated source issue changed.
P02-T02 independent Review Complete / Conformant, zero findings; reviewer
independently reran three map tests, checked producer old/new sensitivity and
workflow order/env/digest. P03-T01 publication remains. Bounded source Review
has no blockers; hosted CI/live acceptance remain unclaimed.
