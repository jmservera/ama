# Issue 441 phase details

## Phase 1

* Frontmatter: title, description, author, ms.date 2026-11-04, ms.topic reference, matching ADR 0006.
* Sections: Status, Context, Decision, Consequences, Diagram, Open decisions, Evidence boundaries.
* Staff memory (ADR 0004) and regulatory no-send (ADR 0005) explicitly not widened.

## Phase 2

* Copy `resident-service-boundary.{excalidraw,svg,png}` from the 2026-10-23 tracking folder; verify with `cmp`.
* PNG described as Chrome render of the SVG, not native Excalidraw export.

## Phase 3

* BRD line 56, PRD lines 121 and 1358, `docs/architecture/README.md`, `docs/reference/README.md` row.
* Log: append-only, blank line before heading, `Refs #441`.

## Phase 4

* Relative-link existence check, non-ASCII scan, `python3 tools/rpi-checks.py --changed`.
* No code: ruff, mypy and unit tests not applicable.
