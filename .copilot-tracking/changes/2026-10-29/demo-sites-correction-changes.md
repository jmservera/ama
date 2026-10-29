---
title: Demo sites correction changes
description: Local command evidence and explicitly blocked live correction sequence
ms.date: 2026-10-29
---

## Execution Boundary

Task ID eb7ee1f8-42fd-48a8-9c24-a1cbebb99513; demo-sites-correction.
Full plan declared. Research executed; plan Ready for local-only execution.
One independent critique Complete / Revise, original retained. PC-001 rejected
because it invents a temporary-directory ban contrary to the user's explicit
lock/venv instructions; PC-002 applied with explicit synthetic isolation.
No repeated critique. Plan and phase details share this identity.

Initial and observed origin/main baseline:
77c87e0d76b827544fde9b2f2ce7dfbd9d879232.
Branch ops/sites-redeploy-20261029b, clean at intake. No source changes planned.
No az, gh, alternate Azure REST/SDK, `.env`, private data, live secret access,
cost query, cloud mutation, push or PR. Fresh cloud configuration is unknown.
Implementation outcome: Partial / live actions Blocked, not two-site delivery.

## P01-T01: Backups, SQL and Revision Boundary

Fresh full backups of both apps: NOT PERFORMED. Do not reuse the previous
session's backup as a current rollback baseline. No live SQL shape/count
verification, ACR build/policy change, app update, rollback or job execution.
No claim of fresh exact configuration or Manual-trigger equality.

| App | Historical final revision (not freshly read) | Historical digest (not fresh) | This round before/after |
| --- | --- | --- | --- |
| ca-resident-demo | ca-resident-demo--rollback-20261029-073718 | sha256:fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7 | Unknown / no mutation |
| ca-cutover-test-demo-api | ca-cutover-test-demo-api--emp-main-20261029-072248 | sha256:41db94689ae934e3daa6c7f8fb57d8de5cc58a53995efd50217189231ac1f0c1 | Unknown / no mutation |

Historical source: both-demo-sites-redeploy-changes.md in this dated changes
directory, not an observation by this round.

Coordinator pending sequence:

1. In an allowed context, capture full management configuration/auth/all
   revisions for both apps, protected ACR projection and eight job templates
   in private backup storage. Keep secret values out of logs/git.
2. Through the existing in-VNet init job only, execute a narrowly reviewed
   view-only batch from current resident SQL definition. Do not invoke default
   initialize/reseed. Preserve/restore the exact job template and Manual
   trigger. No public SQL/private endpoint/RBAC/server change.
3. Return only counts and ordered column names, never row content; compare
   the 17-column reader shape including documents_json and narrow view-only
   principal rights. Do not change row windows or grant base-table SELECT.
4. Build the two images from a fresh exact main SHA with approved ACR route,
   prove source/digest/config binding, protect old digests and restore exact
   frozen policies on every exit. Do not delete tags/images.
5. Create one resident forward revision using exact raw-template handling,
   keeping env/secretref/identity/registry/ingress/min0 and retained rollback.
   Require target revision Healthy and latestReady plus anonymous curl.
   If startup fails, collect its console/system logs while it exists BEFORE
   rollback to the captured previous digest. Never retry a forward revision
   within the one-revision allowance.
6. Only then create one employee revision from main (including #541), with
   identical preservation/readiness proof. Keep all eight jobs Manual exactly.
7. Only after both sites are healthy may the separately gated authority
   operation proceed; unresolved prerequisites below currently park it.

Public `/healthz` is the documented route; the requested `/health` is also
observed if reachable, not silently equated with `/healthz`. Either anonymous
response may originate from an old revision and cannot establish new readiness.

Expected ordered names from
src/core/src/zava_forward/core/resident_showcase_sql.py, not a live SQL read:
`case_id`, `email`, `email_count`, `provenance`, `valid_from`, `valid_to`,
`revoked`, `address`, `town`, `postcode`, `stage`, `closed`, `measures_json`,
`measures_text`, `sensor_home_id`, `sensors_json`, `documents_json`.
Expected count 17; actual live shape/count remains unknown.

## P01-T02: #521 Parked, Exact Owner/Coordinator Actions

Inspected edd7f4dedd4b602a55bf2bc651c81b1b85521aed from the local branch;
not cherry-picked and not included in observed main (ancestry test exit 1).
Current main cannot accept January expiry: its packaged cap is still
2026-12-31T23:59:59Z. The authority branch uses an exclusive
2027-02-01T00:00:00Z end, covering all January 31 UTC.

Required before apply:

* Coordinator must reconcile source integration/image selection and expiry
  refresh with the single resident forward-revision limit. Do not apply a
  January config to the old-cap main image or silently create a second
  revision after both sites are healthy.
* Owner credential operator must provide the owner-held replacement password,
  generate its verifier privately and a fresh session-signing key, then use a
  separately reviewed exact-version write operation for the existing secret
  names. The current helper accepts Create only and refuses Modify; do not
  weaken it or add roles. No values in arguments, transcripts or git.
* Owner must identify individually approved existing synthetic SQL rows and
  their provenance/window. Through the existing private job, apply #521's
  transactional WITH CHECK constraint migration, then renew only that approved
  row set without clearing revocations or changing identity rights.
  Managed-identity SQL authentication has no password to rotate.
* Record expiry/alert metadata, bounded rollback-version interval, reference
  refresh, fresh narrow-rights proof and owner-performed sign-in, cross-case
  denial, logout and session-expiry checks. This operator performs no live login.
* Supply current all-in USD700 headroom/renewal funding evidence before any
  paid extension. No cost query is needed or performed by this blocked round.
  Model tariff/inference authority remains unchanged.

## Command Results: Intake and Research

All commands below completed unless an explicit status says otherwise.
Read tools return the named repository documents, not commands against Azure.

| Command or operation | Result |
| --- | --- |
| `git pull --rebase` (first shell command) | exit 0; Already up to date |
| `git status --short; git branch --show-current; git log -6 --oneline; git remote -v` | exit 0; clean, named branch, origin jmservera/ama |
| `git show --stat d6067f19` | exit 0; merged #543 docs and SQL regression |
| `git log -3 --format=...; git branch -vv --list ...; git log -4 --oneline chore/resident-authority-extension-521; git log -1 --oneline origin/main` | exit 0; authority edd7f4de is unmerged, main 77c87e0d |
| `git show edd7f4de --format=fuller --stat; git diff edd7f4de^ edd7f4de -- infra src; git config --local --get user.email; git config --local --get user.name` | exit 0; exact commit source inspected; existing noreply identity |
| `git show --format= --name-only edd7f4de; git diff edd7f4de^ edd7f4de -- src` | exit 0; policy, SQL tests and docs delta read |
| `git show edd7f4de:infra/README.md` (renewal section); `git diff ... -- infra/scripts/resident_showcase_sql.py infra/sql/resident-showcase.sql`; `git show edd7f4de:...resident-authority-extension-521-changes.md` | exit 0; exact rotation, migration and original blocked validation read |
| `/tmp/mv/bin/python --version; python -m pip show mypy ruff playwright zava-forward-api zava-forward-core zava-forward-agents` | exit 0; Python3.12.3, mypy2.4.0, Ruff0.17.1, Playwright1.64.0; editables initially another worktree |
| `git merge-base --is-ancestor edd7f4de HEAD` | exit 1, expected negative ancestry result |
| `git show edd7f4de:infra/README.md` (line locator); `git diff --name-only origin/main`; `lslocks --noheadings --output PID,COMMAND,PATH` (filtered exact heavy path) | exit 0; no tracked source delta and no holder observed at that instant; not lock admission |
| Prior-session bounded search | completed; no additional relevant deployment evidence |
| Source/evidence reads and focused rg/glob calls | completed; research C1-C8 and input pointers recorded; no `.env` or private datasets read |
| Independent critique task | Complete / Revise; original PC-001/PC-002 preserved; no tests or cloud work by critic |

## P02: Validation

Shared nonblocking admission succeeded for the initial setup attempt.
`flock -n -E 75 /tmp/ama-rpi-heavy.lock /tmp/mv/bin/python <external-validator>`
returned 2 because editable pip with `--no-build-isolation` found no setuptools.
No tests ran in that attempt; original log retained at
validation/editable-setup.log, SHA256
2422d3447bd1c8b0367c4ba3e81dd872b6f7d77585e6c836d56bd5fcbb7c2761.
This was a genuine missing build dependency, not a test failure or busy lock.
Retry uses normal pip build isolation from the existing pyproject contract,
`--no-deps -e src/core -e src/agents -e src/api`; no manifest edit or unrelated
tool installation. Second nonblocking admission succeeded and holds the
shared lock over editable setup, checks and owned SQL/browser work.
Retry logs/results use separate validation-complete/ paths, not overwrites.

`docker image inspect mcr.microsoft.com/mssql/server:2022-latest --format '{{.Id}}'`
and `docker info --format '{{.ServerVersion}}'` returned exit 0.
Available local SQL image
sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718,
Docker29.9.0. No image pull, live registry or unrelated container inspection.
An attempted read of nonexistent src/core/build-requirements.txt returned
not found; the build requirements file is under src/, no file was created.

External evidence root:
/home/azureuser/.copilot/session-state/eb7ee1f8-42fd-48a8-9c24-a1cbebb99513/files/.
No full publication gate is executed: its az Bicep preflight is prohibited.
No receipt, source pin update or publication approval is implied.

### P02-T01: Initial Complete-Validation Attempt

The second admitted invocation returned exit 1, with successes and local
harness errors preserved separately. Core full discovery: exit 0,
1471 tests in300.604s,191 opt-in skips. Core Ruff lint/format and mypy passed
(104 format targets,157 typed source files). API Ruff lint/format and mypy
passed (56 format targets,107 typed source files).

API discovery initially returned exit 1 before tests: core fixture roots
preceded API tests, causing `test_buildings` to import from core instead of
API. This is an invocation-path collision, not a source regression.
Both existing synthetic browser checks passed with pinned axe4.10.3:
employee chat and resident assistant/callbacks. No live credentials/models.

Owned local SQL container start/port lookup succeeded, then the parent
validator's import failed because its interpreter started before editable
installation. No SQL test executed in that attempt. Its finally cleanup
removed only the exact owned container, exit0. No cloud SQL or foreign
container accessed. The current source was never changed.

Third invocation `flock -n -E 75 /tmp/ama-rpi-heavy.lock
/tmp/mv/bin/python <external-validator> --resume-local` was admitted
nonblocking. It reruns only failed API discovery with the owning project's
src/tests first, and SQL checks with explicit current core source in the
parent's import path. Completed static/core/browser checks are not repeated.
Original logs remain in validation-complete/; correction logs use
validation-corrections/. This local harness resume is not a full-gate receipt
resume and carries no publication claim.

### P02-T02: Anonymous Live HTTP Observations

Each invocation was `curl --silent --show-error --max-time 45
--connect-timeout 15 --output /dev/null --write-out
'status=%{http_code} bytes=%{size_download}' <public HTTPS URL>`.
No authentication, cookies, redirect following, login or response content
readback. Bodies were discarded, so no body hash is claimed. This is a safe
reduction of the planned body-hash evidence, not a health/readiness upgrade.

Common host suffix: happyriver-ace49996.uksouth.azurecontainerapps.io.

| UTC request start | App | Path | HTTP | Bytes | curl exit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-29T09:49:28Z | ca-resident-demo | /health | 404 | 23 | 0 |
| 2026-10-29T09:49:52Z | ca-resident-demo | /healthz | 200 | 50 | 0 |
| 2026-10-29T09:49:52Z | ca-cutover-test-demo-api | /health | 401 | 0 | 0 |
| 2026-10-29T09:50:23Z | ca-cutover-test-demo-api | /healthz | 200 | 2 | 0 |

These are observations of existing public ingress only, not current main,
Healthy revision status or authority acceptance. No revision was created.

`git status --short; git diff --check; git diff --name-only;
git log -1 --format=%H origin/main` returned exit 0 during validation.
Only the six current evidence artifacts were untracked; no tracked source
delta. No pin update needed.

## Amendments and Divergences

Execution is deliberately evidence-only under the later no-az instruction,
not the earlier live approvals. No source fix is invented. Setup correction
to normal build isolation is ordinary local judgment after missing setuptools.
Body hashes omitted because anonymous probe bodies were deliberately
discarded; statuses and byte counts retained. Original critique unchanged.

### Final Local Validation Results

The third admitted invocation completed exit0. API discovery passed:
1274 tests in461.534s,316 skips. These general-discovery skips are not
integration passes and their IDs are not exhaustively audited here.
Core resident SQL suite passed34/34 with zero skips against the exactly
owned loopback SQL Server, including #543's missing-document-projection
regression. SQL-backed resident browser passed, including synthetic sign-in,
own-home isolation, cookie/session denial, sign-out failure handling and
360px layout. Existing employee and resident assistant browser/axe passes
remain separate from SQL compatibility and live acceptance.

| Invocation (full argv, cwd, UTC, duration and log hash in machine evidence) | Exit/result |
| --- | --- |
| Initial editable setup, no build isolation | 2; setuptools unavailable; original retained |
| Corrected editable setup, normal build isolation | 0; this worktree core/agents/API installed |
| Core `ruff check . --no-cache` | 0 |
| Core `ruff format --check . --no-cache` | 0;104 targets |
| Core `mypy --cache-dir <external>` | 0;157 source files |
| Core `unittest discover -s tests -q` | 0;1471 tests,191 skips |
| API `ruff check . --no-cache` | 0 |
| API `ruff format --check . --no-cache` | 0;56 targets |
| API `mypy --cache-dir <external>` | 0;107 source files |
| Initial API `unittest discover -s tests -q` | 1; import-path collision before discovery |
| Pinned public axe4.10.3 curl fetch | 0; SHA256 equals repository pin |
| `checks.employee_chat_browser_check --axe <pinned> --out <external>` | 0; actual fallback and browser/axe checks |
| `checks.resident_assistant_browser_check --axe <pinned> --out <external>` | 0; constructed chat/callback browser/axe checks |
| Initial exact-owned `docker run --detach --rm ...` | 0; parent import subsequently failed before SQL tests |
| Initial exact-owned `docker inspect` port only | 0; loopback33267 |
| Initial exact-owned `docker rm --force` cleanup | 0 |
| Corrected API `unittest discover -s tests -q` | 0;1274 tests,316 skips |
| Corrected exact-owned `docker run --detach --rm ...` | 0 |
| Corrected exact-owned `docker inspect` port only | 0; loopback33268 |
| Core `unittest test_resident_showcase_sql -v` with owned SQL flags | 0;34 tests,0 skips |
| `checks.resident_demo_browser_check` with owned SQL flags | 0 |
| Final exact-owned `docker rm --force` cleanup | 0 |

Generated machine evidence:
.copilot-tracking/changes/2026-10-29/demo-sites-correction-evidence.json.
It contains22 subprocess command records across all attempts, not secret
values. Each external log hash was verified by export. The generated test
SQL credential existed only in process/container memory and was not printed,
read from a real secret store or committed. Readiness used SELECT1 on the
owned loopback endpoint only; no private SQL connection was attempted.

Export command `python3 <external>/export_evidence.py` returned exit0.
`git diff --check; git diff --exit-code <source-sha> -- src infra docs;
docker container ls --all --filter name=ama-correction-eb7ee1f8-sql
--format '{{.Names}}'` returned exit0 with no remaining exact-owned SQL
container and no tracked source/infra/canonical-doc delta.
Earlier source-integrity check also returned exit0;
HEAD src tree22af89af213f65d89011ea264f4f653de35dbeac.
The one failed partial apply_patch was inspected and only its remaining
details hunk retried; no source or historical artifact was overwritten.

## Pre-Review Reconciliation

P01/P02 complete for the bounded local plan; all live deliverables remain
Blocked/Unknown as stated above. P03 original Review and local commit pending.
No new source, infra, knowledge-base or pinned-data change. Full publication
gate, exact-head publication assessment, hosted checks, human approval and
#521's unmerged-source runtime validation are NOT established by these checks.
Ready for one original independent Review, not acceptance of live delivery.
