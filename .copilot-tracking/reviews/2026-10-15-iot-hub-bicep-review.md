# Review: IoT Hub Bicep module (issue 140)

Execution: once. Outcome: conformant with open items.

* AC1 tier/region/units/cost/retention: recorded (proposed, pending owner approval; cost unverified).
* AC2 module with consumer group, routing fallback, diagnostics: met.
* AC3 least-privilege role, no keys: met (disableLocalAuth, receiver role).
* AC4 network: met (production private endpoint; public only in development).
* AC5 provisioning and credential owner: decided in README (individual enrolment; DPS deferred).
* AC6 build/lint/test and budget: met; what-if not run (open).
Follow-ups: live what-if, price confirmation, owner ADR 0003 approval, BRD OD-43.
