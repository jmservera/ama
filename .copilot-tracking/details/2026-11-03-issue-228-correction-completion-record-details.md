# Details: correction and completion record

* `workOrderRecordRows` in `src/api/src/zava_forward/api/web/role-screens.js`: per work order, corrections (reason, by, at), completion from `history` (by, at) or "Who recorded it is Unknown", and review fixed as Unknown.
* Manager panel "Corrections and completion on record"; contractor field "Completion on the work order".
* Tests: `WorkOrderRecord` and `test_completion_shown_as_record_not_acceptance` in `src/api/tests/test_procurement_screens.py`.
