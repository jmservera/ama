<!-- markdownlint-disable-file -->
# Research: issue 1238 C3 audit payload provenance (1110)

Recorded 2026-11-10T01:00Z at frozen head `ecbe7fc1300c561b538778ccef2f8fcbc89ee034`
(tree `17bc2ea4ced31fc59d665e303ae4d67835d5302f`). Research disposition:
executed (native source reading plus the complete independent findings file
`functional-findings.json`, 1 High, read in full). Counter: C3 of 5, two remain.
C2 records and all earlier adverse outcomes are preserved unchanged.

## Finding being corrected

Independent 17da High: `_authorization_holds` accepts a stored approval when the
binding digest matches and any generic audit entry with the same actor, action,
case and detail text exists. The detail text names only request, attempt and
role. Two document-only attacks (no trusted setter, no forged audit):

1. After a genuine control-owner approval of evidence E1, a writer changes
   `supersession.evidence_ref` to E2; the reviewer approves E2; E1 still counts.
2. A writer restamps an old approval with the current public binding digest;
   the same generic audit entry still matches.

## Source facts

* The handler returns the audit detail; `resident_action` writes it with
  `self.audit(...)` in the same locked operation on JSON, SQLite and MSSQL, so
  the digest can ride in that existing detail with no store or schema change.
* The audit chain is hash-linked; changing a detail breaks it, so an approval
  payload digest inside the detail cannot be altered without breaking the chain.
* Everything needed (case, request, reservation, attempt, role, bound identity,
  binding id and digest, evidence reference) is available in the handler.
* Legacy entries (generic detail, no digest) will not match: fail closed.

## Fix scope

Add a canonical approval-payload digest (SHA-256 of canonical JSON over case,
request, reservation, attempt, role, bound identity, binding id, binding digest
and the SHA-256 of the evidence reference) appended to the audit detail; verify
the recomputed digest, from current row and current binding, when counting an
earlier approval. Raw evidence text is never logged. Nothing else changes.

Not widened: shallow private dict and subclass admission, whole-audit scan
performance, reserved shared store, server, schema. Whole F3 stays unmet; the
real binding and approvals are human gates.

Planning Readiness: Ready.
