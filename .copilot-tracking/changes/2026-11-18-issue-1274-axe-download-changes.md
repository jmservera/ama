---
title: Issue 1274 axe download changes
ms.date: 2026-11-18
---

Tier classification: FOCUSED (no `src/` change; no permissions, action pins, secrets or deployment change). The edit adds a digest check to a CI download, a security-strengthening change to a hashed workflow; a conservative reader may take FULL. `rpi-checks.py --all` was not run (owner instruction); coordinator decides before publication.

## Files

* `.github/workflows/src-ci.yml`: axe step retries 5x on any error, downloads to `.part`, `sha256sum --check --strict`, then `mv`.
* `tools/rpi-checks.py`: `WORKFLOW_HASHES["src-ci.yml"]` updated.
* `tools/test_rpi_checks.py`: `test_src_ci_axe_download_is_bounded_and_verified_before_use`.
* `docs/reference/research/issue-1274-axe-download-hardening-2026-11-18.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Per-criterion proven/unproven

| # | Status | Note |
| --- | --- | --- |
| 1 | Proven (demo) | retained 504 logs for 1243, 1271, 1273 classified; fixture output separated |
| 2 | Proven for actionlint and axe; unproven for AWF | AWF is upstream generated gh-aw code |
| 3 | Proven for actionlint and axe | 12 installer tests, new workflow regression, test_rpi_checks 110 OK |
| 4 | Partly proven | real checksums verified; independent exact-head review and hosted CI not possible (no push) |
| 5 | Already ticked | PR 1275 route |

## Validation

* `python3 -m unittest discover -s tools -p test_rpi_checks.py`: 110 OK. `test_install_actionlint.py`: 12 OK.
* ruff check and format check on the src-ci tool file list: pass (test_rpi_checks reformatted once). mypy --strict installer files: pass.
* actionlint 1.7.7 via verified installer over five native workflows: exit 0. Wrong-digest sha256sum: rc 1.
