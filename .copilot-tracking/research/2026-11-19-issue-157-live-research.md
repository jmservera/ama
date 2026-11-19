# Issue 157 live loop: research (2026-11-19)

Task: issue-157-live. Refs #157. Synthetic demo, desktop only; live Azure authorised (rg ama, cap USD 700).

## Unticked criteria (gh, 2026-11-19)

1. Complete the #440 stabilization checkpoint (first unmet).
2. If accepted, child features are accepted.

## Findings so far

* `python3 tools/check-legacy-references.py` fails at head with one violation: `docs/reference/README.md:1355` names retired `prototype/` without archive tag `v0.21.0`. The existing test `tools/test_check_legacy_references.py::test_repository_has_no_violations` covers it.
* Triage draft D2 of docs/reference/research/stabilization-checkpoint-triage-440-live-2026-11-18.md (allowlist) is otherwise resolved; the residual is this README row.
* D3 (unreachable ChatIsolation.turn) still has no non-test caller; it is a src security-adjacent change needing the FULL tier, so it is routed, not edited.

Planning Readiness: Ready. Research disposition: executed.
