# Issue 1274 live r2 changes (2026-11-19)

Refs #1274. No source, workflow or test change. Tier FOCUSED. Synthetic demo, desktop only; no Azure action.

Validation run today: `python3 -m unittest discover -s tools -p test_install_actionlint.py` 12 tests OK;
`python3 -m unittest discover -s tools -p test_rpi_checks.py` 113 tests OK. mypy, ruff and `rpi-checks.py --all`
not applicable (no src or infra Python change; --all forbidden).

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Endpoints, logs, installers | Proven for the demo | Retained job logs for 1243, 1271, 1273 in `docs/reference/research/issue-1274-axe-download-hardening-2026-11-18.md`; AWF logs show 504 but the AWF installer is upstream |
| 2 Bounded fail-closed retrieval (ticked) | Proven for actionlint and axe | Installer and verified axe step |
| 3 Regressions (ticked) | Re-proven | Tests above |
| 4 Real verification, review, hosted CI, merge | Partly proven | Checksum verification earlier recorded; exact-head review, hosted CI and merge need a push |
| 5 Resume route (ticked) | Already recorded | #1275 |

Unproven: AWF 0.28.23 bootstrap recovery (generated gh-aw code, FULL tier), hosted CI on a reviewed head, merge.
