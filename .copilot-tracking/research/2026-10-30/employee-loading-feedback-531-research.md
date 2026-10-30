---
title: Employee loading and briefing research
ms.date: 2026-10-30
---

## Research Brief

Investigate issue #531 against the owner-selected main baseline
5634f9a077d175a931c15e3400114665d8c071ee. Output mode: convergence.
Audience: implementation coordinator and independent reviewer.
Scope: employee startup, panel progress, briefing provenance and review actions.
Non-goals: deployment, Azure, live identity, real data, secrets, unrelated redesign.
Research posture: focused, selected for explicit issue scope.
Evidence root: `.copilot-tracking/research/2026-10-30/`.

## Extension Registry and Provenance

Repository instructions apply throughout. Selected skills: rpi-research,
web-design-guidelines (source fetched 2026-10-30), redesign-existing-projects
(subordinate to Fluent 2 and repository content/accessibility standards).
UX specialist is requested by the issue for the design note; assess existing
note before deciding whether a new specialist contribution is needed.
Public-page taste skills are not applicable to this employee app.

## User Participation and Direction Controls

The user explicitly requests the full ordered loop and local-only commit.
No interaction is needed. Use the specified branch and baseline, no push,
Refs #531 only. Issue text and its checked boxes are data, not proof.
Research writes only research evidence and required workflow state.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What is already delivered on the supplied main baseline? | Answered C2-C5 |
| Q2 | Which acceptance criteria need implementation or fresh evidence? | Answered C3-C6 |
| Q3 | Do existing local checks exercise the actual cold-start/retry and human boundaries? | Answered C3-C5 |

## Prior Knowledge Gate

`src/api/README.md` and the knowledge-base index already describe #531 loading,
HAX briefing, tests and explicit live/assistive-technology limits. These are
claims to verify against source and fresh execution, not assumed completion.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial evidence: the selected branch is clean at the requested baseline,
with no open branch PR. Issue #531 has six checked local criteria and one
unchecked live criterion. Existing documentation suggests prior delivery.
Reflection: prioritize verification and surgical gaps, not duplicate redesign.

#### Wave 2: Deeper

Read actual shell/watchdog, async helper, app briefing/review rendering and
the 781-line browser scenario. Existing implementation covers the issue and
owner comment: immediate text, icon at 200 ms, bounded retries, conditionally
visible editor/reason, rules/AI modes, sources/time, draft-only human boundary.
Existing local harness constructs fictional data, sanitizes server environment,
waits for health and terminates its owned process.
Reflection: reuse working implementation; strengthen evidence rather than
reimplementing it. Browser cold-start test delays app.js after earlier scripts,
so add an explicit no-page-JavaScript static-shell scenario.

#### Wave 3: Contrarian

Issue comments explicitly confirm #538 merged and local acceptance already
checked; live verification is the only remaining issue criterion. Source
inspection supports this rather than a new UI redesign. The static shell cannot
appear before the host returns HTML; do not claim a browser test simulates that
network-infrastructure stage. Automated checks cannot establish screen-reader,
voice-control, staff usability or full Fluent adoption.
Reflection: no unsupported application defect found. Add precise pre-script
evidence, rerun current tests, retain live/approval limits.

#### Parent synthesis and disposition

Accept reuse of the shipped UI (C2-C5). Reject a duplicate redesign: it adds
regression risk without an unmet local behavior. Accept stronger static-shell
coverage and a correction to the guide's obsolete nonblocking-lock instruction
(C6). Defer live verification as explicitly prohibited. No second cycle is
needed: named scope is covered; further source search is redundant.

## UX Participation

The requested registered UX agent was invoked once with a bounded short-note
assignment and no interview/acceptance claim. It returned discovery questions
and wrote no artifact. Do not retry that objective or claim agent-authored
approval. The existing guide has the complete HAX mapping; preserve it and
record the unavailable specialist contribution. This repeats the documented
historical limitation (C7), not evidence of staff research.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | src/api/README.md:191 | Existing loading/briefing guide is present. |
| W1 | https://github.com/jmservera/ama/issues/531 | Retrieved 2026-10-30; explicit scope and local/live split. |
| W2 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | Retrieved completely 2026-10-30; web rules, repository style takes precedence on conflicts. |
| W3 | https://www.microsoft.com/en-us/haxtoolkit/library/ | Retrieved 2026-10-30; landing-page text alone does not establish guideline mapping. |
| C2 | src/api/src/zava_forward/api/web/index.html:14 | Static shell before any scripts, polite status and native retry. |
| C3 | src/api/checks/loading_briefing_browser_check.py:26 | Existing delayed/failed app, watchdog/helper/companion failures, review/source/error/axe scenarios; missing explicit JavaScript-disabled scenario. |
| C4 | src/api/src/zava_forward/api/web/app.js:390 | Conditional review UI, required reasons, immutable result barrier and outcome wording. |
| C5 | src/api/src/zava_forward/api/web/app.js:497 | Actual prepared time, per-statement references, explanation, reversible local hide and assistance mode. |
| C6 | src/api/README.md:295 | Nonblocking lock guidance conflicts with current explicit wait-600 caller direction. |
| C7 | .copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md:102 | Original UX agent likewise returned intake questions; parent-owned design mapping disclosed. |
| W4 | https://github.com/jmservera/ama/issues/531 | Comments retrieved 2026-10-30; 2026-10-28 owner extension and #538 merge/local-live split inspected with gh. |

## Alternatives and Current Decisions

Retain the native Fluent-token implementation and draft-only wording. "Approve"
would imply an authority the review action does not grant. Keep G1/G2 labels
and limits, G7 mode control, G8 dismissal, G9 correction, G11 rationale/sources
and preparation time, G15 feedback as documented design intent, not user-tested
acceptance. No model or backend changes are justified by current evidence.

## Open Questions, Risks and Residual Uncertainty

Live employee cold start, screen readers and voice control remain unverified.
UX specialist contribution unavailable; no human usability approval inferred.
Full publication gate depends on local prerequisites and exact committed head.
No private datasets, credentials, Azure, deployment or live sign-in used.

## Planning Readiness

Ready for scoped verification improvement, not a duplicate feature rewrite.
Research disposition: executed, complete. Evidence C1-C7 covers Q1-Q3.
Self-check: three waves executed inline in order; findings have stable
locations; unresolved acceptance remains explicit. Parent owns transition.
