<!-- markdownlint-disable-file -->

# Changes: climate-paired-alt-source-178-corr1

| Field | Value |
|---|---|
| Date | 2026-10-22 |
| Plan | .copilot-tracking/plans/2026-10-22/climate-paired-alt-source-178-corr1-plan.md |
| Corrected head parent | d314d7c6945a51909517394725577ccd19d5d1ac (base 9e55a392b95c90730c6410b9a4db4ad3a5ae70ce) |

* tools/climate_paired_bounds.py: monthly minimum and maximum now carry value, every tied UTC timestamp (chronological) and the paired value of the other variable.
* tools/test_climate_paired_bounds.py: replaced the bare-value monthly assertion; added split-month tie test and monthly versus annual reconciliation test (24 tests pass).
* docs/reference/research/climate-paired-bounds-178.json: regenerated from the same retained raw fixtures; only the monthly blocks changed shape; all other fields identical.
* Synthesis paragraph and log entry added. Earlier history, the first receipt (/tmp/ama-alt-source-1430-178, sha256 a19ee1a7...) and the original review record are preserved and now historical for head d314d7c6.
* P03 outstanding at time of writing: gate result and receipt are recorded in the PR description and final report, kept external.
