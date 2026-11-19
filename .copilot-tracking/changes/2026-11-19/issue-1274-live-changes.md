# Changes 1274 live (2026-11-19)

Tier: FOCUSED (no src change). Files: research note, docs/reference/README.md index row, docs/reference/log.md entry.

Validation: `python3 -m unittest discover -s tools -p test_install_actionlint.py -v` 12 OK; live installer run verified 1.7.7; Markdown/link and diff review. Not run: tools/test_rpi_checks.py, hosted CI, rpi-checks.py --all.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Identify failing endpoints/logs | Unproven (logs no longer retrievable) |
| 2 | Bounded fail-closed retrieval | Proven |
| 3 | Focused regressions | Proven for 12 regressions; no workflow change |
| 4 | Real verification, review, hosted CI | Verification proven; rest unproven |
| 5 | Resume route | Already ticked |
