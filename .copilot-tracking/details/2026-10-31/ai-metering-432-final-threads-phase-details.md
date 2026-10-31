---
title: AI metering final threads phase details
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->
Task: issue-432-pr-602-final-threads.

<!-- P01 -->
## P01: Corrections

<!-- P01-T01 -->
### P01-T01

C1-C2: introduce a specific mismatch exception carrying only a bounded model
string (<=512) or None. Bound receipt returned_model as well. The durable model
field receives a consistent 512-character shape_result bound; other metadata
retains its current bounds. evidence() maps
only that exception to model-mismatch, preserving usage and withholding text.
Assistants.complete handles that outcome independently of retryable errors,
uses existing quarantine/release suspension, and marks mismatch attestation.

<!-- P01-T02 -->
### P01-T02

C3: validate parameters first; nest only the SQL report read in DispatchHeld
handling. Use existing unavailable/Unknown report shape plus the safe hold code.
Do not catch arbitrary database errors or mask malformed parameters.

<!-- P01-T03 -->
### P01-T03

C4-C7: keep strict Consumption.output() for immutable joins and repairs. Add
a publication-only helper returning unresolved status/reason/cost on
DispatchHeld, logging only its safe code. Legacy/priority catch after initial
save, retain original AI comparison, update shown source/model/mode/citations
or items to the manual route, attach unresolved attribution, and save consistent
state without another provider call. Envelope must reflect fallback as well.
SQL chat uses a private finalization callback after actual sequence allocation,
inside the existing message transaction, passing store.db to strict output.
On hold mutate the not-yet-inserted message to FALLBACK/no evidence/workflow-only;
the same transaction commits message and any successful join, or rolls back.
JSON saves the actual message first, links its real sequence, and on hold
replaces only that message's content/evidence/model under Store.lock and saves.
Receipt includes unresolved/Unknown state. No public message-edit API or schema.
Non-hold/link/save errors propagate; SQL rollback leaves no phantom join.

<!-- P02 -->
## P02: Evidence and Publication

<!-- P02-T01 -->
### P02-T01

Extend the existing typed external API harness (maximum four test methods,
no removals). Construct repeated closed-schema price events to exactly 9,999
after authority; real request adds reservation+completion. No private datasets.
For each JSON/SQL draft/priority/chat verify persistence, fallback consistency,
safe metadata, 10,001 threshold, no extra request, restored incomplete joins.
Mismatch fixture controls test bounded model behavior and worker roundtrip.
HTTP tests verify actual response/status/sections under capacity/invalid evidence.
The fourth test method covers SQL/JSON unexpected publication errors, message
save failures and actual-sequence finalization after another SQL writer advances.
Update only source-only documentation, knowledge index and append-only log.

<!-- P02-T02 -->
### P02-T02

Run ruff check ., ruff format --check ., mypy from src/api; core static checks
cover typed helper/chat changes with core's config. Unit tests run from src/api
with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Use existing dependency environment if available; install with pip only after
a missing tool/dependency failure. One independent Review assesses the complete
implementation boundary, not hosted/human/live approval; preserve its original
outcome and route open findings to later work without repeating Review.
No unresolved scoped finding permits a success claim or thread resolution.

<!-- P02-T03 -->
### P02-T03

Read gh authenticated user; use local privacy-safe email for author/committer.
Commit all current-task implementation and original evidence with supplied
co-author trailer. Ordinary git push -u origin HEAD, no force or PR merge.
Await successful applicable CI on the exact pushed PR head before final
thread resolution; a pending reply may disclose pending validation.
Reply to each precise thread with commit/test evidence and resolve via GraphQL.
CI is the explicitly selected publication gate; report pending/failing hosted
checks accurately and leave #432 referenced rather than closed.
