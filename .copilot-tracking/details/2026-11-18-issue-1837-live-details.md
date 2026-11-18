# Issue 1837 live details

* Phase 1: `src/api/tests/test_nomination_api_routes.py`. Decision: do not add urlencoded parsing server side (would bypass the trusted-proxy CSRF header path); keep the JSON bridge.
* Phase 2: new check reuses the test fixture; axe 4.10.3 SHA verified; target-size recorded, not asserted.
* Phase 3: `docs/reference/research/issue-1837-live-demo-evidence-2026-11-18.md`. Live probes write nothing.
* Tier: FULL classification (src/api/checks file and write-handler tests); full gate not run by instruction.
