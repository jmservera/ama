---
title: Issue 2187 live, heavy lock only for Docker, SQL and browser groups (2026-11-23)
description: Verifies the gate takes the heavy lock only for heavy groups, names what #2215 and #2286 merged, and records the per-criterion evidence
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Local gate-tool check; no `src/` change, no Azure access, no browser proof (a local tool has no UI), no `rpi-checks.py --all`. Tier: focused, documentation only.

## What merged

* Commit 46c328182a (2026-11-21, #2215) added `needs_heavy_lock(groups)` to `tools/rpi-checks.py`. It is true only for `browser`, `mssql`, `logo-0600` and any `image-*` group; `main` otherwise uses `contextlib.nullcontext()` in place of `heavy_lock`.
* #2286 (merged 2026-11-23T01:41:01Z, Refs #2186 #2188) changed receipt-inert paths and concurrent image builds. It did not alter the lock selection, so it is not the source of this behaviour.
* `tools/test_rpi_checks.py` holds `test_heavy_lock_only_for_docker_sql_or_browser_groups` (groups `static`, `project-*`, `tooling`, `infra` lock-free; `mssql`, `image-api`, `logo-0600`, `browser` locked) and `test_main_skips_lock_without_heavy_group_and_takes_it_with_one`.

## Evidence

From `tools/` at head 5c08bedd8f: `python3 -m unittest test_rpi_checks -q` printed `Ran 129 tests ... OK`. The remaining groups (`preflight`, `project-*`, `namespace`, `static`, `infra`, `migration`, `extra-*`) do not use Docker capacity in the Runner dispatch.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Lock only when a heavy group is selected | Proven | `needs_heavy_lock` plus the `nullcontext` branch in `main`; both tests pass |
| Focused runs without Docker or SQL groups skip the lock | Proven | `test_main_skips_lock_without_heavy_group_and_takes_it_with_one` |
| Test added | Proven | the two tests above, from #2215 |
| Remainder after #2286 | None found | #2286 did not touch the selection; the behaviour was already complete |
| Live full-gate run showing a worker proceeding during a held lock | Unproven | needs `--all` or a held lock during a real run; `--all` is forbidden here |

Observation: the issue is still open although its criteria were delivered by #2215; closing it needs the owner or the PR that records this evidence.
