---
title: Resident chat RV-001 phase details
description: Execution and validation boundary for the issue 563 follow-up
ms.date: 2026-10-30
---

## P01-T01

Completed. Narrowed chat.route repair admission using
host-owned lexical/intent checks. Do not send refused text to a model for
classification. Safety stays first. Preserve existing protected-topic ordering,
fixed-topic behavior, own-case projection and all inference accounting.
Tests belong outside the installed package in src/api/tests.

Use constructed loopback HTTP fixtures and a scripted AzureAdvisor with mocks
for reservation, token and transport. Negative examples must equal the existing
host answer, not merely return 200 or an AI fallback label. Positive household
repair examples must reach generated text when enabled. No actual Azure call.

## P02-T01

Complete. P01 evidence: 22 chat tests pass; 30 negative/protected route examples
and ten generated positives. Household subject/predicate and bounded
information-query matching reject keyword-only/off-topic text; command guards
and single-clause admission keep action/instruction text on the host.
Unrecognised/mixed requests are conservatively refused, not model-classified.

Run README resident discovery and complete configured API Ruff/format/mypy.
Existing opt-in local SQL skips must be reported separately. Use an existing
installed runtime if valid; install only upon a missing-dependency failure.
Store raw logs in this session's external files directory. No web files change;
the existing browser evidence is historical, not rerun or current UI acceptance.

Final resident discovery: 149 run in 66.767s, 142 passed, six existing opt-in
local SQL skips and one existing opt-in browser skip. API Ruff lint passes,
59 files already formatted, configured strict mypy passes for 113 source files.
No new dependency/install needed. P01/P02 evidence and markers reconciled.

## P03-T01

Original handoff: independent Review of baseline 66924f3a to then-current working diff
and child evidence. Review output is resident-chat-ai-563-rv001-review.md.
Local commit and post-commit full gate had not yet executed at that handoff.
Fresh read-only fetch shows origin/main f7482602 is an ancestor of HEAD;
the parent's original ancestry failure remains historical, not a current claim.

Run one independent rpi-review for this bounded follow-up, preserving the
parent's original adverse Review. Reconcile current child artifacts before
handoff. Commit source and dated evidence locally with authenticated GitHub
noreply author/committer, Refs #563 and the supplied Copilot trailer.
Then attempt the complete local gate externally; no publication is requested.
If ancestry or tooling blocks it, retain the blocker without cloud fallback,
history rewrite, skip token or fabricated receipt.

Executed: this task's Review Complete / Not accepted; routed implementation
has separate complete-admission artifacts. Local persistence in 48001b35
retains the adverse Review. Complete gate subsequently ran and failed on
unexpected API integration/dependency skips, blocking browser/mssql.
No accepted original Review, passing receipt or publication is claimed.
