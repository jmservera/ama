---
title: Issue 1828 CI correction cycle 2 review
description: Single post-implementation review of the mypy patch target correction
ms.date: 2026-11-16
ms.topic: reference
---

## Execution and outcome

Review executed once by the implementing worker. Outcome: conformant for the FOCUSED scope; independent exact-head review, push, PR update and hosted CI remain with the coordinator and are unobserved.

## Assessed boundary

Diff against 8e9324bc69a59bc4efbd128fa50d1cf7974649e7: one line in `src/api/tests/test_map_viewport_premise.py` plus tracking artifacts.

## Findings

* None material. The dotted patch target resolves the same global `time.monotonic`; the virtual clock, the four tests and their assertions are unchanged; CI-parity bare `mypy` now passes (307 files); 124 focused tests, Ruff check and format pass; the full employee browser check passed twice on the new head with 14 axe scans, zero violations and zero skips.
* Disclosures (not defects): baseline reproduction preceded the research-open witness; the `launch` witness event was refused for want of a brief; two operator invocation errors before any check ran; state pointers edited with `sed`; the prior independent review Pass is historical for this head.
* No application, authorization, consent, map or keyboard change; no web UI file changed, so no web-design-guidelines conformance claim is made.

## Routed work

Coordinator: independent exact-head review, push, update PR #1829, read hosted `src-api` and other CI on the new head.
