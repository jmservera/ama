---
title: Quality sensor demo #1288 correction 1 research
ms.date: 2026-11-08
---

Prospective C1 research, written 2026-11-08T19:40Z (UTC) after the C1 request (19:37Z). The original
research, plan, changes and review of candidate `b89520be` are preserved unchanged.

## Source base

* Frozen start `b89520be47d5d08f6d73a0352a8da8a14dabf8b3` (tree `441c2f1e`), integrated base `ecb28815`.
* Fetched `origin/main` = `c50e9f0b` (differs from `ecb` only in `.github/rubric/scores/badge.svg` and `latest.json`).
* Merged with `git merge --no-ff origin/main` (no rebase/reset/force): working head `ef6c05e9`, tracked tree clean.

## Findings under correction

Independent functional assessment, verdict request_changes (H5/M4), nine findings. Evidence read this session:

| # | Evidence | Disposition |
| --- | --- | --- |
| 1 | `core/synthetic/live_readings.py` `Reading.row()` emits `source_type=SYNTHETIC`, `scenario=live-simulator`, `schema_version=live-sim-reading-v1` (19 chars), `label`. Values are weather-derived (daily climate anchors, per-home offset, noise, sunlight). `src/api/README.md` live-contract section is interface evidence only. | Classify by schema/scenario, label synthetic weather-derived non-calibrated; keep in demo. |
| 2 | UI latest is a separate query; the six-hour seal capture may omit it. | Put latest into the one immutable capture used by UI, model and citations. |
| 3 | Seal window timestamps change the digest every six hours even for empty/withheld/unavailable captures. | Make captures clock-independent; trigger on substantive change only. |
| 4 | `review_flag` labels every returned quality-evidence output L4. | Flag only for proactive, current, eligible, returned, sensor-citing output. |
| 5 | `_view`, `listing`, `detail`, `export` replay the stored snapshot after consent withdrawal. | Withhold sensor values/citations/derived flags in current projections; keep stored records. |
| 6 | No installation marker exists in the retained store. | Say pre/post-retrofit unavailable in model source and UI; quality-record anchor is a separate named non-retrofit anchor. |
| 7 | UI `QUALITY_ROLES` includes Programme Support Officer; the `quality-evidence` registry roles do not. | Align the sensor panel to the endpoint role set without granting other assistant rights. |
| 8 | Consent reads the whole `sensor_consumer_control` table per home. Table is keyed by `sensor_id` with JSON body; `sensor_id` for a home is `sensor_key(home)` (stock) or `SENS-SYN-...` (backfill). | Bounded point lookup by candidate sensor IDs plus bounded `sensor_reading` home/time query. |
| 9 | Retained primary key is `(sensor_id, reading_id)`; citation key `sensor:{reading_id}` drops the sensor. | Encode both in the key. |

## Tooling discovery

* Local SQL Server 2022 image `mcr.microsoft.com/mssql/server:2022-latest` is present (docker). `tools/rpi-checks.py` shows the maintained container recipe: loopback publish, 3 GB, `ZF_TEST_MSSQL=1`, `ZF_SQL_*` environment.
* Resource check 19:38Z: `/` 12 GB free, `/mnt` 7 GB free, no holder of `/tmp/ama-rpi-heavy.lock`.
* Web guidelines: raw source fetched from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` at 19:39Z (complete, supported raw retrieval).
* Task-owned ignored inputs: `/tmp/ama-1288-venv`, `/tmp/ama-1288-br`, `.playwright-mcp` outputs. Inventoried at the end; not deleted.

## Planning Readiness

Ready. Research disposition: executed. No external evidence outside the repository and the guideline source was needed.
