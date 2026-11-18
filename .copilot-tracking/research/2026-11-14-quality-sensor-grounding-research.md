# Research: retained sensor values and Quality AI flag grounding (Refs #1288)

Date: 2026-11-14. Disposition: executed. Planning Readiness: Ready.

* Stack: branch is stacked on `origin/feat/demo-164-chat-grounding-provenance-0900` (#1641). The issue paths `api/chat.py` and `api/views/` do not exist; the real surfaces are `core/chat_case_answers.py` (rules chat), `core/chat_isolation.py` (facts), `core/assistants.py` (`review_flag`), `core/sensor_view.py` (read model), `web/ops.js` (`sensorPanel`) and `web/assistants.js` (`reviewFlagBlock`); there is no `role-screens.js` sensor panel.
* Retained schema holds only `temperature_c` and `humidity_pct` (`sensor_view.COLUMNS`). `dew_point_c` and `mould_risk_index` are not retained and `sensor_view` forbids invented variables, so they are reported as not retained, never estimated.
* Gaps: the panel showed values but no `[sensor:...]` citation or origin; the flag listed only sensor/reading IDs; case chat had no sensor intent or sensor facts.
* Decision: panel/read-model text is `decision_rule`; the Quality finding is `generative_model` with deterministic cited values beside it. Chat uses the existing authorised `Assistants.sensors` view (role, consent and bounds already enforced) injected into `ChatIsolation`.
