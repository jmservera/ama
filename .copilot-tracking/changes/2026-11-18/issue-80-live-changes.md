---
title: Issue 80 live changes
ms.date: 2026-11-18
---

Refs #80. Tier FOCUSED; no source change.

## Changes

* Added `docs/reference/research/issue-80-live-transition-thresholds-evidence-2026-11-18.md`.
* Added an index paragraph in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Import shows mapping, conflicts, row preview, source unchanged | Ticked before; not re-opened | n/a |
| Every list offers Excel or CSV export; Excel one-way | Ticked before; not re-opened | n/a |
| Export retains version, source, approval, supersession history | Ticked before; not re-opened | n/a |
| Owners set the staged transition thresholds | Unproven; cannot be proven for the demo | Owner decision; no thresholds or owners exist in ADR 0001 or code |

## Validation

* `src/importer` unittest discover: 125 tests, OK.
* No mypy or ruff run: no Python changed. Link review and `git diff` read.
* Not run: `rpi-checks.py --all` (not FULL tier), hosted CI (not pushed).
