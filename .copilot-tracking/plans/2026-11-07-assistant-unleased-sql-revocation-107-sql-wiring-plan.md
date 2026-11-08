---
title: Plan for SQL wiring of the unleased revocation test (#107)
description: Relocate generated metadata, wire the class into the runner SQL group, plan one normal main merge, and freeze for a later FULL admission
ms.date: 2026-11-07
---

Research: [research](../research/2026-11-07-assistant-unleased-sql-revocation-107-sql-wiring-research.md). Details: [details](../details/2026-11-07-assistant-unleased-sql-revocation-107-sql-wiring-details.md). Critique: [critique](2026-11-07-assistant-unleased-sql-revocation-107-sql-wiring-critique.md). Earlier plan and author-only critique are preserved unchanged.

## Decisions

* Source delta limited to `tools/rpi-checks.py` (one tuple entry), `tools/test_rpi_checks.py` (one assertion), the critique-driven isolation correction inside the existing new test classes of `src/api/tests/test_assistant_release.py`, plus dated RPI records. No production, schema, approval or attestation change, and no workflow edit.
* No service, SQL, FULL run, lock wait, push, PR, rebase, force or retarget. No ticks and no closing keyword; publication later uses `Refs #107` and `Refs #104`.
* Skipped SQL is never reported as accepted. Baseline format diagnostic and the original skip are preserved.

## Phases

* [ ] Phase 1: commit these records, then relocate the three generated metadata folders and verify origins and clean status.
* [ ] Phase 2: append the selector and the tool test; apply the critique's test-only isolation correction (mixin `setUp` removing non-`fx-` release rows after base setup, final assertion filtered to `fx-CAP`); run focused tool tests, ruff, mypy and the SQLite selectors with unmasked exits.
* [ ] Phase 3: one normal merge of the settled admitted main (`a1d265340` or a proven score-only descendant), preserving blobs and modes; verify parents and delta.
* [ ] Phase 4: changes record, one author Review, state update, freeze clean. FULL pending the coordinator's nonqueued admission.
