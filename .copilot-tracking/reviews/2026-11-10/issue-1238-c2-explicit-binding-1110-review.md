<!-- markdownlint-disable-file -->
# Review: issue 1238 C2 explicit approval-role binding (1110)

Execution: one Review (code-review agent), 2026-11-10T00:46Z, after
implementation and validation, on the uncommitted diff plus the research, plan,
details and changes records. Not repeated for this task. Findings route to
later work. This file is the original outcome; it is not edited afterward.
The earlier review at
[2026-11-09 review](../2026-11-09/issue-1238-manual-verified-1109-review.md)
is preserved unchanged.

Outcome: Conformant. The reviewer traced the code and tests and did not re-run
them; the passes are from the changes record and the raw logs.

Verified by the reviewer: nothing in production code assigns or builds a
binding from staff, requests, rows, body or environment; the unconfigured
refusal is the first statement and writes nothing; stored approvals count only
under the current digest, for the bound person and with a matching audit entry;
SQL replay refuses a changed binding; the first four criteria and the existing
guards are untouched; README and changes claims do not overreach.

## Findings (routed to later work, none blocks conformance)

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| RV-1 | Low | Immutability is shallow: `_roles` is a plain dict, and `isinstance` accepts subclasses. Needs in-process access, which is the trusted composition boundary | Later: store roles in a read-only mapping, or check `type(binding) is SupersessionBinding` |
| RV-2 | Low | `_authorization_holds` reads the whole audit per stored approval; bounded to at most two approvals per call | Later: needs a filtered audit accessor in the shared store, out of scope here (reserved) |

Test gap noted: mutation of `_roles` is not tested (belongs with RV-1).
