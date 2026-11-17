---
title: Issue 151 WCAG baseline refresh plan
ms.date: 2026-11-17
---

## Plan

* [ ] Phase 1: add a dated section "Counted guard-suite measurement (2026-11-17, #151)" to `docs/reference/research/ux/wcag-conformance-baseline.md` with the measured counts, the per-role screen guard files and the explicit statement that these are engineering evidence, not conformance or assistive-technology results.
* [ ] Phase 2: add one regression test in `src/api/tests/test_wcag_workbench_baseline_151.py` asserting the section exists, names the measured counts, and that the static counts it quotes (22 assets, 15 tables, 9 aria-invalid sites) equal source.
* [ ] Phase 3: append `docs/reference/log.md` entry; run targeted tests and `ruff format --isolated --line-length 100 --check` on the test file; commit.

Details: [plan details](../details/2026-11-17-issue-151-wcag-baseline-refresh-details.md). Critique: single self-critique below.

## Critique (one pass)

Compatible: keep wording free of conformance claims (applied). Manual screen-reader row C4 stays unticked; issue stays `Refs #151`.
