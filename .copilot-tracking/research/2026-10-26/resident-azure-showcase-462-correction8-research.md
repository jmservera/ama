# Research: hosted review on 5d9c62ff (#462), 2026-10-26
* Thread 4383091817: public grants outside the default set must be refused in every permission class; the previous predicate only covered classes 0, 1 and 3, so class 4 (database principals, IMPERSONATE) and others were missed. Note NULL-schema objects would escape a NOT IN, so ISNULL is needed.
* Review summary: app.py issued a fresh CSRF cookie on every /demo/session, so a second tab replaced the cookie and the first tab's header token no longer matched. The CSRF token is a stateless signed double-submit token, so reusing a valid held token is safe.
* Planning readiness: Ready.
