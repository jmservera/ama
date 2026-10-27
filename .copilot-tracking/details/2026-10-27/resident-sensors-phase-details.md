<!-- markdownlint-disable-file -->
# RPI Phase Details: Resident sensors

Task ID: 468; slug: resident-sensors; date: 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/resident-sensors-plan.md.
Evidence: .copilot-tracking/research/2026-10-27/resident-sensors-research.md.

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Boundary | Complete; subsequent RV-001 source guards and 114 focused tests pass |
| P02 | Presentation | Complete: real HTTP/Chromium checks pass |
| P03 | Validation | Complete: core/API suites, Ruff/mypy and browser pass |

<!-- rpi:phase id=P01 -->
## P01: Own-home sensor boundary

<!-- rpi:task id=P01-T01 -->
### P01-T01: Source view and strict projection

C1-C5/C7 show separate sensor tables and home.stock_id, with signed session
ownership. Extend infra/sql/resident-showcase.sql as a source-only optional
projection: typed NULL home ID/empty JSON if tables absent, otherwise correlated
TOP 48 SYNTHETIC readings joined through sensor register and case stock ID.
Dynamic CREATE VIEW must quote correctly and keep schema unchanged beyond view.
Use JSON ordered newest first in SQL then chronological domain output.
Readings carry home identity internally for validation; never emit that identity
or sensor/reading IDs. Validate all rows, finite values, UTC, bounds/fault labels,
maximum count. Malformed projection denies rather than silently normalising.
No runtime query selecting arbitrary browser IDs, no new grants.
Tests: SQL text and mock cursor, strict parsing, empty/fault/missing values,
two residents with distinguishable histories, revoked/forged requests.
Completion: domain/API tests demonstrate values and cross-home refusal.
Dependency: existing reader and authority code. No unresolved design decision.

PC-001: sensor_id, register.home_id, reading.home_id and case home.stock_id use
Latin1_General_100_BIN2 comparisons. Both source_type fields must equal SYNTHETIC.
The reading's own home_id is retained internally and compared exactly by Python.
Test mismatched/case-distinct homes and non-synthetic sources.

Subsequent RV-001 implementation adds DATALENGTH guards after converting
VARCHAR/NVARCHAR identity/provenance operands to NVARCHAR(MAX), avoiding SQL
comparison padding without truncation or trimming. Add source-query regression
assertions for every guard and parser padded-identity/provenance negative cases.

PC-002 outcome contract (JSON uses INCLUDE_NULL_VALUES):

| Input | Outcome |
| --- | --- |
| Invalid JSON/shape/identity/provenance/UTC or unknown fault | Deny malformed envelope |
| Null measurement | Keep timestamp; channel unavailable with "Not recorded" |
| Non-finite or out-of-generator-bound numeric measurement | Keep timestamp; channel unavailable with "Outside demo range" |
| OUTLIER/STUCK | Both channels unavailable with explicit fault text |
| Valid measurement | Native meter and chart point, no safe/unsafe colouring |

Latest is latest observation even when unavailable. No older-value substitution.
Generator bounds (-10 to 45 C, 0 to 100 percent) are fictional plotting ranges,
not health thresholds. Browser covers sibling valid channel, faults, singleton.

<!-- rpi:phase id=P02 -->
## P02: Accessible sensor presentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Gauges, history and table

C6/W1 and UX standards require native semantics and no colour-only status.
Use native meter with label/value/time for valid values, no fake zero for missing
or invalid readings. Show explicit latest recorded date and synthetic label.
Two static single-unit SVG plots with axes/units, accessible name/description,
gaps for unavailable values, same data in native table under details/summary.
Reuse Fluent aliases in demo.css. No header/index markup edits or animation.
Test full, sparse and empty histories; keyboard table disclosure; narrow reflow.
Dependency: P01. Completion: browser-observed own-home readings and table.

<!-- rpi:phase id=P03 -->
## P03: Verification and documentation

<!-- rpi:task id=P03-T01 -->
### P03-T01: Local tests, browser and source documentation

Use fresh generated two-home sensor histories with fictional IDs, no files from
private stock. Run actual HTTP server with constructed reader/session auth,
Chromium on loopback. Assert health response, sign-in isolation and gauges/table
values. Check 320/390/1280 reflow, reduced motion and keyboard disclosure, capture
console/page errors. Keep results under dated changes evidence.
Run core/API unit discovery with shared test paths, changed-file ruff/mypy.
README must explain optional tables, source-only view apply dependency, recorded
not live values and no safety judgement. No full-gate/SQL/browser conformance claim.
Dependency: P01/P02. Completion: exact command results recorded before Review.

PC-003: all test/browser subprocess environments remove inherited ZF_* settings
without reading/printing values; set ZF_TEST_MSSQL=0 explicitly. Check other
opt-ins from source before discovery. No .env is loaded. SQL tests intentionally
skip; browser uses real app with constructed reader, not SQL-configured entry.

Completion evidence: core 1380 tests OK (186 skipped), API 1068 tests OK
(308 skipped); focused boundary 113 OK (19 skipped), focused generator/resident
65 OK; changed Python Ruff/format and mypy (4 core, 2 API files) pass; 23 local
HTTP/Chromium assertions pass. Existing temporary synthetic SQLite unit fixtures
ran; no SQL Server connection, view apply, private snapshot or Azure operation.
README explains source-view coordination and non-live/safety limitations.
