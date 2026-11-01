# Research: #175 external source licence, retrieval date and attribution

* Task: issue-175-source-provenance (Research disposition: executed; Planning Readiness: Ready)
* Existing evidence: the 2026-10-16 acceptance audit in `docs/reference/research/retrofit-synthetic-data/data-dictionary.md` shows three of four criteria met; only "each external source records licence, retrieval date and attribution" is unmet.
* Register: `provenance-register.json` has SRC-CENSUS-TS054, SRC-IMD-2025 and SRC-ONS-BOUNDARIES with `retrieval_date: null` and provisional licence and attribution wording. SRC-OSM and SRC-OWNER-MODEL are complete.
* Retrieval date evidence: the private README and git history (`Add 60K homes` commit, 2026-10-01) give no download date for these three. Git commit date is an upper bound, not a retrieval date, so no date is invented.
* Licence evidence retrieved 2026-11-01:
  * gov.uk IMD 2025 page footer states Open Government Licence v3.0; published 2025-10-30 (matches README).
  * ONS terms and conditions page states Open Government Licence v3.0 for ONS statistics (covers Census 2021 and ONS boundaries). The Nomis disclaimer page could not be machine-read, so Nomis hosting terms stay noted as unchecked.
* Conclusion: licence and attribution can be confirmed now; retrieval date for the three sources stays an owner open item. Criterion 2 remains unmet, so the PR must use `Refs`.
