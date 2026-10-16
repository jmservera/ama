---
title: Issue 176 phase details
description: Implementation and validation boundaries
ms.date: 2026-10-16
---

## P01

P01-T01: stock_fabric.main reads each source exactly once, computes SHA-256
from those consumed bytes, decodes register with utf-8-sig and cases with
the existing utf-8 semantics. Add --as-of, validate using provenance.parse_as_of
before any writes, record nullable as_of and input_sha256 mapping with stable
logical keys register/cases, never paths. Keep stock-fabric-v1 algorithm,
summary(), fabric_rows() and output rows unchanged. Omitted as-of means unknown,
not today or an invented source date. Use io.StringIO(decoded, newline="")
to preserve quoted CRLF and BOM semantics; omit cases from input_sha256
when none was supplied, never invent a digest.

P01-T02: extend the existing repeated CLI-run test with explicit as-of and
digest assertions. Add at most two focused methods covering omitted/changed/
invalid date, changed seed, changed source bytes and nonempty refresh byte
preservation. Construct only fictional CSV/case files in TemporaryDirectory.
Pin known legacy row tests unchanged. No private dataset tests. Include BOM
and quoted CRLF compatibility, independently mutate register encoding and
JSON whitespace while asserting identical non-summary payloads and exact
independent digest changes. Inspect/spy on read-once input consumption.

## P02

P02-T01: use local pip-installed projects; absolute per-project PYTHONPATH.
Run core unittest modules test_stock_fabric, test_synthetic_determinism,
test_sensor_stock and test_generated_dataset, ruff and mypy on changed
production/test code. Run CLI twice on a wholly fictional register and compare
all bytes as a local app smoke, including nonempty-output refusal.
No Azure validation; this is offline tooling, not delivered cloud acceptance.

P02-T02: update src/core/README.md, the existing synthetic-data README,
docs/reference/README.md and append docs/reference/log.md. Include exact
AC1 partial/blocked boundary, AC2 current manifests versus historical outputs,
AC3 documented proposed policy versus unperformed owner approval. No source,
resident, safety or financial approvals invented.

P02-T03: one read-only implementation review; record findings
and explicitly disposition every finding before delivery. Unresolved in-scope
correctness/provenance/privacy/write defects block successful delivery; a
published blocked draft must say so. Unrelated findings and already documented
issue acceptance gaps may be deferred. Do not schedule a second independent
review or critique. Configure
authenticated privacy-safe local identity and commit trailer; push normal
topic branch and open main PR with Refs #176, evidence, validation and explicit
unmet acceptance criteria. Never edit issue body or merge PR.
