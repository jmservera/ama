# Issue #1274 live research (opened 2026-11-19)

Status: open. Scope: first unmet acceptance criterion of #1274 (hosted official-release download resilience). Demo is synthetic, desktop only; no Azure action is needed.

Opening reading: issue body and two owner comments (closure audit 2026-11-11, demo readiness 2026-11-12). Criterion 5 is ticked; criteria 1 to 4 are unticked.
Merged #1275 already ships `tools/install-actionlint.py` (bounded, fail-closed, pinned digests) and `tools/test_install_actionlint.py`, wired into `.github/workflows/src-ci.yml`.

## Findings

Research disposition: executed. Planning Readiness: Ready.
Evidence note: `docs/reference/research/issue-1274-live-release-download-criteria-2026-11-19.md`. Criterion 1 proven for #1243 (job 128696067639, curl 504 exit 22); #1271/#1273 runs not retrievable. Criteria 2 and 3 already delivered by #1275. Criterion 4 checksum part proven; hosted CI needs a push (forbidden). No unmet code-addressable criterion; no src change.
