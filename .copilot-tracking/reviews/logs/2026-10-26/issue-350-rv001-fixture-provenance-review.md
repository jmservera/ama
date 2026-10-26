<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-001 fixture provenance review
description: Independent review of the runtime-produced fixture change, outcome preserved as returned
ms.date: 2026-10-26
---

Single independent read-only `rubber-duck` review, run 2026-10-26 after implementation and focused tests. No second review.

Verdict as returned: Non-conformant, RV-001 partially resolved.

* RV-501 (blocking as labelled by the reviewer): the default `bundle()` still uses the hand-built `case_write()` and `ai_record()` helpers; only the new `RuntimeProducedEvidence` tests override them with runtime evidence. Either route the default through `RuntimeFixture` or narrow the claim to an additive runtime regression.

Confirmed by the reviewer: evidence is genuinely produced by `Store.log_call`, `detail`, `verify_ledger`, a reload and `ai_priority` with only `_chat` scripted; PC-501..504 honoured; negative tests are not vacuous; offline release disclosure is honest (overall `blocked`, acceptance `not-accepted`); RecursionError and Application Administrator regressions remain; only the test file changed; 85 tests OK; no `__pycache__` left.

Disposition: the outcome is not relabelled. The claim is narrowed as the reviewer allowed. The default `bundle()` helpers stay hand-built on purpose because they drive boundary shape tests (for example the 40-contact cap, truncation and malformed shapes) that the runtime does not produce on demand. RV-001 is partially resolved: a runtime-produced contact, reload, audit and AI path now proves the unchanged checker accepts real runtime shapes and rejects runtime template fallbacks and mutations. The hand-built default fixtures remain and are routed as a residual, not closed. This narrowing and the residual are not independently re-verified.
