# Research: issue 175 OS attribution year decision (2026-11-03)

Disposition: reused. Planning Readiness: Ready.

* Merged PRs already delivered: #369 (audit), #238 (register and PII-free check), #648 (licences), #787 (retrieval dates), #846 (year recheck).
* Criteria 1, 3 and 4 are met by earlier work. Criterion 2 is blocked only by the OS copyright year in SRC-ONS-BOUNDARIES (placeholder "[year to confirm]", rejected by privacy.source_issues).
* Owner decision 2026-11-03: use 2026, marked "to confirm before external use". No official source names the year (#846 recheck), so this is a decision, not a verified fact.
* Smallest slice: record 2026 in the attribution, keep the caveat in a separate register field external_use_status (the audit only scans licence, attribution and url for "to confirm"), update the audit test, docs and log.
