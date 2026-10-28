---
title: Case journey unsaved-edit correction changes
description: Execution and validation evidence for the seven-thread correction
ms.date: 2026-10-28
---

## Invocation and Scope

Full correction plan P01/P02. Research Ready, one critique executed and directly
disposed. First dependency-ready work: P01-T01. Existing branch fast-forward
checked, already up to date at d3fbba58 (bot rubric commit included).

## Execution

P01 complete. Source boundaries and tests remain as locked in plan.
No Azure/az, secrets, .env, private dataset or remote mutation performed.

* P01-T01 retains the live document output node in the case session, without
  retaining the upload form or stale case-mutation closures. aiNotes captures
  submitted text/reason and updates the read-only document wording on Edit.
* P01-T02 stores unresolved field snapshots in the case session. Live clean
  controls remove their snapshots; dirty controls update them. Pending loaders
  cannot erase the cache. Proposal restoration remains ID/revision-bound;
  verification clears submitted metadata only, not unsent JSON.
* P01-T03 recorded forms capture immutable values before invoking async work.
  Upload kind is captured before FileReader. Handoff runs its mutation inside
  refresh. Resident forms pass dispatch snapshots through response handling.
  Shared comparison preserves later text, checkbox and even same-name file
  replacements. If success removes the form, later edits remain copyable.
* P01-T04 checklist fields use measure/version/item keys and restore only after
  async construction. Other measures/versions recover separately. Funding
  textarea keys use AI record identity; older edits never replace fresh AI text.
* Earlier recovery controls retain original binding/type metadata. Explicit
  discard removes both their UI and cached keys. Existing case-leave warnings,
  permissions and server source-hash validation remain authoritative.

No change to `case-workspace.js`, journey algorithms, CSS, endpoints or schemas.
Related API guide documents preservation and this correction's lock bound.

## Validation and Publication

System Python lacked Playwright; existing repository .venv imports Playwright
and installed API correctly. Use that environment, no install needed.
Mandatory complete publication gate calls prohibited az; do not invoke it.
Permitted static/unit and bounded shared-lock browser validation completed.
Push and thread resolution blocked pending compliant required gate evidence.

## P02-T01 Commands and Actual Results

External evidence root:
`/home/azureuser/.copilot/session-state/637bc46e-ba61-44da-a786-3dd2de5194f6/files/correction-validation/`.
No generated browser output was added to git.

* `node --check` on app.js, assistants.js, ops.js and panels.js: pass.
* From src/api, `../../.venv/bin/python -m ruff check .`: pass.
  `ruff format --check .`: 48 files already formatted.
  Configured line limit 100; all newly added Python lines also independently
  checked at <=100, including exempt legacy browser code.
* From src/api, `../../.venv/bin/python -m mypy`: success, 94 source files.
* `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m
  unittest discover -s tests -q`: exit 0, 1158 tests, 314 reported skips,
  443.683 seconds (`api-unit.log`). These skips do not establish full gate,
  SQL/integration or live-provider acceptance.
* Latest affected-suite command: same PYTHONPATH and interpreter, `-m unittest
  test_case_journey test_design_system test_content_standard test_handoff_api
  test_ui_support test_ai_tasks test_assistants test_resident_api -q`: exit 0,
  212 tests, 51 reported skips, 52.199 seconds (`focused-final.log`).
  Earlier focused semantic/mutation run: 40 tests, no skips. Final semantic
  check after changes: 24 tests, no skips.
* Journey command from src/api: same PYTHONPATH/interpreter, `-m
  checks.case_journey_browser_check --axe <evidence-root>/axe-4.10.3.min.js
  --out <evidence-root>/journey-09`: exit 0, 141 PASS assertions.
  Chromium 156.0.8078.4, pinned/hash-verified axe 4.10.3, 38 scans,
  zero detected violations and zero uncaught page errors. Original keyboard,
  all six journey steps, retained tabs, forced colours/reduced motion, reflow
  and real chrome.tabs.setZoom=2 assertions remain. Screen-reader and staff/live
  acceptance are not implied.
* Assistant command: same PYTHONPATH/interpreter, `-m
  checks.assistants_browser_check`: exit 0, 30 checks (`assistants-02.log`),
  including overlapping loaders, prior-revision recovery and own verification.
  Synthetic provider only; no billable model or retained data accessed.

Every browser admission used `flock -n` on FD 9 for the mandated shared
`/tmp/ama-rpi-heavy.lock`; retry every 15 seconds with a 2400-second deadline.
One attempt waited about 75 seconds for another owner. Final journey admitted
2026-10-28T21:50:04Z. Locks released immediately on each suite's completion.
No indefinite blocking or foreign process/resource mutation.

## Preserved Failed Attempts and Corrections

Original focused unit extraction failed because the new shared snapshot helper
was not included in its isolated Node fixture. Include the shipped helper,
including same-name file-replacement semantics; subsequent semantic tests pass.
Journey attempts 01-06 retain their original external logs: Playwright requires
a Python handler wrapper, recovery details were already open after restoration,
the fixture uses coordinator@example.test rather than rae@example.test,
FileReader dispatch requires request-event synchronization, and a call changes
the document's source hashes. The Edit display check now obtains fresh source
evidence after proving unsent edits survive the call, preserving the server's
hold/approval boundary rather than weakening it.

Mypy initially rejected nullable post_data_json indexing in the new browser
assertions. Explicit dictionary guards resolve all four errors. Browser-08
proved measure/version and file isolation; final journey-09 additionally proves
two distinct AI record identities and vanished-form recovery through another
refresh. Earlier evidence is not overwritten or relabelled as success.

## Review Handoff and Remaining Work

Assessed implementation diff against d3fbba58, eight source/test/guide files:
SHA-256 `bfac509bb360f234ada27986406f0b6fce060890918d64f00714650357b41b40`.
One independent original Review executed: Complete / Not accepted, two High
checklist ownership defects RV-001/RV-002. It remains immutable. Later scoped
implementation and exact regressions are recorded in the checklist-findings
changes artifact; no repeated critique or original Review.
P02-T02 local commit completed in b314ed00; P02-T03 remains blocked. Human
screen-reader, staff usability, live deployment and hosted acceptance remain
pending. Later fixes/tests do not establish independent closure.

## Local Commit and Remote Handoff

Source, regressions and all dated original/later RPI evidence committed in
`b314ed0061a7f8447ab39b159cb78b457324c4ba` with Conventional Commit message,
authenticated privacy-safe author/committer and required Copilot trailer.
Final handoff is documentation-only; source/test/guide diff identity remains
`20b79ed6e234cfc904e040ab5505dbe87068dc23cb8049cade63a20420cd0ea3`.

Read-only GitHub recheck after commit confirms PR #529 remains OPEN at remote
d3fbba58 on the requested topic, with all seven named threads unresolved.
No push, PR-text update, reply or resolution was attempted. Required full gate
cannot run without prohibited az, and later source lacks independent exact-head
acceptance. Preserve `Refs #526` when eventual gated publication becomes possible.
