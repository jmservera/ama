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

Implementation and original RPI evidence committed as 77c58553 with the
required privacy-safe identity and co-author trailer. Main f11d29e4 merge
required three documentation/rubric conflict resolutions: main rubric bytes
selected exactly; both complete knowledge log histories and both index entries
retained. A subsequence check proves neither full log history lost any line.
Correction source/tests remain byte-for-byte unchanged from 77c58553.
Merged API lint/format/mypy pass (67 formatted files, 126 typed source files);
all four correction methods pass again, no skips. Original independent Review
is unchanged, not repeated. Ready for ordinary merge commit/push and CI.

## Hosted Correction Evidence

Pushed merge candidate 34cefd51. Source CI 41212264506 failed only core's
existing sensor-privacy transport test: its unrestricted Mock returns a Mock
for the new publication helper rather than None. Update that existing external
fixture explicitly; do not weaken the production status contract.
Rubric run 41212264566 completed but its status is 76/100 versus 77/100, a
publication blocker rather than a success. Automation advanced only rubric
outputs to 34b3259c; safely fast-forwarded.

Hosted source review found two tightly coupled completion defects: a revoked
release cannot be suspended, and transactional assistant output linkage can
roll back the very mismatch quarantine at capacity. Preserve the original local
Conformant-for-source Review unchanged; these later concrete findings are
additional correction evidence, not a repeated Review or relabelled verdict.
P02-T03 now includes skipping suspension for already terminal releases and
staging publication hold handling before task/event serialization, retaining
quarantine/settlement and withholding actionable output with unresolved state.
Add the fourth permitted external method for revocation/capacity combinations;
update the existing sensor mock only. Required checks and CI must pass before
claiming/closing these findings.

Implemented the later hosted findings directly: only active releases are
suspended; revoked/suspended records retain terminal state while completion
saves mismatch evidence. Assistant publish_output runs in the authoritative
transaction before task/event serialization. A hold saves unresolved/Unknown
attribution, withholds actionable output, retains quarantine (or fails the
otherwise ready proposal to the manual route), and closes attempt settlement.
Fourth external method proves eight matching/mismatched-model, capacity and
revocation combinations, including actual 10,001/10,002 event partitions.
The existing sensor-privacy Mock explicitly returns None from publish_output.

API/core ruff, format and mypy all pass after this source correction. New
completion-combination and former CI-failing sensor test pass (2 methods).
Final relevant API-run command additionally includes test_sensor_privacy:
344 tests, OK, 52 existing optional skips. Full core suite is also running to
verify the previously failing CI scope rather than only its individual case.
No further critique or Review is run; original local/hosted outcomes retained.

Full core suite completed: 1,638 tests, OK, 206 existing optional skips.
Correction c74e891c was ordinarily pushed. New main #604 advanced while tests
ran; PR became conflicting, so pull_request source/rubric CI did not schedule.
Merged origin/main 28fbe6b6, selecting main rubric exactly and retaining all
knowledge log entries. No correction source/test bytes changed during this
merge. Revalidate merged API static checks and push merge to restore CI.
