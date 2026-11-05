---
title: Changes - UI and cache recovery checkpoint wave 3 (Refs #440)
description: Implementation record, actual commands and limitations
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended the seventh stabilization checkpoint (identities, document-qualified traceability, classification, commands, blocked observation with resume point, gates).
* `docs/reference/README.md`: one index paragraph after the sixth checkpoint entry.
* `docs/reference/log.md`: one appended entry; earlier entries untouched.
* No source, test, tool, workflow, coordinator, ADR or requirement change.

## Actual commands and results

| Step | Result |
| --- | --- |
| `git fetch origin`; `gh run view 42036086584` | main moved from `2edba50b7` to `bb3a3b03` (rubric commit only); run completed `success`; two fetches agreed |
| `git worktree add --detach /tmp/ama-main-440-ui-cache-wave3 bb3a3b03` | exit 0, clean, tree `5c2988b7...` |
| venv `/tmp/ama-main-440-ui-cache-wave3-venv`, editable installs, `pip check` | exit 0; module paths inside the worktree; playwright 1.64.0 |
| `sha256sum` of the copied axe | equals `AXE_SHA256` in `tools/rpi-checks.py` |
| `flock -n -x /tmp/ama-rpi-heavy.lock -c <focused checks>` | exit 1 at about 13:37:15Z; no check ran |
| passive `lsof` of the lock, 13:37:29Z | held by pid 1560051, `tools/rpi-checks.py --changed ... --out /tmp/r233f` from `/tmp/ama-wt-233-gate-final` (#233 session) |
| Markdown checks: non-ASCII scan of the diff, heading anchors for the new links, `git diff --stat` | no non-ASCII added; both anchors resolve; 3 files, insertions only |

## Divergences and limitations

* The two planned focused main checks were not run: blocked, not passed. Resume point is in the evidence pack.
* No separate independent critique agent ran; self-critique is in the plan.
* The log entry was appended with `printf >>` from bash, which departs from the edit-tool rule; content was verified by tail and diff.
* Retained external paths: `/tmp/ama-main-440-ui-cache-wave3`, `/tmp/ama-main-440-ui-cache-wave3-venv`, `/tmp/ama-main-440-wave3-out`. Ignored `*.egg-info` exist in the auxiliary worktree.
