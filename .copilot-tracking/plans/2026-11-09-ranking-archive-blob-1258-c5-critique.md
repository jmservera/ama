# Issue 1258 Blob listing validation plan critique, cycle c5 (2026-11-09)

Refs #1258. One critique of the final-candidate c5 plan (`.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-c5-plan.md`) by an independent read-only subagent (rubber-duck), executed once. No Blocking finding; two Significant findings. Dispositions below are applied directly; none needs an owner decision, none conflicts with a confirmed decision, and the critique is not repeated.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC5-1 | Significant | A nonblank-text check accepts `<Name>ranking-x.json<Other/></Name>`, treating a malformed name as valid | Accepted. `Name` must have no child elements. Regression added (text plus nested element) in core `VerifyTests`. |
| PC5-2 | Significant | The parser can raise `LookupError` or `ValueError` for unsupported encoding declarations, escaping the fixed text | Accepted. Parser failures (`ET.ParseError`, `LookupError`, `ValueError`) map to the fixed `BlobArchiveError`. Regression added with an unsupported encoding declaration. |

Applied to the plan details: the `Name` rule is "exactly one direct `Name` child, no child elements, non-blank text", and the parse guard covers the three exception types.
