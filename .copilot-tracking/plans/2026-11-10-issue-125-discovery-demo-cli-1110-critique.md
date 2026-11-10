<!-- markdownlint-disable-file -->
# Critique: issue 125 fixed synthetic discovery-demo CLI plan

* Executed once (independent `rubber-duck` agent, read-only), 2026-11-10 (actual tool UTC observed after critique: 2026-11-10T03:04:50Z; no earlier time is claimed). Not repeated.
* Verdict: approve-with-changes. No blocking finding. Hand-derived hours (survey 36.5, design 60, install 12), references (SYN-EVT-001 to 006) and gap confirmed; no rounding issue; plain-dict digest stable.

## Findings and direct dispositions (compatible, applied; no user decision required)

| Severity | Finding | Disposition |
| --- | --- | --- |
| Significant | `authorise_tool("query_approved_analytical_store")` is allowed regardless of readiness, so company-connection DENY must be derived from the readiness report, not tool policy | Applied: `company_connection` is DENY computed from `status != READY_FOR_OWNER_DECISION` and `connection_to_company_data_permitted is False`; tests assert it; tool decisions are labelled policy decisions, never dispatched |
| Significant | Clean-environment subprocess does not detect env/home/data-path reads | Applied: add in-process tests patching `builtins.open`, `os.environ` access and `os.getenv` to fail during `run_demo`, plus a subprocess with a poisoned `ZF_DATA` and empty HOME asserting no files are created |
| Minor | Fallback expectation used an ellipsis | Applied: the full literal string with six references is the expected constant |
