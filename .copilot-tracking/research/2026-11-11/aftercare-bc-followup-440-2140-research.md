---
title: Aftercare post-1458 current-main follow-up research (Refs #440 #1402 #1401)
description: Prospective read-only research for a dated follow-up observation on main after PR 1458 merged
ms.date: 2026-11-11
---

## Status and disposition

* Research disposition: `executed` (read-only Git and GitHub queries, 2026-11-11 about 21:41 UTC). Planning Readiness: `Ready`. No test has been run yet.
* Trigger: PR 1458 `fix(aftercare): refuse existing blank intake state` MERGED 2026-11-11T21:34:00Z as `bc123235af30b63de9808c97a430860f1e00dcc8` (PR head `ff6c181ea7921ace9d1704c6890b3beda1d5cd3b`). #1402 and #1401 CLOSED; #133, #134, #89 and #440 OPEN.
* Not a source correction or authority reset. The earlier checkpoint (frozen head `4d7be2015672d62eba5d325d9da025af07f1c036`, observation pin `077ad5ad2`, independently approved with zero findings) stays untouched; its "pending PR 1458, static blank gap" statements were correct at that pin and cannot establish the integrated behaviour.

## Identities read

| Item | Identity |
| --- | --- |
| Fresh `origin/main` (fetched 21:40Z) | `bc123235af30b63de9808c97a430860f1e00dcc8`, root tree `ee35ec2e34c70111005cb173597698af9e72359e`, one commit past `077ad5ad2`; equals the merge commit named in the trigger, so no newer main |
| Trees at main | `src` `297e248aef8140e34ecaa059acd68ee067951d23` (was `51feb8eaaed8` at the pin), `docs` `2dcd87665c46632c2fd353417518a84a1291f6cd`, `infra` `a022907662e2a98374f36d8f641eefd29d0dc798`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `56e251c7cd6762cd4f344fa393150649ae020875` (the last four equal the pin) |
| Source paths changed pin to main | Exactly `src/core/src/zava_forward/core/aftercare_intake.py` (blob `96674907da90` to `fb25f9f5de5b`) and `src/core/tests/test_aftercare_intake.py` (`b3f220bb1e11` to `ed815f6bd3b5`) |
| Branch head `4d7be201` | A documentation-only child of `077ad5ad2`; its source does NOT include PR 1458 and is not used for observation |

## What PR 1458 changes

One predicate: `_parse` is now `if text is None: return _blank()`; a present blank or whitespace document goes to `json.loads` and raises `StateInvalid`. Five tests in new class `BlankStateTests` (absent state initialises and replays; blank read refused and bytes preserved for `""`, `"   "`, `"\n\t \n"`; blank write refused; HTTP handler 503 twice with bytes preserved; existing non-empty document not reset). Acceptance criteria of #1402 are all ticked on the issue; that is issue state, not an observation here.

## Selected smallest existing selectors

| Id | Selector | Covers |
| --- | --- | --- |
| B1 | `src/core` `test_aftercare_intake` (module) | `BlankStateTests` blank initial-state boundary, `PersistenceTests` corrupt and non-blank damaged-state refusal, replay |
| B2 | `src/core` `test_aftercare.SnapshotTests` | Numeric restore of the register at 999, 1000, 1001 and refusals |
| B3 | `src/core` `test_aftercare_store` (module; JSON and SQLite adapters, SQL Server opt-in skipped) | Numeric restore through persistence, restart and replay at 999 to 1001 |

Not run: API screen modules (no API path changed), SQL Server, browsers, full or `--changed` gates, the 125-test campaign as a set, the personal-handoff campaign.

## Method constraints

* Observe an exported tracked-source tree of exactly `bc123235` (git archive of `src`) in a new external folder, not the dirty primary checkout and not branch `4d7be201`; prove module origins and input hashes. The installed distributions are editable installs of the owner's primary checkout, so the explicit `PYTHONPATH` of the export is required and origins must be proven.
* No install unless a selected command reports a missing dependency. Constructed synthetic data only.

## Limits and unknowns

* Hosted CI of `bc123235` is not read as passing here. SQL Server behaviour of the blank boundary is unreachable via `DocumentStateStore` by source reading and is not run. Numeric restore on SQL Server stays unobserved.
