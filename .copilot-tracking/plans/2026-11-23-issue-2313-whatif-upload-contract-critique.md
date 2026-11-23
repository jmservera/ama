# Critique (single pass): verdict accept

* Risk: duplicates `workflow_errors` in test_pipeline. Mitigation: that helper does not assert upload or id-token scoping; the new test is narrow.
* Risk: brittle on step names. Mitigation: match on `uses` prefix and `with.path`.
