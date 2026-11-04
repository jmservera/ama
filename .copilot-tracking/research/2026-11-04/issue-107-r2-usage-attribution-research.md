<!-- markdownlint-disable-file -->
# Issue 107 R2 usage attribution: research

Research disposition: reused (the 2026-11-03 forecast research and PR 915 ranked this first). Planning Readiness: Ready.

## Delivered already (merged PRs, not redone)

* PR 287, 293, 301: base criteria 1 to 5 and RAI 2, 4, 6, 7, 9.
* PR 863: Tokenomics 1. PR 915: Tokenomics 3 (forecast).

## Unmet

* RAI 1 (approvers unset, OQ-017), 3 (serving attestation), 5 (independent Azure SQL race evidence), 8 (delivered-build evidence). These need human, Azure or legal steps.
* Tokenomics 2: usage per assistant and per accepted proposal.

## Findings

* `Consumption.report` aggregates the whole cohort only. Reserved events carry the opaque `capability`; completed events carry tokens; output and review events carry acceptance.
* Slice: a `by_capability` breakdown computed from those events. No schema change, no DDL, no new write, no case content. Not security, infrastructure, SQL or deployment tier.
