# Issue 441 changes (2026-11-04)

* Added `docs/adrs/0007-optional-resident-service-over-shared-case-authority.md` (Accepted 2026-11-04, exercise only).
* Added `docs/architecture/resident-service-boundary.{excalidraw,svg,png}`, byte-identical to the 2026-10-23 tracking copies (`cmp` verified).
* Updated BRD, PRD (two places), `docs/architecture/README.md`, `docs/reference/README.md`; appended a `docs/reference/log.md` entry.
* Unchanged: original case study, ADR 0001 to 0006, owner memory, the original proposal and its evidence.

## Validation

* Run: relative-link existence check on the five edited Markdown files and the ADR (no broken links); non-ASCII scan of the ADR (none).
* Attempted: `python3 tools/rpi-checks.py --changed --base origin/main`; it returned `BLOCKED: Global heavy-resource lock timeout` (the lock is held elsewhere). Not retried or bypassed.
* Not run: ruff, mypy, unit tests (no code changed), the complete gate, benchmarks, full suites.

## Unmet issue criteria

* Criterion 5: the requirements owner has not dispositioned the FR-044/AC-084 wording for publication. The ADR keeps per-message review normative.
* Criterion 9: publication gates and exact-byte independent review are not complete.
