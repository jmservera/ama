---
title: Complete resident repair request admission
description: Later implementation of the routed issue 563 admission finding
ms.date: 2026-10-30
---

## Scope and Accepted Direction

Task issue-563-complete-admission / resident-chat-ai-563-complete-admission.
Parent issue-563-rv001 / resident-chat-ai-563-rv001. This later implementation
continues the original user-requested RV-001 fix, not an unrelated follow-up.
The independent follow-up Review is Complete / Not accepted and remains
immutable. Its routed RV-001 requires complete-request matching instead of
household-prefix matching and command-word blacklist growth.

Replace partial admission with a fullmatch over recognised repair observations
and informational questions. Unknown detail/combined action text is refused.
Keep genuine dead-rat/household positives, protected routes, accounting and
consent. No UI, Azure, model, infrastructure or expiry changes. Same topic branch.

No new research/critique/product decision needed: reuse the routed finding and
original confirmed requirements. Do not rerun the earlier task's Review or
claim acceptance from it. This later task receives its own single Review of
the complete-request implementation after validation, following the original
user request to implement then review.

## Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement complete request recognition
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fullmatch grammar and external mixed-request regressions

Approved writes: chat.py, test_resident_chat_api.py, related API README and
dated tracking artifacts. Add all four Review reproductions plus unpunctuated
instruction/action continuations. Preserve enabled dead-rat answers and
informational reporting guidance. Assert no model/reservation/token/transport
for refusals. Use finite host-owned patterns; never ask AI to classify.

Completion: whole-message host grammar implemented and shared with action
exceptions. 38 explicit negative/protected examples plus 84 appended-request
combinations keep exact host replies and zero model work. Fourteen generated
repair positives pass; existing disabled/own-case tests retained.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and persist
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Resident suite, API tooling, evidence and local commit

Depends on P01-T01. Rerun full resident discovery, API Ruff lint/format and mypy.
Preserve previous successful/adverse evidence and this later validation
separately. Commit locally with authenticated noreply identity, Refs #563 and
Copilot trailer, then attempt the complete local gate externally. No push.

Completion: resident 149 run/142 passed/seven existing opt-in skips; full API
Ruff/format/mypy pass. Implementation and dated original evidence committed
48001b35112755d502d75380ac9b29039b8e216b. Complete local gate ran externally
and failed on unexpected API integration/dependency skips; browser and mssql
groups blocked by that prerequisite. Failed receipt is retained, not accepted.

<!-- rpi:phase id=P03 -->
### [x] P03: Review the later implementation once
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Independent complete-request implementation Review

Depends on P02-T01. Assess the frozen complete-request source in 48001b35,
external validation and failed full gate. This is the first Review of this
later task, not a rerun of either earlier Review. Preserve its one outcome,
then persist final lifecycle evidence locally. No source changes during Review.

Completion: resident-chat-ai-563-complete-admission-review.md records Complete /
Conformant for bounded source scope, zero new substantive findings. Source
remains exactly 48001b35. Preserve both earlier adverse Reviews. Final lifecycle
evidence is persisted locally without push; no passing full-gate receipt or
whole-issue/live/human acceptance follows from this Review.

## Follow-Up Items

Earlier Review does not accept the later source. A passing exact-head complete
gate and independent assessment remain publication prerequisites. Parent RV-002 actual-model/live and
RV-003 human/content/AT approval stay with their owners outside local scope.

## Final Handoff

P01-P03 executed, bounded source correction complete and independently reviewed.
Local-only persistence includes the full validation history, original adverse
Reviews and later Conformant Review. Full publication gate remains failed,
and any final lifecycle commit invalidates exact-head receipt applicability.
No new source work, push, Azure operation or next child task is authorised.
