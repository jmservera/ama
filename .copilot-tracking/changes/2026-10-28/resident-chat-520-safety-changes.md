---
title: Resident chat safety routing correction changes
description: Implementation evidence for task 520-safety
ms.date: 2026-10-28
---

## Status and Scope

Task 520-safety, full plan requested. P01, P02-T01 and P02-T02 complete; local commit pending.
Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-safety-plan.md.
Details: .copilot-tracking/details/2026-10-28/resident-chat-520-safety-phase-details.md.
Research: .copilot-tracking/research/2026-10-28/resident-chat-520-safety-research.md.
Original critique: .copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-safety-critique.md.

## P01: Safety routing and regressions

Baseline actual installed reproduction at 49561c34: both supplied reports route
`home`; ordinary smoke detector documents and CO detector status retain documents
and status. System Python initially raised ModuleNotFoundError; created a task-owned
session venv and installed existing editable core/agents/api dev distributions.
No dependency manifest changes or private-data reads.

New tests before source fix: 3 methods, 78 failures, exit 1. Both quoted reports
fail exact route/HTTP safety assertions; an electric-shock/status report also
reaches the mocked advisor, proving the missing safety boundary. One negative
table expectation incorrectly placed status ahead of home; corrected that expected
value to preserve existing home-before-status ordering, not change production behavior.
Raw baseline: session files/safety-baseline.log.

Added whole-word bounded report/context combinations before ordinary matching,
47 hazard cases and 30 ordinary route/HTTP comparisons. Existing SAFETY text and
ordinary branch order unchanged. Added quoted reports to actual browser flow
with exact HTTP answer and latest-entry assertions. API README explains finite
coverage and ordinary detector/query boundaries. P01 complete.
Ordered smoke-report phrases handle terse "Smoke in my home" and actual observed
smoke without interpreting "see smoke alarm documents", "documents coming" or
"filling forms for my smoke alarm" as observations. This preserves the
whole-word/context intent instead of expanding generic token matching.

## P02: Validation and Review

Focused command from src/api with task venv Python and
PYTHONPATH=tests:../core/tests:../agents/tests:
`python -m unittest test_resident_chat_api test_resident_chat_agenda test_resident_assistant_api -q`.
Initial focused run: 33 tests, OK, exit 0. No skips. Ruff100/format on changed typed
files passed. Raw evidence: session files/safety-focused-final.log.
Heavy checks use flock -n on the caller-selected shared lock, bounded
2400-second retry deadline; the focused run acquired immediately.
Pinned public axe 4.10.3 downloaded; SHA256 matches existing checker constant
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
Installed Chromium executable exists. First API-wide run was stopped by its
owned session before completion to strengthen those ordinary-question boundary
regressions; no success/count claimed from that interrupted run. A fresh complete
final-source run then passed every selected check.

Final-source checks already complete: Ruff100 project check passes; format
reports 51 files unchanged; strict mypy passes all 97 source files; final focused
suite repeats 33 tests, OK. API discovery: 1182 tests in 429.630 seconds,
OK with 316 skips. These general-discovery skips are not SQL or full-gate
evidence. Actual loopback Chromium 156.0.8078.4 passed all resident chat/callback
assertions including both quoted hazard reports; pinned axe executed in 32 states,
zero reported violations and seven color-contrast incomplete states (anonymous,
document-facts, document-facts-320-text-200, signed-in-chat,
typed-hazard-human-route, typed-ahead-draft-preserved, page-error-help).
Console errors and external browser requests: none. Human/AT acceptance not run.
This is not WCAG conformance or a claim that the incompletes have been accepted.
Independent baseline comparison confirms all 30 ordinary table routes equal
their original HEAD routes, not merely current typed-topic equivalents.
AST comparison confirms the answer function and every ordinary routing branch
are unchanged. Literal comparison confirms SAFETY is byte-for-byte unchanged.

Source boundary for final validation and independent Review:

| File | SHA256 |
| --- | --- |
| src/api/src/zava_forward/api/resident_demo/chat.py | b12f26572e474910b6bbbdd9e772b96d63da10f02efcba29c6a68742dc17ee0b |
| src/api/tests/test_resident_chat_api.py | e8e50a93c84a6500cde60171b2153450d1fa090919ca2a03e10ef17f15831636 |
| src/api/checks/resident_assistant_browser_check.py | 52345ab07fafa547bf7cde23bafbef87dadeb69cd1e89a8939a71649cdb1f73e |
| src/api/README.md | 5c5705065ff62504a595cae70d24a9d39af86f8d37641f5e430f1c09af5c9113 |

External raw logs and browser assets are retained under
/home/azureuser/.copilot/session-state/8bb23fe0-ccff-47eb-9be9-7179dc4f9a4e/files/.
These are scoped execution evidence, not a full-gate receipt.

| Final command from src/api | Exit / evidence |
| --- | --- |
| python -m ruff check --line-length 100 . | 0, safety-ruff.log |
| python -m ruff format --line-length 100 --check . | 0, safety-format.log |
| python -m mypy | 0, safety-mypy.log |
| python -m unittest test_resident_chat_api test_resident_chat_agenda test_resident_assistant_api -q | 0, safety-focused-final2.log |
| python -m unittest discover -s tests -q | 0, safety-api-discovery-final.log |
| python -m checks.resident_assistant_browser_check --axe SESSION_FILES/axe-4.10.3.min.js --out SESSION_FILES/safety-browser | 0, safety-browser.log and safety-browser/report.json |

SESSION_FILES denotes the exact session files directory above; commands used
the task venv Python and documented test-only PYTHONPATH. A single shared-lock
holder owned the final run (PID 352058, acquired 2026-10-28T22:26:34Z); no lock
contention, foreign process interruption, az or Azure calls. Wrapper always uses
flock -n with a 2400-second deadline. Browser report SHA256:
37507c4f64710df4f7d9dbe9c9ae0168924264e9ea8e9dc6bf9ee3408b8b2ded.
Git diff --check passed.

### Original Independent Review

Exactly one Review executed, Complete / Residual work. Bounded source assessed
Conformant with no implementation defects. Reviewer independently inspected raw
logs/report and verified source/report SHA256, unchanged SAFETY/answer/ordinary
ASTs and the 47/30 route tables. Original record:
.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-safety-review.md.
RV-001 Medium routes the missing full receipt/publication to coordinator.
RV-002 Low retains seven contrast incomplete states and unperformed human/AT
acceptance for its existing owner. No source correction, second Review or
acceptance upgrade follows. Review statements about pending commit describe its
original assessment boundary and remain unchanged.

## Amendments and Divergences

None. PC-001 disposition rejects an unsupported parent path restriction and
replacement of the caller's explicit shared lock; original critique unchanged.

## Blockers and Remaining Work

Only local commit remains in the permitted scope; Review complete.
Mandatory complete publication gate preflight executes az bicep version
(tools/rpi-checks.py preflight). Explicit no-az means no full gate run, push,
thread resolution or publication approval claim in this task.
Coordinator must establish a new committed exact-head/current-main full receipt
and independent exact-head assessment before normal push and thread resolution.
Final pre-Review fetch: topic HEAD and origin topic both
49561c345e367a4abfd289cf2cfdf8c7036ab61d; origin/main
1dde6a908c20358dbb3067dcdd674e5ad0bd246d. PR open and unchanged, Refs #520 present.
Post-Review/precommit fetch confirms the same three identities. Authenticated
GitHub account resolved to login jmservera, numeric ID 8036360; commit email is
constructed from that API response, not a private email or global Git change.

## Acceptance Boundaries

No new legal/safety advice; SAFETY must remain unchanged. No operational report
or alert is sent. Finite lexical regression coverage is not general hazard
detection, whole-issue approval, accessibility or human acceptance.
