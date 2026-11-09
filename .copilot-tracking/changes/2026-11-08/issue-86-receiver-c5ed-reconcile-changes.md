---
title: Issue 86 receiver c5ed reconciliation changes
description: Changes record for the normal merge of the published parent c5edb320 into the child
ms.date: 2026-11-08
---

Scope: issue #86 only, `Refs #86`, local only. Tier FULL for the eventual candidate; this continuation is LIGHT preparation.

## Change

* One normal `--no-ff` merge of `c5edb320ad10d3d73bb985bfb82b2d0bee94381a` into the child, after the prospective research, plan, details and critique were committed alone (first parent `6ee3e03b`).
* Merge commit `6a03b398eb6037b75c84748a570b49cb8877ca03`, tree `32329016dd14e5b0c59103191a0c0095d9fbe4e4`, parents `6ee3e03b` and `c5edb320`. The earlier frozen `a8bfcca0`, local parent `e888a499` and main `f548b65f` are ancestors (explicit exit 0 each). The earlier wrong ancestry brief and the stopped FULL attempt are preserved unchanged.

## Conflict resolutions (child side, justified per file, not blind)

* `src/core/src/zava_forward/core/appointments.py` and `src/core/tests/test_quality_procurement.py`: `git diff c5ed HEAD` has 0 deleted lines, so the child contains every published hunk; the child also keeps the later sole-missing-capacity Unknown branch (`b205ed37`).
* `docs/architecture/cutover-evidence-pack.md`: 185 insertions and 1 deletion against `c5ed`; the deleted line is the older `ms.date`. The child's newer date and added content are kept (critique finding 1 exception).

## Automatic merges

`quality.py` and `store.py` merged without markers and are byte-identical to the child. `store.py` still contains the `require_quality_evidence` and `quality_evidence_gate` references from #1226 (3 matches). `gates.py`, `procurement.py`, `test_gates.py` and `test_hazard_referral.py` were already contained in the child.

## Preservation proof

* The non-tracking tree of the merge equals the first parent's (empty `git diff --name-only HEAD^1 HEAD -- . ':!.copilot-tracking'`); production source and the complaint adapter are unchanged.
* Complaint and quality blobs (`complaints_route.py`, `resident_decisions.py`, `store.py`, `appointments.py`, `quality.py`, `test_resident_decisions.py`, `test_quality_procurement.py`), `docs/reference/log.md` and `.github/rubric/scores/latest.json` equal their pre-merge blobs (snapshot `/mnt/ama-gates/snap/pre-c5ed-blobs.txt`).
* All 47 tracking paths changed on `c5ed` since merge-base `56eec736` have blobs equal to `c5ed`; no earlier tracking file was modified or deleted; the log prefix is unchanged (0 diff lines).
* Parent worktree, remote, main and PR target untouched; no push.

## Light checks

Scratch `/home/azureuser/.local/share/ama/gates/g86-receiver-light-r1`, whole git archive, non-editable venv.

| Check | Exit | Result |
| --- | --- | --- |
| pip install core, core[dev], agents, api | 0 | no first-run failure |
| import origin | 0 | store, resident_decisions, appointments from the scratch venv site-packages |
| unittest quality_procurement, gates, hazard_referral, resident_decisions | 0 | 505 tests OK, 111 skipped (SQL/Azure opt-in) |
| mypy | 0 | 269 files, no issues |
| ruff check src tests | 0 | passed |
| ruff format --check src tests | 0 | 215 files formatted |

Raw `.out/.err/.exit` files are in the scratch directory. Skipped SQL/Azure/AT tests are not acceptance.

## Not done

No FULL, SQL, browser, Docker or scanner run. Old receipts stay invalid. Pending: fresh current-base FULL, independent exact-head assessment of both the local-parent delta against `e888a499` and the published-receiver delta against `c5edb320`, hosted checks and human approvals. A child merge into the parent needs a separate parent integrated FULL. The #1238 supersession policy and the original Medium findings stay open.
