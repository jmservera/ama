# Research: issue 2202 final live proof (2026-11-22)

Disposition: executed (reuses prior probes from the deployproof run, adapted).

## Scope

* Deployed: API `ca-cutover-test-demo-api--0000053`, resident `ca-resident-demo--0000025` (main 7a125f470: #2245 meter fix, map retry, #2008 .xlsx preview).
* Unticked criteria of #2202: images rebuilt and rolled; revisions Running and Healthy with hardening enforced and rollback noted; owner demo checks (sensor charts, map gauges, consent checkbox, chat routing, half of homes); live receipt and log entry.
* Checks requested: employee chat 10 asks with times, map, xlsx check-a-spreadsheet with a sample synthetic file, resident chart, safety count, handoff waiting view, chat AI hold label.

## Evidence found

* Prior notes: issue-2202-deployproof-2026-11-22.md (revision 0051/0023), issue-2202-live-deploy-2026-11-22.md, issue-2191 coverage re-proof, issue-2192 consent proof.
* Sample file: docs/reference/research/demo-workbook/demo-case-list.xlsx (synthetic).
* Probes reusable: probe_staff.py, probe_resident.py, probe_ask_latency.py (2245), live_import_check.py (2008).

## Planning Readiness

Ready.
