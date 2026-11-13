# Changes: integrate #146 and #79 audit commits

* Cherry-picked (-x) dd90536f as 8df9d6108 and 45e821cc as 378d0f997; no conflicts.
* Regenerated docs/architecture/cutover-reference-inventory.tsv (14 lines shifted by docs/reference/README.md additions); the cutover audit checker then passes (130 rows, 1913 locations).
* Verification: test_cutover_audit 9 OK; infra tests.test_bicep_policy 61 OK (no test_bicep_policy under src/orchestrator; it lives in infra/tests); git diff --check 0; broken relative links in added lines 0; secret scrub 0 hits.
* Tier: Focused (documentation-only plus generated inventory TSV).
