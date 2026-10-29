<!-- markdownlint-disable-file -->
---
title: Resident content and journey research
description: Focused evidence for issues 153 and 154
ms.date: 2026-10-27
---

## Research brief

Task identity: issues-153-154 / resident-content-153-154. Audit the existing
workbench content and design resident/representative journeys for synthetic,
staff-assisted demonstration. Output mode: audit, explicitly preparing planning.
No live contact, new portal, authority changes, translation claims or human
acceptance. Read issue bodies and comments first; inspect linked requirements,
current web assets and regression tests next.

## Research parameters and direction controls

Focused posture, selected for the owner's bounded documentation and smallest
safe copy-fix request. Existing branch `docs/resident-ux-153` is clean and has
no existing PR. One PR to main covers both sibling issues; do not broaden to
parent #149. Local tests only. No full gate, Azure, secrets, private data or uv.
At most one scoped changed gate, only if justified by size.

## Extension registry and participation

Repository instructions and RPI phase contracts selected. Web design guidelines
selected; fetch upstream before any web edit and refresh for review.
Accessibility skill selected for design boundaries, not certification.
Public-page redesign and visual restyling skills skipped: no redesign requested.
Research inline because requirements, UI and evidence are tightly coupled.
User explicitly requested the complete ordered loop; no routine phase prompt.
Human wording, usability and assistive-technology approval remain owner steps.

## Initial questions and candidate areas

* Q1: What content is actually exposed by the current core flow, including errors?
* Q2: Which resident/representative design requirements and boundaries apply?
* Q3: Which small copy fixes are safe without changing decisions or stored values?
* Q4: Which criteria must remain open for human review or broader implementation?

Internal candidates: linked BRD/PRD/ADR sections, UX standards and journey atlas,
`src/api/src/zava_forward/api/web`, API/core message paths and tests.
External candidate: the web-design-guidelines upstream command source only.

## Research cycle log

Cycle 1 opening: prior knowledge is partial. Existing standard explicitly
disclaims universal content coverage. Issue #153's owner comment appoints
Juan Manuel Servera, contradicting the standard's "no reviewer appointed".
Appointment is not evidence that any wording was reviewed.
Wider, Deeper and Contrarian waves will be recorded in that order.

## Findings, evidence and readiness

### Wave 1: Wider

Read both issue bodies, comments and prerequisites #150/#86/#87/#88/#91;
read #149/#155/#156 for the surrounding acceptance boundary. Reviewed the
knowledge-base index, memory, original/addendum, resident maps, atlas,
content/design/WCAG standards and ADR 0006. Reflection: records and staff
screens exist; resident-facing design is not equivalent to staff role screens.
The prospective optional portal changes the older staff-only framing, but does
not authorize a new portal in this task.

### Wave 2: Deeper

Read the current case/list/draft/AI, finance/technical/resident, appointment/
quality, chat/alert, account/time and reference-viewer content paths and current
copy regression. Read linked requirement rows and negative acceptance cases.
Reflection: universal reason/owner/action and vocabulary removal cannot be
claimed from seven lexical files. Dynamic server messages and stored finance
values remain visible; extension must distinguish source copy from evidence.
Representative review date is an exclusive boundary in core, so plain wording
must preserve "from this date", not imply continued access on that date.

### Wave 3: Contrarian

Challenged a universal "audit passed" conclusion against `api()` raw error
forwarding, the stored finance option, server ranking error, alert unknown
owners, and independent appointment authority. Challenged "no named reviewer"
against the owner's actual comment, and "no resident service" as a perpetual
scope rule against the dated optional-portal amendment. Reflection: preserve
quotes/data and authority logic; disclose residuals instead of sanitizing
everything or inventing owners. A scoped design contract with text wireframes
is feasible without pretending to deliver real resident views.

## Evidence log

| ID | Source | Evidence |
| --- | --- | --- |
| C1 | `docs/reference/research/ux/content-standard.md:25` | Six internal vocabulary families, reason/owner/action and exact AI label |
| C2 | `src/api/tests/test_content_standard.py:13` | Seven-file lexical guard, narrow exceptions, no visibility parser |
| C3 | `src/api/src/zava_forward/api/web/app.js:28` | Shared raw server errors and generic fallback, no universal owner/action |
| C4 | `src/api/src/zava_forward/api/web/panels.js:185` | Supplied per-measure choice and representative source/task/date controls |
| C5 | `src/core/src/zava_forward/core/resident_decisions.py:501` | Authority valid strictly before review date, current safe route required |
| C6 | `src/api/src/zava_forward/api/web/ops.js:375` | Offer separate from agreement, works consent separate, no sending |
| C7 | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1420` | FR-045/046/048/049 version-bound decisions, pause, booking, closure |
| C8 | `docs/brds/agentic-retrofit-programme-brd.md:1` | FR-045/046, NFR-008/009, RULE-022, OD-41/42 remain governing design inputs; requirement IDs are stable locators |
| C9 | `docs/reference/research/ux/customer-journeys/customer-journey-atlas.md:222` | Five themes and their choice/privacy/quality trade-offs |
| C10 | `docs/reference/research/ux/customer-journeys/residents.md:46` | Resident and representative hypotheses, not direct research |
| C11 | `docs/adrs/0006-src-layout-and-cutover.md:63` | API assets in src; tests outside package |
| C12 | `docs/reference/research/ux/wcag-conformance-baseline.md:18` | Proposed AA scope and Not run human checks, not certification |
| C13 | `src/api/src/zava_forward/api/web/assistants.js:40` | AI disclaimer exists but proposal acceptance wording can be clearer |
| W1 | https://github.com/jmservera/ama/issues/153 (retrieved 2026-10-27) | Owner comment 2026-10-15 appoints Juan Manuel Servera, not completed review |
| W2 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-27) | Full upstream rules fetched before web edit; native labels, focus, errors, reduced motion |
| W3 | https://github.com/jmservera/ama/issues/154 (retrieved 2026-10-27) | Five design/validation criteria; no live contact |
| W4 | https://github.com/jmservera/ama/issues/155 (retrieved 2026-10-27) | Usability programme lacks actual participants/results |

## Findings mapped to questions

Q1 answered by C1-C4/C6/C13: document an explicit audit inventory with residual
messages, not a universal pass. Q2 answered by C5-C12/W3: design six assisted
journeys plus shared task-scoped representative and safe-contact rules.
Q3 answered by C4/C5/C13: change only resident draft heading/disclaimer,
representative review-date label, assistant technical label/review disclaimer,
and ordinary "hold the same role" wording. Add focused regression evidence;
do not migrate data or change behavior. Q4 answered by W1/W4/C12: appointed
reviewer, actual wording review, representative user/AT checks and live-service
privacy/service decisions are distinct; actual review remains Not run.

## Alternatives and decision state

Accept bounded audited docs and literal copy corrections for planning.
Reject broad error rewriting, stored-value migrations and framework/portal
changes as disproportionate and potentially authority-changing.
Defer universal core-flow/error and resident usability acceptance with explicit
owner actions. No operational legal determination or new regulatory claim.
All research inline; no delegated researcher is implied.

## Planning readiness and self-check

Research disposition: executed. Planning Readiness: Ready for bounded changes,
not for live use or issue closure. Three waves complete; no new cycle needed:
remaining gaps need human evidence or broader implementation, not more desk
research. Evidence IDs, dated external sources, alternative dispositions and
next-phase boundaries are recorded. RPI parent advances to Plan under the
explicit full-loop request.
