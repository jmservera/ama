<!-- markdownlint-disable-file -->
# Concrete Correction ONE: progress-event-capture-102

Date 2026-10-17. Session42f9a956-d770-4f0e-86d7-582be8452547.
Input: the single original Review, Complete/Defects found, RV-001 and RV-002.
No second Review, repeated critique or coordinator acceptance.

## Implementation and Finding Disposition

RV-001: progress.history validates the complete as-of handoff lifecycle before
retaining numeric waits. An invalid later state now nulls already-produced
waits with status Unknown. Earlier as-of before the contradiction retains its
known duration. No event reordering, past rewrite, new transition or backfill.

Actual JSON/SQLite/MSSQL domain test first offers, receives and accepts through
registered actors. A separate copied-history adversarial case then appends the
contradictory Received after Accepted. Versions stay1/2/3/4 and source unchanged.
At 10:03:20 the180-second wait remains measured; at10:05 it is Unknown.
Trusted/untrusted/unknown-audit reports and exact semantic CSV parity are checked.
The regression failed first with180.0 instead ofNone before production fix.

RV-002: the existing SQL post-COMMIT method now checks exact event count, prefix,
new append version, exact event type and identical history from second/restarted
connections, both before and after refused retry. Audit count/no false rejection
assertions retained. Ten actual operations: advance, return into pause, supported
return out of pause to earlier Contacting resident, reopen, offer, receive,
accept, quality submit, quality accept and quality handover. This tests available
domain behavior, not a fabricated generic resume or completion method.

## Fresh Local Runtime Evidence

Failing-first command:

```bash
PYTHONPATH=src/core/tests .venv/bin/python -m unittest \
  test_progress_event_capture.JsonCapture.test_later_contradictory_handoff_invalidates_wait_only_when_observed -q
```

One run, one failure:180.0 is notNone. After the coherent correction batch, JSON
and SQLite capture classes passed26 tests. Broader final selector:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_progress_event_capture \
  test_progress_reports test_handoff_lifecycle test_hazard_referral \
  test_change_provenance test_quality_procurement test_resident_decisions \
  test_stock_reconciliation test_grant_lifecycle_controls \
  test_finance_match_controls test_finance_signoffs test_progress_report_api \
  test_workflows test_resident_api test_role_matrix test_procurement_api -q
```

457 run,394 pass,63 explicit existing opt-in/backend or JSON COMMIT-boundary
skips,119.677s. Initial invocation omitted src/api from PYTHONPATH:455 run with
one tests-package import error and63 skips, not a successful suite. Corrected
namespace invocation above reran the entire selection. No test weakened.
Injected failure logs and existing unavailable-law-store refusal are expected;
unittest exited0. This is not a full repository/core suite claim.

Configured Ruff check, Ruff format --check and mypy run from each of src/core
and src/api using ../../.venv/bin tools: all pass,116/55 source files typed.
One test file formatted using configured Ruff. No added dependency installation.

## Fresh Actual Loopback MSSQL Evidence

Restarted ONLY owned progress102-8f7a5abbc2. Its Docker-assigned loopback port
changed after restart; original readiness attempt on retained stale port was
interrupted without claiming success. The private session helper now discovers
the actual Docker port, without printing/committing credentials. Verified
SELECT1 through the actual driver, then ran:

```text
local-sql-102.py run test_progress_event_capture.MssqlCapture test_progress_report_api.MssqlProgressApi -q
```

25 actual tests passed,42.228s. Unique fictional task databases retained.
Exact event/audit once proved with second writer, post-COMMIT sync failure,
retry/restart, rollback and failed recovery. Own SQL container immediately
stopped after selector; inspected Exited afterward. No other container touched.
Session receipt files correction1-mssql.txt and correction1-targeted-rerun.txt
retain full output locally; no secret/config committed.

## Corrected Installed-Source Image Evidence

```bash
docker build -q -t progress-event-capture-102:correction1 -f src/api/Dockerfile src
.venv/bin/python src/check-container.py api progress-event-capture-102:correction1
```

Image sha256:4b333413196256096b79453af524e586712914052654e95f51fad36141c87076.
Existing checker passes enforced non-root controls, five negative probes and
hardened/plain compatible API startup with loopback health. Then same image,
UID/GID10001, read-only root, no capabilities, no-new-privileges, temporary state
and read-only test mounts ran JsonCapture, SqliteCapture, ProgressApi and
JsonProgressApi:48 run,47 pass,one JSON COMMIT-boundary skip,13.744s.
Installed six changed core module SHA256 hashes match host sources exactly.
No source-tree production import workaround, Azure, private data or live AI.

## Limits and Remaining Publication

Original adverse Review and complete finding set remain immutable in outcome;
these are concrete implementation receipts, not a second independent verdict.
History gaps/legacy precision, whole-home actuals, human/legal/resident controls,
JSON cross-file crash boundary and operational forecast prerequisites remain.
Actual quality.py overlap with #88 is declared for coordinator integration.
P03-T01 complete; P03-T02 authorized own-main integration and publication next.
