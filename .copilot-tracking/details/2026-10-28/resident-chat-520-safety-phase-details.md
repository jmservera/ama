---
title: Resident chat safety correction phase details
description: Task-owned implementation and validation contracts
ms.date: 2026-10-28
---

Task: 520-safety. Plan:
.copilot-tracking/plans/2026-10-28/resident-chat-520-safety-plan.md.
Research C1-C7 is adequate; no new regulatory or company facts are needed.

<!-- rpi:phase id=P01 -->
## P01: Implement safety-first matching and regressions

<!-- rpi:task id=P01-T01 -->
### P01-T01: Lock behavior in tests

Use unittest subTest tables for quoted reports and plausible variants:
carbon-monoxide/CO alarm sounding/beeping/going off, reported monoxide exposure,
smoke from socket, room filling with smoke, socket sparking/smoking, electrical
shock, flooded electrics or water leaking through a light. Existing fire, gas,
damp/mould routes stay unchanged. Include home/document/appointment/status words
and untrusted ordinary instructions to prove safety precedence.
Negative table: routine detector paperwork/status, smoke-alarm forms, socket
improvements, smoking policy, water question and all ordinary supported topics.
Assert exact route and HTTP SAFETY equality, source/label, absence of own-home
details and action, and no advisor/provider calls. Run positives before fix to
retain real failure, then repeat after fix.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement bounded matching

Keep existing safety vocabulary first and preserve later branches byte-for-byte
where possible. Add a small readable helper only if the combined predicate is
unwieldy. Reuse words(question); context requires whole words so co does not
match consent/company and socket alone does not become an emergency. Do not
attempt a general natural-language classifier, negate hazards automatically,
or infer that absence of a match means safe. Reuse SAFETY unchanged.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Browser and documentation

Add both quoted reports to existing typed-question browser flow after consent,
assert existing safety answer and no new home details in the latest answer.
Conversation history may retain earlier own-record answers: scope the assertion
to the latest response rather than falsely requiring all history to be empty.
Keep existing browser flow/semantics/assets. Update API README to describe the
bounded safety-first report matching and ordinary detector-query behavior.

<!-- rpi:phase id=P02 -->
## P02: Validate, independently review, and hand off

<!-- rpi:task id=P02-T01 -->
### P02-T01: Local validation

Use the task-owned Python 3.12 session venv; editable core/agents/api dev installed
only after observed ModuleNotFoundError. From src/api, PYTHONPATH supplies tests
and ../core/tests:../agents/tests, not package source hacks.
Run focused resident chat/agenda/assistant tests, then API discovery. Run project
Ruff and format (100), mypy. Browser uses constructed loopback fixtures, no real
SQL/private dataset/remote model. Use pinned axe 4.10.3 checked by existing digest.
All heavy checks take /tmp/ama-rpi-heavy.lock using flock -n in a bounded retry
loop with a monotonic 2400-second deadline; release via owned process exit.
No az, Azure fallback or indefinite blocking. Record commands, counts and skips.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Original independent Review

After implementation and reconciliation, dispatch one fresh reviewer with exact
source and artifact boundaries. Read-only source, write only original Review.
Assess the task, not whole issue acceptance. Route Review findings to later
tasks; do not loop back to Implement or rerun Review within 520-safety.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Local commit

Resolve gh api user, configure repository-local privacy-safe email, and use it
for author/committer. Conventional Commit plus exact required Copilot trailer.
Include research, plan, details, original critique/dispositions, changes, original
Review and state. No secrets or external runtime evidence binaries committed.

<!-- rpi:task id=P02-T04 -->
### P02-T04: Publication boundary

tools/rpi-checks.py preflight unconditionally invokes az bicep version; repository
instructions require a new full exact-head receipt for this final RPI candidate.
Explicit no-az means publication blocked, not permission to downgrade checks.
Do not invoke full gate, push, change PR body, or mark an unpublished correction
resolved. Coordinator must obtain full receipt, fetch current main, independently
assess exact head, push normally, reply with fixing commit and resolve named thread.
State and final response must say local-only if that remains the outcome.

## Current Execution State

P01-T01/P01-T02/P01-T03 and P02-T01 complete. The matcher uses bounded report phrases as
well as word combinations to avoid "see smoke alarm documents" and "filling
forms" false positives. Final scope: 47 hazard and 30 baseline-equivalent
ordinary queries, within the three-method test budget. SAFETY/answer and ordinary
branch ASTs unchanged. Ruff100, format, mypy 97 files, 33 focused tests and
1182-test API discovery (316 skips) passed. Browser passed: 32 axe states,
zero reported violations, seven color-contrast incompletes, no console errors
or external requests. P02-T02 original Review Complete / Residual work; source
conformant with no implementation defects. P02-T03 local fixing commit
8e57253a8dbe30ada2ec747552ef12533e476955 verified with required trailer and
privacy-safe identity; source hashes match the original Review. P02-T04 remains
blocked by the full-gate/no-az conflict, not a waived publication requirement.
RV-001 Medium routes publication to coordinator; RV-002 Low routes contrast/human
acceptance to its existing owner. Original Review is preserved, not repeated.
No push, thread reply or resolution. PR text remains Refs #520. Final handoff
changes only dated evidence/status and does not change the assessed source.
