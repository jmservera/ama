---
title: Issue 1360 served-transfer outcome diagnostic plan (read-only, no repair grant)
ms.date: 2026-11-10
task_id: 1360-outcome-diagnostic-1110
---

## Objective

Decide, by one bounded native counterexample investigation, whether the importer `transfer` generic `OSError`/`ValueError` message "Nothing was recorded" can be printed after the served SQLite store has already committed the refusal document and audit. The deliverable is evidence and a handoff. It is not a product fix.

## Authority and boundaries

* Read-only product diagnostic. No product, test, configuration or documentation implementation. No repair grant. The numbered issue 1360 does not reset the spent 135 C5 allowance (zero left). Finite allowance history beyond that is UNKNOWN.
* All diagnostic scripts, synthetic fixtures and live SQLite databases live only under the owned external evidence folder or the owned temp env `/tmp/zf-1360-1110`. The worktree receives only new original RPI records.
* No default or private `ZF_DATA`, no Azure, model, network (except the one pip install into the own env, already done), provider, container, deploy or spend. No push, PR, GitHub or board action, rebase or nested agent.
* The word "reproduced" is used only for an actual durable counterexample observed in the real CLI process and confirmed by an independent reopen.

## Approaches (maximum two, failed attempts preserved)

* Approach 1: the CLI is run as a real subprocess through a diagnostic driver that wraps `SqlStore.save` and `SqlStore._sync` in process, then runs the actual `zava_forward.importer` `__main__` with `transfer`. Before the transfer's save, a second independent `SqlStore` connection commits a real save of an unrelated document (`form_schemas`), changing `meta seq` without touching `import_exceptions` (no optimistic conflict). After the transfer's real `COMMIT`, the wrapped `_sync` (called from `save` only) first confirms through a separate read-only SQLite connection that the new refusal document, audit entry and sequence are already durable, writes that proof, and only then raises `OSError`. A second run raises `ValueError` at the same point if cheap.
* Approach 2, only if Approach 1 cannot create an independent non-conflicting sequence change because the independent writer is rejected: use a real seed-merge as the independent writer, with the same injection. If the failure is any other reason (hook not reached, commit not proven), stop with the exact unreproduced hypothesis and do not invent a third approach.

## Phases

1. Research: static source paths, existing adjacent tests, baseline focused Importer tests (done before plan).
2. Plan, details, critique (this file, details, one self-critique with direct dispositions).
3. Implement (diagnostic only): changes record created and referenced in state before implement-start. Build the driver and the owned fixture, run approach 1, capture raw exits and stderr, independent reopen, idempotent retry, ledger and refused-file hash comparison, control runs, cleanup of owned temp paths, then re-run the focused baseline unchanged.
4. Review: one self-review of diagnostic conformance (not a product approval).
5. Handoff and commit of new original RPI records only after a source-equality proof against the base.

## Success criteria

* The injected failure is shown to occur only inside `_sync` called from `save` after `COMMIT`, with the independent read proving commit first.
* Real CLI exit code and stderr captured from the subprocess.
* Independent clean reopen shows the retained refusal document, retained `recorded_import_refusals` audit entry and the unrelated independent writer commit.
* Repeat transfer exit 0, `added=0 already_present=1`, no second audit entry or second creation.
* Original ledger database and refused source file hashes equal before and after.
* Controls keep the known branches distinct: conflict rollback, `CommittedReloadError`, partial, driver error, pre-commit `ValueError`, store-open failure (existing test file, run unchanged).
* Source tree equals the pinned base apart from new RPI records (`git diff` against base empty for `src/`, `docs/`, `tools/`, `.github/`).

## Stop conditions

* A witness refusal: stop, preserve it, no blind retry.
* An unreachable hook after the two approaches: record the exact unreproduced hypothesis.
* Any need to touch product, test, config or documentation files, default data, or the network: stop and record a blocker.

## Follow-up routing (not authorised here)

If reproduced, a source fix needs a dated finite correction grant or reconciliation by the owner. The smallest proposed patch (CLI-only conservative wording for the generic branch, plus a real-save regression test) goes in the handoff as a proposal only.
