---
title: Issue 93 live changes (2026-11-23)
ms.date: 2026-11-23
---

Tier: FULL classification (src/agents/evals touched, privacy-gate semantics unchanged); only targeted checks run, rpi-checks.py not run (coordinator owns the gate). Local commit only, no push.

Files: docs/reference/research/retrofit-synthetic-data/provenance-register.json (two entries), src/agents/evals/eval-manifest.schema.json (description keyword), docs/reference/research/issue-93-criteria-recheck-live-2026-11-23.md (new), docs/reference/README.md, docs/reference/log.md, evidence folder `.copilot-tracking/evidence/2026-11-23/issue-93-live-20261123T150451Z/`.

Defect: #2316 added three public eval payloads without provenance-register entries; `test_form_review_pack` failed on main (270 tests, 1 failure). After the fix: 284 tests OK, 45 skipped (12 modules plus `test_synthetic_provenance`); `test_eval_harness` 8 OK. Full `src/agents` suite: 13 failures/errors, all in `test_paired_report_command`, identical on the stashed baseline (pre-existing, unrelated, not fixed here). Not run: mypy (no Python change), hosted CI, SQL Server variants, full gate.

Live probe: 5 GETs 200, read-only, no write, no Azure resource created.

| Criterion | Proven? | Basis |
| --- | --- | --- |
| C1 Stabilization checkpoint #440 | Unproven | #440 and #2301 open; needs owner pivot/defer approval, non-worker review, published PR |
| C1a BRD/PRD/ADR reconciliation | Proven for finance rows | Issue body cites wrong BRD IDs; owner edit pending |
| C1b Local regression checks | Proven after fix | 284 tests OK, 45 skipped |
| C1c Bugs dispositioned | Proven for #93 | Register regression fixed in this commit; no open bug issue; unrelated paired-report failures pre-existing |
| C1d Azure residuals and owner decision | Unproven | Owner decision is human; #96 residual in #2140 |
| C2 All children closed or deferred | Proven | #94 #95 #96 #99 closed; remainder deferred #2140 |
| C3 No automated bid, match approval, claim certification or cash | Proven (already ticked) | Tests plus live views |
