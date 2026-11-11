---
title: Aftercare numeric-order integrated-main checkpoint research (Refs #440 #1401 #1402 #134)
description: Read-only research before a bounded checkpoint record for merged PR 1456 (issue 1401) on main, with the unmerged PR 1458 (issue 1402) blank-state gap kept pending
ms.date: 2026-11-11
---

## Status and disposition

* Research disposition: `executed` (read-only Git, source and GitHub queries, 2026-11-11 about 21:20 to 21:30 UTC). Planning Readiness: `Ready`. Nothing here is a test result.
* Trigger, not a new issue: the recurring checkpoint criterion of existing issue #440 ("after every completed feature wave") for the aftercare ordering correction that reached `main`. It is not the old #440 C6 and not a retry; it spends no finite correction allowance of #1401, #1402, #134 or #440 and reopens no exhausted campaign.
* Duplicate check: `docs/architecture/cutover-evidence-pack.md` has one aftercare section, "Aftercare integration current-main checkpoint (2026-11-10, Refs #440 #89 #133 #134 #1401 #1402)", for PR 1400 at `64c3f9191`. It lists #1401 and #1402 as OPEN inherited findings with static reads only. A grep for `1456` and `a3862eed` finds no record. The delta below is therefore not an identical existing checkpoint; no stop condition applies.
* The personal-handoff 75-test campaign (PR 1449 section) is a different surface and is not reused or repeated.

## Identities read (2026-11-11)

| Item | Identity |
| --- | --- |
| Start pin | `077ad5ad20293a1d79932ea14e9f639dd11e5a22` |
| Fresh `origin/main` (fetched 2026-11-11T21:21Z) | `077ad5ad20293a1d79932ea14e9f639dd11e5a22`, unchanged; worktree HEAD equals it, branch `docs/aftercare-wave-checkpoint-2119`, source clean at start |
| Trees at the pin | root `d1dde25bc3476772bd9d97711558ed87d1f7a035`; `src` `51feb8eaaed8d83d578164cebd06bb89861924e3`; `docs` `2dcd87665c46632c2fd353417518a84a1291f6cd`; `infra` `a022907662e2a98374f36d8f641eefd29d0dc798`; `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`; `.github` `56e251c7cd6762cd4f344fa393150649ae020875` |
| Trigger merge | PR 1456 `fix(core): restore aftercare concerns in numeric identifier order`, MERGED 2026-11-11T20:04:04Z as `a3862eed4a324b13715eeebf0c98053d9079dec1` (root tree `ab22886c8202b843de0afb233d3a2dc4c64178be`), an ancestor of the pin. `Closes #1401` |
| Since the merge | `git diff --name-only a3862eed4 HEAD` lists only `.github/rubric/scores/latest.json` (rubric score commit `077ad5ad2`). No `src`, `infra` or `tools` path differs, so the pin source equals the merged source |
| Blobs (core, at pin) | `aftercare.py` `59b66dd1eed0` (was `115f639bc782` at PR 1400), `aftercare_intake.py` `96674907da90` (unchanged), `aftercare_store.py` `e5bd737c6d9b` (unchanged) |
| Documents (blobs at pin) | BRD 0.21.0 `draft` `34d88395de86`; PRD 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20` and ADR 0006 `956da1a3b804` Accepted. None changed by PR 1456. Draft and in-review are not approval |
| Issue states (read live) | #440, #133, #134, #89, #132 and #1402 OPEN; #1401 CLOSED by the merge. Nothing is ticked, closed or opened here |
| Hosted state of main | `Capstone Rubric Scorer` for `a3862eed4` completed success; for the pin `077ad5ad2` only `Infrastructure PR what-if` (skipped) is listed. A skipped or absent workflow is not a pass; no Source CI result for the pin is claimed |

## Pending candidates, excluded from main acceptance

* PR 1458 `fix(aftercare): refuse existing blank intake state` (closes #1402): OPEN at head `ff6c181ea7921ace9d1704c6890b3beda1d5cd3b`, branch `fix/aftercare-blank-state-1402-1111`, base `main`, no review decision recorded. Its body states a parser-predicate change in `aftercare_intake.py` plus five tests, 67 intake/register tests and 13 API screen tests at its own head, and an independent exact-head approval. Those are candidate policy and evidence, not observation on `main`. Its blank-document repair is NOT on `main`.
* PR 1455 `test(api): verify connected-home specialist screens` (#134, branch `docs/demo-connected-walk-plan-134-1111`): OPEN, unmerged, excluded; it is the same plan topic as the #134 walkthrough recommendation, not aftercare source.

## What PR 1456 changes (static read)

`src` diff is three files. `aftercare.py` adds `_concern_number` (regex `AC-\d{3,}`, else -1) and `AftercareRegister.from_state` now restores `concerns` sorted by that number before the existing contiguity, id and outcome checks. `test_aftercare.py` adds numeric-restore tests for 999, 1000, 1001 with text-sorted and reversed key order, and gap, unpadded and foreign-identifier refusals. `test_aftercare_store.py` adds `seed`, `assert_listed`, a 1000-record restart read test and a 999/1000/1001 write, restart and replay test inside the shared `Contract` class, which runs for the JSON `Store`, SQLite and (opt-in) SQL Server adapters.

Why the ordering matters on the persisted path: `aftercare_intake.py` `_txn` writes `json.dumps(doc, sort_keys=True)` and `DocumentStateStore._canon` also sorts keys, so `AC-1000` precedes `AC-101` in stored JSON. Before PR 1456 the register restore relied on insertion order (the finding recorded in #1401 and in the earlier pack section). After it, restore order is numeric and the checks that refuse gaps and non-canonical identifiers are kept.

## What PR 1456 does not change, the pending gap (static read of the pin)

* `aftercare_intake.py` `_parse` (about line 267): `if text is None or not text.strip(): return _blank()`. A present but blank or whitespace-only `FileStateStore` document is still treated as fresh, so a later write can restart identifiers. This is the gap owned by #1402 and PR 1458. At the pin it is read statically only; no probe is run, so the gap is stated from source, not reproduced here.
* The runtime path uses `DocumentStateStore`, whose `read` returns `None` or serialized JSON (`_canon`), so a raw blank string does not reach `_parse` through that adapter. The earlier section and PR 1458's own text say the same; it is a source reading, not a proof about every deployment.
* No HTTP-level 1000-concern journey, concurrency or performance behaviour is changed or measured by PR 1456.

## Requirement trace candidates (document-qualified, proposed)

Reuse the earlier aftercare pack rows by document and ID; BRD and PRD both use FR-049 for different topics, so each trace names its document.

* PRD FR-049, AC-063 (in-review): complaint, remedy, package, handover and financial closure stay distinct. Affected by ordering only in that a restored register must keep every concern visible; whole AC-063 remains unmet (age bands, lease evidence).
* BRD FR-047, AC-089 (draft): closure cannot close an outstanding remedy. Unchanged logic; the restore refusals protect it.
* PRD FR-014, AC-017 (in-review, Not run): intake type, owner, route; contact is not consent. Intake persistence is the affected surface.
* PRD FR-036 (in-review): AI task `aftercare-concern-pack` stays unapproved and manual. Unchanged.
* BRD RULE-014 (draft): a sensor signal is context, never closure evidence. Restore refusal for sensor-dismissed concerns is unchanged.
* ADR 0006 (Accepted): `src` layout and the cut-over; the change is inside `src/core` and its tests only. ADR 0003 (Accepted): runtime-fit context only.
* Human and resident boundaries: no consent is read or written, no resident account or approval is added, closure remains manager-only, a missing owner stays Unknown, and the paper and phone routes remain the manual path.

## Environment findings

* Python 3.12.3, Ruff 0.17.3, mypy 2.4.1, Playwright 1.64.1, Node available. The installed `zava-forward-core`, `-api` and `-agents` distributions are editable installs pointing at the owner's primary checkout `/home/azureuser/source/ama/src`, not this worktree. A run must therefore put this worktree's `src/*/src` first on an explicit `PYTHONPATH` (never `mvp`) and prove import origins; otherwise the primary checkout would be tested.
* MSSQL variants are gated by `ZF_RESIDENT_MSSQL=1` and a task-owned loopback server; they are out of scope here and will report as skips, which are not passes. No SQL service, Azure, model, private dataset or spend is used.

## Selected smallest affected checks

| Id | Selector | Why |
| --- | --- | --- |
| A1 | `src/core` `test_aftercare` (register, `SnapshotTests` numeric restore) | Direct 1456 regressions at the register |
| A2 | `src/core` `test_aftercare_store` (JSON and SQLite adapters; MSSQL skipped) | 999/1000/1001 persistence, restart and replay |
| A3 | `src/core` `test_aftercare_intake` | Intake persistence, replay, roles and the unchanged `_parse` blank behaviour; sits next to the pending gap |
| A4 | `src/api` `test_aftercare_served` and `test_aftercare_screen` | Route contract and staff screen above the register; the screen module runs in a node vm, not a served browser |
| S1 | Ruff check and format check, mypy on the three owned core files | Static check of the changed files |

Not selected: full Core or API discovery, browser suites, MSSQL, the local gate, `--changed`, image build. They are outside the bounded delta.

## Open questions and unknowns

* Hosted Source CI for the pin and for PR 1458's head are not read as passing here.
* Whether any later main commit alters the blank-state behaviour before PR 1458 merges is unknown; the record states the pin only.
