---
title: Changes for #1847 live run
ms.date: 2026-11-23
---
# Changes (#1847)

Tier: Focused (documentation and evidence only; no `src` file changed). Hosted CI and independent exact-head review remain required and were not run (no push).

Files: `docs/reference/research/nomination-bootstrap-isolation-rerun-1847-2026-11-23.md` and its evidence folder, `docs/reference/README.md` index row, `docs/reference/log.md` entry, and the dated `.copilot-tracking` artifacts.

Validation: fresh-process probes and unittest orders on source, editable and noneditable layouts (58, 55 and 58 tests OK; noneditable bulk-first yields the one explicit rejection). Live revisions 0000054 and 0000026 confirmed read-only.

## Per-criterion status

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Layouts, metadata and rejection documented | Proven |
| 2 | Both orders in fresh processes per layout; unsupported rejects | Proven |
| 3 | Origins and identities observed | Proven (purge-split cause stays inferred) |
| 4 | Regression fails on original, passes on fix | Proven (ticked) |
| 5 | No purge, foreign checks retained | Proven (ticked) |
| 6 | Full local gate and external receipt | Unproven, owner-gated: no src change and `rpi-checks.py --all` is forbidden here |

Owner-gated: criterion 6 only. Use `Refs #1847`.
