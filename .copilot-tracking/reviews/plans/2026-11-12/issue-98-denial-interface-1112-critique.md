<!-- markdownlint-disable-file -->
# Plan critique: issue-98-denial-interface-1112

Executed once by an independent rubber-duck agent. Verdict: needs change (compatible). Gap real; no invented authority or scope creep.

* Existing test `test_saved_export_goes_stale_only_for_dependent_fields` conflicts: dependent `area` also changes. Disposition: applied; expectation deliberately updated to name `area`.
* Malformed issue validation underspecified. Disposition: applied; `_issues_by_field` validates list and string `field_id`; tests with recomputed digests.
* Non-blocking: tests for removal, alteration, dependents; accurate reason text. Disposition: applied.
