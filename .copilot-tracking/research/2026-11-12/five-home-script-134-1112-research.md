<!-- markdownlint-disable-file -->
# Research: five synthetic demo homes in the canonical demo script (2026-11-12, Refs #134 #184)

Task `five-home-script-134-1112`. Base `origin/main` `d288b2a893a5a934f4357bbc7be79fa94ab59580` (fresh fetch; HEAD equal). Disposition: executed. Planning Readiness: Ready. Local-only documentation candidate; no push, PR, issue edit, cloud, model, SQL, live probe or spend. Not a reset of any #134 implementation or correction balance.

## Owner direction (task instruction, 2026-11-12)

Simplified demo operating mode: single-instance simulator start/stop (no SQL tickets); FIVE synthetic demo homes; a new reading every minute; Quality AI restricted to the same five homes (supersedes the earlier every-open-case scan scope); deterministic eligibility distinct from paid analysis; during the presentation AI analysis is operator-triggered, not per reading. An eight-hour background limit is a later recommendation, not implemented. Owner request: write the case ids of the five homes into the demo script and, if possible, add direct links.

## Evidence read

* Canonical script: [runbook](../../../docs/capstone/demo/runbook.md), already indexed ([index line 211, 974](../../../docs/reference/README.md)). It has no case ids and no operating-mode section; its frontmatter date is 2026-11-08.
* Original and addendum case study, index, memory and the documentation skill (mode author; content-sensitivity, conventions) read for conventions. Memory is context, not evidence.
* Case id form: generator [build_mvp_dataset.py](../../../support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py) line 254 sets `id=c.cid.replace("CAND-", "ZF-")`; candidate ids are `CAND-{year}-{nnnn}` in [generate_pack.py](../../../support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/generate_pack.py) line 61. Seeded demo case ids therefore look like `ZF-2025-0355`.
* Seeded baseline provenance (committed docs): [data pack README](../../../docs/reference/research/retrofit-synthetic-data/README.md) records the exercise baseline from `build_mvp_dataset.py --seed 20260901 --as-of 2026-10-13`, 980 programme cases, 443 open, seeded to the exercise SQL database after owner reauthorization 2026-10-14.
* The public CSV pack uses a different seed (1341953496), so its candidate states do NOT describe the seeded MVP cases. The `handover-examples.md` candidate ids were rejected as a source for that reason.
* Simulator homes: [live_simulator.py](../../../src/api/src/zava_forward/api/live_simulator.py) `HOME_IDS_SQL = SELECT id FROM cases WHERE closed = 0` and `live_control.py` homes validated by `sensor_identity.home_key` (any non-blank string up to 128 UTF-16 units). So a seeded open case id is a valid home id.
* Route: `app.js` line 412 matches `^#\/case\/([^?]+)(?:\?.*)?$`; links use `#/case/${encodeURIComponent(id)}`; `case-workspace.js` reads `?tab=`. The sensor panel is built in the `quality` tab (`app.js` line 1146, `sensorPanel(id)` inside "Quality and handover"). The static app is served at `/app` (`server.py` line 464).
* Documented origin: [cut-over evidence pack](../../../docs/architecture/cutover-evidence-pack.md) lines 17-20 list the employee origin observed on 2026-10-31. It records that authenticated case navigation was blocked, not run, then. It documents the host only, not current availability.

## Replay of the committed generator (read-only, local)

A throwaway script (not committed) replayed only the simulation part of the committed generator: `build(random.Random(20260901))`, `Sim(...)`, `sim.run(SIM_START)`, exactly as `build_mvp_dataset.main` does before any address work. It does not read the private stock register (address assignment uses a separate `Random(seed + 2)` and is not needed for ids or state). Two runs were byte identical. Result: 980 cases identified on or before the 2026-09-30 snapshot, 443 open, matching the documented seeded counts. That agreement is the provenance check.

Selection rule (deterministic, not curated): open case; stand-alone building (one dwelling, so no shared building anchor); no safety hazard record; at least one damp report in 24 months; stage not one of the paused, hold or aftercare states; no exit reason; first id in ascending id order for each archetype. Archetypes ARC-01, ARC-02, ARC-04, ARC-05 and ARC-06 each had candidates (ARC-03 had none), giving exactly five.

| # | Case id | Archetype | Property type | Stage in replayed seed (as-of 2026-10-13) |
| --- | --- | --- | --- | --- |
| 1 | ZF-2025-0355 | ARC-01 | End terrace | Quality check |
| 2 | ZF-2025-0382 | ARC-02 | Mid terrace | Quality check |
| 3 | ZF-2025-0286 | ARC-04 | Bungalow | Quality check |
| 4 | ZF-2026-0829 | ARC-05 | Mid terrace | Quality check |
| 5 | ZF-2026-0892 | ARC-06 | Semi-detached | Funding check |

Stage names are the generator state (`Awaiting QA and evidence` maps to `Quality check`; `Funding decision` maps to `Funding check`).

## Findings and limits

* F1. Five reproducible ids exist from committed public code and committed documented counts; no private dataset, `.env`, roster or tenant data was read.
* F2. Sensor-capability is not established by id selection. The simulator uses every open case id as a possible home only when the control cohort lists it; whether the deployed store holds these ids and whether the sensor tables hold readings for them is unknown. The 2026-11-04 sensor seed used a different, owner-private test case. Preflight must confirm.
* F3. The deployed database is a private seed output; the committed generator is the only public evidence of its ids. Later owner operations (seed merge, enrichment, case edits) could alter state. Source selection is not deployed acceptance.
* F4. The Quality-AI-five-homes restriction, the one-minute cadence, the single-instance start/stop and the manual analysis are owner-selected targets. Source still reads "every open case" (`src/api/README.md` line 2173) and an hourly home refresh; this lane changes no source or README. Existing observed/blocked histories stay.
* F5. No deployed-origin availability is claimed. Authenticated sign-in is required; the origin host is documented from a 2026-10-31 observation.
* F6. Stage `Funding check` for case 5 is a weaker Quality fit; kept because the rule is mechanical and removing it would require curation. Recorded as a limitation.

## Planning Readiness

Ready: edit the runbook (frontmatter date, one new section), add an index/log pointer, write a machine-readable handoff outside the repository, keep everything else unchanged.
