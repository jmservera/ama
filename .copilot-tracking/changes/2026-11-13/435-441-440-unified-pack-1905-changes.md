# Changes: unified pack 1905

* Cherry-picked cleanly onto fa494a7ae: 36477121e -> 49d5bc98d, d88a16926 -> 41918253e, 32d7328c3 -> 6dbc4db37, 22e8b2528 -> 623c48fc6. No conflicts.
* Regenerated docs/architecture/cutover-reference-inventory.tsv (one row: src/agents/README.md 482 -> 491; audit was stale, now PASS: 130 matrix rows, 1926 locations).

## Verification

* test_cutover_audit: 9 tests OK. 441 verify test: 5 tests OK. ruff on 441 scripts: pass.
* validation.json SHA-256: candidate, pdf, baseline, speaker script and Q&A hashes match files; picks did not touch validation.json.
* Relative links: no broken link in added content; 17 pre-existing broken links in older docs/reference/log.md entries not changed.
* Secret scrub over the diff: 0 hits. git diff --check: 0.
* Not run: full local gate, hosted CI (Focused tier). Nothing pushed.
