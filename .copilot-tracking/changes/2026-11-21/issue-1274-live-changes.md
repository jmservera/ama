# Issue 1274 live changes

Tier: focused (documentation only; no src change, no rpi-checks run). Validation run: tools/test_install_actionlint.py 12 tests OK; real installer run and independent sha256sum check; link review of the diff.

Changed files:

* docs/reference/research/issue-1274-live-evidence-2026-11-21.md (new)
* docs/reference/README.md (index row)
* docs/reference/log.md (entry)

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1. Identify failing endpoints and installers | Proven for actionlint (#1243, #1271) and AWF v0.28.23 checksums.txt (#1271); #1273 causes unproven (not retained at final head) | Jobs 128696067639, 128703802032, 128680975934, 128684597601, 128681102295, 128683494622 |
| 2. Bounded fail-closed retrieval | Ticked; reconfirmed | 12 tests OK |
| 3. Focused regressions | Ticked; reconfirmed | Same tests |
| 4. Real exact-version verification and hosted CI | Proven for actionlint 1.7.7 (local real download, independent sha256sum, hosted run 42497999337); unproven for AWF 0.28.23 (upstream installer, no repo-owned hook) | Research note |
| 5. Dependent PR resume route | Ticked; unchanged | Issue comment 2026-11-11 |

Whole-issue closure is not claimed; the commit uses Refs #1274.
