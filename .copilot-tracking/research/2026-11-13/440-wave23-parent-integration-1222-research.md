# Research: Wave-1105 and Wave-1143/1211 parent integration (Refs #440)

Task: `440-wave23-parent-integration-1222`. Base `74a93a137a983e0a87418e3321a6847ba9bcd278`. Research disposition: executed (read-only inspection).

## Evidence

* Read `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md` index, `docs/reference/memory.md`; precedent is the Wave-1045 section in `docs/architecture/cutover-evidence-pack.md`, its index row and log entries.
* All 14 child commits share merge base `3b05143179` with HEAD. Each changes only `.copilot-tracking/` files (0 non-tracking paths). The union is 112 unique paths and 0 path appears in two children (`git diff --name-only HEAD...<child>`).
* No child touches `docs/`, `src/`, `infra/`, `tools/` or `.github/`, so no textual merge conflict is expected.

## Child map

| Child | Issues | Recorded outcome (from the brief; verified at implementation against child changes files) |
| --- | --- | --- |
| `fde97a11b55c` | #521 | 53 API cutoff tests OK, 0 skips |
| `6334017082bc` | #136, #137, #360 | full-deps offline `infra/tests` rerun, 4 modules exit 0 |
| `5ab12d36933e` | #107, #159, #432 | loopback fake-provider execute across 5 assistants |
| `c28b8a198216` | #229, #230, #149 | 112 API tests OK and Node pager harness exit 0; range-end `disabled` gap |
| `d824e59e12db` | #165, #188, #1288, #134 | 77 tests OK; seed `20260901` stock conflict trace |
| `d89141c0f296` | #164, #162, #157 | 441 offline chat tests, 1 Chromium skip |
| `0eab0943aa1c` | #441 | link and formula checker; `PRD:609` anchor and ADR 0007 premise mismatch |
| `953e52435e19` | #115, #117, #148 | orchestrator 115 tests OK, 1 MSSQL skip |
| `150749d82632` | #80, #176, #135 | importer 85 and API 33 tests OK |
| `1684a0690fdd` | #79, #76, #82, #83, #86 | 836 tests, 0 failures, 163 skips |
| `8e8845154e9e` | #216, #215, #208 | regulatory suites, 0 failures |
| `7d9f72e7bdda` | #107 | HELD for `src/` edit; failing-first spec |
| `8aafaf43bee0` | #441 | ADR 0007 and `PRD:609` anchor provenance |
| `85177d5bd43a` | #96, #98, #99, #93 | Finance suites 339 tests, 36 skips |

## Planning readiness

Ready. Documentation and tracking integration only; Focused tier (no executable change). No test runs are needed beyond byte-identity, scope and link checks.
