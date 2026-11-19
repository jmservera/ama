---
title: Issue 107 old-image SQL probe correction details
description: Phase details for the finding-by-finding correction
ms.date: 2026-11-17
---

## Fixed protocol (finding 2)

* Steps and actions in order: provision (invoke the five GOOD/REVOKED/MISMATCHED cases, execute index 0), restart_after_revocation (execute the revoked task, reinvoke REVOKED/ZF-1), restart_after_mismatch (execute the mismatched task, reinvoke MISMATCHED/ZF-1), restart_remaining_allowance (execute good2), restart_larger_allowance (execute good3).
* Per step: status ok, integer return code 0, action matches, identity modules equal the packaged set with absolute path and 64-hex hash, `missing` empty, the exact `executed` list with the requested id, `before` pending, boolean `result`, string `after`, no error; exact `reinvoked` list.
* Provision: five distinct non-empty task ids in the requested capability and case order, all pending.
* Missing or malformed evidence is INSUFFICIENT.

## Precedence (finding 4)

Adverse conditions are evaluated first from whatever trustworthy partial observations exist (provider counter, execute result, readback of the host trigger, snapshot state). They give VIOLATED even if another step errored. Completeness problems are kept alongside.

## Pool (finding 6)

One row of four non-negative integers: calls, tokens, used_calls, reserved_tokens. Against `after_remaining`: ceilings may not rise, consumed columns may not fall; a second pool row is a violation.

## Docker lifecycle (findings 1, 5)

* Network `ama-107-net-<run>`: `--internal`, bridge driver, owner and run labels. SQL: default bridge with `127.0.0.1::1433` publish, then `network connect --alias` to the private network. Workers: `--network <private>` only, argv unchanged otherwise (non-root, read-only, caps dropped, no-new-privileges, memory/cpu/pids, one read-only probe mount, `-e KEY` allowlist), SQL at `<alias>:1433`.
* Every expected name is registered before create. An ambiguous create is reconciled with `ps -a`/`network ls` filtered by exact name and both labels, then confirmed by `inspect` (full id, name, labels). No prune, no wildcard.
* Cleanup removes workers, SQL, then the network, up to three removal attempts each, re-listing by exact name and labels to verify absence. The report lists expected, removed, remaining and errors. Remaining or errored resources make an otherwise ACCEPTED run INSUFFICIENT (exit 3); a behavioural VIOLATED is kept with the containment errors.

## Deadlines (finding 7)

`Deadline(total)` caps the whole diagnostic. Every host SQL call (login, query, readiness) runs on a daemon thread with `min(per-call, remaining)`; on expiry the call is abandoned and recorded, later host calls fail at once, the scenario stops with partial observations, cleanup and report run, then `os._exit`. Docker CLI calls use a capped-output runner (tail kept, limit 64 KiB) with timeouts bounded by the remaining deadline during the run and fixed timeouts during cleanup. Limit: a driver call blocked in native code cannot be killed; its owning SQL container is removed instead.

## Output path (finding 8)

Resolve the parent with symlinks (it must exist), refuse `.`/`..`/empty leaves and any path under the resolved checkout, create the leaf with a non-recursive exclusive `mkdir(0o700)`, re-resolve and confirm it is the same canonical location and still outside the checkout, and use and report that canonical path.

## Honest observation limits (finding 3)

Sampled `@@SPID` values are reported only. Fresh process proof is the distinct container id plus hostname equal to the short id; host-versus-worker separation rests on the host connection being created in the supervising process outside any worker.
