# Issue 1274 live r2 research (2026-11-19)

Refs #1274. Synthetic demo, desktop only. Disposition: reused. Planning Readiness: Ready (record-only).

Evidence reused: `docs/reference/research/issue-1274-axe-download-hardening-2026-11-18.md` (retained failure logs for the
#1243, #1271 and #1273 heads, actionlint and axe verification) and
`docs/reference/research/issue-1274-live-release-download-criteria-2026-11-19.md`. The installer
`tools/install-actionlint.py` and the verified axe download in `.github/workflows/src-ci.yml` are on this branch.

Unticked criteria: 1 (endpoints and logs) and 4 (real verification, then exact-head review, hosted CI, merge).
Criterion 1 is evidenced for the demo; criterion 4 needs a push and hosted CI, which this run may not do. The only open
code gap is the AWF 0.28.23 bootstrap, generated gh-aw output with no repo-owned retry hook and a FULL-tier change.
Nothing buildable and demo-relevant remains.
