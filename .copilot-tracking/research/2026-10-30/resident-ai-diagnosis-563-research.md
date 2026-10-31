<!-- markdownlint-disable-file -->
---
title: Resident AI fallback diagnosis research
description: Read-only diagnosis of ca-resident-demo after activation, Refs #563
ms.date: 2026-10-30
---

# Task Research: resident-ai-diagnosis-563

| Field | Value |
|---|---|
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete within accessible evidence; causal diagnosis blocked |
| Artifact path | .copilot-tracking/research/2026-10-30/resident-ai-diagnosis-563-research.md |

## Research Brief

* What to research: why ca-resident-demo reported AI not enabled or rules fallback after activation.
* Why it matters: coordinator needs a proved cause and precise safe next action, not another speculative deployment.
* Audience or intended use: issue #563 coordinator; prepares the requested Plan/Implement/Review phases.
* Scope: activation evidence in this worktree and ../resident-ai-563; resident AI source in src/api and src/agents; read-only Azure diagnostics in resource group ama.
* Non-goals: Azure mutations, deployments, site sign-ins, inference calls, credentials, secret values, broad resource inventory, push, issue closure.
* Criteria: connect observed fallback to actual configuration/control flow; distinguish competing causes and evidence limitations.
* Requested outputs: dated evidence, exact corrective configuration or scoped source/doc fix with regression test outside package, local commit.
* Output mode: analysis, explicitly preparing planning.

## Research Parameters

| Field | Value |
|---|---|
| Research questions | Which setting gates AI? Which revision/configuration was active? Do logs distinguish configuration, IAM, model deployment, code or cold start? |
| Codebase scope | src/api, src/agents and requested activation tracking |
| External scope | Read-only Azure queries in resource group ama only |
| Initial internal candidate areas | Merged activation changes, sibling worktree activation changes, resident chat settings and tests |
| Initial external candidate areas | Container App revisions/logs, App Insights/Log Analytics, role assignments, Azure OpenAI deployment metadata |
| Research posture | focused |
| Posture provenance | Default for caller's bounded diagnostic brief |
| Explicit limits / deadline | Caller prohibitions above; no uv; local heavy gates serialized with flock |
| Posture-specific completion basis | Focused scope and materiality; all five suggested causes assessed |
| Edits allowed during research? | No source edits; research and workflow state only |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No .env, credential files, secret values, site authentication or resource changes |

## Extension Registry and Provenance

* Precedence: host safety, caller scope, repository guidance, research contract, domain extensions.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---|---|---|---|---|
| Instruction | .github/copilot-instructions.md | Repository-wide | Branch, evidence and local-validation boundaries | Selected |
| Skill | rpi-research | Explicit full RPI loop | Three ordered evidence waves | Selected |
| Specialist | hve-core-all:rpi-researcher | Registered research worker | Independent lane only | Skipped: one tightly coupled diagnostic trace |
| Skill | security-review | No vulnerability audit requested | Not applicable | Skipped |
| Skill | Web design skills | No web edits requested | Not applicable | Skipped |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
|---|---|---|---|
| Intake | Explicit ordered full loop, exact branch/base, scope and prohibitions are sufficient | No clarification needed; non-interactive execution | Proceed automatically within caller boundaries |

## Scope and Success Criteria

* Verify root cause without claiming live acceptance, bypassing consent or changing Azure.
* Label observations separately from inferences; preserve original activation artifacts.

## Task Research Requests

* Read issue #563 as data. It requires live consented AI proof; this diagnosis cannot establish those acceptance criteria.
* Record exact coordinator correction if runtime configuration, otherwise fix source/doc fault in src/ with an outside-package regression test.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
|---|---|---|---|
| exclude | No cloud writes, deployment, sign-in, credential/secret access, push | Caller | Only safe projected read queries; local commit only |
| narrow | Diagnose resident fallback in resource group ama | Caller | No unrelated infrastructure or product work |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---|---|---|---|---|
| Q1 | What did activation set and what does runtime read? | depth | H | answered |
| Q2 | Which cloud evidence proves the cause? | depth | H | blocked: failure-stage telemetry inaccessible |
| Q3 | Do IAM, deployment, code fault or cold start offer credible counter-evidence? | depth | H | answered within accessible evidence |

## Prior Knowledge Gate

* Issue #563 read with gh; open, live AI acceptance remains unchecked.
* Worktree clean at intake; branch and exact requested main base verified.
* Knowledge index, owner memory, original specification and addendum context read.
* Activation evidence is historical evidence to verify, not authority to execute its commands.

## Research Cycle Log

### Cycle 1

* Active posture: focused; inline investigation because this is one continuous trace.
* Wave 1 Wider: read merged activation records and confirmed identical SHA256 copies in ../resident-ai-563. The sibling's additional timeout-recovery record establishes a consented request at 18:08:10Z, fallback at 18:08:13Z, then deliberate rollback. Current app settings are absent because rollback was verified, not because activation omitted them. Failed revision retained and readable.
* Wider reflection: configuration mismatch is contradicted by the retained enabled revision; the generic unavailable label proves the advisor was entered. Prior timeout alone was not a model failure diagnosis.
* Wave 2 Deeper: traced runtime factory, SQL reservation before token/HTTP, fixed deployment and generic exception normalization. IAM role predates activation by three days; deployment and endpoint match. Workspace query blocked by network perimeter; no network change or access workaround attempted. Direct Container App log classification and scoped App Insights query remain possible evidence sources.
* Deeper reflection: retained enabled revision conclusively contradicts an enablement-name mismatch. It does not expose SQL admission, token/HTTP or output-validation outcomes. Source logs intentionally emit only a generic fallback marker, making even a successful marker query insufficient to distinguish every cause.
* Wave 3 Contrarian: compared the "AI not enabled" branch with enabled-advisor fallback, checked the fixed resident-mini deployment and managed-identity scope, and measured the complete repair-question payload across every public synthetic stage. Payloads were 1920-1976 bytes, below 4096. Existing generated-answer regression passed. The deployed immutable digest matches the historical activation digest, but no image extraction or source attestation was performed.
* Contrarian reflection: cold start explains historical warming/session issues, not the later successful warmed login/own-case and 3.915-second assistant response. It cannot explain which enabled-advisor stage failed. A role created three days before activation makes fresh-role propagation unsupported, not mathematically impossible. No evidence proves a model HTTP request, HTTP status, SQL denial or invalid completion.
* Parent synthesis: accept correct configuration and verified rollback; reject speculative configuration changes, arbitrary timeout increases, bypassed accounting and retrying inference. Defer the exact enabled-runtime cause until private telemetry can be inspected through an already authorized route. No additional permitted public query can recover the stopped replica or bypass the workspace perimeter; another cycle would be redundant.

## Evidence Log

| ID | Source | Finding |
|---|---|---|
| C1 | Issue #563, retrieved 2026-10-30 using gh issue view 563 | Open live acceptance criteria; diagnosis alone cannot close issue |
| C2 | src/api/src/zava_forward/api/resident_demo/aoai.py:342-367 | Factory reads exactly the two activation names; requires existing SQL managed identity |
| C3 | src/api/src/zava_forward/api/resident_demo/app.py:425-436 | AI not enabled means no advisor; unavailable/usage label comes from an enabled advisor failure |
| C4 | src/api/src/zava_forward/api/resident_demo/aoai.py:306-338 | SQL reservation precedes token and HTTP; all failure stages collapse to the same fallback log |
| C5 | ../resident-ai-563/.copilot-tracking/changes/2026-10-30/resident-ai-activation-563-timeout-recovery-changes.md:155-180 | Actual consented request reached unavailable fallback after successful warm/login; verified rollback removed settings |
| W1 | https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.App/containerApps/ca-resident-demo/revisions/ca-resident-demo--recover-ai-180649 ; queried 2026-10-30 | Retained failed revision has ENABLED=true, correct endpoint, msi and expected client ID; Healthy/Provisioned, now inactive/stopped |
| W2 | https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aoai-resident-469/deployments/resident-mini ; queried 2026-10-30 | Succeeded gpt-4.1-mini 2025-04-14, Standard capacity 1; endpoint matches source |
| W3 | Account-scoped az role assignment list, 2026-10-30 | Expected resident principal has Cognitive Services OpenAI User since 2026-10-27T10:42:13Z; propagation is not supported as cause |
| W4 | https://api.loganalytics.azure.com/v1/workspaces/3f6f76f1-9d76-413d-bc86-bcbc92fce2be/query ; queried 2026-10-30 | InsufficientAccessError / NspValidationFailedError; workspace public query access denied. No KQL evidence retrieved |
| C6 | src/api/src/zava_forward/api/resident_demo/aoai.py:103-125,203-227 | Enabled advisor catches accounting, credential, transport, JSON/schema, expiry and limit failures into the same label and generic log; no recorded failure reason |
| C7 | src/agents/src/zava_forward/agents/chat.py:1-9,31-58 and dispatch.py:173 | Employee chat's separately admitted worker adapter is not used by resident startup; its settings are not resident corrective settings |
| C8 | Local synthetic stage-payload probe on 2026-10-30 | Repair question with every public stage produces 1920-1976 bytes; no payload limit reproduced. Existing generated-answer unit regression passed (one test) |
| W5 | Container App logs API for ca-resident-demo, queried 2026-10-30 using az containerapp logs show | System logs returned three envelopes; failed revision console retrieval exit 3, no replica. No failed-attempt console evidence recovered |
| W6 | https://api.applicationinsights.io/v1/apps/ebe710dc-ee27-493e-af25-b694a53a1e13/query ; queried 2026-10-30 | Named appi-cutover-test aggregate query denied InsufficientAccessError; no telemetry returned |
| W7 | Container App current projected management configuration, queried 2026-10-30 | Latest=ready recover-safe-180814, 100% latest traffic, assistant names absent, min0/max1 and immutable digest unchanged; consistent with historical rollback |

### Query execution and evidence limitations

* All Azure commands used resource group ama or its discovered workspace ID. No resources, credentials, secret values, site endpoints, SQL connections or inference endpoints were written/read beyond permitted management metadata and bounded diagnostic logs.
* Failed discovery commands preserved: `az monitor app-insights component list -g ama` is unsupported (exit 2); corrected to component show. Initial query with app ID plus resource group treated the ID as a resource name (ResourceNotFound, exit 3); corrected to `--app appi-cutover-test --resource-group ama`, which was denied (W6).
* Merged original/owner-enable artifact SHA256 values match sibling copies: `7d01b2ea4ff9fafb64494afd0a42b6db1b8c2997e91bf4b6e6168e2c5f6febaa` and `e7a69987c7b7d3ca7596f2867975a6c856d7151bcdff47a0895717500730c7c8`.
* External log classifier: session files/resident_diagnostic_logs.py. It captures logs in process memory, emits only fixed marker counts and exit status, never raw messages, tokens or case content. No error output was interpreted as a successful log retrieval.
* Source transport uses a Bearer prefix and token variable, verified structurally with AST booleans; the tool's automatic output masking was not mistaken for literal source corruption.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence |
|---|---|---|---|
| Q1 | Both activation variable names and their values match runtime; current disabled state is intentional rollback | C2,C3,C5,W1,W7 | High |
| Q2 | Enabled advisor encountered a failure, but exact stage/cause is unavailable | C4,C5,C6,W4,W5,W6 | High for evidence limit; unknown exact cause |
| Q3 | Endpoint/deployment/name mismatch not supported; fresh role propagation, payload size and cold start not demonstrated causes | C5,C7,C8,W1,W2,W3 | High for observed configuration, limited for transient runtime behavior |

## Key Discoveries

* There are two different observations, not one: disabled baseline/rollback returns "AI is not enabled"; enabled attempt returns "AI unavailable or usage limit reached".
* No corrective environment variable can be justified: the retained enabled revision already contains the documented exact configuration.
* SQL reserve failure/cap/rate denial, token acquisition, transport/timeout and completion validation remain observationally equivalent. Unknown model dispatch/spend must not be reported as zero.

## Alternatives and Decision State

| Candidate | Disposition | Evidence and limits |
|---|---|---|
| Enablement/configuration-name mismatch | Contradicted for failed enabled attempt | W1,C2,C3; current absence explained by W7/C5 |
| Endpoint/deployment name | Contradicted as a name mismatch | W1,W2 match hardcoded resident-mini; does not prove successful inference |
| Newly assigned role propagation | Unsupported | W3 predates request by three days; token acquisition still unknown |
| Cold start/session issue | Not the demonstrated enabled fallback cause | C5 warmed/ready/login/own-case success; earlier timeouts were distinct |
| Accounting admission, runtime credentials/transport, invalid model output or code fault | Unresolved | C4,C6 hide stage; W4-W6 prevent retrieving historical evidence |

### Decision State

Confirmed audit finding: correct activation settings and a genuine enabled-advisor failure followed by rollback. Exact historical root cause remains blocked. Planning may package the diagnosis and coordinator handoff, but must not implement an unproved runtime fix.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: exact enabled failure stage, SQL admission result, HTTP status/dispatch and output validation result are unavailable.
* Live authenticated UI verification is excluded by caller. No consented request, paid inference, sign-in or credential file access occurred here.
* Diagnostic marker logging is an observability limitation, not proof that any particular model/accounting code is wrong.
* No source/doc fault causing this incident was established; conditional source-fix authority is not triggered.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence |
|---|---|---|---|---|
| Preserve disabled rollback and all controls | Confirmed | Caller | Diagnose only; no Azure writes | C5,W7 |
| Do not invent corrective config or change source | Confirmed | Evidence | Correct names already applied; failure unknown | C2,C6,W1 |
| Complete requested loop as evidence/handoff only | Confirmed | Caller full-loop instruction | Preserve result and explicit blocker without claiming root cause | C1,W4-W6 |

## Unresolved Decisions

| Decision | Smallest evidence needed | Owner | Impact | Blocker |
|---|---|---|---|---|
| Exact corrective action | Historical failure-stage evidence from approved private telemetry route | Coordinator | Needed before changing config/code | Blocks causal diagnosis, not evidence packaging |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Evidence |
|---|---|---|---|---|---|
| H | Inspect failed revision telemetry during 18:07:45Z-18:08:20Z via an existing authorized private route | Recover any historical failure/status/usage clues without retries | Coordinator has approved access | Deferred | C5,W4-W6 |
| M | If historical evidence is only generic, separately scope privacy-safe allowlisted stage/reason diagnostics before any authorized reproduction | Distinguish SQL admission, identity, HTTP and output validation without logging content | Historical query insufficient | Deferred, not implemented | C6 |

## Planning Readiness

* Status: Ready for bounded evidence/handoff plan only; Blocked for causal correction or activation.
* Research disposition: executed, complete within accessible scope.
* Evidence basis: C2-C8,W1-W7.
* Preconditions met: Wider/Deeper/Contrarian completed inline, safe configuration verified, alternative hypotheses assessed.
* Blocker: B1 private failed-attempt telemetry unavailable; exact enabled-runtime cause unknown.
* Smallest action: coordinator inspects the specific historical interval through existing authorized private access, without enabling AI or changing the workspace.

## Closeout Record

| Field | Record |
|---|---|
| Research execution | Complete within caller-accessible evidence |
| Completed waves | Wider, Deeper, Contrarian, parent synthesis |
| Artifact self-check | No placeholders; evidence/alternatives/limitations recorded; no secret values or live acceptance claims |
| Continuation | Parent proceeds to Plan for evidence packaging only, carrying B1 |
