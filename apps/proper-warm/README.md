---
title: Proper Warm Application PoC
description: Run and inspect the synthetic transactional retrofit workbench
ms.date: 2026-10-07
ms.topic: how-to
---

## Purpose and Boundary

This is a working local proof of concept, not the full PRD MVP or a production
service. It demonstrates one home lifecycle and representative paths across
nine workflows, using constructed cases only. The API owns state, control
gates and audit; the UI does not approve work by changing a filter.

Role selection is deliberately local impersonation, **not authentication**.
All approvals, consent records, referrals, installations and ledger entries
are exercise records. No resident is contacted, no supplier instructed, no
hazard clock controlled, no payment made and no claim submitted.

The evidence assistant is a deterministic simulator. It can assemble a cited
draft or create an owned manual fallback; it is not a deployed or evaluated
language model and is not proof of agentic autonomy.

* [Architecture, contracts, threat model and rubric gaps](../../docs/architecture/proper-warm-poc.md)
* [Created resource inventory and teardown](../../docs/architecture/proper-warm-resources.md)
* [Current PRD](../../docs/prds/proper-warm-retrofit-programme-demonstrator.md)
* [Versioned scenario and coverage manifest](./manifest.json)

## Start with Docker

Prerequisites: Docker Engine/desktop with Linux containers and Compose.
Run from the repository root in PowerShell:

```powershell
docker compose -f .\apps\proper-warm\compose.yaml config --quiet
docker compose -f .\apps\proper-warm\compose.yaml up --build -d
curl.exe --fail http://127.0.0.1:3410/health
node .\apps\proper-warm\scripts\verify-runtime.mjs
```

Open [http://127.0.0.1:3410](http://127.0.0.1:3410). The published port binds
only loopback. Do not change it to public ingress: there is no real identity.
Check the inventory first if project names, volume or port already exist.
Never adopt or delete another user's Compose resources.

### Synthetic Data Generator

The owner's generator is available under
`support\synthetic-data\retrofit-flow\proper-warm-year-one\generator`.
It was exercised with seed `1341953496` and `--dry-run`: 980 candidates,
13 observed tables and 23,528 total rows, with zero generator validation
errors. No existing pack or private answer key was overwritten.

The existing [year-one pack](../../docs/reference/research/retrofit-synthetic-data/manifest.json)
is analytical evidence, not an authority to approve work. This transaction PoC
deliberately retains the nine versioned, constructed acceptance fixtures.
It does not silently translate tracker status, contact outcomes or generated
ground truth into consent, safety clearance or release decisions. A reviewed
import/quarantine adapter remains a disclosed PRD gap.

To validate the local generator without writing any data, run from the root:

```powershell
python .\support\synthetic-data\retrofit-flow\proper-warm-year-one\generator\generate_pack.py --seed 1341953496 --dry-run
```

The generator is private working material and is not copied into the app or
container. Generation without `--dry-run` writes a pack and separate answer
key; use explicit new output paths rather than overwriting existing evidence.

```powershell
docker compose -f .\apps\proper-warm\compose.yaml ps
docker compose -f .\apps\proper-warm\compose.yaml logs --tail 20 app
docker compose -f .\apps\proper-warm\compose.yaml restart app
```

The named volume retains the database through restart and container recreation.
Seed data is created once, atomically, not overwritten on each startup.
An incompatible or unreadable database fails explicitly; it is not silently
replaced. All command writes use a transaction with event and replay records.

## Start without Docker

Node **24.18.0** is the validated runtime; `node:sqlite` is version-sensitive.
No npm install is needed; there are no third-party runtime dependencies.

```powershell
Set-Location .\apps\proper-warm
npm test
npm run evaluate
npm start
```

Native execution defaults to loopback, port 3410 and a local ignored database.
Do not run native and container copies on the same port. `DB_PATH`, `PORT`
and `HOST` are process configuration; container persistence uses `/data`.

Optional repeatable browser verification requires Python Playwright and its
Chromium runtime (already available in the validated workstation). With the
app running, from the repository root:

```powershell
python .\apps\proper-warm\scripts\verify-browser.py
```

This check deliberately adds sourced synthetic update/fallback events to
EX-HOME-900 and verifies a held-home rejection, exact lost-response retry,
export, filtering, drilldown and mobile reflow. It is not read-only and must
never target a live service. `--artifacts` optionally saves desktop/mobile
screenshots to an explicitly selected local directory.

## Two-Minute Demonstration

1. Start in the programme view. Filter to an exception workflow and select a
   home: show the blocker, current owner, evidence and resident update owner.
2. Select EX-HOME-531: the hazard hold blocks progression. A draft or receipt
   does not clear it. The linked hazard service keeps real clock authority.
3. Select EX-HOME-900: switch the labelled demo actor as prompted by the
   command form. Record sourced assessment, separate review/design, scoped
   decision, budget/funding/contract, committed capacity and work release.
   Advance only after each gate; submit installation as contractor, accept
   quality and handover independently, match invoice and retain resident update.
4. Send a handoff: receipt does not transfer ownership; acceptance does.
   Resident update ownership remains separate. Generate a cited assistant
   draft, then demonstrate failure/manual review without stage progression.
5. Export the record and show its version/events. Restart the container and
   confirm the same state. Cohort metrics reconcile to visible constructed cases,
   not an invented company improvement.

An unsatisfied gate intentionally returns an owned error. Read it, record the
missing evidence as the appropriate demo actor, refresh and retry. Do not
describe a denied action as a technical failure or bypass the gate for the demo.
The automated test suite exercises the longer happy path reproducibly.

## API and Retry Contract

GET `/api/config` is the canonical role/action/field/workflow contract.
GET `/api/cases`, `/api/cases/:id`, `/api/portfolio`, `/api/export`,
`/health` and `/metrics` expose constructed state and operational observations.
`workflow` and `q` filter list/portfolio consistently.

POST `/api/cases/:id/commands` accepts:

```json
{
  "action": "submit_assessment",
  "expectedVersion": 1,
  "idempotencyKey": "demo-assessment-001",
  "payload": {
    "evidenceId": "EX-SURVEY-900-V1",
    "reason": "Constructed survey ready for separate review",
    "source": "exercise:survey-900"
  }
}
```

Send `x-demo-role: assessor` plus the same-origin browser request headers.
The server rejects unknown fields, unauthorised actors, stale versions and
unsatisfied gates. GET reads default to viewer and are intentionally not
field-private; this is a synthetic workbench, not production privacy enforcement.

An idempotency key binds case, actor and canonical intent. Retries must reuse
the exact envelope/key, including expected version, after an ambiguous network
failure. Replays return the original committed response; refetch current case
before another action because later commands may have advanced it.
Same key with changed intent/actor is a conflict, never a second write.

POST `/api/cases/:id/assistant` has `mode` `draft`, `disabled` or `failure`.
Failure and disablement remain visibly failed and create deduplicated manual
review work; no success-shaped substitute draft is returned.

## Operations and Recovery

`/health` probes store readiness. `/metrics` and structured request logs expose
request status, latency and counts. They are local engineering observations,
not proof of customer SLOs or benefits. Request bodies, credentials and resident
data are not intentionally logged.

For a store error, stop writes and inspect the explicit error and container
logs. Preserve the named volume; do not reset it as a recovery shortcut.
An authorised operator may restore a consistent backup or intentionally reset
synthetic state, recording which state is lost. There is no production backup,
HA, legal immutability or disaster-recovery claim.

Normal stop preserves state:

```powershell
docker compose -f .\apps\proper-warm\compose.yaml down
```

Destructive reset is a separate human action. Confirm the owned volume name
against the inventory, export anything needed and then remove only that volume.
Do not use wildcard cleanup, `docker system prune` or broad deletion.
Image removal is optional and independent from stopping containers.

## Known Gaps and Release Gates

Workbook import/quarantine, bulk commands, full forecasts/history/heatmaps,
multi-measure gates, eleven complete staff workspaces, actual file uploads,
external system adapters and the full grant claimable/accepted/rejected
contract are not delivered. `claimed` is simulated submission only, never
acceptance or cash receipt. The manifest and architecture label partial coverage.

Cloud deployment requires real Entra identity and server authority,
managed relational persistence, evidence retention/access controls, verified
region/service/licence support, operational/legal/professional approval,
data protection and model evaluations. Do not lift this SQLite/demo-role image
into a publicly accessible or multi-replica Container App.
