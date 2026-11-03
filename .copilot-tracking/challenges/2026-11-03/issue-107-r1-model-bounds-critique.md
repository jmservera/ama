<!-- markdownlint-disable-file -->
# Issue 107 R1 model bounds: critique (one pass)

Execution: executed once on the final plan. Verdict: proceed.

* Risk: putting the bound in `REGISTRY` changes `registry_hash` and proposal dedupe. Disposition: applied, separate constant.
* Risk: claiming the bound proves cost. Disposition: applied, README says code bound only; cost Unknown, no price.
* Risk: overclaiming #432 criterion 1 closure. Disposition: Refs only; issue stays open.
