# Issue 220 live critique (2026-11-21), executed once

Verdict: proceed with changes applied.

* Risk: tolerating an empty roster oid could admit another person. Mitigation: `identity.verified` binds code and email to the tenant and object id, and code and email must still equal the roster row. A different oid yields a different derived code and email, so it is still refused. A roster row that records an oid must still equal the actor oid.
* Risk: a roster row with a different non-empty oid. Kept refused (existing test of an impostor stays).
* Finding applied: `_owner_rights` compares the same three keys against the same oid-less roster row, so a named owner would be refused too. Use the same comparison there.
* Finding applied: the edit must not relax the all-empty case: an actor with no code or email stays refused.
* Out of scope: criterion 5 live success needs a redeploy (not authorised); retaliation over time is production-only.
