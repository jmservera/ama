<!-- markdownlint-disable-file -->

# Task Research: employee-briefing-manager-visibility

| Field | Value |
| --- | --- |
| Date | 2026-10-28 |
| Researcher | rpi-research, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-28/employee-briefing-manager-visibility-research.md |

## Research Brief

Research existing manager roles, permitted case reads, assignment identity and
briefing/UI consumers. Audience: implementer and PR reviewers. Output mode:
convergence. Deliver programme-wide permitted open cases to manager briefings,
with explicit scope labels, without changing assignment or authorization.
JSON and SQL parity, unbound identity regression and actual browser label
evidence are acceptance criteria.

## Research Parameters

Focused posture, selected for the bounded caller request. Internal candidates:
src/core stores/workflows/identity, src/api server/web/tests/checks, PR #514
and its research. External candidates: named GitHub PR and current web
guidelines only. Evidence root: .copilot-tracking/. Research is read-only
except its artifacts and required workflow state.
No Azure, secrets/.env, private data, uv, new roles or authorization expansion.
The explicit /tmp/brief-common.md owner limit prohibits --all and permits at
most one --changed gate only for large changes; use focused local checks for
this bounded change. Do not claim a full receipt.

## Extension Registry and Provenance

| Kind | Candidate | Selection and authority |
| --- | --- | --- |
| Instructions | Repository guidance; /tmp/brief-common.md | Selected: src layout, local checks, owner-created branch, Refs PR |
| Skill | rpi-research | Selected: evidence-led three-wave research |
| Skill | web-design-guidelines | Selected: fetched current source before web edits |
| Skill | redesign-existing-projects | Skipped: no visual redesign |
| Specialist | RPI Researcher | Skipped: one tightly coupled trace, inline |

## User Participation and Research Decisions

User explicitly requests all four phases and publication, so no additional
phase or plan confirmation is needed. This is a finite manual full-loop
request, not consent to an ongoing automatic follow-up session.

Owner decision (2026-10-28), verbatim: "Show all programme cases to manager roles
on the briefing".

## Scope and Success Criteria

Preserve personal assignments, home scope, consent and approval checks.
Programme scope must be the existing permitted set, excluding closed cases.
Use existing MANAGER_ROLES, no new roles. Non-manager and unbound identities
retain zero assignments when unassigned. Verify response, AI input and browser
copy rather than just a label.

## Direction Controls

* Add: manager programme-wide briefing, explicitly labelled All programme cases.
* Exclude: new role/assignment/authorization rules, deployment and live data.
* Preserve: personal My cases assignment semantics unless evidence shows a
  caller-required separate programme view is needed.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is the existing manager role set and permitted-case boundary? | depth | Answered C2-C4 |
| Q2 | Which consumers select and describe the briefing's cases? | depth | Answered C5-C7 |
| Q3 | How can JSON/SQL and browser tests prove scope without live data? | depth | Answered C8-C9 |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, API/source README and PR
#514 research. Branch fix/employee-briefing-manager-visibility is clean,
owner-created at origin/main 98b0bb98f2424dd23c00e386378f44892a7a79e0.
PR #514 is merged. Its assignment-only finding is historical verified
context, not authority to retain manager briefing wording.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

PR #514 and source searches identify Store.briefing, Store.list_cases,
SqlStore page/count overrides, app.js aiBox and existing MANAGER_ROLES.
Reflection: briefing and My cases are independent consumers; inspect permitted
reads and identity binding before selecting a shared briefing selector.

#### Wave 2: Deeper

MANAGER_ROLES contains exactly Retrofit Programme Manager and Programme Support
Officer (C2). The API checks projection.allowed before briefing (C3). Staff
already have permitted all-case reads; contractor case reads remain company
scoped, and contractor/unknown/admin-only briefing is denied (C4).
Store.list_cases delegates to the existing store-specific page_cases, so use
that existing boundary, not a new scan of raw cases. SQL inherits briefing.
Reflection: no new role or authorization rule is necessary. My cases and counts
remain assignment-only, including for unbound managers.

#### Wave 3: Contrarian

Challenged treating roster binding as a manager permission prerequisite:
identity.bind explicitly preserves authenticated role without a staff match
(C6; PRD AC-141/143). An unbound manager may read programme cases but must keep
zero assignments. Challenged using raw status_line in the expanded prompt:
Programme Support Officer cannot see adjustment reasons; projected list status
already replaces sensitive waiting text (C4-C5). Use the projected status.
Challenged code-only briefing caching: the same workload code can occur under
different current roles and email attribution, and permission/reason policy can
change. Bind cache entries to current actor, role, reason visibility and selected
permitted IDs, preserving existing release and continuity checks.
Reflection: label-only edits and removing owner_code globally are insufficient
and unsafe. Do not change prompt instructions/registry release versions or
priority recommendations, and do not infer consent from case visibility.

#### Parent Synthesis and Disposition

| Claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Manager briefings can use permitted all-case reads | C2-C5 | Accepted | Already authorized reads; no new roles |
| Unbound managers should be assigned programme cases | C6 | Rejected | Role grants view, never ownership |
| My cases should become programme-wide | C7; owner quote | Rejected | Quote scopes change to briefing; preserve assignments |
| Expanded prompt may use raw reason text | C4-C5 | Rejected | Reuse projected status for role-safe facts |
| Existing cache key is sufficient | C5-C6 | Rejected | Actor, permission and scope changes require separation |

#### Cycle Re-entry Evaluation

No further cycle required: focused code trace answers all material questions.
Live deployment, SQL Server and real-user/accessibility acceptance are outside
the local evidence boundary and must not be inferred.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Prior assignment-only findings and live-data limits | .copilot-tracking/research/2026-10-27/employee-case-workspace-research.md:109 |
| C2 | Existing two manager roles | src/core/src/zava_forward/core/workflows.py:13 |
| C3 | Existing endpoint default-deny role check before briefing | src/api/src/zava_forward/api/server.py:270,469 |
| C4 | Staff/contractor/unknown permissions and reason projection | src/core/src/zava_forward/core/projection.py:34-73; src/core/src/zava_forward/core/store.py:249-312 |
| C5 | Raw assignment scan, top-eight cap, code-only cache and prompt | src/core/src/zava_forward/core/store.py:726-754 |
| C6 | Role and binding are independent; binding never grants role | src/core/src/zava_forward/core/identity.py:169-223; docs/prds/zava-forward-retrofit-programme-demonstrator.md:2216-2222 |
| C7 | Personal queue remains explicit assignment perspective | src/api/src/zava_forward/api/workbench.py:32-35; src/api/src/zava_forward/api/web/app.js:257-269 |
| C8 | Existing shared JSON/SQLite task fixtures and release checks | src/api/tests/test_ai_tasks.py:21-79,215-233; src/api/tests/test_assistant_release.py:562-621 |
| C9 | Synthetic real-server browser harness and safe isolated environment | src/api/checks/design_system_browser_check.py:225-288 |
| C10 | Requirements retain server field rights, assigned default and bounded proposals | docs/prds/zava-forward-retrofit-programme-demonstrator.md:457,484,489,549; docs/adrs/0006-src-layout-and-cutover.md:63 |
| W1 | PR #514 merged; no authorization expansion in its change | https://github.com/jmservera/ama/pull/514, retrieved 2026-10-28 |
| W2 | Current web rules fetched successfully | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-28 |

## Alternatives and Decision State

Selected: guard briefing with existing projection.allowed; select list_cases
with all for existing manager roles and mine otherwise; preserve deterministic
top-eight cap, source/release/continuity checks and role-projected waiting status.
Return explicit scope/label and candidate/summary counts; display these in the
briefing only, with neutral loading/refresh copy. Cache with actor, role, reason
visibility and selected case IDs. Rejected: changing all personal queues,
owner codes, roles, auth maps, raw programme scans or AI activation.

## Risks and Residual Uncertainty

No claim of live Entra mapping, production SQL Server or real model verification.
Browser engineering checks are not WCAG/user acceptance. Full --all gate is
explicitly prohibited by the owner brief. Referenced epics #73/#104 and #360
retain their outstanding criteria; no issue closure or checklist change.

## Planning Readiness

Ready. Research disposition: executed, complete. All three waves complete,
questions and selected approach mapped to C1-C10. No unresolved implementation
decision. Parent proceeds to Plan under explicit full-loop user direction.
