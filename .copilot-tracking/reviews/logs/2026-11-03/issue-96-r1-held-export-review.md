<!-- markdownlint-disable-file -->
# Review: issue-96-r1-held-export (executed once by the implementing agent; not independent)

* Outcome: conformant for the slice; no open findings.
* Checked: read-only, no writes, no authority claims, rights check reused, SQL and JSON parity, ASCII docs.
* Limitation: export is core only; no API or UI exposes it. Independent exact-head review, hosted CI and human approval remain required.
* Criteria: 1 unmet (no approved template); 2-4 already met; 5 unmet (no reviewed export exists; the held export only fixes the invariant); 6 partly met (#510, #888), rule/calculation/approval staleness unmet. Use Refs #96.
