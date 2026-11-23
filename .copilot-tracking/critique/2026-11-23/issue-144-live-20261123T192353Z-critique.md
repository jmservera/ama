# Critique: issue 144 plan (single pass)

Verdict: proceed.

* Risk: a text-regex test over Bicep is brittle. Mitigation: reuse the existing RESOURCE split approach in test_container_hosting_completeness.py and assert on `image:` and `command:` lines only.
* Risk: workload names differ between Bicep symbols and pipeline keys. Mitigation: explicit symbol-to-key table in the test; the test also fails if a new workload symbol in containerapps.bicep is not in the table.
* Does not prove the pipeline ran or tags exist; stated as unproven in the changes record.
* No src change, so focused tier. No conflict with confirmed decisions.
