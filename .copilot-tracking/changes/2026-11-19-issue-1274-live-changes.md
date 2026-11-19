# Changes: issue 1274 live (2026-11-19)

No source change (tier FOCUSED; FULL not required, rpi-checks.py --all not run).

Files: docs/reference/research/issue-1274-live-release-download-criteria-2026-11-19.md (new), docs/reference/README.md and docs/reference/log.md (entries), .copilot-tracking artifacts.

Validation: `python3 -m unittest discover -s tools -p test_install_actionlint.py` 12 tests OK; installer run verified both official assets against pinned SHA-256. mypy, ruff and web checks not applicable (no code or web file changed).

| Criterion | Status |
| --- | --- |
| 1 Identify failing endpoints | Proven for #1243 (job 128696067639, curl 504); #1271/#1273 runs not retrievable |
| 2 Bounded fail-closed retrieval | Proven for actionlint (#1275); AWF is upstream, unproven |
| 3 Focused regressions | Proven for actionlint (12 tests); no WORKFLOW_HASHES change |
| 4 Real checksum, review, hosted CI, merge | Checksum proven; hosted CI and merge unproven (no push allowed) |
| 5 Dependent PR resume route | Already ticked |

Unmet: AWF 0.28.23 bootstrap recovery, hosted CI on a reviewed head, merge.
