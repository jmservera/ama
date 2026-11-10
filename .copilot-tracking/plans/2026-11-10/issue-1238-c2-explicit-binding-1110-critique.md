<!-- markdownlint-disable-file -->
# Critique: issue 1238 C2 explicit approval-role binding (1110)

Execution: one critique pass (rubber-duck), 2026-11-10T00:36Z, on the
prospective plan, details and research, before any test or source edit. Not
repeated for this task. Verdict: Revise. Original verdict preserved; the
dispositions below were applied directly to the details. No user decision
needed (Q6 is not re-asked).

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | A public digest does not prove an approval occurred; a store writer can copy it and forge an authorization | Accepted. A prior authorization counts only if the hash-chained audit holds the matching `resident_service_supersede_authorize` entry (same actor, case and detail). The digest is kept as binding provenance only. Test a forged row with the correct digest and no audit entry. The claim is narrowed: a writer who also forges audit breaks the chain, which this action does not re-verify per call |
| PC-002 | Blocking | Binding could change between the handler and SQL replay; replay validates a detached result and SQL persists the original | Accepted. The binding is captured once per operation in the validation context; replay refuses with PermissionError if the binding differs. Test on SQLite and MSSQL by swapping the binding inside replay |
| PC-003 | Blocking | Rotation A to B to A with no call between leaves A approvals valid again | Narrowed, not engineered. Restoring an earlier binding revalidates approvals that carried its digest. Documented as unsupported: rotation and restoration need a governed process; a restored policy needs a new `binding_id`. No claim of rotation support |
| PC-004 | Non-blocking | `bind` fixture name collides with an existing helper; independent-review test uses Pam | Accepted. Fixture is named `synthetic_binding`; each test binds explicitly |
