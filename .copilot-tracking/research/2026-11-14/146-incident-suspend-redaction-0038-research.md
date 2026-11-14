---
title: Issue 146 incident suspension and diagnostic redaction research
date: 2026-11-14
task_slug: 146-incident-suspend-redaction-0038
---

## Scope

Remaining offline engineering slice of #146 (criteria 5 and 6): a seeded critical-harm or
approved-threshold breach creates an owned incident, suspends only the affected AI task, keeps manual
work running and never re-enables silently; diagnostic logs carry no raw prompts, responses or PII.
Prior surfaces: PR #1579 and PR #1590 (not re-edited here).

## Evidence

* `core/monitoring_coverage.py`: `reconcile_events` (idempotent window count), `evaluate_indicator`
  (BREACH sets `incident_required`, names owner or reports `breach without owner`).
* `core/continuity.py`: `suspend` requires a named `incident_owner`, scopes to one registered task or
  `all`, records affected proposals; `restart_propose`/`restart_decide` need independent persons, a
  trusted OID-bound `ai_restart` capability and a matching authority reference (OD-35 unappointed).
* `api/tests/test_operator_suspension.py` drills cover suspension, manual fallback and restart denial but
  not the chain from a seeded event stream and breach verdict into the incident record.
* `core/diagnostic_logging.py` patches `Logger.makeRecord`; it dropped `extra`, `exc_info` and non-token
  args but its message-text patterns covered only email, JWT, bearer and IPv4. Probing showed these leaked
  in formatted messages: SAS `sig=`, `api-key:`, `sk-` keys, Basic auth, UK postcodes, UK phone numbers, NI
  numbers, `resident_ref=`/`uprn:` pairs, `Name(...)` exception reprs and `Error: text` lines; and
  redaction of an `Authorization: Basic x` pair left the credential.
* `core/chat_privacy.py` already defines phone, postcode and NI patterns; reused shapes.
* `monitoring_coverage._SENSITIVE` duplicated the narrow pattern; now shared.
* Environment: `/home/azureuser/source/ama/.venv` does not exist; system `python3`, `ruff`, `mypy` with
  `PYTHONPATH` set to this worktree's `src/*/src` were used. `uv` not used.

## Disposition

Research executed. Planning Readiness: Ready. Gaps: (1) redaction patterns, (2) no end-to-end breach
to suspension to no-silent-restart test.
