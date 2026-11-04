<!-- markdownlint-disable-file -->
# Review: issue-96-r2-export-freshness

Executed once by the implementing agent (not independent; independent exact-head review and hosted CI remain required). Outcome: conformant for the slice.

* Read-only: no store writes; no reviewed, submitted or eligible claim.
* Behavioural tests prove dependent-only staleness, invalid copies and schema staleness.
* Focused tier only; no security, infrastructure, SQL or deployment change.
* Criteria 1, 5 and 6 remain unmet (see research). No box ticked; PR uses Refs #96.
