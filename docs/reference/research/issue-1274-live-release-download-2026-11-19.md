---
title: Issue 1274 resilient release downloads, criteria proof for the demo
description: Per-criterion evidence for #1274 gathered 2026-11-19 on main 910adb0a1
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only, no Azure use. Refs #1274. No source change: the bounded, fail-closed installer
`tools/install-actionlint.py` and its tests already landed through #1275, so no unmet criterion needs new code.

## Evidence recorded

* `python3 -m unittest discover -s tools -p test_install_actionlint.py -v`: 12 tests, OK. They cover 504 then
  recovery, all-504 exhaustion with bounded attempts, browser-to-API fallback, truncated body, wrong checksum on
  every source, oversized response, auth token dropped on foreign redirect, checksums file missing the pinned
  digest, invalid archive and exit codes.
* Live run `python3 tools/install-actionlint.py <tmpdir>/bin` against the official endpoints: both
  `actionlint_1.7.7_checksums.txt` and `actionlint_1.7.7_linux_amd64.tar.gz` "verified from github.com on attempt 1"
  against the pinned size and SHA-256; the installed binary printed `1.7.7`. The temporary directory was deleted.
* `gh api repos/rhysd/actionlint/releases/tags/v1.7.7`: asset ids 221573254 (2080472 bytes) and 221573261
  (1119 bytes) match the pinned identities in the installer.
* `gh run view 42469282088` (the #1243 head `fb7231c788`): the retained failing job is `src-namespace`; the
  retained log does not show the actionlint step, so the original HTTP 504 text is no longer retrievable.
* Latest Source CI on main (run list, `src-ci.yml`): success at e2ecee256, 2026-11-08.

## Per-criterion result

| # | Criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Identify failing endpoints and retained logs for the #1243, #1271 and #1273 heads | Unproven | Endpoint (release download for `actionlint_1.7.7_linux_amd64.tar.gz`) is named in the issue; retained job logs no longer show the failing step and the AWF 0.28.23 bootstrap logs were not retrievable |
| 2 | Bounded retrieval, fail-closed checksum | Proven (offline and live) | Installer source plus the live verified install above |
| 3 | Focused regressions, WORKFLOW_HASHES, rpi-checks tests | Partly proven | The 12 regressions pass; no workflow was changed, so no hash update was needed; `tools/test_rpi_checks.py` was not rerun |
| 4 | Real checksum verification, independent exact-head review, hosted CI, merge | Partly proven | Real verification proven; review, hosted CI and merge are not applicable to a local frozen candidate |
| 5 | Dependent PR resume route | Ticked in the issue | Recorded in #1275 |

The AWF bootstrap scope is an upstream setup action with its own retries and hashes; no mirror, action upgrade or
workflow change was made.
