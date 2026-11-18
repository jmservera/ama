---
title: Epic 195 demo proof, per-criterion results (live run 2026-11-18)
description: Proven and unproven results for the three unticked acceptance criteria of epic 195, measured with gh, repo checks and read-only Azure CLI on the synthetic demo, plus the guard fix for triage draft D2
ms.date: 2026-11-18
ms.topic: reference
---

Refs #195. Scope: synthetic demo, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure authorised (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed. Only read commands ran against Azure, so nothing was created and nothing needed deleting. No credential was read or printed. Repository base: `171d44edf` (main). Validation tier: FOCUSED; no `src/` or `tools/` change.

## Result

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Stabilization checkpoint of #440 completed before closure | Partly proven | Checkpoint executed and triaged ([triage note](stabilization-checkpoint-triage-440-live-2026-11-18.md)); the one repo-side blocking finding for #195 (D2) has a candidate fix that is held back as FULL tier; owner-approved pivot or defer decision and filing of draft issues are not agent-provable |
| 2 | All child issues closed or explicitly deferred by the owner | Not met; not provable | 4 of 11 children closed (#196, #197, #199, #290), 7 open with unticked criteria; no owner deferral recorded |
| 3 | Deployed container image rebuilt from `src/` and verified running | Running proven; `src/` build provenance partly proven | Revision healthy and `/healthz` 200 (live); registry unreadable so the digest cannot be tied to a build run; runtime banner attributable only to `src/` |

## 1. Stabilization checkpoint (#440)

* #440 is open; its own unticked criteria are filing deduplicated issues and delivering PR artifacts. This note does not tick them.
* The triage note records 3 draft issues. D1 (`/api/time/status` returns 500 on Azure SQL) touches SQL, so it needs the FULL tier and is only marked here. D2 (the legacy-reference guard fails at head) gates #195 closure through #201 and #203 and has a candidate fix held back as FULL tier (see below). D3 (unreachable `ChatIsolation.turn`) is non-blocking.
* Not provable by an agent: owner approval of any pivot or deferral. Draft issues were not filed (publishing is the coordinator's decision).

## 2. Child issues (gh, 2026-11-18)

| Issue | State | Open acceptance criteria |
| --- | --- | --- |
| #196 ADR | closed | none |
| #197 parity matrix | closed | none |
| #199 module migration | closed | none |
| #290 skeletons | closed | none |
| #198 rubric | open | 2 unticked (dual-window dip record, cut-over registry PR) |
| #200 repoint | open | 1 unticked (new tag deployed and verified) |
| #201 cut-over gate | open | 3 unticked (build deployed, private data relocation, owner sign-off) |
| #202 archive and delete | open | 2 unticked (registry PR for `mvp/` globs, old workflows and branch protection) |
| #203 verify references | open | 2 unticked (reference search, deployed app and CI green) |
| #344 public access | open | 5 unticked (public edge and 401 behaviour, parity) |
| #350 src parity | open | 9 or more unticked (tenant, data, AI, map, law) |

No comment records an owner deferral (no match for owner deferral wording in any open child). Owner sign-off, branch protection and tenant prerequisites cannot be proven for the demo. Result: unproven.

## 3. Deployed image

Read-only Azure CLI and HTTP, 2026-11-18:

* `ca-cutover-test-demo-api`: latest revision `ca-cutover-test-demo-api--0000031`, created 2026-11-17T19:42:06Z, health `Healthy`, running state `Running`, 1 replica.
* Image `<registry redacted>/zava-forward-api@sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`; resident app `ca-resident-demo--0000012` runs `zava-resident-demo@sha256:65481780...`.
* `GET https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/healthz` returned 200.
* Console log of the running replica contains `Zava Forward is running at http://0.0.0.0:8088`. That string exists in `src/api/src/zava_forward/api/server.py` (line 2340) and in no Python file of the `mvp/` tree at archive tag `v0.21.0` (`git grep "running at" v0.21.0 -- '*.py'` matches only the `src/` copy). The server also runs the `zava_forward` package named in the container env settings.
* Not proven: the digest's build run. `az acr repository show` fails (registry public access Disabled); `az acr task list-runs` shows only 10 runs, all `Failed` (latest `dbp`, 2026-11-18T15:15:48Z), none producing an output image; `gh run list --workflow src-deploy.yml` returns no runs. Provenance would need an image label or a retained build record. Playwright sign-in was not repeated; signed-in rendering from this revision is recorded in [deployed-parity-live-2026-11-18.md](deployed-parity-live-2026-11-18.md).

## Legacy-reference guard (triage draft D2): fix held back

Before: `python3 tools/check-legacy-references.py` reported 30 violations; 11 came from three guard tests that assert on retired paths on purpose (`tools/test_epic_legacy_path_retirement.py`, `tools/test_epic_parity_matrix_old_paths.py`, `tools/test_private_mvp_data_exclusion.py`).

Candidate change (not in this commit): name archive tag `v0.21.0` in the docstrings of the two path-only files, add the one file that names the retired package to `GUARD_FILES`, and add a unit test. On the working tree it reduced the violations from 30 to 19 (observed; raw output not retained). It edits the gate allowlist and three gate tests, which changes gate semantics, so it takes the FULL tier and needs the complete local gate and an owner decision. It is a separate follow-up and the guard is unchanged here.

Residual (adverse, preserved): 19 violations remain in dated live notes `issue-198-rubric-*`, `issue-203-live-references-*` and `src-repoint-live-audit-200-*` and their raw `.txt` captures. Each new live research note that quotes `mvp/` re-trips the guard, so `test_repository_has_no_violations` keeps failing at head. Recommended follow-up: scope an exemption for dated generated evidence (a gate-semantics edit, owner decision) or add the tag to each note. D1 stays FULL-tier work.
