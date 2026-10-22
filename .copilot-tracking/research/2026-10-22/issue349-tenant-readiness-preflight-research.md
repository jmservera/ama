<!-- markdownlint-disable-file -->

# Task Research: issue349-tenant-readiness-preflight

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-10-22                                                                            |
| Researcher / agent | RPI Agent (rpi-research, inline), Sonnet 5.5                                          |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-research.md |

## Research Brief

* What to research: whether the tenant blocker of #349 can be reduced before Blob live transport (#360) completes by a read-only capability preflight, and what that preflight can and cannot inspect with the current signed-in credentials.
* Why it matters: #349 acceptance (tenant setup, private credential delivery, real-user tests) needs an authorized tenant owner. A repeatable sanitized report separates absent, denied and unknown prerequisites from fabricated ones.
* Audience: the coordinator, the owner and an authorized tenant owner.
* Scope: `infra/scripts/initialize-api-auth.py`, `infra/scripts/create-api-app-registration.sh`, `infra/entra/app-registration.json`, `src/api/src/zava_forward/api/auth.py`, the live Container Apps auth configuration and Graph read capability.
* Non-goals: any tenant, app, role, staff, RBAC, ingress or infrastructure mutation; secrets, private roster or data; granting rights; closing #349; transport (#360) and costs (#126).
* Criteria: sanitized aggregate status only; no app IDs, object IDs, UPNs, tokens or credentials printed or committed.
* Requested outputs: research artifact and a justified implement/not-implement decision.
* Output mode: convergence.
* Owner decision (supplied, treated as data): the synthetic demo may match Entra roles from demo-tenant evidence, use random demo assignments when evidence is absent and a fixed admin ProgrammeManager; production roles are manually assigned through the Enterprise App. No directory-admin or professional approval is implied.

## Research Parameters

| Field                          | Value |
|--------------------------------|-------|
| Research question(s)           | Q1 to Q6 below |
| Codebase scope                 | infra/scripts, infra/entra, infra/tests, src/api auth |
| External scope                 | none (Azure CLI behaviour observed locally) |
| Research posture               | focused |
| Posture provenance             | parent selection from a bounded internal brief with named targets |
| Explicit limits / deadline     | read-only, offline-safe, no paid worker or Azure job, no private data |
| Edits allowed during research? | no, research-only |
| Resolved evidence root         | .copilot-tracking/ |
| Known constraints              | strict file ownership (no edits to setup-entra.py, staff_*.py, existing tests or docs) |

## Extension Registry and Provenance

| Kind        | Candidate                            | Match and provenance              | Disposition |
|-------------|--------------------------------------|-----------------------------------|-------------|
| Instruction | AMA repository instructions          | applyTo `**`                      | Selected: branch/PR, evidence and no-fabrication rules |
| Skill       | rpi-research                         | caller-required                   | Selected |
| Skill       | web-design-guidelines and web skills | no web file touched               | Skipped |
| Specialist  | RPI Researcher subagent              | lanes tightly coupled, low volume | Skipped; inline fallback |

## User Participation and Research Decisions

| Checkpoint  | Rationale                                        | Answers | Decision |
|-------------|--------------------------------------------------|---------|----------|
| Intake      | Non-interactive session; the brief is sufficient | n/a     | Proceed with focused research |
| Convergence | Non-interactive; no material fork                | n/a     | Select the standalone checker |

## Scope and Success Criteria

* Every question is answered with evidence or the smallest missing evidence.
* Live probes print only booleans, counts and classifications.

## Task Research Requests

* Determine whether Graph/app lookup, the intended single-tenant app, a valid UUID audience, app-role definitions and public callback configuration can be inspected; report absent, denied and unknown explicitly.
* Implement only if justified.

## Direction Controls

| Control | Direction | Source | Effect |
|---------|-----------|--------|--------|
| exclude | Private roster, `.env`, tokens, secrets, identities | caller | Probes use projections returning booleans/counts only |
| exclude | Editing existing files and owned areas | caller | New files only |
| narrow  | Bounded offline/read-only prerequisite slice | caller | No acceptance claim |

## Research Questions

| #  | Sub-question | Type | Priority | Status |
|---:|--------------|------|----------|--------|
| Q1 | What auth contract must the tenant satisfy? | breadth | H | answered |
| Q2 | What does the deployed API's auth configuration show now? | straightforward | H | answered |
| Q3 | Can Graph registration lookup be inspected with the current credentials? | straightforward | H | answered |
| Q4 | Which safe CLI patterns exist, and which commands must a read-only checker forbid? | depth | H | answered |
| Q5 | What is the non-destructive callback requirement? | depth | M | answered |
| Q6 | Is a new standalone checker justified without touching owned files? | breadth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: the current GitHub issue (open, no comments).
* Reused (verified): the 2026-10-16 observation that `ca-cutover-test-api` uses the literal `systemAssignedIdentity`, with no credential setting and token store off. Re-verified today (W1).
* Changed: the issue says read-only lookup with the isolated provisioning profile matched the tenant. Today's current credentials are denied for Graph (W2), so capability differs by credential.

## Research Cycle Log

### Cycle 1

* Active direction controls: all above.
* Posture and completion basis: focused; scope and materiality.
* Limits: none beyond the brief.

#### Wave 1: Wider

* Candidates: reuse `initialize-api-auth.py` helpers; extend `setup-entra.py`; extend the shell helper; write a new standalone read-only checker; document manual `az` commands only.
* Auth contract located: single-tenant manifest, eight app roles plus four capability roles, assignment required, callback path, token v2 (C1, C2). Role map and oid-only binding located (C3, C4).
* Live status, sanitized (W1): account signed in as a service principal; ingress external with an FQDN; auth enabled; clientId is the literal `systemAssignedIdentity` (not a UUID); no client-secret setting name; token store off; unauthenticated action redirects to login; forward proxy Custom; two allowed audiences.

#### Wave 2: Deeper

* Existing safe pattern: `az` with an optional isolated `AZURE_CONFIG_DIR`, `--query` projections, UUID validation and hostname validation (C5, C6, C7).
* Commands a read-only checker must forbid: credential reset with password output (C8), `az rest` PATCH/POST (C9), `az login` and profile directory creation (C10).
* Graph probes (W2): `GET applications`, `GET servicePrincipals` and a name-filtered application query each returned `Authorization_RequestDenied`. The registration, role definitions and callback list cannot be inspected now: status Denied, not Absent.
* Callback requirement: `https://<host>/.auth/login/aad/callback`; an edge host that differs from the ingress FQDN needs Custom forward proxy with `X-Forwarded-Host` and `X-Forwarded-Proto` (C7).

#### Wave 3: Contrarian

* Alternative: extend `initialize-api-auth.py --check`. Rejected: it needs Graph read, raises on the first failure so other statuses are lost, may run `az login`, and its sibling `setup-entra.py` is owned elsewhere (C5, C10).
* Alternative: document commands only. Rejected: today's denial and the literal `systemAssignedIdentity` must be reproducible and aggregated without a person pasting identities.
* Risk: the checker may be mistaken for acceptance. Mitigation: output states acceptance is not established; non-ready items are human blockers.
* Risk: Graph output holds identities. Mitigation: `$select` excludes credentials; only booleans, counts and role contract keys leave the process.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
|----------|----------|-------------|-----------|
| Standalone read-only checker `infra/scripts/tenant-readiness-preflight.py` | C5, C6, C10, W1, W2 | accepted | New file only; reuses patterns; reports denied/absent/unknown |
| Extend existing scripts | C5, C10 | rejected | File ownership and fail-fast behaviour |
| Documentation only | W1, W2 | rejected | Not repeatable |
| Per-assignment/staff inspection | C4 | rejected | Needs identities; roles are assigned by the tenant owner |
| Credential presence by value | C8 | rejected | Only a boolean "secret setting name present" |

* Re-entry decision: no further cycle; no substantial new material and remaining sources are redundant.

## Key Discoveries and Evidence Log

### Codebase evidence

| ID  | Finding | Location |
|-----|---------|----------|
| C1  | Manifest: single-tenant `AzureADMyOrg`, assignment required, callback path `/.auth/login/aad/callback`, token v2, eight app roles plus four capability roles | infra/entra/app-registration.json:3 |
| C2  | Shell helper builds `ZavaForward.<key>` roles for User members, `api://<appId>` identifier URI, token v2 | infra/scripts/create-api-app-registration.sh:72 |
| C3  | Runtime maps `ZavaForward.*` role values to workbench roles; capability roles separately | src/api/src/zava_forward/api/auth.py:32 |
| C4  | Staff matched only by `oid`; email fallback opt-in and off by default; unknown oid denied | src/api/src/zava_forward/api/auth.py:143 |
| C5  | Existing helper runs `az` with an isolated config directory and JSON output | infra/scripts/initialize-api-auth.py:11 |
| C6  | Auth read with a `--query` projection; clientId parsed as a UUID | infra/scripts/initialize-api-auth.py:89 |
| C7  | Edge callback requires Custom forward proxy headers; callback is `https://<fqdn>/.auth/login/aad/callback` | infra/scripts/initialize-api-auth.py:107 |
| C8  | Secret reset and vault write path; must never run in a read-only checker | infra/scripts/create-api-app-registration.sh:96 |
| C9  | Graph write via `az rest --method PATCH`; forbidden | infra/scripts/create-api-app-registration.sh:83 |
| C10 | `initialize` raises on first failure and can `az login` into a created profile | infra/scripts/initialize-api-auth.py:121 |

### Live evidence (2026-10-22, sanitized)

| ID | Finding | Source |
|----|---------|--------|
| W1 | Auth: enabled; clientId literal `systemAssignedIdentity`; no secret setting name; token store off; redirect-to-login; Custom proxy; two audiences | read-only `az containerapp show` and `auth show` projections, resource group `ama`, app `ca-cutover-test-api` |
| W2 | Graph `applications`, `servicePrincipals` and filtered application reads denied (`Authorization_RequestDenied`) for the current service-principal credentials | read-only `az rest --method GET` |

## Technical Scenarios

### Selected approach: standalone read-only readiness checker

* Default read-only; allowlisted `az` calls (`account show`, `containerapp show`, `containerapp auth show`, `rest --method GET`) with `$select` lists excluding credentials.
* Checks: tenant discoverable; ingress FQDN; auth enabled; audience UUID vs `systemAssignedIdentity` vs absent; secret setting name present (boolean); Graph application lookup by that UUID; single-tenant audience; `api://<client>` identifier URI; expected app-role contract; required callback present and forward-proxy requirement for an edge URL; service-principal assignment-required flag.
* Status vocabulary: `ready`, `absent`, `denied`, `unknown`, `mismatch`, `not-applicable`. Any non-ready item is a human blocker and exits non-zero. No remediation.

### Alternatives considered

* Extend setup-entra.py or initialize-api-auth.py: rejected (ownership, fail-fast).
* Documentation only: rejected.

## Potential Next Research

* Authorized tenant owner supplying the registration, roles, credential path and staff binding (human blocker).
* Blob transport (#360) for private credential delivery.

## Research Disposition and Planning Readiness

* Research disposition: executed (inline, one complete cycle).
* Planning Readiness: Ready.
* Human blockers outside this slice: tenant authority to identify or create the registration and roles; Graph read for the checking identity; private credential delivery (#360); staff reconciliation; real-user callback and denial tests.

## Self-Check

* Every finding has a C or W ID; no identities, UPNs, object IDs or credentials recorded; research-only held (no source edits).
