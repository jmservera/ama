# Issue 2310 details, live run 2

Phase 1: extend `ProxyHttpTests` using the existing in-process server. Assert 401 and absent Location for each method and Accept combination; assert `/sign-in` 302 to the Entra login URL. No server change because the code already satisfies the criteria; the test is a regression pin for wider cases.
Phase 2: `python3 -m unittest tests.test_auth` with the documented PYTHONPATH.
Phase 3: changes record and research note.
