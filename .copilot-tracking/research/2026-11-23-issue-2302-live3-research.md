---
title: Research for #2302 (third live run)
date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

## Findings

* Criteria 1 and 2 are proven by earlier runs (`docs/reference/research/issue-2302-ai-economics-live-2026-11-23.md`, live screenshot on revision 0000055, core and API tests). Criterion 3 is a remote issue edit left to the owner.
* New angle: the server validator (`tokenomics.assert_tokenomics_invariants`) forces per-outcome costs to Unknown when `accepted_outcome_count` is 0 and every cost to Unknown when no price source is configured. The browser renderer `aiEconomicsRows` enforces neither rule; it prints any positive-looking string. A stale or non-conforming payload with a price-less or outcome-less "cost per accepted outcome" would show a number where the BRD view must show Unknown.
* Existing tests (`test_overview_ai_economics_100.py`) cover numeric and zero-string costs only, not these two denominator rules.

## Plan input

In the renderer, show per-outcome costs as Unknown when the accepted-outcome denominator is not a positive count, and show all costs as Unknown when the price source is Unknown. Add one regression test with subtests. Tier FULL (src change); targeted tests only.
