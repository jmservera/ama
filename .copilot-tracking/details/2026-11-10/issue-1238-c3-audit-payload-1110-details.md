<!-- markdownlint-disable-file -->
# Details: issue 1238 C3 audit payload provenance (1110)

Prospective, written 2026-11-10T01:00Z. Plan:
[plan](../../plans/2026-11-10/issue-1238-c3-audit-payload-1110-plan.md).

## Design

* `_approval_digest(binding, case_id, req_id, reservation_id, number, role,
  evidence_ref)`: SHA-256 of canonical JSON (sorted keys) of case, request,
  reservation, attempt, role, bound identity (`binding.identity(role)`),
  binding id, binding digest and `sha256(evidence_ref)`.
* `_approval_detail(...)`: `"<req> formal-route attempt <n> supersession
  authorized by the <role> [approval <digest>]"`. The handler returns it for
  both the first and the completing authorization.
* `_authorization_holds` gains the attempt and the record's evidence reference:
  it recomputes the digest from the row's role, the current binding and the
  current `evidence_ref`, and requires an audit entry (actor, action, case)
  whose detail equals the recomputed detail exactly. The existing digest,
  identity checks stay. Legacy generic details cannot match.
* Evidence mismatch therefore withdraws the earlier approval; the next
  authorization restarts evidence from the new value.

## Tests (red first, in the inherited class: JSON, SQLite, MSSQL)

* Evidence substitution: genuine E1 approval, then only `evidence_ref` -> E2
  in the stored row, audit untouched; reviewer approves E2: attempt stays
  Pending, E1 approval withdrawn, audit raw text never contains the evidence.
* Binding restamp: genuine approval under binding A; trusted fixture switches
  to binding B (same bound people, new id); the row is restamped with B's
  digest; audit untouched; completing approval does not supersede.
* Legacy generic audit entry: a row stamped with the current digest whose only
  audit is the old generic detail does not count.
* Legitimate unchanged-reference quorum still supersedes (existing tests);
  audit detail contains a digest and not the evidence text.

Existing tests keep default-deny, SQL replay, receipt and no-send coverage.
