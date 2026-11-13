# Research: Wave-1045 parent integration (Refs #440)

Base SHA: `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Branch `docs/demo-wave-integration-parent-1045`. Tier: Focused.
Disposition: executed (inspection only).

## Findings

* Eight child commits all descend from base; each diff is `.copilot-tracking/` only (counts 7, 22, 7, 14, 9, 9, 10, 8 = 86 files); zero `src/`, `infra/`, `tools/`, `.github/` paths.
* Child summaries: #134 no-op alignment (26 blobs already in main); #107 AI telemetry (79 unit tests, 43-entry probe); #521 cutoff 2028-01-01 (77 non-SQL OK, 27 MSSQL skips, API deferred); #136 Bicep (5 templates exit 0, infra/tests partial failure deferred to Wave 2); #1288 IoT (68 Core OK, 480 API exit 0, 169 MSSQL skips); #225/#226 UX audit (37 tests, advisories); #227/#229/#230 UX audit (47 tests, paging and AT follow-ups); #134 preflight (74 tests, 20260901 five-home).
* Target: `docs/architecture/cutover-evidence-pack.md` ends with the #891 section (2026-11-13) and `docs/reference/README.md` has an index row at line 912 for it; `docs/reference/log.md` is append-only, ends with the #891 entry.
* Planning Readiness: Ready.
