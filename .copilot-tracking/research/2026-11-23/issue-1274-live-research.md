---
title: Research for issue 1274 live closeout (2026-11-23)
---

## Scope

Compare each acceptance criterion of #1274 with main at `342fad401d`. The issue concerns hosted CI release downloads, so live revisions 0000054/0000026 of the Azure apps are not an input; no Azure resource was touched and no credential was read.

Research disposition: executed (fresh observations) and reused (prior retained-log reads in `docs/reference/research/issue-1274-live-evidence-2026-11-22-run2.md`).

## Findings

* Criteria 2, 3 and 5 are ticked and still hold: `tools/test_install_actionlint.py` 12 tests OK, `tools.test_rpi_checks` 129 tests OK today.
* Criterion 4 (actionlint part): `tools/install-actionlint.py` verified checksums and archive from github.com on attempt 1; independent `sha256sum -c` OK; binary reports 1.7.7.
* Criterion 1: the failing endpoints were identified in the 2026-11-22 note (actionlint release URLs for #1243/#1271; AWF `checksums.txt` for #1271). Job logs re-read today show only 2026-11-08 timestamps; #1273 logs remain unretained.
* Hosted: newest `Source projects CI` on main is run 42497999337 (success, 2026-11-08). No hosted run on a new exact head can exist without a push.

Planning Readiness: Ready. Evidence-only, no src change, focused tier.
