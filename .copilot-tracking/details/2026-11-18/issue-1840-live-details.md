# Details: issue 1840 live

Date: 2026-11-18.

## Phase 1: confirm dependency

Run `ls src/api/checks`, `git cat-file -t 510fd90f`, `git fetch origin 510fd90f`, `git ls-remote` for the parent topic. Success: file present. Observed: absent.

## Phase 2: record blocker

Write the changes record with the per-criterion table. No source file is touched.

## Phase 3: review and commit

One review, then a local Conventional Commit with `Refs #1840`.

## Deferred design for the fix (not implemented)

In `completed()`, require for the requested task: a matching execution record and reinvoke record, boolean `result`, observed states present, and no errors; reuse the fixed-protocol checks; return `INSUFFICIENT` when any is missing unless separate trustworthy adverse evidence proves `VIOLATED`. Add failing-first tests removing `restart_after_mismatch.executed[0].result` and the reinvoke state from `tests.good()` while an active MUTATED row remains. Also reproduce the two untyped `config()` mypy calls at lines 1255 and 1417 in an isolated environment.
