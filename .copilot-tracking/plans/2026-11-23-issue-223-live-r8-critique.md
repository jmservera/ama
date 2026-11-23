# Critique issue-223-live-r8 (2026-11-23)

Executed once. Verdict: proceed.
* Risk: changing the shape of `review_evidence` could break projection or forged-evidence checks. Mitigation: field is additive; `_retained_evidence_ok` ignores unknown keys; run src/api test_ai_tasks and src/core 223 tests.
* Risk: clock skew gives negative values. Mitigation: clamp to >= 0; omit (None) when `created` is unparseable.
* Scope: src/core change takes tier FULL checks (targeted tests, mypy, ruff); no rpi-checks --all.
