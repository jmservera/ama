---
title: Both demo sites redeployment changes
ms.date: 2026-10-30
---

## Execution Boundary

Task f09558e0-64f4-4440-856f-8e9a302dbb6f, demo-sites-redeploy.
Declared scope: full plan. Research Complete / Ready; one critique Complete /
Revise, PC-001..004 directly applied. Full-loop phase progression explicitly
requested by owner; no automatic follow-up session opt-in.
Pinned main ffd8f35e63b24905b9aeb937dbf2a7fe9968747f, clean at intake,
topic chore/ops-redeploy-both-sites-1030, pull already up to date.
Owner renewed deployment authority through2026-11-15 accepted.

## Commands and Initial Results

| Command or operation | Result |
| --- | --- |
| git status --short; git branch --show-current; git remote -v | Clean matching topic, expected origin |
| gh pr view 542/545 --json number,title,body,mergedAt,url; file paths | Both merged; corrected SQL and exact-template route identified |
| git pull --ff-only origin main | exit0, already up to date, HEAD=origin/main pinned SHA |
| gh pr list --head chore/ops-redeploy-both-sites-1030 --state all | No prior PR lifecycle |
| gh pr view 550 | exit1, issue not PR; resolved via gh issue view |
| gh issue view 550/551/552/503/553/554/556 --json number,title,body,state | exit0; named feature acceptance and merged implementations read |
| az account show; az group show -n ama; az resource list -g ama | exit0, Enabled expected subscription, existing two demos/hub/ACR/eight jobs |
| docker info --format '{{.ServerVersion}}' | exit0,29.9.0 |
| flock -n /tmp/ama-rpi-heavy.lock true | exit0 probe only; build must separately acquire |
| gh api user --jq '{id,login}' | exit0; authenticated privacy-safe identity resolved |
| az ad signed-in-user show | exit1, /me requires delegated auth; no role/user guessed |
| az role definition list --name 'IoT Hub Registry Contributor' | exit0, devices/* dataActions only, no management actions |
| az role assignment list --scope exact ama IoT Hub --include-inherited | exit0, no Registry Contributor for current caller |
| in-memory az account get-access-token claim decoding | exit0, verified current VM ServicePrincipal oid; token never printed/persisted |
| One independent final-candidate critique | Complete / Revise, four direct contracts applied, no repeat |

Research and operational source reads are identified in the research artifact.
No .env, private dataset, secret value or model invocation was read/performed.

## P01-T01: Preservation and Admission

Backups and financial preflight executed; deployment admission blocked.
Private execution root:
/home/azureuser/.copilot/session-state/f09558e0-64f4-4440-856f-8e9a302dbb6f/files/redeploy/
Full command output remains private; only sanitized evidence is committed.
Financial admission is conditional: existing all-in USD700 envelope includes
unknown outside-group liabilities U. Scope is ama only, no broader cost read/
role authorized. Renewed authority is not treated as measured cost headroom.

At2026-10-30T08:27:13Z, RG ActualCost returned20 rows USD337.19112853637773,
query2026-10-01 through2026-10-30, no nextLink. RG Forecast returned3 rows
USD36.23934745788574 for30-31 October, includes actual/fresh partial rows.
These totals MUST NOT be added as all-in forecast: scopes/partial actual can
overlap; full outside-group liabilities U, commitments, lag and future amounts
remain Unknown. No broader scope queried. All-in headroom Unknown, paid
operations not admitted under PC-004 and repository local-RPI-gate policy.
ACR push, in-VNet SQL start and both app writes stopped before mutation.
Owner's renewed deployment authority remains acknowledged, not expired.

Approved no-charge role succeeded: IoT Hub Registry Contributor
(4ea46cd5-c1b2-4a8e-910b-273211f9ce47) at exact existing ama hub for verified
current operator ServicePrincipal2d4fe550-794a-4ee9-8093-e680ca02fe18.
Assignment3438cffb-4db8-5470-9d1a-d4861573d030. Only one assignment added,
all prior assignments retained, exact full Hub management response unchanged.
No device/key/network operation or data-plane propagation test occurred.

## P02-T01: Both Local Images Built, Publication Blocked

`flock -n -E 75 /tmp/ama-rpi-heavy.lock python3 <private-root>/images.py build`
exit0. Lock held by wrapper over BOTH Docker builds; no queued/bypassed gate.
Each build used `docker build --label org.opencontainers.image.revision=<SHA>
-t <unique-tag> -f <archive-root>/src/api/<Dockerfile> <archive-root>/src`.
Tracked-source archive SHA256
a6263f027c20a42f99d3566f96c435799d4dbbba4cac743fd724dc01453cabb1,
src tree83d4657d53e4577955ad9d4be66e771a33d4da24, exact pinned main.
No ignored/untracked/.env input, credentials or private data supplied.

| Image | Local image/index ID | Actual config SHA256 |
| --- | --- | --- |
| resident | 885014246f83819475af0d4ffaadd898776253fb089cb36b765527b92f52bf93 | 52a68ac4e785bb3eb6dfaaa0db9bb67c83b07bf7f9f4737431732bddc421dd95 |
| employee | e4fa88041d4f4fedfdd230fa3e3eb5f73a53c89c43bace46e0658dcf30cf9799 | 3e4f5299bdddcf430f2c4d54fb2777515faeb50177f4a19fc12c19ccf1727f98 |

Both config/source-label checks passed. Tags include main-20261030-ffd8f35e63b2
and resident/employee suffix. These are LOCAL images only; no remote binding,
private ACR push or new live digest is claimed. Docker-save scratch tars removed
by their exact owned filenames; built images retained.

## P02-T02 and P02-T03: Blocked Before Write

No SQL initializer execution/template/retry change, schema/table/view apply or
sensor row inspection was performed: financial admission blocked. Historical
table absence is not relabelled fresh counts proof.
No app PATCH, revision, ingress/auth/env/secret change or rollback performed.
Both existing live revisions remain yesterday's source, NOT pinned current main.
No ACR network/export/policy change, token login or registry deletion occurred.

## Remaining Work and Validation

Local builds, full backups and scoped no-charge role completed. Read-only public
browser checks remain independently eligible. Paid registry publish, SQL job and
rollouts blocked for Unknown all-in headroom. No deployment success claimed.
Full publication gate, exact-head assessment, hosted/human approval and push
remain separate coordinator prerequisites, not passes.

## P03-T01: Live Checks and Final Preservation

`git fetch origin main` exit0; source remains pinned. Private `verify.py` exit0.
Exact protected app/auth/history comparison passed for both apps; no added or
removed revisions. Both old targets latest=ready Healthy. All four ama app
minima0, eight complete job definitions equal baseline and all Manual. Full
stable ACR projection equality passed; public Disabled/defaultAllow/no rules/
exports disabled/admin disabled unchanged. No registry data-plane digest check
is claimed; old image references/history retained and no image deletion occurred.

| Live target | curl result | Scope |
| --- | --- | --- |
| Both /healthz | 200 | Existing healthy revisions only, not current main |
| Both / | 200 | Public shells |
| Resident /chat-widget.js and /chat-widget.css | 404 | New shared component is not live |
| Employee /app, /app.js, /ops.js, /chat-widget.js, /chat-widget.css | 401 | Anonymous denial preserved, no authenticated feature proof |

Real Playwright MCP started with only about:blank, no existing owner session.
Resident and employee public pages inspected at1365x900 and390x844; no horizontal
overflow observed. Resident had one password input, zero shared widget scripts/
launchers/dialogs. No password entered or credential obtained. Employee /app
navigation reached Microsoft Entra sign-in; no authentication attempted.
One public-page console error per site was reported by the tool; no clean-console
claim. Public snapshots/logs retained under ignored .playwright-mcp paths listed
in sanitized evidence; no historical/generated-output cleanup performed.

| Feature reference | Live result |
| --- | --- |
| #550 / #556 shared resident and employee chat | Not deployed on resident (assets404/no launcher); employee auth blocked; conversation/input/selector/consent/labels/error semantics not accepted |
| #551 / #553 expanded map filters | Blocked by employee sign-in; markers/header synchronization not exercised |
| #552 / #554 single-case UX | Blocked by employee sign-in; icons/thinner steps/blocker detail/tabs not exercised |
| #503 isolated chat/privacy/grounding | No authenticated/model/human acceptance; prior merged source is not live acceptance |

The browser initially denied an attempted external evidence-file write outside
its allowed roots; the same read-only DOM evaluation was repeated without writing.
No browser success was inferred from that failed output. Aggregate browser
results transcribed into the evidence exporter; no authenticated data included.
Raw automated snapshots are public/sign-in pages only; OAuth URL parameters
are not copied into committed evidence.

## Evidence Export and Pre-Review Reconciliation

Private `export.py` exit0 generated
.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-evidence.json with64
actual command records, hashes of retained stdout/stderr and unique filenames,
external executor hashes, build/config/source proof, cost admission, role and
full final preservation plus browser result matrix. This is sanitized operational
evidence, not a local publication receipt. Token acquisition was in memory only.
Two expected resident auth GET absence responses are retained nonzero; no broad
error suppression. Independent command wrappers all exited0.

`git diff --check` exit0; `git diff --name-only <pinned-main> -- src infra docs`
empty; `git check-ignore <public-browser-snapshot>` confirms ignored artifacts.
No dependency/source/test/documentation change. No new application test suite
was needed to claim this evidence-only blocked outcome; actual builds and live
preservation checks executed. No private dataset/.env/secret/model access.
Original critique unchanged; all active markers remain unchecked where any
required outcome remains unmet. Implementation Partial / blocked, ready for one
independent Review; no later implementation or repeat Review planned.

## Original Independent Review and Parent Dispositions

Exactly one Review executed Complete, implementation Partial/Blocked, outcome
Not accepted for the requested full deployment. Original retained unchanged at
.copilot-tracking/reviews/logs/2026-10-30/demo-sites-redeploy-review.md.
Independent reviewer matched all64 journal entries/128 output hashes, all five
current executor hashes, tracked archive bytes, raw full app/auth/history/jobs/
ACR/Hub and role comparisons without repeating cloud/build/browser operations.
No executed source defect or unauthorized cloud mutation established.

| Finding | Parent disposition and later route |
| --- | --- |
| RV-001 High | Accepted: complete financial admission Unknown. Later rpi-research with owner/coordinator-supplied all-in evidence; no broader reads/RBAC inferred. |
| RV-002 High | Accepted: both current-main deployments and sensor SQL initialization undelivered. Later admitted rpi-implement with fresh source/drift and current executors; never replay unused historical SQL/push paths as approved tooling. |
| RV-003 Medium | Accepted: named authenticated UX remains unmet. Owner acceptance after actual rollout, no credential disclosure or model smoke inferred. |
| RV-004 Low | Accepted: DOM/viewport/sign-in summaries are operator-transcribed; final sign-in snapshot is empty, so raw artifacts alone do not independently prove every browser detail. Curl404/401 evidence remains independent. Preserve the limitation; later provenance/acceptance work, no browser rerun or current-task correction. |

Review observation also retains minor stale research-question status cells;
narrative findings/readiness resolve them conditionally. No artifact correction
or second critique/Review is performed after the original Review.
No recovery, ACR exception cleanup, SQL transaction or data-plane propagation
path was exercised or certified. Local evidence persistence follows; no push.
