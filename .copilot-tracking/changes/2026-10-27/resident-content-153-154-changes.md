---
title: Resident content and journey changes
description: Implementation evidence for issues 153 and 154
ms.date: 2026-10-27
---

## Context and execution boundary

Task ID: issues-153-154; slug: resident-content-153-154. Full plan execution
under .copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md and
matching phase details. Research Complete/Ready; one critique Complete/Revise,
PC-001/002 corrected directly by planning parent. Original critique preserved.
P01 then P02 are active; P03 requires independent Review and publication.

Approved targets: existing content standard, residents journey, index/log;
four existing JS assets and <=4 new methods in existing content test.
No backend behavior, CSS, dependencies, messaging, live accounts/data or Azure.
Small change: neither heavy --changed nor forbidden --all is planned.
Required local units/syntax/owned synthetic browser checks block publication
if failed; actual human wording/usability/AT review remains Not run.

## Planning reconciliation

PC-001 added an explicit fail-closed publication transition.
PC-002 replaced the nonexistent resident_commitments browser script with
the existing design-system owned server plus a session-only four-surface
copy callback, repository-local TMPDIR and explicit semantic coverage limits.
No source or test expansion, user decision or repeated critique.

## Implementation and validation

P01-T01 complete: existing content standard now has a dated surface inventory,
residual dynamic/stored/technical wording and missing-owner/action findings
with responsible remediation roles. Reviewer appointment corrected from actual
owner comment; review remains Not run.

P01-T02 complete: existing residents.md now has J1-J6 task flows/text wireframes,
shared inclusive/assisted/safe-contact rules, R1 representative field/action/
expiry/revocation contract, negative scripts and honest criteria disposition.
Index updated and log appended; no extra competing documentation page.
No operational policy or real contact/SLA was invented. P02 proceeds next.

### P02-T01: Literal copy and regression

Complete. Four JS files only: app draft heading and named-review/no-send
paragraph; assistant requested-mode label and explicit draft-review disclaimer;
representative exclusive review-date label; ordinary same-role wording.
Three added methods in existing test_content_standard.py (maximum four,
none removed) and timecapture.js added to the lexical file list.
All payloads, values, callbacks, authorization/approval/consent behavior,
source quotations, CSS/tokens/non-colour/reduced-motion mechanisms unchanged.

### P02-T02: Local validation

Complete for the approved engineering boundary, not human acceptance.

| Check | Command or evidence | Result |
| --- | --- | --- |
| API targeted units | From src/api, `TMPDIR="$PWD/../../.venv/ux153-tmp" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_content_standard test_design_system test_accessibility_baseline test_resident_api test_assistants -q` | 139 discovered, OK, 51 skipped: 50 opt-in disposable MSSQL tests and one opt-in browser test; SQLite and HTTP resident/assistant tests ran |
| Existing opt-in resident browser | Same cwd/environment with `ZF_RESIDENT_BROWSER=1`, `../../.venv/bin/python -m unittest test_resident_api.ResidentApi.test_browser_commitment_reassignment_response_closure_and_remedy_reopen -q` | 1 test, OK; explicit reassignment, response closure and independent remedy recovery on synthetic loopback fixture |
| Existing design/workbench browsers | From src/api, same TMPDIR and bytecode setting, `../../.venv/bin/python -m checks.design_system_browser_check` | Pass; owned/health-checked loopback servers, Fluent values, focus, named status, 320/390/1280 reflow, reduced motion zero, forced-colour signals and all-role workbench regression; no uncaught JS errors |
| Four-surface rendered copy callback | `checks.design_system_browser_check.main(rendered_copy)` from session script, same TMPDIR, `PYTHONPATH=.:tests:../core/tests:../agents/tests` | Pass; actual case draft and expanded representative form; actual assistantProposal with constructed accepted proposal and timeView with constructed status; no accept/enable action; no uncaught JS errors |
| JS syntax | Repository root `node --check` for app.js, assistants.js, panels.js, timecapture.js | All four pass |
| Markdown and local links | Reviewed added Markdown; resolved local links in both changed UX docs and computed both new index anchors | Pass; no new broken targets/anchors |
| Diff whitespace | `git diff --check` | Pass |

Browser: Chromium 156.0.8078.4. Four-surface callback asserted:
draft heading and exact named-review/no-send text; representative label
associated with its date input; requested-mode label, exact AI warning and
not-approval/consent/safety paragraph on constructed accepted proposal;
same-role refusal on constructed time status. These last two are render-copy
checks, not end-to-end proposal acceptance or time enabling.
Session-only callback path:
`/home/azureuser/.copilot/session-state/072d3e9b-83a5-4dc4-9113-9fb69d1e238e/files/ux153-copy-browser.py`.
It is not a shipped test or a required application dependency.

Initial unit invocation failed because no src distributions were installed.
Created worktree-local venv with system site packages and installed editable
src/core, src/agents, src/api using pip `--no-deps`; no manifest changes.
First browser attempt then failed for missing Playwright; installed the
existing manifest's `playwright==1.64.0` with pip and reran successfully.
No browser download was needed. Unit/browser HTTP fixtures log that the law
store is not loaded; rules remain explicitly unknown, not an accepted
regulatory result. Those warnings did not fail the selected tests.

No disposable MSSQL run, full suite, full/scoped rpi-checks gate, paid model,
Azure, private data, actual resident contact or assistive-technology/user
acceptance occurred. This documentation/literal-copy increment is not large;
the conditional --changed allowance was unused and heavy lock not acquired.
The owner's explicit no---all/local-only instruction supersedes the default
full gate for this task; no receipt or publication-gate success is fabricated.

## Pre-Review reconciliation

P01 and P02 tasks/phase markers complete; matching details current.
Remaining active P03-T01 is one independent Review plus conditional publication.
Human exact-wording review by appointed Juan Manuel Servera, #155 usability/AT
and OD-41/42 operational decisions remain outstanding and outside this
synthetic-only delivery. Both issues remain Refs, no acceptance boxes edited.
Guidelines fetched fully before edits and refreshed fully before Review.
No implementation-blocking engineering result remains unresolved.

## Independent Review and conditional publication

The one independent Review completed with outcome Conformant for this bounded
delivery, not whole-issue or live-use acceptance. No introduced defects.
Original Review record:
.copilot-tracking/reviews/logs/2026-10-27/resident-content-153-154-review.md.
It independently reproduced the targeted units, opt-in resident browser,
design/workbench browser and four-surface callback, syntax and links.
Review source diff against 0ded682bab690d24eb59b78e704be82d337bf6cd:
`97dee43f07ed09aa0e21e2a056badb5f2ee8d89bf182d946e8e8acee6e64cc81`.
Parent reproduced that same source hash after Review; no source correction,
base change, second Review or issue acceptance checkbox edit.

Seven inherited/planned residuals remain: RV-001 universal errors/content;
RV-002 form/announcement/unsaved recovery; RV-003 URL state;
RV-004 growing lists; RV-005 supporting display/localisation;
RV-006 unapproved fixed retention wording; RV-007 actual human acceptance.
The retention statement is an existing internal policy-status tension, not a
new legal finding; no operational period was selected or storage changed.
All findings are routed to distinct later work with owner/next action in the
Review/state. No residual was silently repaired inside the completed task.

RPI task completed through Review; automatic state moves to Follow-up.
P03-T01 publication remains active until commit/push/PR evidence is available.
Named human acceptance and hosted/owner approval remain incomplete.
