---
title: Sensor backfill 177 phase details
description: Task-level contracts and verification boundaries
ms.date: 2026-10-15
---

Task 177 / sensor-backfill-177. Research Ready for bounded partial delivery.

<!-- phase: P01 -->
## P01: Register-backed generator

<!-- task: P01-T01 -->
### P01-T01: Typed adapter and wiring

Add sensor_stock.py for CSV parsing, typed selection and deterministic sensors
from stock_fabric.fabric. Read allowlisted values only, validate all rows,
sort IDs before subset selection and use a full-ID digest for sensor identity.
Require explicit positive homes <= register size for estimate and write. Apply
subset before consent. Limit home IDs to 128 UTF-16 units; stock IDs use a 73-char
SENS-SYN- plus SHA-256 format, reading IDs <=96. Add versioned STOCK_SQL_DDL
(NVARCHAR(128) home, VARCHAR(73) sensor, VARCHAR(96) reading), not a migration;
manifest declares stock-reading-v1 and loader callers select schema explicitly.
Reuse stock fabric safe-destination implementation; keep generated data outside
checkout. Existing sensor_backfill.write/estimate gain optional prepared stock
selection. CLI --register routes through adapter; legacy route remains intact.
All-excluded mode emits headers and zero counts, never division by zero.
Record sanitized fabric/monitoring coverage and input digest; fingerprint adapter
and stock_fabric source as dependencies. Construction affects loss only in new
mode; all factors labelled exercise values. No dated retrofit inferred.

<!-- task: P01-T02 -->
### P01-T02: Semantic and regression tests

One typed core test module (maximum 16 tests) covers shared/opaque IDs, duplicate
and malformed input, sorted selection, fabric parity, construction sensitivity,
grant/decline/unknown choices including all-excluded, exact repeated bytes,
different seed, 730-day UTC boundaries, sharding, actual estimates, portable
load idempotency and unsafe destinations. Existing sensor historical byte tests
must remain; update source fingerprint expectation to include new dependencies.
No test data from private stock. Strictly typed helper/tests; narrowly allow
calls to the already untyped migrated writer, not blanket new-file ignores.
Group identifier bounds/DDL and omitted/oversized subset cases within the same
16-test limit. Existing temporary-directory patterns are authorized for fictional
test data; the critique worker's claimed parent /tmp ban is not applicable.

<!-- phase: P02 -->
## P02: Evidence and delivery

<!-- task: P02-T01 -->
### P02-T01: Documentation and validation

Explain mode choice and synthetic schema in core README and existing synthetic
synthesis. Index and append-only log identify bounded evidence and open child
criteria. Install missing projects/dev tools using pip into session-local venv.
Run all five project suites, lint/format/types. Run actual local App on ephemeral
loopback through existing test_release_record_local_http, verifying denied calls,
released scripted AI proposal and unchanged domain state. Exercise CLI at 730
days on fictional homes and idempotent SQLite loader. Attempt Docker and record
actual failure if denied; no deployment or billable model calls. Record every
command/result including missing-tool probes, not only successful checks.

<!-- task: P02-T02 -->
### P02-T02: Review and publish

Perform one post-implementation RPI review against plan/evidence; route material
findings as open later work, never report conformance with material open findings.
Commit all phase artifacts and state plus intended code/docs, configure verified
GitHub noreply author/committer email, Conventional Commit and required trailer.
Push only feat/src-sensor-backfill-177 and open PR to main with Refs #177, command
evidence and unticked issue/child criteria. CI pending is not passing. Do not
merge or start unselected follow-ups.

## Completion Evidence

P01 and P02 complete for the bounded slice. Implementation commit 00c0137 and
main-targeted PR #320 contain the source, tests, docs and full phase artifacts.
Review execution Complete / outcome Residual work; parent issue and child
criteria remain open as recorded. The changes record contains every validation
command/result and the two-year hourly experiment. CI was initially running;
Docker/local live-platform evidence is not invented.
