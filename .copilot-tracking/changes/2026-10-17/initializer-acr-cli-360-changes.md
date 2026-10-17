---
title: Initializer ACR CLI changes
description: Current command evidence and ordered RPI delivery
ms.date: 2026-10-17
---

Task 360 / initializer-acr-cli-360, branch fix/initializer-acr-cli-360,
starting source bab4bf3a2ac9ec030d78d27063d1390f800c5c7c.

## Ordered Phase Log

Research executed first: focused wider/deeper/contrarian complete, Ready.
Plan executed second: independent critique Revise, PC-001 resolved directly
with exact hosted-digest/source-manifest/local-smoke identity gate. No second
critique. Implement third, P01/P02-T01 complete with image delivery blocked.
Review fourth: one independent execution Complete, outcome Residual work.
No implementation defects; PC-001 resolved. No correction or second Review.

## Scope and Current State

Full approved plan with conditional publication/pin; existing source unchanged.
No new infrastructure/network/IAM/runtime/data actions. Actual command results
and blockers follow; no retrospective success is relabeled current proof.

## Implementation Evidence

P01-T01 actual `timeout 180 docker build -f infra/cutover-proof.Dockerfile
--build-arg API_IMAGE=<retained digest> -t zava-initializer-acr-cli-360:bab4bf3
infra` failed exit 1 at base manifest HEAD: 403 Forbidden,
`denied: client with IP '4.225.218.160' is not allowed access`.
No image created. Actual local retained-base import/help/UID/localhost smoke
unavailable. This is network policy denial, not demonstrated AcrPush/IAM denial,
and does not block the separately authorized hosted experiment.

P02-T01 preliminary focused check failed because zava_forward was not installed.
Restored missing dependencies using pip only in worktree-local .venv, including
four editable source distributions, pinned PyYAML and hashed API requirements.
Identical focused command then passed 83 tests in 12.889s. No source/test edit.
TMPDIR was task-owned before Python startup.

P01-T02 preflight inspects the actual installed CLI archive packager, not just a
custom ignore matcher. Generate/inspect archive locally, assert seven unique
regular paths, every byte matches source commit and record SHA256 manifest.
The CLI adds a duplicate Dockerfile entry with identical bytes. No private data
or unrelated source is allowed. Actual hosted build then follows with service/
client bounds and sanitized output; no debug or SAS URL retained.

P01-T02 first CLI invocation with `-f cutover-proof.Dockerfile infra` returned
`ERROR: Unable to find 'cutover-proof.Dockerfile'.` locally. This is not a hosted
denial. Correct the invocation to root-relative `-f infra/cutover-proof.Dockerfile
infra` and preserve the initial error separately in the command receipt.
Immediately relevant command-path refinement, no source or authority change.

P01-T02 actual corrected build uploaded 20.157 KiB, queued QuickRun `dbc`, and
ran on ordinary cpu2. Service timeout600/client720. Current run Failed
2026-10-17T17:57:22.946003Z to 17:57:29.852767Z; no outputImages.
Sanitized actual logs prove source download and Docker configuration succeeded,
then hosted-agent registry login failed:
`login attempt to https://crcutovertestrzsrg.azurecr.io/v2/ failed with status:
403 Forbidden`. This is NOT source upload failure, not no Tasks capability, and
not demonstrated RBAC denial. No build step/base pull/push/new digest occurred.
Historical dbb success is separately retained, not used to override current dbc.

P01-T03 no image pin authorized because hosted publication and actual image
validation gates fail. Full read-visible before/after job projection hashes
match fbc548ae52b49563b3e6c3c8d0c0cd2ecec8b1d04f8f4c109d9fff77b1c5908e.
Projection includes identity/tags/location and all properties except provisioning
state/eventStreamEndpoint, no values retained. Old proof digest and entire
Manual initialize template/configuration retained. Registry Disabled/None before
and after. The only Azure write was the authorized uploaded source/failed
QuickRun dbc; no workload, network, IAM or backing-resource mutation.

## Validation and Remaining Work

Actual image smoke/publication/pin Blocked, not passed. Focused source tests:
83 pass/zero skips. Actual loopback current-source smoke: welcome/health200,
anonymous me/stats401; one fictional case/zero staff, no SQL, AI off, isolated
HOME/state and fictional tenant UUID. Server terminated and exact fixture
scratch removed. This is not actual retained-base/hosted-image smoke or sign-in.
No executable source/test changes, so unrelated component lint/build suites
are not rerun. Source Dockerfile pinned base/security upgrades and seven-file
context are unchanged.

P02-T01 factual documentation updates supersede only the private-publisher-only
inference, retain historical results and append log without rewriting its prefix.
Full context/source hashes and before/after job fingerprints are in the command
receipt. Review readiness awaits scoped link/diff/privacy/cleanup checks below.
Human/browser/SQL/AI d/e remain UNMET regardless of build outcome.

## Pre-Review Reconciliation

P01-T01/T02/T03 complete through actual attempted/blocked outcomes and unchanged
job proof, not successful image delivery. P02-T01 complete: 83 focused tests/
zero skips; seven added documentation links/anchors, append-log exact old prefix,
untouched source/Dockerfile/context, task JSON syntax/integrity and bounded
credential-pattern/diff checks pass. Native preflight/localhost scratch removed.
Readback confirms dbc Failed with no outputImages, distinct from historical dbb.
No source/tests changed; no unrelated lints/full component suite needed.
Plan/details/executive summary/current receipt synchronized. Remaining P02-T02
Review and P02-T03 publication are terminal parent responsibilities. Missing
real image/pin/human acceptance is explicit, not an unchecked source task.

## Blockers and Follow-Ups

Current hosted-agent login403 prevents publication; exact network-policy versus
identity cause unknown. Current local manifest firewall403 prevents actual-image
smoke. No widening authority requested or assumed. A later authorized existing
route must supply an actual image/digest/local smoke identity record before pin.
Genuine operator tenant/browser/roles/SQL/AI and retirement remain later work.

## Independent Review and Publication Handoff

P02-T02 completed by the one independent reviewer. Outcome Residual work, not
Conformant image delivery. RV-001 Medium image/digest validation blocked;
RV-002 Low genuine live/human acceptance UNMET; RV-003 Low retirement needs
separate authorization. Reviewer independently checked source/manifest, links/
anchors, additive log/diff; did not rerun the reported83tests. No root defect
or correction cycle. No code changes after Review.

P02-T03 publication uses fresh authenticated account id8036360/login jmservera,
repository-local 8036360+jmservera@users.noreply.github.com for both author and
committer and required Copilot trailer. No global configuration, merge, rebase
or force-push. Commit/PR skills' referenced instruction files and changed-files
tool are unavailable in this host; repository conventions and explicit owner
gh/Conventional Commit instructions govern ordinary publication instead.
Final remote/PR verification is recorded externally with exact final head.

Publication actual: evidence commit5504f87ae9a82cc5562bd242b5694a02393b7957
pushed ordinarily and PR385 opened against main:
https://github.com/jmservera/ama/pull/385. Remote/PR initial head matched.
No checks reported at initial inspection; not Pass and no workflow dispatch.
Exact task-owned scratch directory and worktree .venv removed. All plan markers
complete as bounded evidence delivery; image publication remains Blocked.
Automatic session stopped at explicit owner boundary, no follow-up child work.
Terminal lifecycle record is committed/pushed separately so no pre-publication
state falsely claims a PR existed; final exact head checked externally.

## Coordinator-Authorized Integration and Read-Only Diagnosis Continuation

Date2026-10-17, same #360 workstream/PR385; no second full RPI, critique or
Review. Original single Review Complete/Residual work is retained byte-identical.
External coordinator final-head gate is forthcoming, not a Pass.

Clean old local/origin/PR head60134c500112fe6736fbd9a97ff1d079eab9afc6
verified before fetch. Fresh origin/main exactly
bbbc9243505b606550327c64bf5429243f457f2e, as authorized. Rebased two owned
commits, resolving only docs/reference/log.md conflict by keeping exact upstream
prefix then entire own append. Both upstream #84/topic #360 KB routes/history
retained. Intermediate integration head6311b511bb4e2b702305b6be0a882a010a819671
is distinct from actual tested/uploaded sourcebab4bf3. Historical command receipt,
source/context/payload/base hashes and Review are byte-identical to60134c5;
no retroactive test/source claim or mutation.

Bounded diagnosis used GET/read-only commands only: registry and preview
2025-06-01 properties; selected dbb/dbc run metadata; task/agentpool list; ama
VM/pool inventory; registry-scoped Authorization permissions; exact-registry
activity metadata October16 11:55 through October17 18:20/max200, selected
timestamp/operation/status/substatus only. Returned194 events, oldest creation
October16 12:08:01. No actor/claims/request/response-change payload, identity
details, new build log payload, SAS, secrets or private data accessed/output.
Control-plane queries may themselves create ordinary audit read entries;
no Azure configuration/build/runtime write requested.

Existing primary deployment artifact records dba/dbb images captured before
registry isolation. Registry writes completed after dbb13:53:24 success, first
13:56:53.6373221, then14:07:30,14:14:17,22:34:36 October16. This corroborates
network isolation as the strongly supported likely reason default-agent dbc
login403 differs, not exact property-change proof. Current registry publicDisabled/
bypassNone/LegacyRegistryPermissions; both runs QuickRun Linux/amd64/cpu2/task
null/poolnull. Named tasks/pools and inspected ama VM/pool inventory empty.
Caller effective actions["*"] no exclusions, empty dataActions; does not prove
agent token/pull access or justify a new grant.

Official Microsoft docs retrieved2026-10-17: private-endpoint az-acr-build
limitations, Tasks-specific bypass policy, generic trusted services, managed
task identities, dedicated pool billing/regions and network troubleshooting.
Exact URLs/evidence W5-W13 and wider/deeper/contrarian cycle2 in research.
Preview GET confirms networkRuleBypassAllowedForTasks absent, not false.
Documented unset-SAMI default denial is a candidate contributing condition;
actual daemon token identity unknown, no promise generic trusted-service toggle/
caller identity alone fixes it. UAMI exception does not prove available path.
UK South absent from published preview pool-region list; new same-region pool
not assumed feasible; no existing inherited pool or named task demonstrated.
Unknown external private runners are not claimed nonexistent.

Minimal later decision: identify an existing approved private-connected Docker
publisher (preferred no-bypass/no-new-allocation path if one exists), or retain
blocker while separately appraising a costed supported private-pool design or
explicit Tasks-bypass security exception. New pool needs region/quota/network/
allocation-price ceiling approval; bypass relaxes network isolation and exact
identity applicability remains unproven. Regional public-IP option conflicts
with current constraints; auth/IAM change alone unsupported. No such option
authorized/executed, no regulatory approval inferred.

Existing runbook/evidence/index/additive log updated without changing old
observations. No source, dependency, image, tests or IAM/network change; minimal
doc/link/JSON/byte-parity checks only, not fresh component/image/runtime tests.
Exact image smoke/pin and genuine operator/browser/SQL/AI d/e remain unperformed.
Owner explicitly authorizes exact-lease force push ONLY this topic with lease
60134c500112fe6736fbd9a97ff1d079eab9afc6, PRbody update and clean stop.

Integration/diagnosis validation: all11 added relative documentation links/
anchors pass, task JSON parses, git diff --check passes. Every upstream KB
routing row except the intentionally updated own #360 row is retained exactly.
Exact upstream log prefix plus complete prior own append verified. Entire
src/ and infra executable/tests/Dockerfile/ignore byte-identical to newmain;
historical command receipt, original single Review and critique byte-identical
to oldtopic60134c5; all seven payload hashes still match bab4bf3 receipt.
No dependency installation, test/build/image/runtime rerun or fake final-head
acceptance. Coordinator external review remains pending.
