# Details: issue #232 choice queue projection

* Files: src/core/src/zava_forward/core/store.py, projection.py; src/api/src/zava_forward/api/server.py, web/role-screens.js; tests in core and api; checks/role_screens_browser_check.py.
* Response: `{items:[{id,address,town,measure_decisions,resident_update}], total, limit, offset}`; limit 1-100 (default 50), offset >= 0.
* Boundaries: read-only GET, no resident contact, human approval and consent unchanged, manual path is the per-home screen and case workspace.
