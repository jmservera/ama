# Critique (single pass): issue 2245 live plan

Verdict: proceed with amendments applied directly.

* Overriding an open incident suspension under the demo switch would weaken a safety control and is rejected; the owner statement approves model calls, not lifting incident holds.
* Deleting SUS-1 from SQL is rejected (no-delete trigger, audit integrity, "no production changes").
* Expiry must fail closed: unset, naive or non-UTC `ZF_DEMO_EXPIRES_AT` keeps the 2026-11-01 default.
* No web file edit: hold wording goes through the existing `demo_disclaimer` field so the web UI tests are not triggered.
* Live roll of the resident image uses the existing registry push route and `az containerapp update` only; no Bicep.
