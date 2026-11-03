# Details: issue 230 programme queue paging

* Page size 50 (`programmePageSize`); controls render only when total exceeds the first page.
* Status line (`role="status"`) shows "cases N to M of T", that the filter applies to this page only and that this is not a portfolio total.
* Failure: rows unchanged, plain-language message with a next step (manual route: open a case from the case list).
* Native buttons with visible text; Fluent 2 `btn alt` class already in the design-system inventory; no new CSS or inline style.
