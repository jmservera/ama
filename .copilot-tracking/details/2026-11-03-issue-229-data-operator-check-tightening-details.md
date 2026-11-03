# Details: issue #229 slice 3

* Phase 1: in `check_accessibility`, get the regions "Recorded returns and reopens" and "Source conflicts with both values and source details" by role and name; require Returned, Reopened, both return reasons there, and SYN-STOCK-A, SYN-STOCK-B, Unresolved in the conflict region. Remove the generic Returned and Reopened entries from the global list.
* Phase 2: raise AssertionError when ZF_AXE_JS is unset and ZF_AXE_REQUIRED is 1. README states PARTIAL exits 0 and the RESULT line is authoritative.
* Validation: `python -m checks.data_operator_browser_check` with ZF_AXE_JS (pinned SHA-256 verified), with ZF_AXE_REQUIRED=1 and no axe file; ruff check; mypy with --cache-dir=/tmp/mypy-229.
