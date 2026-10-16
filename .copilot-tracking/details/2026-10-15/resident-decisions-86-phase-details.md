---
title: Resident decisions phase details
description: Marker-addressed implementation context for issue 86
ms.date: 2026-10-15
---

Task: issue-86 / resident-decisions-86. Evidence C1-C9 and W1-W2 in research.
No blocking design decision for the bounded synthetic slice. Operational
authority, retention, complaint integration and live evidence remain open.

<!-- P01 -->
## P01: Core semantics and guards

<!-- P01-T01 -->
### P01-T01

Extend ResidentDecisionMixin, do not create a second decision system.
scope_record requires an explicit measure, scope reference, design version and
source; context changes leave historical versions intact and current answer
unknown. representative_record versions authority with evidence, wishes,
task list, validity/review dates and safe-contact reference. Decision writes
must match the registered current context and require a supplied source.
Representative answers reference the exact authority version checked at write.
Direct resident statements remain recordable despite invalid representative
authority. A negative answer records measure-specific human review needed.
An explicit new supplied acceptance is required before readiness can return.
Critique corrections: explicit technical design is required, context revisions
are monotonic, review date is exclusive at use time, and referenced latest
authority is revalidated on every release. A fresh acceptance after a negative
answer also requires a supplied human review evidence reference. Independent
review names its contested actor and reference; that actor and its service
handler cannot be the reviewer, and only the reviewer updates/closes it.

<!-- P01-T02 -->
### P01-T02

Use shared resident_gate reasons for all discretionary release paths and the
SQL transaction's dependent-case guard. Legacy aggregate answer is history,
not consent to new scoped work. Legacy aggregate refusals also remain history:
they cannot override newer scoped choices or block independent siblings.
Draft templates
must not disclose through an unchecked legacy representative. Projection must
withhold new authority records and source narratives from roles without need;
existing AI input allow-lists must not gain these fields.
Work-order versions store explicit resident_bindings (measure/context revision).
Unknown or changed bindings block; case-wide advance binds all current measures.
SQL transactional checks carry those bindings and recheck current authority and
context with the same clock. Quality submissions bind their supplied measure
scope revision; acceptance/handover guard only that binding. Legacy/unbound
quality evidence remains evidence, never release authority. Urgent hazard
intake/release remains independent.
Detach all nested projections; new narratives/authority only for the
intersection of resident and recorded-need roles. AI proposals use staff-facing
non-addressed fallback, not the protected resident/representative template.

<!-- P02 -->
## P02: API/UI and regression evidence

<!-- P02-T01 -->
### P02-T01

Reuse POST /api/cases/{id}/resident dispatch; every actor comes from the session.
Update staff forms for scope, source, authority and non-prefilled decisions.
Remove the misleading case-wide answer editor, retaining its historical display.
Expose context, readiness and representative status to permitted staff.
Independent review is separate from formal complaint and requires distinct
service/redress owners. No invented real complaint URL or live sending.

<!-- P02-T02 -->
### P02-T02

Two new modules only: JSON/SQLite core contract tests and authenticated HTTP
app exercise. Include reject-without-mutation, reopen persistence, expiry
boundary, multiple representatives, interpreter-only, safe-contact changes,
stale context, legacy acceptance, role projection, AI nonmutation and paused
case complaints/hazard availability. Adapt shared constructed readiness
fixtures only where existing tests genuinely need a prior supplied consent.
No changes to synthetic generator seeds that would fabricate resident answers.
Include actual technical-action invalidation, context switch-back, B-only
release with A paused, authority changed after acceptance and stale two-store
write refusal. Check projected GETs cannot mutate saved case or history.

<!-- P03 -->
## P03: Validation and delivery

Authorized delivery follow-up: merge current origin/main using the owner's
exact fetch/merge strategy. Preserve both feature sets, append-only log and all
mypy override entries. Recheck hazard/technical/stock/resident gates together,
portable SQL and authenticated endpoint inventory/role coverage. Run full
core/API/agents suites with absolute source/test PYTHONPATH, then
`/tmp/zf164/bin/mypy .`, Ruff check and format check in touched projects.
Update evidence and PR #319 with Refs #86, commit and ordinary topic push.
Resumed 2026-10-16: all eight conflicts resolved; core 392, API 516 run/99
skipped and agents 70 suites pass. Requested mypy/Ruff/format checks pass
in all three projects. See the changes record's resumed integration results;
hosted CI and live/human acceptance are not inferred from these local results.

<!-- P03-T01 -->
### P03-T01

Missing tool/package probes justify pip editable dev installation in a local
venv. Run all five suites, lint/format and typing using component configs;
preserve migration exemptions, add no broad new suppression. API uses shared
fixture PYTHONPATH per src/README. Record precise commands, failures and fixes
in the changes artifact. Local endpoint tests must actually bind loopback and
exercise HTTP, not merely inspect source.

<!-- P03-T02 -->
### P03-T02

Update core/API READMEs, knowledge-base routing/index and append-only log.
One final review compares plan/changes/test evidence and routes residual work
without another implementation/review loop. Commit code and all RPI artifacts,
use authenticated noreply identity and required co-author trailer; push named
branch and open Refs #86 PR to main with commands/results and unticked criteria.
