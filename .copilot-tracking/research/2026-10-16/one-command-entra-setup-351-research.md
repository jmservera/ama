<!-- markdownlint-disable-file -->
# Task Research: one-command-entra-setup-351

## Research Brief

2026-10-16, RPI research, Complete. Refs #351. Refs #344.
Output mode: convergence. Focused posture selected for the owner's bounded
infrastructure task. Evidence root: `.copilot-tracking/`.
Audience: the exercise operator and implementation reviewer.
Scope: one standard-library entry point, existing ama infrastructure, private
roster, Graph app roles, browser callbacks and isolated device-code login.
Non-goals: deployment, SQL staff writes, directory-wide consent, policy changes,
real legal approval, account creation or operational acceptance.

## Extension Registry and Participation

Repository instructions and ADR 0006 apply. RPI phase skills selected.
No research delegation: this is one continuous infrastructure/auth trace.
The owner expressly requested research, plan, implementation, review and PR;
non-interactive execution needs no ordinary phase prompt.
Manual-mode task progression is authorized by that full-task request; no
automatic follow-up session has been requested.

## Research Questions and Prior Knowledge Gate

* Q1: Why does callback repair fail? Answered by C1.
* Q2: How must #344 coexist? Answered by C2/C3.
* Q3: What can tenant post-work safely automate? Answered by C4/W1/W2.
* Read original case study, addendum, knowledge-base index, owner memory,
  housing-association primer, ADR 0006 and applicable repository guidance.
* Owner-supplied failure is confirmed by the UUID coercion, not a live probe.

## Research Cycle Log

### Cycle 1, Wider

Read initializer, creation helper, manifest, Container Apps and edge modules,
staff initializer and README. Reflection: callback-only repair cannot create
missing directory objects; SQL binding remains a different private-network job.

### Cycle 1, Deeper

Read #344's local branch and pending infra diff without modifying its worktree.
The remote branch is not published (fetch attempted and unavailable); local
branch plus uncommitted additive entry point are the available evidence.
Reflection: discover actual Front Door origin host links, not assumed suffixes;
preserve auth exclusions/token storage and use Standard forwarded headers.

### Cycle 1, Contrarian

Challenge "first matching app", replacing appRoles, rotating every run, printing
raw CLI errors, and auto-consenting broad Graph permissions. All are unsafe.
Private Key Vault may be unreachable from operator: support an explicit
Container App secret fallback; never weaken networking. Do not claim directory
read access proves write authority. Do not infer roles from private staff codes.
An older code/userId-only roster needs explicit role enrichment.
Reflection: fail ambiguous discovery, preserve unrelated grants/roles, report
human and SQL prerequisites; poll boundedly, never report false completion.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Non-UUID client values fail before discovery | infra/scripts/initialize-api-auth.py:94 | High |
| C2 | API auth has existing exclusions, token-store and bearer-only settings | infra/modules/containerapps.bicep:174 | High |
| C3 | Front Door links origin host to API; #344 adds an existing-app edge entry point and Standard proxy | infra/modules/edge.bicep:79; local feat/public-browser-access-344 infra/public-edge-existing.bicep and infra/modules/edge-existing-auth.bicep | High, pending branch work |
| C4 | SQL oid binding/restart is separate from enterprise-app assignment | infra/scripts/initialize-workbench-staff.py:267; infra/README.md:701 | High |
| C5 | Manifest defines eight persona roles; shell helper uses stable UUID5 role IDs | infra/entra/app-registration.json:11; infra/scripts/create-api-app-registration.sh:43 | High |
| W1 | Graph addPassword returns secret only once; delegated writes require authority as well as consent | https://learn.microsoft.com/en-us/graph/api/application-addpassword?view=graph-rest-1.0 | High; retrieved 2026-10-16 |
| W2 | CLI auth supports current Container App auth surface | https://learn.microsoft.com/en-us/cli/azure/containerapp/auth?view=azure-cli-latest | High; retrieved 2026-10-16 |

## Alternatives and Decision State

Accepted: standalone Python standard-library orchestrator, isolated Graph/login
profile, read-only operator management profile, tag/name API discovery plus
origin-linked Front Door discovery, additive registration/assignment updates.
Rejected: shell chaining, managed identity as a human registration, implicit
first match, automatic directory-wide admin consent, SQL from this operator.
Keep the old callback API for compatibility but route its CLI to the new tool.
Use manifest roles, stable legacy IDs and explicit per-entry roster roles.

## Risks and Remaining Evidence

Azure writes, tenant permissions, actual private roster and human sign-in are
unexecuted. Front Door origin matching cannot prove Private Link approval,
DNS/certificate readiness or end-to-end authentication. No real IDs, directory
payloads, secrets or emails belong in artifacts/logs. Generic portal URLs avoid
embedding object IDs. Admin consent remains an explicitly human action.

## Readiness and Self-check

Research disposition: executed. Planning Readiness: Ready.
All three waves complete; internal/external claims grounded above, alternatives
and remaining uncertainty explicit. No further discovery cycle would change
the bounded implementation; live acceptance is a later operator gate.

## Owner-Selected Implementation Continuation (2026-10-16)

Research disposition: reused with focused current-source inspection. Planning
Readiness: Ready. Main merged as d007c69 with both log sides retained.
The current PR #352 head was fetched read-only after its named remote branch
was unavailable. Unlike the earlier local snapshot above, the published
`infra/modules/edge-existing-auth.bicep` uses Custom X-Forwarded-Host and
X-Forwarded-Proto headers. Preserve that configuration; retain linked origin/
route validation for `--public-url` and legacy CLI delegation. No branch edits.

Installed core/agents/api editable with pip in a fresh isolated venv and
reproduced 169 infra tests with one failure: secret lifecycle inventory expected
a hardcoded URI despite the intentional secret-name parameter. Workflow
inspection also found three formatting failures in the newly added compiled
policy assertions. These are directly coupled CI regressions, not new scope.

Known live sentinel remains owner-supplied evidence, not a tenant inspection.
Mock cases now cover both creating a missing registration and finding an
existing one before wiring the real UUID client; no private roster or dataset.
Vault metadata listing is an endpoint preflight, not evidence of write
authority; post-probe races still require explicit handoff recovery.
