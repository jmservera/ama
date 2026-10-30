<!-- markdownlint-disable-file -->

# Task Research: authenticated-live-acceptance

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/authenticated-live-acceptance-research.md |

## Research Brief

* What: authenticated live acceptance for issues #550, #551 and #552.
* Purpose / audience: owner acceptance evidence, not issue closure or operational approval.
* Scope: the two owner-supplied Azure Container Apps sites, issue criteria,
  documented authentication/roster controls, and relevant browser contracts.
* Non-goals: source fixes, private-data edits, role changes, Azure deletion,
  push, deployment, blanket accessibility certification or issue closure.
* Criteria: each of the 19 issue criteria classified proven or unmet with
  actual evidence and explicit partial/blocked limitations.
* Output: dated research, plan, critique, execution, Review and session state;
  one local commit with Refs only.
* Output mode: audit, explicitly preparing acceptance execution planning.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | How can the supplied identity safely reach both sites; what must be observed; what could invalidate acceptance? |
| Codebase scope | src/api, infra guides, UX baselines, relevant existing tracking evidence |
| External scope | Supplied two sites; GitHub issues #550-552; Microsoft sign-in provider |
| Initial internal candidates | src/api/README.md, infra/README.md, browser tests, UX baseline |
| Initial external candidates | Issue bodies and supplied deployed sites |
| Posture / provenance | Focused; bounded caller task |
| Limits | No private dataset edits, role changes, Azure deletion, push, or secret disclosure |
| Edits during research | Evidence and required workflow state only |
| Evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Scoped authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions, all paths | Branch, privacy, evidence, local gate | Selected |
| Skill | rpi-research | Three-wave evidence protocol | Selected |
| Skill | rpi-plan / rpi-implement / rpi-review | Later phase protocols | Deferred to respective phase |
| Skill | web-design-guidelines | Scoped web review source | Selected for Review; no web edits planned |
| Specialist | Independent critique and Review agents | Bounded independent assessment | Later gates; no research delegation needed |

## User Participation and Research Decisions

User explicitly requests the full loop, two exact sites, identity and secret
handling, and local commit without push. Execute that finite loop autonomously;
do not infer authorization for follow-up implementation or system changes.
No interaction is needed for routine phase advancement.

## Scope and Success Criteria

Preserve all 19 criteria, including compound obligations; a partial result is
unmet overall. Authentication success does not prove roster authorization.
No login snapshots, traces, HAR, console dumps or secret-bearing screenshots.
Only read the password inside browser automation, with no return/logging.

## Task Research Requests and Direction Controls

* Use actual authenticated Playwright, not source tests as a live proxy.
* Use only documented existing roster controls; otherwise report missing binding.
* No private dataset inspection or mutation to create access.
* Do not modify issues or remote branches.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What are the exact criteria? | Straightforward | Answered: W1-W3 |
| Q2 | What authentication and roster access is supported? | Depth | Open |
| Q3 | What browser observations and counterchecks avoid overclaiming? | Depth | Open |

## Prior Knowledge Gate

Read original case study, addendum, knowledge-base index and owner memory.
Memory is context, not evidence. Working branch is clean,
chore/auth-acceptance-1030, with no associated PR; current source ffd8f35e.
No prior live acceptance is assumed valid.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Issue bodies retrieved with gh on 2026-10-30. Nine chat criteria, four map
criteria and six case criteria define 19 overall decisions. Reflection:
shared component provenance and automated coverage require source evidence
alongside live behavior; browser appearance alone cannot establish them.

#### Wave 2: Deeper

Read C1-C6. Existing /tmp/mv Python has Playwright; system Python does not.
The MCP code sandbox cannot import local filesystem modules, so use the
existing local Python browser environment rather than place the password in
tool parameters. Reflection: the resident showcase has its own password
verifier; the supplied employee Entra identity may not be a resident account.
Do not substitute a different identity or invent enrolment.

#### Wave 3: Contrarian

C1 distinguishes an unbound manager's programme access from personal
assignments. C2 requires tenant/OID binding, not email matching. C3's roster
initializer applies SQL bindings and restarts; it is not an ordinary read-only
roster UI and conflicts with the caller's no-private-data-edits boundary.
Do not use it to create access. C4-C6 are local synthetic checks, not deployed
proof. Fresh web guidelines were retrieved successfully; they do not override
the repository's owner-selected Fluent system or ASCII documentation style.
Reflection: mark denied access and unmeasured compound obligations unmet,
not inferred passed from source tests. No additional research cycle is needed:
remaining uncertainties are the intended live execution questions.

#### Parent Synthesis and Disposition

Accept actual UI sign-in and safe same-origin account-status checks.
Reject private roster reads/writes, synthetic auth and source-only live claims.
Defer unavailable direct screen-reader, cross-browser and user acceptance.
The focused research questions are covered sufficiently to plan execution.

## Evidence Log

| ID | Source | Retrieval | Finding |
| --- | --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/550 | 2026-10-30 | Nine shared-chat criteria |
| W2 | https://github.com/jmservera/ama/issues/551 | 2026-10-30 | Four expanded-map criteria |
| W3 | https://github.com/jmservera/ama/issues/552 | 2026-10-30 | Six single-case criteria |
| C1 | src/api/README.md:3497-3508 | 2026-10-30 | Roster-bound code and own/all access distinction |
| C2 | infra/README.md:724-746 | 2026-10-30 | Tenant/OID binding and sanitized evidence requirements |
| C3 | infra/README.md:2777-2784 | 2026-10-30 | Initializer --apply --restart mutates private bindings; excluded |
| C4 | src/api/README.md:9-48 | 2026-10-30 | Case icon, disclosure and scroll contracts |
| C5 | src/api/README.md:51-110 | 2026-10-30 | Shared chat, consent, loading and unsupported answer contracts |
| C6 | src/api/README.md:485-524 | 2026-10-30 | Expanded filters, keyboard and list contract |
| C7 | src/api/README.md:769-785 | 2026-10-30 | Separate resident showcase authentication and record-use consent |
| C8 | docs/reference/research/ux/wcag-conformance-baseline.md:18-30 | 2026-10-30 | 320/390/1280 widths; direct accessibility remains separate |
| W4 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-30 | Fresh UI review rules successfully retrieved |

## Alternatives and Decision State

Use the provided identity through the deployed sign-in UI. Reject synthetic
sessions, bearer-token shortcuts and roster edits as substitutes for live
authenticated acceptance.

## Open Questions, Risks and Residual Uncertainty

Roster binding, deployed revision parity, resident enrolment and full accessible
interaction remain unknown. Chat may invoke a paid model; only the bounded
owner-requested acceptance questions are within scope.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for bounded acceptance
execution, not a prediction that access or any product criterion will pass.
Q2/Q3 answered by C1-C8. Self-check: three ordered inline waves, all material
findings traceable, no research delegation or product changes, no secrets read.
