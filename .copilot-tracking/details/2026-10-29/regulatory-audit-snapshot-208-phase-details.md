---
title: Regulatory audit snapshot implementation details
description: Bounded task details for 208-audit-snapshot
ms.date: 2026-10-29
---

Task ID: 208-audit-snapshot. Research C1-C5 establishes readiness.
No blockers or unresolved user decisions.

<!-- P01 -->
## P01: Snapshot correction

<!-- P01-T01 -->
### P01-T01: Deterministic regression

Complete. Used existing make() JSON fixture and one recorded answer. Capture
expected usage before patching. Open the real audit binary stream and wrap it;
patch only regulatory_chat.open. At read, append one valid unrelated audit
record whose content exceeds MAX_BYTES using a separate real writer, then
delegate the requested read length to the original stream. This guarantees
growth after EOF capture, without nondeterministic scheduling. Assert initial
size below bound, later size above bound, read argument equals captured size,
unchanged usage, and a successful subsequent bounded-partial read. Run the
new test against original code before applying the production correction.

<!-- P01-T02 -->
### P01-T02: Bounded read and documentation

Complete. Replaced read(MAX_BYTES) with read(size-start) and clarified the existing
README snapshot paragraph. Retain all other error and truncation behavior.
No new public interface or configuration.

<!-- P01-T03 -->
### P01-T03: Validation and reconciliation

Complete. From src/core ran installed ../../.venv/bin/python with PYTHONPATH=tests:
unittest test_regulatory_chat test_regulatory_usage test_regulatory_privacy -q.
Run ../../.venv/bin/ruff check . and ruff format --check ., then git diff --check.
Record exact results and deviations. Reconcile plan/details/changes and state,
then hand off once for independent Review of baseline-to-working-tree diff.
Commit implementation and dated original evidence locally after Review.
Results: 29 focused tests passed in 22.391s; Ruff check passed for src/core;
Ruff format --check passed (110 files already formatted); git diff --check
passed. Original-code regression reproduced JSONDecodeError in 0.209s.
No remaining implementation markers, blockers, amendments or follow-ups.
