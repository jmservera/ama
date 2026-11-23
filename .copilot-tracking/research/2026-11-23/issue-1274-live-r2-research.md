---
title: Research for issue 1274 live re-proof run 4 (2026-11-23)
---

## Scope

Re-prove the unticked #1274 criteria 1 and 4 at main `5c08bedd8f`. Synthetic demo, desktop only. The issue concerns hosted CI release downloads; Azure apps are not an input and no credential is read.

Research disposition: executed. Findings are appended below after collection.

## Findings

* Criterion 1: job 128696067639 (run 42469282088 attempt 1, head fb7231c788, 2026-11-08T10:01:37Z) log line 1382 downloads `https://github.com/rhysd/actionlint/releases/download/v1.7.7/actionlint_1.7.7_linux_amd64.tar.gz` (checksums URL on 1383) and line 1397 reads `curl: (22) The requested URL returned error: 504`, line 1398 `Process completed with exit code 22`. The same run attempt 2 failed only in `src-namespace` (a fixture/test job, not a download). #1271 AWF `checksums.txt` and #1273 evidence: see the prior notes; #1273 logs are not retained.
* Criterion 4 (actionlint): `tools/install-actionlint.py` with GITHUB_TOKEN unset verified checksums and archive from github.com on attempt 1; binary 1.7.7; independent curl plus `sha256sum -c` gave `a.tgz: OK` (checksums 1119 bytes, prefix ac22e6577b8d133c; archive 2080472 bytes, prefix 023070a287cd8ccc).
* Tests: `test_install_actionlint.py` 12 OK; `tools.test_rpi_checks` 129 OK.
* Hosted: newest `Source projects CI` on main is run 42497999337, success, 2026-11-08. PR #1275 merged 2026-11-08 (merge 4bc1e3f336). No hosted run on a new exact head without a push.

Planning Readiness: Ready. Evidence-only, no src change, focused tier.
