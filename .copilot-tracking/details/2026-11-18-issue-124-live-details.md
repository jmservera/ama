# Details: issue #124 live proof (2026-11-18)

Phase 3 files: docs/reference/research/issue-124-phase0-discovery-evidence-2026-11-18.md (new), docs/reference/README.md (one paragraph after the #130 entry), docs/reference/log.md (append), .copilot-tracking/evidence/2026-11-18/issue-124-live/ (probe.py, probe.json), changes record.
Success: per-criterion table; unticked criteria stay unticked; no source or Azure change.

## Steps

* Phase 1: read the three discovery modules and their tests; locate runtime consumers in `src/api`, `src/orchestrator`, `src/agents` and `src/importer` (none found).
* Phase 2: one critique pass; scope stays offline.
* Phase 3: run the 59 unit tests (output in `unittest.txt`), run `probe.py` to produce `probe.json`, write the evidence note with the per-criterion table, add the README index paragraph and append the log entry.
* Phase 4: one review, link check of the note, secret scan of evidence, commit with trailers, no push.
