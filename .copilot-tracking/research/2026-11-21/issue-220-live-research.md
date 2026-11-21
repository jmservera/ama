# Issue 220 live research (2026-11-21)

Refs #220. Synthetic desktop demo. Only criterion 5 is unticked ("No retaliation, inferred refusal or delayed hazard response").

Research disposition: executed.

## Evidence

* Demo API `ca-cutover-test-demo-api` revision 0000040 (created 2026-11-21T12:51Z), image digest `sha256:2efbf683...ecea4b4` = main 78ecac16af per the knowledge-base log. It contains the earlier `_same_signed_in_person` fix (e91b6fa81c).
* Live re-run of the r4 probe (`.copilot-tracking/evidence/2026-11-21/issue-220-live-r8/run1.out.txt`): the staff-recorded `nomination_record` write is still refused 403 "Reload your current staff identity before recording this step.", with `hazard_concern` true and false. Forbidden fields (`retaliation_flag`, `refusal`, `hazard_pause`, `priority_penalty`) give 400; protected-state hashes unchanged; hazard hold unchanged.
* Diagnosis (`diag.py`, values hashed): the signed-in principal has code, email, oid and tid; the roster row for the same email carries the same derived code and email. `/api/me` shows rows without an oid.
* Offline reproduction: a roster row whose code and email are the derived Entra values but which stores no oid is not matched by `identity.matches`, so `bind` returns the unbound derived principal. `_same_signed_in_person` then compares `oid` (actor has one, roster row has none) and refuses. Reproduced on JSON Store: PermissionError with the same message.

## Finding

Real defect. `resident_decisions._same_signed_in_person` requires oid equality even when the roster row records none, so a staff member whose roster row is keyed by the derived code and email can never record a route step. The check should require code and email to match and oid to match only when the roster row records one. `identity.verified` already ties code and email to the verified tenant and object id, so this does not admit another person.

## Planning readiness

Ready. Tier FULL (src change). No Azure change; a live write proof needs a redeploy that is not authorised, so live stays unproven after the fix.
