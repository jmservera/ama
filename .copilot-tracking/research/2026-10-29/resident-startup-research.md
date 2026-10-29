<!-- markdownlint-disable-file -->
---
title: Resident image startup research
description: Local-only diagnosis of the failed main resident image
ms.date: 2026-10-29
---

## Research Brief

* Target: explain repeated termination of ca-resident-demo--res-main-20261029-072628.
* Use: support a scoped source fix or document a newly required setting.
* Scope: resident image, entry point, runtime configuration, SQL startup and tests.
* Non-goals: Azure access/mutation, real SQL, secrets, private datasets, push.
* Criteria: reproduce the failure using the main image with dummy settings, isolate
  the failing startup boundary, and distinguish observed local failure from cloud hypotheses.
* Output mode: convergence; parent-owned full Research -> Plan -> Implement -> Review.
* Posture: focused (default for the named failure and source scope).
* Evidence root: .copilot-tracking/; date 2026-10-29.

## Extension Registry and Participation

Repository instructions and src component guides apply. rpi-research selected
for evidence; the parent will activate the remaining phase skills. No frontend
changes are planned, so frontend design skills are not applicable. Research
is a single continuous startup trace and is investigated inline, without
research delegation. User supplied sufficient boundaries; non-interactive
execution requires no routine questions. Independent critique and Review
will retain their original outcomes.

## Direction Controls and Prior Knowledge Gate

User explicitly requests local Docker builds from src/, dummy settings using
the app's setting names, ruff, mypy, relevant unittests, local commit with the
specified trailer, and no push. Clean branch fix/resident-startup was created
from origin/main d70ee60ab3d7346a9991cf64382d9985f4d09f2e.

Requested redeployment artifact was absent in this worktree/main. Read the
exact file in the known redeploy-2 worktree before source investigation:
`/home/azureuser/source/ama-wt/redeploy-2/.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md`.
Read its sanitized machine evidence, cited resident activation-log summary and
resident build log. No app backups, .env, credentials or secret values read.
Activation console unavailable; the earlier summary does not establish a
specific exception. Old-image recovery success is not current-main success.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Does main import/configure/serve using the ten declared settings? | Depth | Answered locally, C5/C8/C9 |
| Q2 | Which SQL operation is required before bind, and did #525 change it? | Depth | Answered, C5-C7/C9 |
| Q3 | Do port, probe, missing-setting or import alternatives explain the failure? | Depth | Answered locally, C8-C9; Azure cause unverified |

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Deployment evidence confirms successful main build but failed activation and
no failed-revision console traceback. The template supplies ten settings,
port 8089, managed identity SQL and two secret references. Hypotheses include
required settings, expiry/secret validation, SQL schema compatibility, import,
port/probe and observed secretRef CLI serialization drift.

Reflection: prioritize the entry-point sequence and locally reproduce before
attributing cloud failure to the speculative 16/17-column SQL difference.

#### Wave 2: Deeper

Built main with its exact Dockerfile/src context. No-setting startup exits 2
with the expected required-expiry message, not an import error. All ten app-style
setting names with dummy managed-identity values pass configuration and reach
SQL authentication (network none, exit 2 InterfaceError, as expected).

Against a task-owned local SQL Server, installed the actual pre-#525 SQL text
from `9bfed518^`, constructed one synthetic case/allowlist row, and ran the
unmodified main image. It exits 2 with SQL ProgrammingError. Direct local
driver trace reports `Invalid column name 'documents_json'`. Applying the
current SQL template to that local database makes the SAME image/settings
serve on 0.0.0.0:8089 with health 200, shell 200, unsigned view 401, wrong
host 403, and the image's configured HTTP healthcheck command 200.

Reflection: the image has a deployment prerequisite, not a missing mandatory
chat setting. No runtime fallback or broader SQL permissions are justified.

#### Wave 3: Contrarian

Challenged import, timezone, port, probe and new-setting theories by starting
the exact unmodified main image successfully after only changing the local
view. Callback agenda remains opt-in; its absence is not fatal. AI is disabled
by default; no model setting is required. Dummy managed identity cannot prove
Azure authentication. The failed revision has no console traceback, so the
cloud's actual schema, expiry, secret resolution and connectivity remain
unverified. SecretRef serialization drift is a separate historical hypothesis,
not needed to produce the demonstrated local termination.

An initial external harness mistakenly used the host-published SQL port inside
the SQL container network namespace. Its OperationalError result is retained
in resident-sql-probe-original-port-error.json, not used as causal evidence.
Corrected only the harness to container-local 1433 before the comparison.

Reflection: local evidence strongly isolates a sufficient failure cause but
does not prove it was the unique cause of the historical Azure failure.
Stop: named questions answered to the authorized local boundary; cloud checks
cannot be performed under this task.

## Evidence Log

| ID | Finding | Source | Confidence |
| --- | --- | --- | --- |
| C1 | Image context src/, entry module resident_demo, non-root, port 8089 | src/api/Dockerfile.resident-demo:1 | High |
| C2 | Ten runtime settings; read-only SQL managed identity; min0/max1 | infra/resident-demo.bicep:132 | High |
| C3 | Deployment helper changes only fixed resident-owned resources | infra/scripts/resident_demo_deploy.py:1 | High |
| C4 | Main image built; console unavailable on failed revision | Prior redeploy changes and resident-activation-log-summary.json (external local evidence above) | High for recorded result, not causal proof |
| C5 | Startup validates settings, reads list_rows before binding | src/api/src/zava_forward/api/resident_demo/__main__.py:26 | High |
| C6 | Reader explicitly selects documents_json; #525 added it | src/core/src/zava_forward/core/resident_showcase_sql.py:24; git show 9bfed518 | High |
| C7 | Current view defines document projection, prior view does not | infra/sql/resident-showcase.sql:183; git show 9bfed518^:infra/sql/resident-showcase.sql | High |
| C8 | No mandatory agenda/AI setting | src/api/src/zava_forward/api/resident_demo/__main__.py:32; src/api/src/zava_forward/api/resident_demo/aoai.py:238 | High |
| C9 | Same main container fails old view and serves with current view | External session files/resident-sql-probe-main-d70ee60a.json and resident_sql_probe.py | High, local only |

No external web sources used. External local probe files are under
`/home/azureuser/.copilot/session-state/f568fbf4-e1b7-45d5-ae08-d7034d24a85b/files/`.
Main image ID:
`sha256:e7308bca68dc315405b2054f51497d0eb02fe33c21c8c4b6e21d485abfc6def2`.
Image ID differs from the prior rollout build; this is a fresh same-source
build, not a claim of byte-identical rebuilt dependencies or prior image.

## Alternatives and Decision State

Selected: document the required SQL-view update before an image-only rollout
and add a real local SQL regression that rejects the old projection and proves
restoration by the current template. No new required app setting was found.

Rejected: adding a mandatory agenda/model setting (C8), changing the port/probe
(C9), silently substituting empty documents or broadening SELECT grants
(would hide missing facts/alter the safety boundary).

Deferred: live schema/secret/auth/connectivity confirmation and any rollout
require separately authorized work. Q1-Q3 answered locally (C5-C9). No production
code bug was demonstrated; do not make a speculative runtime change.

## Planning Readiness

Ready. Research disposition: executed, Complete. Parent transition to Plan.
Self-check: three ordered inline waves complete; alternatives challenged;
observations distinguished from Azure hypotheses; no secrets or private data.
