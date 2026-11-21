# Issue 2203 critique (single pass)

Verdict: proceed with changes applied directly.

* Risk: removing the five-home table breaks `test_runbook_five_home_*`. Applied: relabel in place and keep the heading, headers and five rows.
* Risk: stating live results as facts that were only source-proven (checkbox, offline alert). Applied: every row carries an Observed or Not verified label with the date.
* Risk: leaking the tenant or user identifiers. Applied: no OID, tenant id or email in retained files; secret scan in validation.
* Risk: runbook ms.date and heading anchors referenced elsewhere. Applied: keep existing headings; add new sections only.
