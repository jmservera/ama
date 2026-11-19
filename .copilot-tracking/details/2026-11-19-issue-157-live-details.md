# Details: issue 157 live (2026-11-19)

Phase 1: edit the index row so the `prototype/` mention reads "`prototype/` removed in #202 step 1 (archive tag v0.21.0)". Expected: check-legacy-references exits 0.
Phase 2: `python3 -m unittest tools/test_check_legacy_references.py`. Failing before, passing after.
Phase 3: changes, review, README index row for the new research note, log entry.
