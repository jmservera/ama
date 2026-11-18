---
title: Changes for #162 live isolation proof (r2)
ms.date: 2026-11-18
---

## Files

* Added `docs/reference/research/issue-162-live-isolation-evidence-2026-11-18.md` and `docs/reference/research/issue-162-live-isolation-2026-11-18/` (probe, login helper, raw output of two runs, four screenshots).
* Updated `docs/reference/README.md` and `docs/reference/log.md`.
* No `src/` change. Tier FOCUSED. `rpi-checks.py --all` not run.

## Per-criterion table

| Criterion | Proven / unproven | Basis |
| --- | --- | --- |
| 1 server-side owner keying | Proven live (forged principal headers and owner fields have no effect); ticked | raw/03 |
| 2 role matrix, cross-user denied | Cross-user read of a real foreign thread unproven live (one Entra identity); proven locally (33 tests OK) | raw/03, unittest |
| 3 projection of retrieved context | Unproven live; local tests only | needs model call and second role |
| 4 never shared into another prompt | Unproven live; local tests only | needs two users and a model call |
| 5 injection test set | Not re-run live; local test only | local test |
| 6 admin and break-glass audit, policy | Partly proven (refusals audited live, grants unproven live, policy decided for demo only); left unticked | prior break-glass note |
| Anonymous and resident-session access to chat and memory | Proven live: 302 to Entra, 404 on resident app | raw/03 |

## Validation

* `python3 -m unittest tests.test_chat_isolation` from `src/api` (with the documented PYTHONPATH): 33 tests OK.
* Markdown link and diff review; mypy and ruff not applicable (no package source change; probe is evidence).
* Hosted CI: not run (nothing pushed).

## Divergences

* Overwrote the earlier run's `issue-162-live` research and state files by mistake; restored with `git checkout`; this run uses `-live-r2` names.
* Run 1 failed to add memory (400); kept as raw/02. Resident screenshot caught the sign-in spinner; labelled as such.
* The `implement-start` witness qualification "source was already dirty" arises from the r2 files and probe created before it.
