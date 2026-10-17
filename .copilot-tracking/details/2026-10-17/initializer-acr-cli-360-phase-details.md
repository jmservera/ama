---
title: Initializer ACR CLI phase details
description: Execution gates and preservation evidence
ms.date: 2026-10-17
---

Task 360 / initializer-acr-cli-360. Research C1-C5/W1-W4 reused.
Ready after PC-001 direct resolution from the one final-candidate critique.
Current execution: P01 complete as bounded attempted/blocked outcome, P02-T01
complete. P02-T02 independent Review Complete/Residual work; P02-T03 publication
complete as open main PR385, initial evidence commit5504f87 remote/PR matched.
Terminal lifecycle push verified externally. No source
features or image pin delivered. Commands/results in changes and receipt.

<!-- P01 -->
## P01: Local and hosted validation

Execution complete: local base HEAD403, actual hosted upload/download succeeded
then cpu2 dbc registry login403. No real image smoke/push/digest/pin.
P01-T03 complete through unchanged-job proof, not an update. Full projection
hash equal; existing Manual initialize command never run.

<!-- P01-T01 -->
### P01-T01: Local retained-base image

Run docker build using infra/cutover-proof.Dockerfile, context infra and
API_IMAGE=crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d.
The base is not cached. Bound command to 180 seconds. Record exact sanitized
failure if inaccessible; no arbitrary substitute. If available, inspect UID,
compare copied file hashes, import five scripts without networking, run two
help CLIs and launch installed API on localhost only using a tiny fictional
fixture, no SQL/AI/tenant environment. Verify health and protected API denial.
Override the proof ENTRYPOINT; never invoke initialize or worker main.
Keep task-owned Docker tags/containers and exact cleanup names.

<!-- P01-T02 -->
### P01-T02: Hosted quick build

Use az acr build -r crcutovertestrzsrg -g ama -f infra/cutover-proof.Dockerfile
--build-arg API_IMAGE=<retained digest> -t zava-forward-cutover-proof:<unique
source-SHA/time tag> --timeout 600 --no-logs infra.
CLI 2.91.0 resolves the supplied Dockerfile against cwd before archiving,
despite help describing it as context-relative. The initial context-relative
attempt failed locally before any upload; corrected root-relative path retained.
Use client timeout 720. CLI may emit upload SAS references in errors: capture
privately with restrictive permissions and sanitize before retaining evidence.
Verify native upload allowlist/source SHA256 before cloud upload. Do not use
debug. Record run ID and inspect show-run status/outputImages if queued;
show-run digest is ARM evidence, not direct data-plane/local image proof.
No pool, bypass, networking or credential changes.
If command blocks before scheduling, retain error and explicitly say no hosted
agent access was tested. If hosted succeeds, attempt safe actual image pull/
validation only through existing access; absence of local image validation
keeps pin blocked.
Mandatory single identity gate after hosted success: join run ID, submitted
seven-file path/SHA256 manifest and manifest hash, source commit, retained base,
hosted repository/digest, local RepoDigest/image ID, six payload hash comparisons
and actual smoke results in one sanitized receipt. Pull by repository@sha256,
not mutable tag; run the P01-T01 UID/import/help/localhost checks on that exact
hosted digest. A separately built local image cannot attest the hosted output.

<!-- P01-T03 -->
### P01-T03: Pin or unchanged proof

Before any pin inspect actual update implementation or ARM contract and preserve
entire container array including six environment entries, command/args/resources,
all configuration/registry/secret references, identity/environment/tags/settings.
Prefer narrowly scoped PATCH with complete unchanged template and only selected
image modified, never an image-only container object. Require fresh comparison
and optimistic concurrency where service supports it. Stop on drift.
Store only canonical hashes and names/counts, not values or secret payloads.
Independently read back and compare normalized entire response excluding only
expected service metadata/image. No start/job-run or secret-payload test.
Only the exact hosted digest satisfying P01-T02's single identity gate may be
pinned. If any proof is unavailable or mismatched, no update; compare current
job settings fingerprints and image.

<!-- P02 -->
## P02: Evidence and publication

Pre-Review execution: 83 focused tests pass, zero skips. Actual current-source
localhost welcome/health200 and protected401 pass on one fictional case/no SQL/
AI off. This does not meet exact image gate. Seven added docs links/anchors,
append-only log prefix, exact source/base/context and JSON/privacy-pattern/
whitespace checks pass. No runtime source or tests changed.

<!-- P02-T01 -->
### P02-T01: Regression/evidence

Use a task-owned worktree .venv only if chosen checks fail on missing dependencies;
pip installs source distributions, not PYTHONPATH=mvp. TMPDIR under task scratch
before Python startup; remove exact scratch after tests. Run four existing modules:
test_container_contract, test_private_cutover_proof, test_staff_azure,
test_initialize_workbench_staff. No private datasets. Documentation-only changes
need link/diff review, not broad unrelated suite/lint.
Update historical runbook/evidence with a dated superseding section, preserve old
observations, replace current KB routing, append log without rewriting history.

<!-- P02-T02 -->
### P02-T02: Independent Review

Reconcile all task markers, actual results, unmet gates and receipt. Activate
rpi-review once and delegate exactly one bounded independent full-task review.
Review execution and outcome are distinct. Findings route later unless a concrete
root defect fits explicitly authorized bounded correction (up to two cycles).
No repeated Review or invented acceptance; required human review stays unchecked.
Actual execution: one independent Review Complete, outcome Residual work.
No implementation defects. PC-001 resolved. RV-001 Medium exact-image delivery,
RV-002 Low genuine live acceptance and RV-003 Low retirement route distinct
later work. No correction cycle or second Review.

<!-- P02-T03 -->
### P02-T03: Publish

Fresh gh api user for repository-local noreply identity, matching author/committer,
Conventional Commit and Copilot trailer. Push this topic normally, open main PR
Refs #360, verify remote/PR head. Do not merge/rebase/force-push or close issue.
Owner explicitly requested stopping at clean pushed PR or genuine blocked result.
Actual publication: https://github.com/jmservera/ama/pull/385, initial evidence
commit5504f87ae9a82cc5562bd242b5694a02393b7957, main base and topic head
verified. CI rollup empty at initial inspection, not Pass; no manual workflow
dispatch or paid rubric dispatch. Task scratch and worktree .venv removed by
exact owned paths. Terminal parent records stopped session and verifies final
remote/PR head externally. No new cloud operation or Review.
