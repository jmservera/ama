# Details: issue #175 source retrieval dates (2026-11-02)

## Phase 1

* Edit the three source entries in provenance-register.json: `retrieval_date` 2026-10-01; `verification` states the owner decision, the first-commit basis and commit 068fb08ce. Keep the ONS OS copyright year as an explicit open item.

## Phase 2

* test_synthetic_provenance.py: the audit must report exactly `SRC-ONS-BOUNDARIES:provisional_attribution`, the dates must equal 2026-10-01 with the owner-decision basis recorded, and the CLI `--sources` must show no retrieval-date finding.
* Update retrofit-synthetic-data README.md and data-dictionary.md (two places) and src/core/README.md.

## Phase 3

* Append a dated entry to docs/reference/log.md; no index change (no file added or moved).
