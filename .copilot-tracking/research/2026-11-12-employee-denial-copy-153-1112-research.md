---
title: Issue 153 employee confirmed-denial copy trace research
ms.date: 2026-11-12
task_id: 153-blocked-copy-readiness-1112
task_slug: employee-denial-copy-153-1112
---

## Outcome

NOT_READY (research-only). No distinct, literal issue #153 criterion 3 gap was demonstrated for the traced action, so no plan, critique, implementation, source edit, regression, original post-implementation Review, PR or acceptance tick was produced. Planning Readiness: Not ready (nothing to plan).

Phases that did not run: Plan, independent plan critique, Implement, post-implementation Review, web-design-guidelines load and fetch (no web edit was made), full or `--changed` gates, hosted CI.

## Pinned inputs

* Worktree `/home/azureuser/source/ama-demo-wt/issue-153-blocked-copy-readiness-1112`, branch `research/employee-denial-copy-153-1112`, target `main`.
* `git fetch origin main` at 2026-11-12 21:4x UTC: `origin/main` = `HEAD` = `59eac895112ebb97cfa6c27413b3d398e6f056e4` (`feat(core): add source-completeness dimension to paired equity check (Refs #128) (#1481)`). Worktree was clean.
* Issue #153 actual body (retrieved with `gh issue view 153`, updatedAt 2026-11-12T21:42:32Z): open; criteria 1 and 4 ticked, criteria 2, 3 and 5 unticked. Criterion 3 reads literally "Error and blocked messages state the reason, owner and next action".
* Actual history: 18 comments (2026-10-15 to 2026-11-12) and a timeline of labels, parent #149, cross references to #215, #149, #242, #402, #350, #501 and project status changes. Material entries: 2026-10-31 closure audit (C3 unmet: "generic/raw API errors, technical refusals and Unknown/Unassigned regulatory ownership still lack a reliable owner/action"); 2026-11-06 #1237 document-control refusals; 2026-11-09 and 2026-11-10 staff-time copy (#1335); 2026-11-10 and 2026-11-11 personal-handoff read and HTTP guidance (#1367, #1376, #1449); 2026-11-12 #1470 proposal-card plain language (not redone here, its finite formatting permission is not renewed); final comment 2026-11-12T21:42:31Z starting this bounded trace with the rule that existing complete wording or exhausted authority means research-only NOT_READY. Raw capture: `/tmp/i153/body.md` and `/tmp/i153/comments.json` (outside the repository).
* Context read: `docs/reference/README.md` index, `docs/reference/memory.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/research/ux/content-standard.md`, the instructions in `.github/`. The employee-facing standard requires a reason, an owner and a next action in blocked messages; this trace checked that literally.

## Trace of one action

Action: employee case workspace, "Ready to book the installation" (POST `/api/cases/{id}/advance`), refused by the safety-stop reason. This is an existing non-funding confirmed blocked action. The funding reason is excluded from the finding (issue #82); it appears in the output below only because the fixture also has no funding.

Code path (all at `59eac8951`):

* `src/api/src/zava_forward/api/web/app.js` `caseView` button at line 1106 calls `refresh(() => api(.../advance))`; `api()` (line 81) copies `data.error` into `e.message` and `data.reasons` into `e.reasons`; the catch branch at lines 1021 to 1026 renders `e.message` as `p.err` plus one `<p>` per `e.reasons` entry, unless the write is recorded or uncertain (history-barrier wording, left untouched).
* `src/core/src/zava_forward/core/store.py` `advance()` raises `GateError(why)` from `gate_reasons()` (lines 169 to 176); `server.py` line 1572 maps it to `409 {"error": "Not ready yet.", "reasons": [...]}`. The open-hazard reason is `Home retrofit work is stopped for safety review. Owner: <hazard owner> (referral follow-up). Next action: obtain external service evidence and an independent decision to restart retrofit work.`

Actual execution, isolated venv `/tmp/i153/venv` with `pip install -e core -e agents -e api` from this worktree (the pre-existing editable installs point at the coordinator checkout, which was not used or modified), the `src/core/tests` dataset fixture on the path only for the test data, real `ThreadingHTTPServer`:

* After `hazard-raise` on case ZF-2 (stage "Final checks before ordering"), the actual API returned `409 {"error": "Not ready yet.", "reasons": ["Funding has not been confirmed. Owner: Sam Example. Next action: check the funding and record it.", "Home retrofit work is stopped for safety review. Owner: Sam Example (referral follow-up). Next action: obtain external service evidence and an independent decision to restart retrofit work.", "Resident decision or authority needs confirmation. Owner: Resident Liaison Officer. Next action: review the affected measure's current scope, supplied answer and authority."]}`. Full output: `/tmp/i153/trace2-out.txt`.
* Actual Chromium (Playwright 1.64.1, installed browsers, served app at `/app`, signed in as the fixture user) showed the Final checks card before the click listing the same three reasons with Owner and Next action, and after the click the status region read `Not ready yet.` followed by the three reasons, each with Owner and Next action. The server reason was not lost. Output: `/tmp/i153/ui-out.txt`.

## Finding

For this action the reason, an owner and a safe next action are already provided end to end, both before the click (Final checks card) and after the confirmed denial (screen text). Reading the catch block alone suggests a bare `e.message`, but the payload carries structured `reasons` that the block renders, so no defect is established there.

Observations that are not demonstrated gaps and are not authorized here:

* The safety-stop "Owner" is the hazard's follow-up owner (the raiser until referral). The decision authority is the hazard hold's `accountable_role` ("Building Safety Liaison"), which the message does not name. Whether to name it is a role and authority wording decision for the owner and the Building Safety Lead, not a literal criterion 3 failure, and it would be speculative role assignment.
* Sibling refusals outside the one traced reason: `400 "This case is not at the final checks."` (stage precondition) has no owner or next action. It is unreachable from the normal screen because the button renders only when `can_advance` is true, so it appears only on a stale view, which the user did not ask to trace. `400 "A single evidenced work order ... Ask the contract manager to issue and book it."` (ZF-3) states reason, owner and next action.
* The generic `Not ready yet.` heading precedes specific reasons; it is not a raw or generic error.

## Authority

No source edit is warranted, so remaining finite history and authority were not consumed. PR #1470's finite formatting permission is not treated as a grant. No funding, resident-facing, proposal-card or status-semantics change was considered.

## Remaining criteria

Issue #153 criteria 2, 3 and 5 stay unproven and unticked: universal core-flow terminology removal, universal error and blocked-message coverage (this trace covers one action only), and named-human resident-wording review (Juan Manuel Servera appointed, no actual review recorded). No accessibility, WCAG or human acceptance is inferred.

## Checks that ran and did not run

Ran: the actual API trace and Chromium trace above (scripts and outputs in `/tmp/i153`, not repository files). Did not run: unit tests, ruff, mypy, journey or axe suites (no code or tests changed), hosted CI, web-design-guidelines fetch, any gate script.
