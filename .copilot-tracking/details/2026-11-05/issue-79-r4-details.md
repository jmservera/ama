---
title: Issue 79 plan details, slice 4
ms.date: 2026-11-05
---

## Phase 1: runner

* `run(operation, archive_dir, today, *, cases, as_of, policy_version, exercise, registry, free_bytes)` returns a dict and never raises for expected failures. Fields: `operation`, `status`, `today`, `window` (start today, end next day), `run_key`, `policy` (version, hash, owner, status, signed, sign-off problems), `schedule` (proposed, not approved), `refusals` (code, message, next action) and `retention_note`.
* `status` values: `ok`, `problem`, `due`, `current`, `blocked`, `published`, `already_published`, `exercise`, `refused`.
* Refusal codes: `unknown_operation`, `bad_date`, `policy_unknown`, `approval_missing`, `archive_unverified`, `source_missing`, `source_invalid`, `capacity_missing`, `publish_failed`.
* Approval gate: `ranking.signoff_problems(policy)` must be empty unless `exercise`. The registry entry must exist with a matching content hash.
* Run key: first 16 hex characters of SHA-256 over policy hash, as_of and window start. No random seed is consumed because ranking is pure.
* Capacity: free bytes at the nearest existing ancestor of the archive, writable, at least the exact record size.
* CLI: `schedule|publish|verify --archive --today [--cases --as-of --policy --exercise]`; exit 0 ok, 1 problem, 2 refused; JSON on stdout. No defaults for archive, date or data.

## Phase 2: tests

* `src/core/tests/test_ranking_publication_runner.py`: 17 tests covering idempotence, case-order independence, draft refusal with the shipped policy unchanged, missing sign-off record, exercise, source, future-dated and stale source, and capacity failures, damaged archive, bad inputs, schedule windows, verify staleness, CLI exit codes, persisted Store round trip and a static no-clock/no-environment/no-delete check.
* `src/core/pyproject.toml`: add the two modules to the existing mypy `disallow_untyped_calls = false` override group (they call untyped `ranking` and `store`).

## Phase 3: documentation

* `src/core/README.md` runner paragraph; `docs/reference/log.md` entry dated 2026-11-05. No index change: no knowledge-base file was added or moved.
