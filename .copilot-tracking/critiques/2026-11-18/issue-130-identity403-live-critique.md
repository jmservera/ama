# Critique of the issue 130 identity 403 plan (2026-11-18)

One critique pass, final candidate plan, self-run (no confirmed decision conflicts).

* Risk: relaxing a security comparison. Disposition: accepted with limits. Compare email, code and oid (case-folded, all must match, including both empty), never display name or tenant metadata. Role is not compared; the principal's role is validated by `require_role` and previously could not match for Entra anyway. Flagged for human security review.
* Risk: tests prove only the positive path. Disposition: applied. Add a refusal test that patches `_person` to return a different roster person (the only way to reach the comparison, since `_actor` already refuses forged bindings) and a mutation probe showing the test fails without the check.
* Risk: SQL parity. Disposition: applied. The tests live in the base class so the SQLite subclass runs them.
* Verdict: proceed. FULL tier applies (src security control); the coordinator forbade `rpi-checks.py --all`, so the full gate is unrun and stated as such.
