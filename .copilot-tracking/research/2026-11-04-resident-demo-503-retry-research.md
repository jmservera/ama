# Research: resident demo 503 retry (#1054, slice 2)

* Merged PR #1067 delivered `Retry-After: 3` and busy wording in `resident_demo/app.py`; bulkhead of 8 kept. Its plan listed slice 2 (client retry) and slice 3 (re-measure burst).
* Client already shows `res.body.error` (busy wording) in the error panel, which has a "Try again" button (`index.html`, `demo.js` fail/start).
* Gap: no automatic retry; a transient shed still lands on the error panel.
* Disposition: executed (code read only). Planning Readiness: Ready.
* Unmet and out of reach here: decision on 8 (needs a live re-measured authenticated burst on `ca-resident-demo`), live verification.
