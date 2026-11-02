# Research: issue #175 source retrieval dates (2026-11-02)

* Research disposition: executed (targeted, local evidence only)
* Planning Readiness: Ready

## Evidence

* Owner decision (jmservera, #175 comment, 2026-11-02): retrieval date is the first commit date in this repository that references each source.
* `git log -S` for `TS054`, `c2021ts054`, `IMD 2025`, `Indices of Deprivation 2025`, `LSOA 2021`, `LAD December 2021`, `BFC` and `geoportal.statistics` all return 068fb08ce, 2026-10-01 as the earliest commit. Generic `LSOA` is earlier (f48fdc655, 2026-09-27) but is not a source-specific reference, so it is not used.
* Offline audit: `source_issues` in `src/core/src/zava_forward/core/synthetic/privacy.py` rejects non-ISO retrieval dates and any licence/attribution/url matching `expected|to confirm|wording to confirm`.
* Register state on main: licences and Census/IMD attributions already confirmed 2026-11-01 (no "expected, owner to confirm" wording remains). SRC-ONS-BOUNDARIES attribution still contains "[year to confirm]" for the OS copyright year.

## Finding

After recording the dates, the audit's only remaining finding is `SRC-ONS-BOUNDARIES:provisional_attribution`. The OS copyright year is not recorded by any local source and must not be invented. Issue #175 criterion 2 therefore stays unproven.

## Source files

* docs/reference/research/retrofit-synthetic-data/provenance-register.json
* src/core/tests/test_synthetic_provenance.py
