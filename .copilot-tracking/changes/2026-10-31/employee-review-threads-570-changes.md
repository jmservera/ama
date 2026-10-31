---
title: Employee acceptance review-thread changes
description: Implementation, validation, review and publication evidence for PR 601 follow-up
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Scope and Inputs

Task ID: 570-review-threads. Slug: employee-review-threads-570.
Plan/details/research use this slug under their 2026-10-31 directories.
One independent plan critique Complete / Pass, zero findings. Implement P01
and P02-T01; parent owns independent Review P02-T02 and publication P03-T01.
No old evidence changed. Main merge Already up to date; no score conflict.
Caller explicitly requires CI gate, no full local gate wait, pip only/no secrets.

## Implementation Opening

Start P01-T01 with real-producer regression and strict negative matrix, then
cluster-only tolerance. P01-T02 adds hosted CLI and paired digest, plus API guide.
Validation and independent Review follow the complete coherent source batch.

## Validation Environment

Missing zava_forward import confirmed by ModuleNotFoundError before pip install.
External task-owned venv:
/home/azureuser/.copilot/session-state/5456b2a9-23f9-4bf1-9783-c9efe79d6e95/files/validation-venv.
Installed editable src/core, src/agents, src/api[dev] with pip.
No source manifest change or private dataset access.

## Completed Work and Validation

### P01-T01: Cluster tolerance and regressions

Added exactly two methods to the existing test module, zero removals.
Real producer regression with 501 unique fictional cases and default cap
failed before the fix (`map_projection` returned None). Cluster-only 1e-9
degree containment slack fixes it without changing point/geographic/schema
checks. The table-driven matrix covers all four edges, both modes, inside/
outside slack, exact geographic endpoints, boolean/nonfinite coordinates
and malformed bounds. All 18 acceptance/identity tests then passed including
all three Chromium regressions, zero skips.

### P01-T02: Hosted execution and same-commit pin

src-ci.yml now runs the maintained acceptance CLI immediately after Chromium
install with the documented PYTHONPATH. Discovery qualification/CLI exit
contract unchanged. Exact-byte workflow SHA-256 and tools pin:
9964408b3a69e4bbc01955dcab15612e8794280f1170e6b2d67ec75672224262.
API guide/index/log describe the bounded change and synthetic/hosted boundary.

### P02-T01: Initial static checks

Configured API Ruff check passed; 66 files already formatted. Initial mypy
found test-only list[int] assignment of float at the bounds mutation.
Changed negative-fixture bounds literals to floats; rerun passed. This is
ordinary in-scope typing repair, not a plan divergence.
No complete local gate or live acceptance is claimed.

### P02-T01: Verified command results

| Check | Result |
| --- | --- |
| Acceptance and identity test modules | 18 passed, zero skips; real Chromium included |
| Maintained CLI with documented env | Exactly three passed, zero skips; exit 0 |
| Maintained CLI with task-owned empty browser path | Exactly three qualified missing-browser skips; exit 1, not passing acceptance |
| API configured Ruff and formatting | Passed; 66 files already formatted |
| API configured mypy | Passed; 125 source files |
| Gate-tool tests, requested discovery command | 39 passed; printed negative-fixture failures are intentional inner subprocesses |
| Gate-tool isolated lint/format/strict mypy | Passed; two files |
| Parsed workflow structure/env/digest | Discovery before installation, CLI after installation, documented env and exact-byte pin verified |
| Changed-adapter isolated Ruff/format | Passed with existing E501 exemption; one file formatted |
| Full API discovery | Passed: 1441 tests in 613.621 seconds, 320 skipped; quiet output does not enumerate aggregate skip reasons |
| Complete local gate | Not run, explicit caller instruction; CI is gate |
| Hosted CI / live identity acceptance | Not claimed |

### Immediately Relevant Planning Reconciliation

API guide update also updates knowledge index/log as repository guidance
requires. Scope text now names those directly related files. Fully isolated
adapter lint found one pre-existing E501 at the unchanged embedded-JavaScript
line 158 (107 characters); no unrelated source change made. The configured
API exemption already covers it. Isolated adapter checks rerun with E501
exempted and all other selected rules active; formatting passed. Plan/details
now state this actual boundary, preserving approved behavior and requested
component validation. No significant/different caller decision required and
no critique repeated.

## Amendments, Divergences and Follow-Ups

No material divergence. Ordinary typing repair and immediately relevant
scope/static-check qualification are recorded above. Original live identity
prerequisite remains outside selected repairs. Hosted checks and owner merge
are separate gates.

## Pre-Review Reconciliation

Implementation scope P01 and P02-T01 complete. Plan markers/details, changes
evidence and handoff agree. The producer failure before the fix and successful
focused/CLI/static/tool/workflow results are preserved, including initial
test-only mypy failure and existing isolated E501 exemption. Full discovery
passes; its 320 skips are not executed integration acceptance. Selected
modules/maintained CLI prove three Chromium executions and zero skips.
P02-T02 independent Review and P03-T01 publication remain. No active source
blocker; original live identity and hosted/owner gates are separate follow-ups.
Review readiness: Ready for one independent Review of bounded source diff.

## Independent Review Result

P02-T02 executed once. Execution Complete; outcome Conformant; zero findings.
Canonical original Review:
.copilot-tracking/reviews/logs/2026-10-31/employee-review-threads-570-review.md.
Reviewer independently reran three map tests, loaded the original adapter
in memory against the same real produced payload to verify fail/pass
sensitivity, and verified parsed workflow order/env/digest. Bounded source
hashes retained in Review; not an exact-head or hosted approval receipt.
P02 markers/details reconciled. P03-T01 publication remains.

## Publication Preparation

Authenticated GitHub account resolved again as id 8036360/login jmservera;
repository-local author/committer email is the privacy-safe noreply address.
Remote branch advanced to 5243f4c593feca9a34ea6ec8c1ee9f47f187dd0c with only
a rubric-score commit; inspected divergence is one remote commit affecting
only .github/rubric/scores/latest.json. Source Review boundary unaffected.
Non-force push recovery will follow caller's `git pull --no-rebase` direction
if rejected. No branch rewrite, full local gate, PR merge or issue closure.

## P03-T01: Verified Publication and Thread Disposition

* Repair and original RPI evidence commit:
  2e288c2b, `fix(api): tolerate cluster roundoff and enforce acceptance browser CI`.
  src-ci.yml and tools/rpi-checks.py pin are in that same commit.
  Required Copilot trailer and privacy-safe author/committer used.
* Initial `git push -u origin HEAD` rejected non-fast-forward. Executed
  `git pull --no-rebase`, merging only the remote rubric commit without
  changing any of the seven independently reviewed source hashes.
* Retried `git push -u origin HEAD` successfully. Local and remote HEAD both
  419adec170216651c2a6e447dd676b6b0ac0f316 at publication verification.
  No force, rebase, amend, main write or PR merge.
* First thread reply:
  https://github.com/jmservera/ama/pull/601#discussion_r4431840461.
  PRRT_kwDOUU8JX86yQ7KW resolution returned isResolved=true.
* Second thread reply:
  https://github.com/jmservera/ama/pull/601#discussion_r4431840462.
  PRRT_kwDOUU8JX86yQ7Kg resolution returned isResolved=true.
* Replies distinguish real local Chromium execution from quiet discovery
  skips and pending hosted/original live acceptance. Original #570 not closed.

## Final Execution State

P01, P02 and P03 tasks complete. Single critique Complete / Pass and single
Review Complete / Conformant retained unchanged. Publication bookkeeping
updates only this changes record, plan, details and state; original Review
remains the uncommitted bounded source assessment, not exact-head approval.
The completed selected task leaves its automatic parent session running.
Ranked distinct follow-ups: hosted CI/owner approval first, independent
identity/live original acceptance second. No new child work selected.
