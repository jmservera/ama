<!-- markdownlint-disable-file -->
# RPI Changes: Resident generated answers

## Metadata

Task ID: issue-563. Date: 2026-10-30. Declared scope: full plan.
Plan: .copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md
Details: .copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md
Original critique: .copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md

## Execution Status

P01/P01-T01, P02/P02-T01 and P03/P03-T01 executed. Task loop complete;
original Review Not accepted, full local gate blocked, no publication.
Original critique executed once,
Pass with no findings. Approved source/test/UI boundaries are in the plan.

## Execution Summary

Research isolated host routing and guidance-ID-only output as source causes.
Default-off and omitted Bicep settings are prerequisites, not verified live state.
Implement generation without bypassing consent, accounting or authority checks.

## Completed Work

### P01-T01: Source cause and resident UI

Core Advisor now includes a generated-question method. Host routes in-scope
typed case/document/form/home/repair questions to it, retaining legacy explicit
topics and protected human/rules routes. AzureAdvisor requests bounded
answer/source-ID JSON and shares precommitted accounting/HTTP validation with
legacy inference. Sources are host-owned, raw text renders as text. Default-off,
expiry, rate/cost bounds, no-retry and reauthorization remain.
Resident consent now explicitly covers question plus limited own-case model use.
Existing small metadata renders AI-generated and visible unapproved/incorrect/
human-help detail; native source details remain collapsed.
API guide records causes, four owner settings and unchanged expiry/deployment
gates. Eight new unit methods and one new browser check cover these boundaries.

## Implementation-Time Plan and Detail Updates

### Directly related fixture and browser expectation update

The original API fake row uses the unmapped stage "Survey", so its truthful
projection is an unknown update. The new grounding test initially expected a
survey text and failed; it now explicitly sets canonical "Survey being booked"
before checking the grounded prompt. No production fallback or mapping changed.
The existing shared-widget browser rat-refusal assertion was updated to the
intentional disabled-AI repair fallback. This preserves current feature intent;
no user decision or repeat critique was needed. Plan/details markers reconciled.

## Initial Validation Record (Historical)

Initial resident discovery: 146 run, one new fixture-expectation failure,
seven existing opt-in skips. Initial focused mypy passed. Ruff check passed;
format check requested formatting, applied with the existing formatter.
Original logs remain external. These initial failures are superseded by the
final local validation below, not erased.
External task-owned runtime installed after
the existing runtime lacked source distributions. No shared runtime modified.

## Blockers and Remaining Work

No local implementation blocker. Actual-model/live acceptance and human approval
remain separate; no deployment or push. P03 was subsequently executed below;
RV-001 acceptance and advanced-main publication blockers remain open.

## Final Local Validation: P02-T01

External evidence root:
/home/azureuser/.copilot/session-state/0187b0f6-c98e-4159-80bc-4c269348ac7c/files/

| Check | Result | Exact scope/evidence |
| --- | --- | --- |
| Resident API discovery | Passed | 147 run, 140 passed, seven existing opt-in SQL skips; resident-units-verified.log |
| API Ruff | Passed | ruff check . and ruff format --check . from src/api; 59 formatted files |
| API mypy | Passed | Complete configured API scope, 113 source files |
| Core advisor | Passed | Six tests; targeted Ruff, format and mypy |
| JavaScript | Passed | node --check resident_demo/web/assistant.js |
| Generated-answer browser | Passed | generated-browser-complete/results.json and seven PNGs |
| Shared-widget browser/axe | Passed | shared-widget-browser/results.json and sibling .log; exact pinned axe 4.10.3 hash |
| Resident assistant/callback browser/axe | Passed | resident-assistant-browser/report.json and sibling .log |
| Diff whitespace | Passed | git diff --check |
| Actual model, authenticated live, human/AT | Not run | Outside local scope; no claim of model quality, whole issue or WCAG acceptance |

Final generated-answer browser: Chromium 156.0.8078.4 / Playwright 1.64.0;
real ephemeral loopback app, constructed sign-in and scripted Azure transport,
no cloud call. Consent prevented HTTP/reservation before permission; question/
own-case grounding reached transport with other-case and identity exclusion.
Output rendered as text, not executable markup. Sources started collapsed and
opened/closed by Enter. Label geometry: 12.8px regular type, 17.90625px high,
zero padding/border, body 16px. Panel widths at 1280/390/320 were 448/358/288px
at 100% text, within viewport at 200% text too. Reduced motion token 0s.
Unavailable and disabled states retained honest inability, no-report disclaimer
and housing-officer route; withdrawal cleared the thread. No page errors or
external requests. Desktop/narrow screenshots were visually inspected.

Original browser attempt timed out because the fixture did not re-enter its
question after the intentional consent-change draft clear. The corrected test
fills the question after permission; no application change/bypass was used.
A later eighth cross-surface unit initially supplied "contact" for the fake
unknown-stage record; changing its scripted legacy response to "unknown"
matched existing validation. Initial failure logs remain external. Final suite
passes all applicable tests. A transient import-name lint collision during
host-owned notice addition was fixed with an explicit alias before validation.

## Pre-Review Reconciliation

Plan and details mark P01/P02 complete. Eight unit methods, one new browser
check, one related existing browser expectation; no removals. Host-owned repair
inability/no-report notice now survives generated output and is visible in UI.
P03 original Review and local persistence remain, not misreported complete.
No material plan divergence or repeated critique. Review ready. Exact generated
source validation is structural, not a proof of semantic correctness.

## Original Independent Review: P03-T01

Review executed once, Complete / Not accepted.
Original: .copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-review.md.
RV-001 Medium: broad repair words admit unrelated requests (a poem about a rat,
car repair, a broken robot joke) and report/contact-action requests. They can
consume model budget and transmit consented own-case grounding instead of the
planned deterministic refusal. The desired dead-rat home question does reach
generation, but full host-admission behavior is not accepted. No external
action/model execution is claimed for the review reproduction.
RV-001 is routed to a later rpi-implement work item; no post-Review source edit,
repeat Review or closure claim in this task.
RV-002/003 Low preserve separate owner deployment/actual-model/live evidence
and human/content/AT acceptance follow-ups. Original critique Pass and original
adverse Review are both preserved. Parent corrected the research header and
PNG count only; no source or validation evidence was rewritten after Review.

## Local Persistence and Full-Gate Boundary

Local-only persistence is authorized with Refs #563 and Copilot trailer.
Authenticated GitHub ID/login yields 8036360+jmservera@users.noreply.github.com
for author and committer, configured repository-locally. No push, PR/issue edit,
deployment, authority extension or merge is performed.

Read-only fetch before persistence found origin/main
f7482602ee8dd8e7eb36dc05426732a56aa982f7, while the reviewed source base is
7c13115631a163061038d69754a8feb2732daca6. No rebase/merge is authorized or
performed. Full-gate execution follows the local implementation/evidence commit,
in an external clean exact-commit worktree so task-generated editable-install/
Python/Ruff caches do not masquerade as clean inputs or require unsafe cleanup.
No existing tracking/generated history is deleted or moved. The external gate
receipt/log will remain external; a blocked gate is not publication evidence.

Implementation and dated original evidence committed locally as
f3be331041c25f86fde3bb64d6b35046146007e3, with privacy-safe author/committer,
Refs #563 and the requested Copilot trailer. Main worktree tracked/untracked
status was clean after commit; ignored install/Python/Ruff caches remain
unmodified rather than claiming authority to delete unknown historical inputs.

Full gate command in the clean exact-commit external gate-candidate worktree:
`PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base
f7482602ee8dd8e7eb36dc05426732a56aa982f7 --lock-timeout 0 --out
/home/azureuser/.copilot/session-state/0187b0f6-c98e-4159-80bc-4c269348ac7c/files/full-gate-original`.
It returned exit 1: "BLOCKED: Candidate does not descend from the reviewed
main base". Exact log: external files/full-gate-original.log. No SQL/image/
scanner/full-suite run or passing receipt followed this guard. No ancestry
rewrite, merge, skip flag, cloud fallback or shared-lock interference occurred.

This final closeout commit changes only lifecycle evidence and invalidates any
earlier exact-head gate claim; none was passing. A final same-command external
clean exact-head attempt uses files/gate-final-candidate and
files/full-gate-final with sibling .log, after a fresh read-only main fetch.
Its external result is authoritative; no success or receipt is preclaimed.

## Return-to-Caller State

Full local RPI loop executed; implementation persisted, original independent
Review Complete / Not accepted. All P01-P03 execution markers checked, not
acceptance checkboxes. Automatic session remains running at Follow-up, with
no child started. Ranked work: RV-001 bounded admission/refusal fix; owner
activation/actual-model/live evidence (RV-002); human/content/AT (RV-003).
No issue criteria ticked, no closing keyword, push or Azure change.
