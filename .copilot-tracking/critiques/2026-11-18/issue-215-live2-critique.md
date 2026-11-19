# Critique (one pass, 2026-11-18)
* Risk: removing sticky tools could push Send out of the panel on short windows. Mitigation: panel is overflow:auto for resizable, and the test asserts tools stay inside the panel at 700px height. Accepted.
* Risk: tests that assert the old CSS strings. Mitigation: run existing web UI tests. Accepted.
* Verdict: proceed; no conflict with owner decisions. Scope is CSS plus one test, no SQL/security/infra.
