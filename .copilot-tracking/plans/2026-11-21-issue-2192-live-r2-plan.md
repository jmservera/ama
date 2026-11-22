---
title: Issue 2192 live plan (round 2)
date: 2026-11-21
---

Tier FULL (src change). Targeted tests only; the coordinator runs gates. No push, no PR.

## Phases

* [x] Research: live probe found the resident checkbox writes consent for `sensor_home_id` while the employee view reads home id = case id.
* [ ] Implement: the resident consent change also applies to the resident's case-id home when it has controls (unknown-home tolerated); card state still reads the resident's own sensor home.
* [ ] Tests: API test that the case-id home receives the same grant and withdraw calls, and that a missing case-id home does not fail the request.
* [ ] Validate: targeted API tests, ruff, mypy in `src/api`.
* [ ] Record: research note with per-criterion table, index, log, changes record.

## Critique (executed once)

* Verdict: accept with changes. Finding 1: applying to two homes is not one transaction; accepted because each call is atomic and audited, withdrawal is attempted on every home and fails the request if any attempt fails (fail closed shown as an error, state re-read). Finding 2: do not widen the SQL principal; confirmed, only the existing dedicated principal is used. Finding 3: avoid core changes; confirmed, change stays in `src/api/.../sensor_consent.py` and `app.py`.
* Live redeploy of the image to `ca-resident-demo` is out of the local commit scope but is needed for a live re-proof; it is recorded as unproven if the build or deploy is not completed.
