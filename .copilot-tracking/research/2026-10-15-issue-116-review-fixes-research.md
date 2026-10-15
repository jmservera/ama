# Issue 116 review fixes: research

Scope: three review findings on the role endpoint inventory PR (#116).

* `ai_tasks.source_labels` emitted `Contact {d}: {outcome}` for every role; `store._facts` already gated on `reason_ok`.
* `assistants.capture` read appointment `outcome` unconditionally for works-resident-coordination.
* `projection.hold_notes` only walked contacts, appointments and hazards.
* Constraint: assistant source signatures are computed by workers without a user, so the need check must be role-independent per capability.

Planning readiness: Ready.
