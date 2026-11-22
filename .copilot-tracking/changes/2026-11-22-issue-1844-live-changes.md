---
title: Issue 1844 live changes
ms.date: 2026-11-22
---

Tier: Focused. No `src/` file changed; the temporary CSS removal used for failing-first was reverted (`git status` clean for `src/`).

Added: `docs/reference/research/issue-1844-live-20261122-2026-11-22.md`, two log files under `docs/reference/research/mobile-map-summary-1844-live-2026-11-22/`, an index row in `docs/reference/README.md` and a log entry.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Failing-first with served-byte identity | Proven (5 of 5 controls covered without the rule; identity hashes pass) |
| 2 | Four viewports, both tile states, hit tests and keyboard | Proven (8 states, 5 controls, 0 covered) |
| 3 | Focus, selection, desktop, no overflow | Proven |
| 4 | Attribution at short and tall heights | Proven |
| 5 | Existing map and axe checks, zero skips | Proven (436 PASS, 0 skips, 0 axe violations); manifest hash not applicable; 14 axe color-contrast incompletes recorded, no conformance claim |
| 6 | RPI artifacts, tier, independent review, hosted CI | Unproven in part: artifacts and tier done; independent exact-head review and hosted CI need a push, which is forbidden here |
