<!-- markdownlint-disable-file -->
# Task Research: resident-live-acceptance

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher | RPI parent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md |

## Research Brief

Investigate safe authenticated live acceptance of the resident showcase for
Refs #550, #551 and #552. Audience: owner and independent evidence reviewer.
Output mode: audit, explicitly preparing a bounded execution plan.
Scope: exact issue criteria, earlier adverse evidence, documented sign-in
contract and scoped accessibility basics. Non-goals: product changes, employee
authentication, Azure changes, enrolment repair, secret inspection and closure.

## Research Parameters

Focused posture, selected by the parent for the named sources and bounded task.
Evidence root: .copilot-tracking/. Research is read-only except its artifact
and workflow state. External scope: the three GitHub issues, resident site and
current Web Interface Guidelines. Credentials remain unread during Research.
Explicit limit: at most two actual browser-form login attempts; stop at 401.

## Extension Registry and Provenance

| Kind | Selection | Authority and rationale |
| --- | --- | --- |
| Instruction | Repository AMA and RPI tracking conventions | Dated evidence, baseline context, local commit, preserved adverse outcomes |
| Skill | rpi-research | Three ordered inline waves and planning readiness |
| Skill | web-design-guidelines | Fresh source retrieved 2026-10-30; scoped review only |
| Skill | accessibility | WCAG/ARIA references and limitations, not conformance certification |
| Specialist | No research delegation | One coupled bounded trace; direct source reading is sufficient |

## User Participation and Research Decisions

The explicit full-loop request supplies scope, target, limits and local-only
publication direction. No intake question is necessary or possible in this
noninteractive run. Automatic execution is directly requested, not inferred
from an existing manual session.

## Scope and Success Criteria

Retain all 19 compound criteria in the final matrix, distinguishing resident
observations, employee-only obligations and inaccessible map/case surfaces.
Proven requires actual applicable evidence; source or public shell evidence
does not prove authenticated behavior. Unknowns remain unmet, not defects.

## Direction Controls

* Resident URL only: https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io.
* Read the supplied credential file only inside automation, trim lines,
  never emit identity/password, mask fields, disable all recording.
* Use actual POST /demo/login form with its CSRF. No API auth shortcut.
* On 401 record only sanitized non-secret page text and HTTP status, review
  documented rules, and stop live work. No retry-based diagnosis.
* Local Refs-only commit; no push, issue edits, closing language or Azure calls.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What do the issues actually require on the resident site? | Straightforward | Answered by W1-W3 |
| Q2 | What sign-in contract and failure limit constrain the attempt? | Depth | Answered by C4-C5 |
| Q3 | What did earlier acceptance actually prove? | Straightforward | Answered by C1 |
| Q4 | What separates browser basics from full accessibility acceptance? | Depth | Answered by C6-C7 |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory for context.
Read the explicitly supplied sibling-worktree Review. Its 401 is historical,
not proof that today's supplied identity must fail. Its public-shell observations
are not authenticated feature proof and will not be promoted.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Retrieved all three issue bodies with gh. #550 has nine compound criteria;
#551 has four expanded employee-map criteria; #552 has six single-case
criteria. Reviewed the earlier 19-row matrix and public-only limitations.
Reflection: test resident chat only after access and consent; preserve map/case
criteria as unmet/not applicable to resident rather than silently dropping them.

#### Wave 2: Deeper

README lines 4268-4281 require CSRF cookie/header, same-origin JSON form
submission, five source failures and sixty total per ten minutes. Wrong
password, unknown email and a non-example domain share HTTP 401. Thus a 401
does not identify the cause and must not trigger secret repair. The existing
/tmp/mv Python has Playwright 1.64.0; system Python does not. Reuse that runtime,
with a new nonpersistent browser context and all recording disabled.
Reflection: one attempt is sufficient to obey the owner's immediate 401 stop;
the two-attempt maximum is not a request to retry a rejection.

#### Wave 3: Contrarian

Current README and assistant source say residents have only one assistant,
not employee skill selection. Free-text unsupported questions should abstain
with a human contact route; actual AI generation is not needed to answer the
rat question honestly. Source intent is not deployed evidence. Map/case
criteria cannot be inferred from resident home cards, nor can a public popup
prove authenticated thread behavior. WCAG baseline explicitly retains human
AT and user-research gaps; basic native semantics are not AA conformance.
Reflection: reject source-only substitution and fabricated AI output. Accept
only directly observed subparts; retain whole compound criteria unmet when
any applicable required subpart is unproven.

Parent synthesis: accept C1-C7/W1-W4 as the execution contract, defer actual
live proof to Implement, reject access repair and scope expansion. Focused
scope is covered; further source research cannot establish the live result.
Research disposition: executed. No second cycle is required for planning.

## Evidence Log

| ID | Source | Evidence |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/550, retrieved 2026-10-30 | Nine compound chat criteria, two-site shared use and resident consent/relevance |
| W2 | https://github.com/jmservera/ama/issues/551, retrieved 2026-10-30 | Four expanded map/filter criteria |
| W3 | https://github.com/jmservera/ama/issues/552, retrieved 2026-10-30 | Six case-layout/accessibility/browser criteria |
| W4 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-30 | Current keyboard, focus, forms, live updates, reflow and reduced-motion review rules |
| C1 | ../auth-accept-1030/.copilot-tracking/reviews/logs/2026-10-30/authenticated-live-acceptance-review.md:97 | Earlier resident 401, unknown cause; 18 unmet and one source-only test-coverage proof |
| C2 | src/api/README.md:51 | Shared chat contract, resident-only assistant, consent, honest unsupported fallback |
| C3 | src/api/README.md:770 | Resident chat and explicit record-use consent contract |
| C4 | src/api/README.md:4268 | CSRF/Origin contract; limiter and intentionally indistinguishable 401 |
| C5 | src/api/src/zava_forward/api/resident_demo/web/index.html:36 | Real form and labelled email/password fields |
| C6 | docs/reference/research/ux/wcag-conformance-baseline.md:23 | 320/390/1280 widths, keyboard/AT/zoom boundaries |
| C7 | docs/reference/research/ux/design-system.md:17 | Owner-selected Fluent 2; partial native adoption is not complete adoption |

## Alternatives and Decision State

Selected: bounded real form acceptance. Rejected: direct auth requests,
source-only acceptance, employee expansion and credential/Azure repair.
They cannot supply the requested authorized resident evidence.

## Open Questions, Risks, and Residual Uncertainty

Current deployment parity and supplied-account eligibility are unknown.
Do not diagnose the earlier generic 401 or infer sign-in from public chat.

## Planning Readiness

Ready for bounded acceptance execution, not authenticated-feature acceptance.
All three waves complete; claims have evidence IDs and source locations.
Missing deployed parity/account eligibility remains a live-result uncertainty,
not a reason to block the permitted form attempt. Artifact self-check passed.
