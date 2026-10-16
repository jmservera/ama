---
title: Regulatory security and privacy phase details
description: Evidence ownership and implementation boundaries for issue 217
ms.date: 2026-10-16
---

## P01-T01

Add RegulatoryChat to the existing auxiliary capability map, not the mutually
exclusive staff-role map. Enforce trusted capability checks before regulatory
routes and generic access to regulatory threads. Local password mode remains
explicitly synthetic-only. Register all three auxiliary roles in infra and keep
existing staff-role tests distinct.

Use ChatPrivacy.decision for own-thread retention reporting. Derive review due
from created_at and configured days; do not delete or equate a SYNTH reference
with DPO review. Other regulatory classes remain unknown pending DPO schedule.
No new table is needed.

Inside RegulatoryChat SQL repository transactions, use the existing store audit
append primitive so a failure rolls back both messages/referrals and audit.
JSON's separate file ledger cannot promise cross-file atomicity; state that
limitation explicitly. Record role, citation IDs, reply hash/model and turn
sequence, not content. Existing immutable SQL rule/check/alert events are their
audit records; do not duplicate content into diagnostics.

Require nonempty reasons before the significant-decision evaluator returns clear.
Bump the engine version so older incomplete checkpoints are not reused.

## P02-T01

Maximum 20 added test methods, no removals. Use synthetic fixtures only. Test
positive paths and negative role/object binding, direct and generic HTTP access,
unknown/invalid/SYNTH retention and exact due boundary, SQL audit failure/restart,
reason omission, append-only rule/check/alert records and adversarial inputs.
Existing agents injection tests must still pass unchanged.

## P02-T02

Install projects with pip into an isolated session venv after missing ruff/mypy
was observed. Use absolute project test PYTHONPATH values. Run existing focused
core/API/agents/infra suites, project ruff/mypy and loopback HTTP tests.
No deployment or paid call. Draft DPIA extends the existing chat-memory record
with regulatory data map, risks, purpose, rights/holds and DPO review questions.
README acceptance audit distinguishes all seven issue criteria.

## P03-T01

After P01/P02 implementation and validation, record one Review for that source
and evidence boundary. Publication is still pending at Review, not a source
defect or a claim that the PR already exists. Then commit with the authenticated
account's noreply identity and required trailer, push the topic branch and open
the requested Refs-only PR. Do not modify issue checkboxes or merge.
