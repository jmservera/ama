# Details: issue 2186

* validate_receipt: drop the `scope != "partial"` refusal; pass `inert_only=(receipt["scope"] == "full")` to base_relaxation.
* base_relaxation: when inert_only, any moved path not inert, or under src/ markdown, raises GateError; kind stays "disjoint-move" (or "gated-ancestor").
* Selection for a full receipt is mode "all" and does not depend on the base, so the existing selection and identity checks still apply; identity pins the recorded base.
* Residual risk (recorded): tests read docs/ (for example test_live_doc_links), so a docs move can break the merged result; hosted CI on the merged head covers it, same as the existing partial relaxation.
