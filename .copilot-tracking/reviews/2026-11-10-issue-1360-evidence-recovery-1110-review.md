---
title: Issue 1360 evidence recovery review
ms.date: 2026-11-10
---

Self-run review, not independent. Scope: evidence recovery only.

* Outcome: evidence recovery conformant for the stated scope. Findings: none open against the records.
* Resolved: the E501 inconsistency (fresh importer `ruff check` exit 0 at the exact head); the missing core mypy (exit 0); the core format claim (proven identical to base by temporary copies).
* Remaining gaps: original raw red not reconstructable (a labelled new diagnostic substitutes); original logs lack command headers (new logs carry them); hosted CI, MSSQL core test, full gate and independent exact-head review are unobserved. Core `ruff format --check sqlstore.py` still exits 1, pre-existing and unchanged by the fix; this is not an all-pass claim.
* Routing: this records-only commit changes HEAD, so Root needs an independent exact-head review. No source correction required; no E2.
