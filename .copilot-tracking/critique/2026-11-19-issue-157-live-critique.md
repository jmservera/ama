# Critique: issue 157 live plan (2026-11-19)

Executed once on the final candidate plan, by the worker (self-critique; independent review remains with the coordinator).

Verdict: proceed.

* Scope fits: one failing gate violation (README row naming `prototype/` without `v0.21.0`), covered by an existing repository-clean test. No src change.
* Rejected alternative: removing unreachable `ChatIsolation.turn` (draft D3). It edits security-adjacent src, which needs the FULL tier; this task forbids `rpi-checks.py --all`. Routed as follow-up.
* Rejected alternative: filing triage drafts as GitHub issues or ticking boxes. Owner approval and externally visible writes are outside the brief.
* Risk: the fix does not make #157 criteria provable; the table must say so.
