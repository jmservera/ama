<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-001 fixture provenance plan
description: Prospective plan for runtime-produced contact and AI checker fixtures
ms.date: 2026-10-26
---

Prospective. Written after the research and before the critique and any source edit.

* [ ] Phase 1: one independent critique of this plan, committed before any source edit.
* [ ] Phase 2: add failing tests first in `tools/test_check_demo_feedback.py` only, using runtime-produced evidence: a builder that makes a JSON `Store` from `dataset.DATA`, scripts the AI boundary `_chat`, installs the offline test release, calls `log_call`, `detail`, `verify_ledger` and `ai_priority`, and reloads with a second `Store`. Tests assert the checker passes the runtime-produced `case_write` and `ai` sections, and fails closed when a runtime-produced record is mutated (extra contact, wrong outcome, template source, dropped citations, tampered ledger).
* [ ] Phase 3: keep existing hand-built shape tests; replace the default `bundle` contact and AI sections with the runtime-produced ones only where supported. No checker production change unless a real mismatch appears; then stop and report the choice.
* [ ] Phase 4: focused tests with the existing editable venv: `tools.test_check_demo_feedback` (RecursionError and Application Administrator regressions still present), no install, no Docker, no browser, no gate.
* [ ] Phase 5: one genuine independent review of the change and of the RV-001 disposition.
* [ ] Phase 6: changes, state and review records; local commit with the noreply identity and the Copilot trailer; report; stop before the gate.

If `dataset` or `release_support` cannot be imported, tests skip visibly with the reason and RV-001 is reported as a bounded blocker, not closed.

Out of scope: feature, UI, auth or domain change; checker default or fixture-baseline change; live capture; real AI; SQL; gate; push; PR or issue edits; acceptance ticks.
