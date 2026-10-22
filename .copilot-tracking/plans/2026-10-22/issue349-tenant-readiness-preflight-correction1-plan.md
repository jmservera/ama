# Plan: issue349 preflight correction 1

* [x] P01 Parse the issuer with urlsplit; require https, exact host, no userinfo, port, query or fragment, and path `/<uuid>/v2.0[/]`. Failure reports `mismatch` / `issuer-not-expected-authority`, never ready.
* [x] P02 Add a test covering attacker-host substring, http, userinfo, port, query, fragment, host suffix, extra path and extra prefix segments, plus the valid trailing-slash case.
* [x] P03 Focused tests, ruff, then one new full gate and official receipt verifier before push.

Critique: the independent coordinator review is the single critique of this change; no additional critique run. Disposition: finding accepted in full, no conflicts.
