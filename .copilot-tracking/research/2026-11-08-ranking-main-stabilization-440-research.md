---
title: Ranking current-main stabilization checkpoint 440 research
description: Research for the scoped issue 440 current-main stabilization checkpoint after the ranking publication integration (PR 1239) merged to main
ms.date: 2026-11-08
---

## Identity and method

Task `440-ranking-main-stabilization-checkpoint`. New scoped recurrence of the open checkpoint issue 440, not a rewrite of the earlier sensor or discovery checkpoints, which stay on their own protected branch and PR. Worktree `/home/azureuser/source/ama-wt/checkpoint-ranking-main-440`, branch `docs/ranking-main-stabilization-440`, declared PR target `main`. Local handoff only.

Posture: focused, inline, no worker. The `rpi-research` skill is activated for this phase. Reads only in this phase: no test, SQL, browser, container, scanner, install or lock. Research disposition: `executed`.

## Fresh pins (observed this session)

* Start HEAD `a80acadaa1b7d96a10e71b246e297bc2825d3de5`, tree `5d2df9af254883ec75dedb93ac29bab50482fbe1`; ignored-inclusive status 0 lines; `git fetch` exit 0 and `origin/main` equals HEAD.
* PR 1239 merged to main at 2026-11-08T02:11:31Z as that commit (coordinator file `pr1239-merged-1108.json`: head `ac0f29f92afcc39e0700f67239a4b202f29b7573`, merge commit `a80acada`). The coordinator reports tree equality with the ranking candidate; this session reads the receipt identity tree `5d2df9af254883ec75dedb93ac29bab50482fbe1`, which equals the tree above.
* Document blobs at HEAD: BRD `34d88395de861e9799eb9e24121a21c92c7a5adc` (0.21.0, status draft, ms.date 2026-10-24); PRD `c788b917bafaede215f326f0efc71e071a687f1c` (0.21.0, status in-review); ADR 0002 `cbe21530043ff15432cc6dce1086d080f5eb15b4` (Status Proposed, ms.date 2026-10-24, decision 4 is ranking policy and retained publication); ADR 0003 `d60645397b20fb70ac3d1dc47c7a6c8671201306` (accepted with owner amendment); ADR 0006 `956da1a3b804c803041fe2e8a312bd9f400273ae` (accepted). Draft, in-review and Proposed are not approval.

## Retained evidence read (observed this session)

| Item | Observation |
| --- | --- |
| Receipt `/home/azureuser/.local/share/ama/gates/g79-p-dd92-r1-1108/receipt.json` | sha256 `5627d5758cb14745164054c0c1803544ed0c90f5d064b2fc1b4297ed75a0744c` (matches the supplied value); schema 4, scope full, status passed, failure null, jobs 1, image cache fresh, not resume-eligible, sealed 2026-11-08T01:34:20Z; identity head `ac0f29f9`, base `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01`, merge base equal to base |
| Receipt commands | 205 commands, 192 exit 0 and 13 exit 1; the 13 are `python -c import ...` probes (five project venvs, namespace, infra, migration, five mssql readiness probes), read from the argv in the receipt; no group is skipped (`skipped` is empty) |
| Receipt logs | log files sit beside the receipt; the sha256 of every log read this session equals the receipt value. Counts read from the retained logs: core 2404 tests with 226 skips, agents 273, API 1982 with 339 skips, orchestrator 104, importer 39, static 86, infra 533, migration 25, browser 3 and 1, MSSQL 286 with 1 skip |
| Hosted-only items listed by the receipt | GitHub approvals, protection and checks; OIDC and Azure what-if; manual release or deployment; real AI acceptance. None was observed |
| Coordinator files | `pr1239-merged-1108.json`, `verify-root79-final-merge-1108.stdout` (VERIFIED full local gate at `ac0f29f9`, base `b284d0d3`), `pr1239-final-merge-checks-1108.txt` (hosted src checks listed pass), `root79-published-ac0f-equivalence-1108.json` (308 paths, 4 API pages, 308 blob matches). Their contents are read as coordinator reports; this session did not re-run any of them |

The receipt belongs to candidate `ac0f29f9` against base `b284d0d3`. It is historical, source-qualified premerge evidence and not a fresh command at the squash commit `a80acada`. The browser, Chromium and axe state counts, the four image reports and the MSSQL supplement are not independently re-read here beyond the log counts above.

## Source contracts (static reading at HEAD, no execution)

| Contract | Where observed |
| --- | --- |
| Ranking is a pure function of cases and a hash-checked versioned policy; no clock, seed or model | `src/core/src/zava_forward/core/ranking.py` (`rank`, `snapshot`, `policy_hash`, `rule_order_hash`), `ranking_publication_runner.py` module docstring |
| Policy sign-off is read, not proved: owner, ISO date and a rule-order hash must agree, and a signed policy is a new version file | `ranking.signoff_problems`; current `src/core/src/zava_forward/core/policies/ranking-v1.json` has owner `to be named`, `signoff` null and status "Draft rule order, not yet signed off by an owner" |
| Archive record is immutable and dated per policy version, as_of and snapshot hash; stage file is created exclusively with mode 0600, synced, then hard-linked so the first writer wins and nothing is overwritten; loser reports the existing record; stage removal failure is reported as `stage_retained`; a damaged existing record is refused | `ranking_publication.publish`, `_existing`, `_remove` |
| A failed archive-folder sync after the link raises `DurabilityUnconfirmedError` with the record kept, not a confirmed publication and not a rollback | `ranking_publication._confirmed`; `store.publish_ranking_snapshot` audits `ranking_snapshot_publication_unconfirmed`; `server.py` maps it to HTTP 409 with outcome `committed_unconfirmed` |
| No hard-link support or an unwritable folder becomes `ArchiveStorageError` with a path-free message naming owner and next action | `store.publish_ranking_snapshot` |
| Runner refuses with a coded reason when policy is unknown or invalid, sign-off missing (outside exercise), archive unverified, or space is short; exercise computes and writes nothing; schedule is reported as proposed, retention as a separate Legal decision | `ranking_publication_runner.run`, `PROPOSED_SCHEDULE` |
| API: policy description is readable; snapshot, publication status and publish are manager-only (`MANAGER_ROLES`), publish is a POST; non-managers get 403 | `server.py` routes, `store.ranking_snapshot`, `ranking_publication_status`, `publish_ranking_snapshot` |
| The viewer snapshot file `ranking-snapshot-<version>.json` beside the data is a rewritten cache using a temp file and `os.replace`; it is not the immutable archive and has no no-overwrite contract | `store.ranking_snapshot` |
| AI prioritisation is a separate recommendation record not read by the ranking function; the offline cohort evaluation uses constructed pairs through the real `rank`, states "never fairness evidence" and stays blocked on unapproved thresholds | `agents/cohort_ranking_eval.py` docstring; ADR 0002 lines on AI prioritisation |

## Requirement and decision joins

* PRD PR-006: same data and same published policy version give the same order, visible reason codes, fixed tie-breaks and a named policy owner; changing policy creates a new version. Joins to `ranking.py`, the registry hash and the published-snapshot contract.
* PRD PR-007 and PR-008: AI prioritisation is a recommendation only and never changes a ranking; a person approves every action. Joins to the separation above; no live model effectiveness is established.
* PRD FR-012 with AC-015 and AC-040: missing, conflicting or ineligible inputs produce unknown, held or an explained outcome and not a silent exclusion. PRD FR-054 with AC-073: evaluation record needs approved thresholds; the manifest is a developer fixture and OQ-018 remains open.
* ADR 0002 decision 4 (Proposed): policy file, registry and snapshot; the Done and Partial rows in ADR 0002 still say "no scheduled publish step" and "named policy owner and sign-off still open". Whether those rows were reconciled after PR 1239 is not established here and is recorded as a document-versus-source drift candidate to read in the plan, not as a fix to make.
* ADR 0006: source layout and the local gate boundary only.
* The BRD names ranking only at a general level (Stock Prioritisation Agent, "ranking is arithmetic once weights are agreed", fair prioritisation needs an approved cohort policy); no BRD NFR-numbered ranking requirement is claimed.

## Existing owners compared (gh read-only, this session)

* Open: 79 (ranking epic), 1231 (concurrent-writer metadata, parent topic merged), 1258 (Medium: archive ancestor durability, static evidence, missing nested ancestors synced only to the archive directory), 1259 (Medium: unusable archive path such as a regular file or dangling link can read as a healthy empty archive), 440 (this checkpoint), 81, 86 and 107 (dependent epics named by the user).
* Candidate observations from source (to compare, not to file): the first-publication ancestor durability and the unusable-path classification are already owned by 1258 and 1259. The viewer-snapshot `os.replace` cache is a design choice with no stated retention or no-overwrite contract; it is not a regression of PR-006 and no defect is established.
* Compared against open ranking owners found by `gh issue list --search "ranking in:title"`: 79, 1231, 1258, 1259. No duplicate is proposed.

## Evidence tier and limits

* Tier FOCUSED: the continuation changes checkpoint documentation and tracking records only (cutover pack, index, log, new RPI records). No production code, deployment, infrastructure, SQL or security policy changes. A defect that needs executable change is returned through the coordinator, not implemented.
* Resource state at read time: `/tmp/ama-rpi-heavy.lock` exists; `fuser` showed no holder and no `rpi-checks`, Docker build or test process other than this session. `/mnt` has 5.5 GB free (97 percent used) and `/` has 47 GB free, memory 8 GB available. Scratch must stay small and unique.
* Not observed: live model effectiveness, Azure, acceptance testing, deployed scheduler, filesystem crash or cross-UID behaviour, owner sign-off of rule order, thresholds, retention, whole 79, 1231 or 440 closure, resident or professional decisions.

## Contrarian wave

* The pack is append-only on main at 3007 lines and ends at the parent 73 topic checkpoint (2026-11-07); this record must be appended after it and must not edit earlier sections.
* A source-qualified full pass at `ac0f29f9` could be mistaken for a current full pass at `a80acada`. The tree equality supports that the source is the same, but the receipt base is `b284d0d3`, so the base and hosted merge state differ; the record must keep the source qualification.
* The receipt is not a gate for this documentation child, and `tools/rpi-checks.py --changed` here selects documentation groups only; neither proves runtime behaviour at main.
* Static reading cannot establish crash durability, so 1258 stays an open owner and the publication stays proposed.

## Findings and routing

* No new runtime defect is established by static reading or by the retained receipt. The two Medium followups are existing and unchanged.
* Candidate drift to check in plan: ADR 0002 decision 4 status rows versus current source.

## Planning Readiness

Ready. Gaps carried into the plan: exact focused test selectors and installed-environment proof, ADR 0002 drift check, resource-safe scratch, the focused gate prerequisites and the base rule of `tools/rpi-checks.py` (base must equal current `origin/main`).
