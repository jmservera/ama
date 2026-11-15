# Research: leaseholder consultation check (#92)

* Task: leaseholder-consultation-check-92; stacked on feat/demo-233-same-home-tensions-0825.
* Disposition: executed. Planning Readiness: Ready.

## Findings

* `src/core/.../procurement.py` already had `CONSULTATION_STATUSES`, per-package `consultation_status` (forced `unknown`), `consultation_history`, `contract_event_gate` and `request_contract_event` (always blocked, audited).
* Gaps against #92: no `leaseholder_consultation_status` field on the contract record or list output; the gate gave one generic reason; the procurement screen (`role-screens.js`) tested the forced `consultation_status`, so "applies" and "unknown" were not distinguished and blocking was not stated.
* Existing tests and design decision: supplied records never clear the hold because Legal authority is unverified. This is retained, so `complete` and `not_applicable` stay held pending Legal verification (flagged as follow-up).
