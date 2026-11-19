# Issue 129 live changes (2026-11-18)

Tier: FOCUSED (docs and evidence only; no src change; rpi-checks --all not run).

## Files
* docs/reference/research/issue-129-live-learning-test-evidence-2026-11-18.md (new note)
* docs/reference/research/issue-129-live-learning-test-evidence-2026-11-18/ (raw unittest output and exit codes)
* docs/reference/README.md index entry; docs/reference/log.md entry

## Validation
* src/core `unittest -v tests.test_learning_test_bundles`: 26 tests OK, exit 0
* src/api `unittest -v tests.test_learning_test_bundle_scenarios`: 6 tests OK, exit 0

## Per-criterion table
| Criterion | Result | Basis |
| --- | --- | --- |
| Five bundles specified with non-AI comparators | Proven for the protocol and helper (constructed, not measured: constructed cases, not experiments) | 32 passing tests |
| O10 and O18 to O20 out of scope | Proven in code (rejected by helper; test_five_bundles_exclude_out_of_scope) | core raw output |
| Atlas owner confirms bundle to opportunity mapping | Unproven | Human decision by the atlas owner; no owner confirmation exists and the O16 overlap question is open |
