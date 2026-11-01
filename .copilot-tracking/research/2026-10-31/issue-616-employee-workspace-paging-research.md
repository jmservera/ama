# Research: issue 616 capacity and work orders paging

Disposition: executed. Planning Readiness: Ready.

* Cause: `capacityView` in `src/api/src/zava_forward/api/web/ops.js` fetched `/api/packages` and `/api/workorders` unbounded and rendered a full form set per package and per order. `Store.list_work_orders` projected every order and `list_packages` rechecked evidence for every package.
* Callers of the list shape: role matrix, endpoint inventory, procurement tests and a Node mock in `test_case_journey.py`. The unpaged list must stay unchanged.
* Option chosen: opt-in `limit` (1-100) and `offset` query values returning `{items,total,offset,limit}`; visibility filtered before slicing; only the slice is projected.
* Not available here: the 60,000-home dataset is private and was not read; the live test-user check is left to CI and the owner.
