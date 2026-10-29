---
title: Resident chat 520 research
description: Focused evidence for the resident chat launcher and confirmed appointment finder
ms.date: 2026-10-28
---
<!-- markdownlint-disable-file -->

## Research Brief

Implement issue #520 for the synthetic resident demonstrator, building on
#469 and #164. Audience: implementer and independent reviewer. Output mode:
convergence, preparing planning. Scope: accessible launcher on all resident
pages, own-record grounding, dated regulatory citations, real agenda proposals
and explicit booking confirmation. No Azure deployment, paid inference, real
datasets, secrets, identity changes or claims of human/AT acceptance.

## Research Parameters and Direction Controls

Focused posture selected from the named source targets and bounded issue.
Evidence root: `.copilot-tracking/research/2026-10-28/`.
User explicitly requests the full ordered RPI loop, local validation, one push
where possible, and a PR with Refs #520 only. Heavy runs require nonblocking
`/tmp/ama-rpi-heavy.lock`. No interaction is available; scope is sufficient.

## Extension Registry and Provenance

* `.github/copilot-instructions.md`: selected, source/testing/publication rules.
* `rpi-research`: selected, three ordered inline waves and evidence synthesis.
* `web-design-guidelines`: selected, current source fetched 2026-10-28.
* Fluent 2, WCAG baseline and plain-language standard: mandatory app constraints.
* `design-taste-frontend`: excluded because this is an app screen.
* Research specialists: skipped; this is one tightly coupled code-path trace.
* Independent plan critique and Review: required in their later phases.

## Questions and Candidate Areas

1. What can be reused from resident_demo assistant and its Azure OpenAI route?
2. How are own-record access, agenda availability and consent enforced?
3. Which regulatory snapshots can be safely cited without legal conclusions?
4. Which unit/browser/accessibility and complete local gates are available?

Starting internal areas: `src/api/src/zava_forward/api/resident_demo/`,
`src/api/tests/`, `src/api/checks/`, `docs/reference/research/ux/`,
`docs/reference/regulatory/`, `tools/rpi-checks.py`.
External areas: current Web Interface Guidelines and official sources linked
from the selected local regulatory snapshots.

## Research Cycle Log

### Cycle 1: Wider

Intake verified: clean worktree on the requested topic, no matching open PR.
#469 is closed; #164 retains real-model, human-review and enablement gates.
#520 is open and explicitly leaves human/assistive-technology acceptance pending.

### Cycle 1: Deeper

The existing route has session/CSRF checks and reauthorization after inference.
Only fixed topics cross the model boundary; all rendered prose is host-owned.
The SQL showcase projection has no appointment/consent data and is deliberately
read-only. Existing core appointments record three-party works agreements, not
free-slot scheduling. Reusing them as a scheduler would incorrectly imply works
authority. A separate explicitly synthetic housing-officer callback agenda can
support this exercise without modifying SQL permissions or approving works.

Reflection: preserve the Azure advisor unchanged for its existing topics.
Add host-routed questions for home, consent unknowns, regulations and safety.
Use explicit record-use permission for new chat requests. Agenda proposals and
confirmation stay deterministic and independent of AI.

### Cycle 1: Contrarian

Challenged naive options: freeform model output could invent facts; arbitrary
case selectors could disclose another resident; generated slot suggestions
without a calendar could double-book; a launcher hidden with signed-in content
would fail the all-page criterion; booking works would bypass existing staff/
capacity/safety controls. Reject these. Use a single shared page-level launcher,
clear session content on sign-out, exact request schemas, fresh own-case checks,
SQLite atomic reservations with expiring case-bound proposals, and callbacks
only. Missing agenda configuration must be an explicit unavailable state.

Reflection: offer 1..3 stored future free slots filtered by date/time preference,
not inferred household suitability. Explain that adjustments need a person.
A checkbox confirms one specific proposal; neither chat text nor AI can book.
Cancel remains available and does not imply works consent.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/520, retrieved 2026-10-28.
* W2: https://github.com/jmservera/ama/issues/469, retrieved 2026-10-28.
* W3: https://github.com/jmservera/ama/issues/164, retrieved 2026-10-28.
* W4: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-28. Local Fluent/content standards take precedence where
  typography or heading preferences conflict.
* C1: `src/api/src/zava_forward/api/resident_demo/app.py:319`:
  own-case, same-origin/CSRF assistant route and post-inference reauthorization.
* C2: `src/core/src/zava_forward/core/resident_assistant.py:81`:
  host-owned mandatory text and fixed topic boundary.
* C3: `src/api/src/zava_forward/api/resident_demo/aoai.py:121`:
  existing SQL-capped Azure advisor with labelled deterministic fallback.
* C4: `src/core/src/zava_forward/core/resident_showcase.py:509`:
  read-only positive projection; no appointment/consent information.
* C5: `src/core/src/zava_forward/core/appointments.py:357`:
  works confirmations require separate resident, staff and capacity evidence.
* C6: `src/api/checks/resident_assistant_browser_check.py:28`:
  constructed local HTTP/browser fixture, no real model or SQL.
* C7: `src/api/checks/regulatory_ux_check.py:25`:
  pinned axe digest and reusable rendered WCAG scan helper.
* C8: `docs/reference/regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md:123`:
  sections 2.3.1..2.3.3, source 2024-04-01, retrieval 2026-09-19.
* C9: `src/README.md:60`: full exact-head gate and nonqueued heavy-run admission.
* W5: attempted official currentness check at
  https://www.gov.uk/government/publications/consumer-standards/safety-and-quality-standard
  on 2026-10-28 returned 404. This is not currentness evidence.
* W6: https://www.gov.uk/government/publications/safety-and-quality-standard,
  retrieved 2026-10-28 during implementation verification. Official sections
  2.3.1..2.3.3 match C8. The earlier failed URL is preserved. This establishes
  the selected provision comparison, not the currentness of all applicable law.

## Findings, Alternatives and Decision State

Selected: bounded natural-language routing plus existing fixed questions,
native nonmodal chat dialog and shared bottom-right launcher; deterministic
personal/regulatory answers, existing Azure route for approved topics; explicit
local SQLite synthetic callback agenda with atomic confirm/cancel.

Rejected: new model provider, arbitrary model prose, new works authority,
private/staff dataset access, fabricated appointments, framework redesign.
Consent records absent from SQL stay Unknown. Regulatory text is dated local
evidence, not a claim of current law. Further official currentness verification
is required before consequential use; source-only synthetic explanations may
proceed with that warning. Human wording, screen-reader and real-model #164
acceptance remain pending.

## Research Completion and Self-check

All four questions are answered by C1..C9/W1..W5. One focused inline
wider/deeper/contrarian cycle completed in order. No independent research
delegation was warranted. No material in-scope uncertainty requires another
cycle. No source edits were made during Research.

## Planning Readiness

Ready for bounded synthetic implementation. Research disposition: executed,
complete. Next parent action: Plan, preserving the stated acceptance limitations.
