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
original confirmed requirements. Later implementation does not require the
same Review again, and this invocation does not rerun it or claim acceptance
from the earlier adverse Review.

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
### [ ] P02: Validate and persist
<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Resident suite, API tooling, evidence and local commit

Depends on P01-T01. Rerun full resident discovery, API Ruff lint/format and mypy.
Preserve previous successful/adverse evidence and this later validation
separately. Commit locally with authenticated noreply identity, Refs #563 and
Copilot trailer, then attempt the complete local gate externally. No push.

## Follow-Up Items

Earlier Review does not accept the post-Review candidate. Fresh exact-head
independent assessment and full gate remain publication prerequisites, not
claims made by this local follow-up. Parent RV-002 actual-model/live and
RV-003 human/content/AT approval stay with their owners outside local scope.
