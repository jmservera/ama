---
title: "Research: #215 provenance and audit contract regression test"
ms.date: 2026-11-14
---

* Task: demo-215-provenance-audit-contract-0655. Research disposition: executed (direct read). Planning Readiness: Ready.
* Branch `test/demo-215-visit-consent-grounding-0600`, HEAD `70464f5ff`, stacked on PR #1576 / #1630.

## Findings

* Full `src/api` mypy flags three `unused-ignore` comments on the `roles.Matrix` class lines of the visit-consent, unblock-visit and end-to-end stabilization tests. The sibling `# type: ignore[no-any-return]` comments on `return reply` are still needed.
* `unittest tests.<module>` (the focused command) cannot import `test_role_matrix` because `src/api/tests` is not on `sys.path`; `discover -s tests` hides this. The four modules need a path append before the bare import.
* Case chat (`chat_panel.ask`) stores assistant messages with `model` and `evidence`, audits `chat.answer` (outcome) and `chat.turn` (receipt with outcome and no question text). Replies carry `answer_source`, `model` and `citations`.
* A generative draft with an unsupported claim is replaced by `decision-rules-fallback` with `model` `workflow-only`. A turn with no cited sources is not an `answer`.
* Regulatory chat (`RegulatoryChat`) gives held (`refused`) turns with empty citations, `workflow_only`, zero model calls and a doubt receipt that changes no record.
* Existing evidence is static or per-path; none asserts stored metadata and audit rows agree with the payload.

## Evidence boundary

Synthetic fixtures; API and ledger contract checks only, not live model, browser or staff evidence.
