---
title: Infrastructure integration topic 136 corrective C1 research
description: Research for the docs-only corrective loop C1 on the issue 136 integration topic after coordinator Medium findings F1 to F3
ms.date: 2026-11-08
---

## Identity and method

Task `infrastructure-integration-136-c1`, corrective child of `infrastructure-integration-136` (same session `dc0efcb1-4795-4cd2-b25c-2a66564530b3`). Worktree `/home/azureuser/source/ama-wt/issue-136-integration`, branch `feat/infrastructure-integration-136`, declared target `main`. Local only. Reads only: git, gh, session metadata read, file views; no test, build, install, service, lock, Azure or model call. Disposition `executed`.

Original records are preserved unchanged as dated history: research, plan, details, critique IC-001 to IC-005, topic record, Review RV-001 to RV-003 and state. The critique is not rerun for those records and adverse history is not replaced. Corrections land only in new C1 records.

## Fresh pins (observed this session)

* HEAD `f28e1fe003e1e1d7d2fe43546cbbe0d4a92851d2`, tree `87291f1e8b7a2cb8646660fff70df049966d1338`, ignored-inclusive status 0 lines. `git fetch origin main` leaves `origin/main` at `0f05e9aae70768def8d1d9c300215f9ee2f11638`, no drift.
* The coordinator reports an independent read of the full Main to `f28e1fe0` diff (524 lines, 8 files, 53 KB) and three Medium findings. That is a coordinator report; this session did not re-run it. Each finding below is checked against current files.

## F1: the `0bd489d3` identity

Observed: the local session store holds session `0bd489d3-4546-4229-94f9-d1812eadef27`, repository `jmservera/ama`, branch `feat/slice-144`, summary beginning "Run the full RPI loop (research, plan, implement, review) for GitHub issue #144". So `0bd489d3` is the prefix of a Copilot session UUID for the original 144 loop, not a Git object. The earlier statement that it is "not a valid object" is true only because it is not a commit; the inference "unresolvable in this repository, may exist in another clone, identity unverified" was a misclassification. A Git object database can neither verify nor disprove a CLI session identifier, and the coordinator's registry and native brief independently carry the same metadata.

Corrected 144 identity map (observed unless stated):

* Git lineage: body candidate `6496f61f0361c27c297b97b12a5c46e374cd6a5f` is an ancestor of local `ea7f36c030e7a6fbac740d382fafa54f2de2dbf4`; `6496f61f` is not an ancestor of published `origin/feat/slice-144` at `1a9616d4e9ab89d93a72204d82ee26c70baee06c`; `ea7f36c0` is not an ancestor of the published head.
* Session: original 144 loop is session `0bd489d3-4546-4229-94f9-d1812eadef27`, a conversation identifier, not source and not evidence of any commit.
* Local session metadata is a read of this machine's store; it establishes that the session exists and its branch, not its outcome.

Affected original text, preserved and superseded for current use only (grep of the originals, by file and line at `f28e1fe0`): F1 in research lines 31, 48, 65; critique IC-004; topic record line 129 (C5) and the 144 stacking rule line 47; review RV-002 (line 30). F2 in research line 69; plan lines 30, 32, 59; critique IC-003 (line 17); topic record lines 47 and 141; changes line 47; review line 41; state `next_action` and follow-up rank 1.

## F2: gate ordering

Observed in `.github/workflows/src-ci.yml`: `on.pull_request.paths` includes `src/**`, `infra/**` and several tooling paths; `workflow_dispatch` is also allowed. Hosted CI therefore runs on a pull request or a manual dispatch of a pushed ref, never on an unpublished local commit. The original IC-003 disposition and the plan, topic record and state wording "assessment, fresh selected CI, then draft PR" and "CI before any publication" cannot be satisfied literally: a push or draft PR is needed before hosted CI can run, and this topic's changed paths are `.copilot-tracking/**` only, which the listed path filters do not select, so Source projects CI may legitimately not trigger.

Correct current order, none authorized by this loop: (1) focused local documentation validation (Markdown, link, Git diff, source blob review) and independent exact-head assessment; (2) separately authorized push and draft parent PR to `main`; (3) fresh actual-head hosted checks that GitHub selects, before merge or any 144-dependent publication; (4) required and reported checks and branch-protection mapping remain gates. Path-based non-selection of Source projects CI is not a failure and is not Bicep validation. No manual all-project CI dispatch is proposed for a docs-only anchor. Actual Source CI is absent for this head and must not be described as passed or as code validation.

## F3: module coverage completeness

Declared inventory from pinned files at `f28e1fe0`, with wired-from read by grep of `module` declarations:

* Entry: `infra/main.bicep` (resource group) wires guard, identity, network, monitoring, keyvault, storage, registry, sql, foundry, iothub, apps (conditional), edge (conditional), authTokenStore (conditional), operationalMonitoring.
* `infra/governance.bicep` has `targetScope = 'subscription'` and declares no module; `main.bicep` does not reference it. Separate unit.
* Standalone resource-group units: `iot-hub-live.bicep` (module iothub-scope-guard), `live-simulator-job.bicep` (header: authored and compiled only, not deployed; module staff-initializer-guard), `private-proof-publisher.bicep` (staff-initializer-guard), `public-edge-existing.bicep` (edge-existing-guard, edge, edge-existing-auth), `resident-assistant.bicep` (no module; opt-in, default off), `resident-demo.bicep` (staff-initializer-guard; referenced by `scripts/resident_demo_deploy.py`), `staff-initializer-rbac.bicep` (staff-initializer-guard).
* Modules (20 files): authTokenStore (calls privateEndpoint; from main), containerapps (calls envDns; from main), edge-existing-auth and edge-existing-guard (from public-edge-existing), edge (from main and public-edge-existing), envDns (from containerapps), foundry, keyvault, monitoring, registry, sql, storage (each calls privateEndpoint; from main), guard (from main only; the standalone units call the separate guards listed here), identity, network, operationalMonitoring (from main), iothub (calls iothub-scope-guard and privateEndpoint; from main), iothub-scope-guard (from iothub and iot-hub-live), privateEndpoint (from authTokenStore, foundry, iothub, keyvault, monitoring, registry, sql, storage), staff-initializer-guard (from four units).
* The original topic table consolidated several of these (private endpoint, env DNS, guards, standalone units) without a row each, and listed some by group. The correction is a one-row-per-file table in the amendment.

## Classification

Delivered code (static reading) for every file above. Observed local: this session's reads. Authorized Azure observed: none. Source CI: absent for this head. Unknown: live state, owner and approver confirmations, hosted check selection after a future authorized push.

## Findings and routing

* F1, F2 and F3 are confirmed against current files. No new defect, no new issue, no scope change.
* The 136 acceptance criteria stay unmet; 144 source prerequisites 107 and 118 and the named human decisions stay open.

## Planning Readiness

Ready: one new amendment record (current topic and gate order), one new state record, Changes and Review, with originals untouched.
