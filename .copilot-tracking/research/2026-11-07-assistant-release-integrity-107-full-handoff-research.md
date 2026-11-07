# Research: FULL handoff preparation (#107, prospective)

Parent task `assistant-release-integrity-107`. Planning only; no alignment, test, source, gate, push or PR in this step. Research disposition: executed (git and gh reads).

## Provenance 2026-11-07

* Frozen head 21557a735ce4591857f9b5e15c0efee07b041091, tree 3d966d414424be268e7cd0ba511c65c993be1668, ignored-inclusive clean, branch `fix/assistant-release-integrity-107`, target main.
* origin/main a7f166c74608fe025d047a79448d5d2234622287 (#1247, docs only). Merge base 0f420dc95; main is one commit ahead. #1248 is not resolvable as a PR or issue here (not yet delivered); its publication/main window is unknown, so main may move again.
* Candidate delta: one test in `src/api/tests/test_assistant_release.py`, no production change; the test is SQLite, not SQL Server evidence. 58 prior skips were all disposable SQL Server.

## Owner priority

Demonstrable five-assistant AI ahead of deterministic-only work. This candidate does not deliver that feature; it only protects release/revocation integrity. Not proven by fixtures: actual serving attestation, model effectiveness, employee sign-in, deployment, human approval, real AI call, or any whole #107 criterion.

## Planning Readiness

Ready for planning; integration is deferred until a fresh main is admitted.
