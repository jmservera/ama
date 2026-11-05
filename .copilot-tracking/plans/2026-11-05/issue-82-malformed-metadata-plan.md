---
title: Issue 82 malformed quality metadata plan (2026-11-05, correction)
ms.date: 2026-11-05
---

* [ ] Phase 1: shared regressions in `Flows` first; capture RED (details: `../../details/2026-11-05/issue-82-malformed-metadata-details.md`).
* [ ] Phase 2: minimal guards in `evidence_gaps`.
* [ ] Phase 3: JSON and SQLite targeted tests, configured ruff (check and format, `--no-cache`) and mypy with external caches.
* [ ] Phase 4: commit with gh-derived noreply identity; full gate and SQL Server group pending coordinator admission.

## Critique (single pass, self-run)

* Guards are explicit type checks only: each item must be a dict whose label is a string; `checklist` must be a string, else treated as unreadable (None). No broad `except`. Applied.
* `checklist` that is a non-matching string keeps the existing fallback to the measure checklist. Applied.
* A non-string or missing label on any item makes the record unreadable (Unknown), not a gap list, so it cannot pass. Applied.
* Replacement path unchanged: corrupted means `evidence_gaps != []`, so None qualifies. Applied.
* Corruption persisted and reopened for every backend; SQL Server parity is planned for the final gate, not claimed now.
* Do not reformat the legacy-excluded `quality.py`.
