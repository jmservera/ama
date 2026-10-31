<!-- markdownlint-disable-file -->
---
title: Resident Survey check changes - Refs #571
description: Current synthetic regression and publication evidence
ms.date: 2026-10-31
---

## Metadata

Task 571, resident-survey-check-571. Plan/details/research use the same slug and
2026-10-31 date. Implementation scope: P01; parent owns P02 Review/publication.

## Execution Status

P01 complete; P01-T01 and P01-T02 validated. Approved write boundary: resident browser
check, API guide, current dated artifacts. No runtime/grammar/acceptance change.
P02-T01 complete; P02-T02 remains uncompleted. Independent critique Complete / Pass.

## Execution Summary

Original fix already merged in #573; current full browser check passes.
Research reproduced the obsolete-prompt mismatch on actual local HTTP/Chromium.
Add browser-only refusal/freshness evidence, preserving positive document facts.

## Completed Work

### P01-T01: Fresh refusal coverage

Added one loop/two obsolete document/form inputs after successful document
facts/reflow checks using existing `ask_chat`. It requires refusal, human help,
rules metadata and no Survey/request/document/AI-label leakage in each new
article. No existing positive assertion, unit, helper or runtime changed.
API guide distinguishes merged #573 from this additional browser regression.
Completion evidence: surgical diff matches the plan's coverage lock.

## Implementation-Time Plan and Detail Updates

Task-owned pip environment `/tmp/ama-571-20261031-env` created after system
distribution import failure. Initial no-build-isolation editable install failed
because `bdist_wheel` is missing; recover that declared build prerequisite with
pip before rerunning. Do not alter shared editable environments.
Recovery succeeded with pip-installed wheel and editable core/agents/api into
the task-owned environment. All three distribution paths resolve this worktree.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| Current-base browser | Passed, axe Not run | `/tmp/ama-571-baseline-20261031/report.json` |
| Obsolete prompt red probe | Reproduced | Research records exact failed Survey assertion and recognized green reply |
| Existing obsolete-prompt HTTP unit, system source paths | Passed | 1 test, 0.738s |
| Updated complete resident browser with pinned axe | Passed | Chromium 156.0.8078.4; 32 scans, 0 violations, 42 incomplete-rule occurrences across 31 states |
| Focused document/form/refusal HTTP contracts | Passed | 3 tests, 2.223s; every preserved document assertion unchanged |
| `ruff check .` | Passed | All checks passed |
| `ruff format --check .` | Passed | 65 files already formatted |
| `git diff --check` | Passed | No whitespace errors |
| Exact full API discovery, attempt 1 | Not executed; lock timeout | `flock -w 600` exited 1, empty `/tmp/ama-571-api-units-20261031.log` |
| Exact full API discovery, attempt 2 | Failed: missing declared dependency | Admitted; 1368 tests in 569.618s, 2 import errors (`azure.eventhub`), 320 skips |
| Exact full API discovery, attempt 3 | Passed | 1430 tests, 515.446s, `OK (skipped=320)`; same exact unittest command, `flock -w 1800` |
| Previously failed modules after dependency recovery | Passed | 64 tests, 33.866s |
| Manifest-pinned Ruff and dependency compatibility | Passed | All checks passed; 65 formatted; `pip check`: no broken requirements |

Browser full output: `PASS resident chat and callback flows; axe executed`.
Report `/tmp/ama-571-browser-20261031/report.json`, SHA-256
`9503e463bd668a7e554abf9e2e998b53724a62a180f21df5ee547d8cd27e9974`.
Self-contained commands, outputs and identities:
`.copilot-tracking/changes/2026-10-31/resident-survey-check-571-evidence.json`.
Zero page errors/external requests. Accessibility incompletes remain in the
full external report, not relabeled as passes or WCAG conformance.

## Blockers and Remaining Work

Build prerequisite recovered; first full-unit admission timed out after 600s,
without executing tests. Retry at the same source bytes and preserve the
original timeout; validate P01-T02, then one
independent Review and committed exact-head publication gate.
The admitted second attempt failed only on missing `azure.eventhub` imports
in `test_iot_stream` and `test_sensor_consistency`. Installed pinned
`azure-eventhub==5.15.1`; pip additionally identified missing manifest
`aiohttp==3.14.5` and `azure-iot-device==2.14.0`. Recover the existing API dev
manifest dependencies before the third run; no pin/manifest/source changes.
Recovery completed from existing manifests with pip. Extended only the queue
allowance from 600 to 1800 seconds for the third discovery; source bytes and
required test command remain unchanged. Plan/details and evidence retain both
prior adverse attempts. Full-gate capacity preflight currently admits one
worker; it is not a passing full gate or publication receipt.

### P01-T02: Final validation complete

Full API command from `src/api`, task-owned pip environment on PATH:
`PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests
python3 -m unittest discover -s tests -q`, admitted under the shared lock.
Final log `/tmp/ama-571-api-units-20261031-final.log`, SHA-256
`ccacba6463ba7fa8461f390f61d0070b41be25933233f19be191beaa67edd015`.
Original dependency-failure log SHA-256
`75d652cd5e79c8c0e8c14d4868f86058927e5d6bcbf6bc84abb8cc8c4df1ef20`.
Skips remain explicit opt-in discovery limits; not executed integration claims.

## Pre-Review Reconciliation

P01 plan markers/details, completed work and evidence are current. Exactly one
critique passed, no divergence/source change. Review-ready for bounded source
and synthetic evidence. P02 Review and publication remain incomplete.
Fresh main fetch returned `1330869ea675ff019958846330108b4f45e163ce`, not the
user-supplied base `5666bd33`. Preserve supplied branch/base, no rebase or
history rewrite. Publication requires separately authorized reconciliation and
a fresh full receipt; a passing focused check cannot waive that requirement.

## Independent Review and Publication Handoff

Exactly one independent post-implementation Review executed, Complete /
Residual work. No introduced source defect. Original artifact:
`.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md`.
RV-001 Medium routes publication/base direction to later `rpi-plan`;
RV-002 Low retains separate human/AT/live acceptance. No repeated Review,
source correction or changed acceptance follows this verdict.

P02-T01 is complete; P02-T02 commit/gate/publication is incomplete. Preserve
the owner-supplied branch/base. Commit scoped source, guide and dated original
RPI evidence using privacy-safe identity and required trailer. Run the required
full gate from a fresh detached exact-commit worktree outside this checkout:
local test bytecode/Ruff/editable metadata stay untouched, with no deletion
of unknown ignored inputs. This is an explicit clean validation candidate,
not a waiver of the clean-input or current-main ancestry rules.

## Committed Candidate and Full-Gate Attempt

Original source, guide and dated Research/Plan/critique/changes/Review/state
committed as `437965cb`, with authenticated GitHub privacy-safe author/committer
email and required Copilot trailer. Branch remains
`fix/resident-survey-check-571`, descending from supplied `5666bd33`.

Fresh detached validation worktree:
`/tmp/ama-571-final-candidate-20261031`, exact `437965cb`, clean tracked,
untracked and ignored inputs. Fetched current main:
`1330869ea675ff019958846330108b4f45e163ce`.
Executed from that candidate:
`PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base
1330869ea675ff019958846330108b4f45e163ce --out
/tmp/ama-571-full-gate-20261031`.

Exit 1, exact output:
`BLOCKED: Candidate does not descend from the reviewed main base`.
External log: `/tmp/ama-571-full-gate-20261031.log`. No checks or receipt were
produced: ancestry admission failed before full execution. Receipt verification
and independent exact-head publication assessment are therefore unavailable.
No alternate stale-base gate, skip, rebase, force-push, protection change,
Azure operation, push, PR or issue-criteria mutation was performed.

This final evidence-only update records the actual rejection and preserves the
original independent Review outcome. It does not fix RV-001 or establish a valid
receipt for either commit. P02-T02 is partial: local commit achieved;
publication blocked. Owner/coordinator must authorize base reconciliation,
then run a fresh complete gate for the resulting exact candidate before push.

## Follow-Up Items

Human/AT/live/model acceptance remains outside the synthetic check's evidence.
