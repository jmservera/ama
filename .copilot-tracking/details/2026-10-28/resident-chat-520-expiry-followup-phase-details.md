<!-- markdownlint-disable-file -->
---
title: Resident chat 520 proposal expiry follow-up phase details
ms.date: 2026-10-28
---

# RPI Phase Details: resident-chat-520-expiry-followup

## Metadata

Task ID: 520-expiry-followup. Plan:
.copilot-tracking/plans/2026-10-28/resident-chat-520-expiry-followup-plan.md.
Research: .copilot-tracking/research/2026-10-28/resident-chat-520-expiry-followup-research.md.

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Implement and validate expiry boundary | Complete |
| P02 | Independent Review and publication | Review Complete / Residual work; publication pending |

<!-- rpi:phase id=P01 -->
## P01: Implement and validate expiry boundary

Context: C1/C2/C4 establish the missing post-authorization expiry check and existing rollback.
Intent: preserve the transaction and add only expiry selection and one shared final instant.
Boundaries: no API, schema, browser, clock signature or idempotency changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Regression, red, minimal fix and docs

Use the existing NOW/temporary agenda fixture. For each boundary, create a proposal at NOW,
set callable time to expiry minus one second, and advance it in authorised() to expiry
minus one microsecond, exact expiry, or expiry plus one microsecond. The offered slot is
the next day, so only expiry can cause the conflict. Assert authorization was invoked.
For rejected bookings, reopen Agenda, assert own() is empty, then find/book for another
owner at the final instant and assert the original slot is still available.
Use a distinct disposable agenda for each subtest so even red failures cannot contaminate
later cases. This strengthens the existing approved boundary, without adding test methods.
Maximum additions: one unit method, no removals, no generated output.
Run the new method before changing agenda.py and preserve its expected failing output.
Final code selects o.expires with s.*, samples the clock after authorization once, and
rejects expires <= instant or starts <= instant with existing AgendaConflict.
Keep existing committed-booking fast path unchanged. README clarifies the two deadlines.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Locked validation

Actual probes found no ruff or mypy in current Python. Restore existing manifest-pinned
development dependencies in a task-owned external virtual environment, installing core,
agents and api distributions rather than using source-root path workarounds.
Heavy operations acquire /tmp/ama-rpi-heavy.lock using nonblocking flock with 60-second
retry, up to 40 minutes. Retain external output and original failing evidence.
From src/api use PYTHONDONTWRITEBYTECODE=1 and
PYTHONPATH=tests:../core/tests:../agents/tests for unit/API selectors in the plan.
Run ruff check --line-length 100 ., ruff format --check --line-length 100 ., and mypy
using API configuration. No browser-facing edits means browser harness is not applicable.
Completion evidence: actual command logs, exit codes, test counts and checks, never
relabel preexisting success as current. Full gate unattempted because az is barred.

<!-- rpi:phase id=P02 -->
## P02: Independent Review and authorized publication

Depends on P01 completed evidence. Activate rpi-review once and delegate independent
assessment of exact source diff and validation artifacts. Preserve findings and route
later work without another Review. Leave human approval unchecked.
Record actual outcome and assessed boundary. Resolve authenticated account with gh api
user; configure repository-local privacy-safe author/committer email and required trailer.
Fetch origin before commit/push; if topic advanced via github-actions[bot], rebase onto
it as explicitly authorized, rerun affected checks and record changed boundary.
Do not force push or modify PR closing semantics. Verify remote includes the tested fix,
reply in PRRT_kwDOUU8JX86xTMcu with commit and results, resolve via GraphQL and verify.
Full-gate failure is a declared constraint, not a bypassed or fabricated success.
