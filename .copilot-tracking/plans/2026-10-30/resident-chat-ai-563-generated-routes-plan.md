---
title: Complete-message admission for every generated resident route
ms.date: 2026-10-30
---

## Accepted Scope

Task issue-563-generated-routes / resident-chat-ai-563-generated-routes,
continuing issue-563-complete-admission on the existing open PR 564 branch.
User explicitly requests Implement then Review of PRRT_kwDOUU8JX86x9VaI.
Reuse that thread and current source/tests as adequate research and the original
critique as historical evidence; do not repeat earlier task Reviews or critique.
The earlier Conformant Review covered the repair grammar, not this broader defect.

Require complete-message recognition for status, documents, forms, home and
repair generation; legal/consent questions must not be captured by document
keywords. Preserve safety/manual replies, genuine repair questions and ordinary
record questions. Use finite host-owned grammar, not model classification or
an expanding command blacklist. Explicit fixed-topic requests remain unchanged.

Approved writes: resident_demo/chat.py, test_resident_chat_api.py, related API
README and this task's dated tracking artifacts. app.py is dispatch context;
edit only if routing alone cannot establish the boundary. No UI, Azure,
actual-model invocation, private data, push or unrelated gate repairs.

## Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement all generated-route admission
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reproduce, fullmatch all generated routes and test protected precedence

Add enabled-advisor HTTP regressions asserting exact deterministic replies and
zero advisor/provider/reservation/token/transport activity for both reported
examples and appended requests across all generated routes. Preserve existing
ordinary route expectations and generate plain status and dead-rat positives.
Constrain the existing home-improvement free-text subject as well as keyword
status/document/form branches.

Completion: all generated record routes fullmatch finite recognised questions;
legal/consent handling precedes them. Existing repair grammar and fixed-topic
dispatch unchanged. All 25 chat tests pass, including enabled-AI full-message,
protected and ordinary-record positive matrices.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Resident suite and configured API tooling

Depends on P01. Run README resident discovery, full API Ruff lint/format and
mypy using installed tools; retain external logs and disclose opt-in skips.
Update README with all-route finite admission and protected precedence.
Reconcile implementation evidence before Review.

Completion: explicit-source full resident suite 152 run, 145 passed, seven
existing opt-in skips; full API Ruff lint/format and mypy pass. The literal
README command selected an unrelated editable worktree; failed evidence is
preserved and superseded by the explicit candidate-source run.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and persist locally
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: One independent bounded Review

Depends on P02. Activate rpi-review once and obtain an independent read-only
assessment of this task's exact source delta and evidence. Preserve its outcome,
route any findings to later work, and do not enter a correction/re-Review loop.

Completion: one independent Review executed Complete / Conformant, no source
defect. RV-001 retains existing separate acceptance gates. All source
fingerprints unchanged after validation and Review.
<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Local commit

Depends on P03-T01. Resolve authenticated noreply identity, commit implementation
and original dated evidence with Refs #563 only and the exact Copilot trailer.
No push. No publication acceptance claimed: the prior failed complete local
gate is historical and a new exact-head complete gate is needed for publication.

## Follow-Up Items

Existing complete-gate dependency, live-model and human/AT acceptance remain
outside this local routing correction. Publication owner obtains a fresh
passing exact-head gate before any future push; model-evaluation owner obtains
separately authorised actual-model evidence; resident/accessibility owners
obtain human and AT acceptance. Review RV-001 retains these exclusions without
adding source work or expanding this task.
