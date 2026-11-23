# Changes (2026-11-23)

Implement start: docs-only; no src edit. Tier FOCUSED (basis: no src, workflow, dependency or Dockerfile change).

* Added docs/reference/research/issue-1274-live-evidence-2026-11-23.md
* Indexed in docs/reference/README.md; appended docs/reference/log.md

## Per-criterion table

| Criterion | Verdict |
| --- | --- |
| 1 failing endpoints | Proven for actionlint (#1243, #1271) and AWF checksums.txt (#1271); unproven for #1273 (logs not retained) |
| 2 bounded fail-closed retrieval | Proven (12 tests OK) |
| 3 focused regressions and rpi-checks tests | Proven (12 and 129 tests OK) |
| 4 real checksum verification and hosted CI on reviewed head | Proven for actionlint 1.7.7 locally; unproven for AWF 0.28.23 (upstream) and new-head hosted CI (no push); owner-gated |
| 5 resume route | Proven (merged #1275) |

Azure live revisions 0000054/0000026: not applicable to this CI issue; nothing touched.
