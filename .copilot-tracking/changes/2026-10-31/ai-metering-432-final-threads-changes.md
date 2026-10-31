---
title: AI metering final threads implementation evidence
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->
Task: issue-432-pr-602-final-threads. Declared scope: full correction plan.

## Implementation Opening

P01 active after one independent critique (original Revise preserved,
direct compatible dispositions applied). Implement bounded mismatch, narrow
report holds and persistent publication fallbacks. PC-001 replaces the original
predicted-sequence design with actual-message transaction finalization.
CI is selected publication gate; the complete local gate was not run.

## P01: Completed Corrections

* P01-T01: specific ModelMismatch preserves closed outcome and bounded model
  through shape_result/worker serialization. Completion suspends the released
  record and quarantines even if another completion guard already denies it.
  Usage settlement retains its independent returned/held liability evidence.
* P01-T02: report parameters validate first. Only consumption DispatchHeld
  becomes unavailable/Unknown in the otherwise complete 200 report.
* P01-T03: strict output remains intact; publish_output logs safe holds and
  returns unresolved metadata. Saved legacy/priority comparison records retain
  original AI output but show and return manual text/items with matching
  source/model/mode and incomplete financial state. Priority overlap reflects
  shown manual items. SQL chat finalizes actual sequence and join in one message
  transaction; JSON saves actual sequence then persists fallback replacement.
  Unexpected financial/message/persistence errors continue to propagate.

## P02-T01: Focused External Tests and Documentation

Three added external test methods plus extension of the existing HTTP method
(below four-method maximum; no removals) cover five returned-model boundary
values, real loopback/worker/JSON serialization/quarantine/suspension/settlement,
six SQL/JSON exact-capacity publication routes, persistent manual response
consistency, no redispatch, recovered incomplete/Unknown joins, actual HTTP
capacity/invalid-schema holds, invalid-input 400 and SQL/JSON chat failures/
other-writer actual sequence. Core/API guides, Tokenomics, index and append-only
knowledge log updated; original log entries and regulatory evidence preserved.

## P02-T02: Validation

* API ruff check . and ruff format --check .: pass (66 formatted files).
* API mypy: pass (124 source files), requested PYTHONPATH.
* Core ruff check . / format --check . / mypy: pass (117 formatted files,
  170 typed source files).
* Relevant unit command from src/api with
  PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests:
  `python -m unittest test_ai_consumption_api test_ai_consumption test_ai_tasks
  test_assistants test_assistants_dispatch test_assistant_release test_chat_panel
  test_chatthreads -q`: 326 tests, OK, 51 existing skips. Optional browser/full
  SQL/platform checks were not activated by this focused unit run; hosted CI
  remains separate. Expected missing-law-store warnings do not indicate success
  for legal rule evaluation.
* Final test-only typing guard: exact-capacity method rerun, pass.
* git diff --check: pass; knowledge log diff is append-only.

Initial targeted attempts exposed fixture admission/latency equality issues and
new-test typing errors, all corrected before Review. Global API typing also
found missing SDK distributions; system pip correctly refused unmanaged install.
Restored the existing manifest dependencies with pip/editable installs in an
external isolated session venv, then passed API typing without exemptions.
No manifest change, global install or secrets. Original critique remains Revise
with direct resolving plan/test evidence; no second critique ran.

## Remaining Work

P02-T03 ordinary commit/push and exact-head CI verification/replies/resolutions.
No source blocker; hosted/human approval remains unclaimed.

## Original Independent Review

Execution Complete; outcome Conformant for source scope; zero material findings.
The original record includes tracked source diff SHA-256
2d7d4829817035bedccf8302696d38b601509e86503b36c15cf3b12d27491cb2 and independently
passed API/core static checks plus nine composed test methods. No repeated Review.

## Publication Continuity

Remote rubric automation advanced the topic by one rubric-only commit,
007149d7. Safely fast-forwarded it without changing the reviewed tracked diff
hash above. Fresh main advanced to f11d29e4 (#601 employee acceptance tooling/
documentation). An attempted main merge correctly refused overlapping
uncommitted documentation; no stash, discard or partial merge occurred.
Commit the reviewed correction/evidence first, then merge main with main's
rubric and both knowledge histories retained, and revalidate relevant checks.
This is ordinary ancestry preservation, not history rewriting.
