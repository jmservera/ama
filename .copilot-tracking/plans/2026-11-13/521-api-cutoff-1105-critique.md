# Independent critique: #521 plan (rubber-duck, one pass)

Verdict: approve with changes.

Findings and dispositions:

* Loopback sockets used by API tests: treated as local, not network/cloud; proceed (recorded decision).
* Offline install: apply `--no-build-isolation --no-index`, preflight setuptools; stop and record blocker if unavailable. Accepted.
* Source writes (egg-info, bytecode): set `PYTHONDONTWRITEBYTECODE=1`, check `git status --ignored` after, remove generated egg-info. Accepted.
* Boundary evidence: API test covers 2027-01-31T23:59:59Z allowed and exact AUTHORITY_END rejected, not 2027-12-31T23:59:59Z. Proof claim limited accordingly; no source edits. Accepted.
* Origins/evidence: verify all three distributions in the same env; retain a compact test log summary (test names and counts) in the changes file. Accepted.
