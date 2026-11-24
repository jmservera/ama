# Details: issue 1204 live (2026-11-24)

Phase 1: edit `check_ticks(rows, require_extended=False)`; when true, for each row emit `Violation(tick, "schema", "extended field X missing")` once per row listing missing keys among OPTIONAL_COLUMNS. CLI flag passes it through.
Phase 2: tests (strict rejects legacy row, strict accepts full row, default unchanged).
Phase 3: validation and evidence note.
