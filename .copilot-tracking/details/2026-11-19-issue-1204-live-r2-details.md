# Details: issue 1204 r2

* Loader opens the database with `mode=ro`, never writes. Columns used: id, ready/running/dep_blocked/human_blocked/unknown counts, action_taken, evidence.
* Only the 216-row log has that schema; two other session logs use `classifications` JSON and are not mapped (unproven, recorded).
* Real rows carry no closure-batch, approval or global-stop fields, so only action/evidence, no-progress and recovery rules are exercised on real data.
