<!-- markdownlint-disable-file -->

# Task Research: employee-case-workspace

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher | rpi-research, inline |
| Status | Complete, deployed browser cause partly unresolved |
| Artifact path | .copilot-tracking/research/2026-10-27/employee-case-workspace-research.md |

## Research Brief

Find the actual employee case ZF-2026-0597 qualityPanel failure, empty
briefing and AI configuration cause. Prepare a source fix and redeploy
instructions, not an Azure deployment. Audience: owner and PR reviewers.
Output mode: convergence. Success requires real browser reproduction,
HTTP/static-path evidence, queue/identity tracing and exact employee AI
setting names. Synthetic data only.

## Research Parameters

Focused, selected by default for the owner's bounded failure report.
Scope: src/api, src/agents, src/core, relevant image/infra metadata and
component docs. External scope: read-only metadata for ca-cutover-test-demo-api
in ama and its public static responses. No .env, secret reads, private data,
Azure writes, resource deletion, uv or deployment. Local unit/browser checks;
at most one scoped changed gate for large changes, no full gate, per owner.
Resolved evidence root: .copilot-tracking/.

## Extension Registry and Provenance

| Kind | Candidate | Selection and authority |
| --- | --- | --- |
| Instructions | Repository guidance and /tmp/brief-common.md | Selected; src-only fixes, synthetic tests, existing branch and Refs PR |
| Skill | rpi-research | Selected; three-wave evidence synthesis |
| Skill | web-design-guidelines | Select before any web edit and review |
| Skill | redesign-existing-projects | Skip unless actual visual redesign is needed; preserve Fluent 2 |
| Specialist | RPI Researcher | Skipped; tightly coupled trace, handled inline |

## User Participation and Research Decisions

Full-loop execution and publication explicitly requested; no routine phase
confirmation needed. No issue number supplied; discover only directly relevant
issues. Repo clean, existing owner-created topic branch, no matching open PR.

## Direction Controls

Source repair, not deployment. Do not mask unknown deployed state with local
success. Verify the supplied global-function/load-order hypothesis rather than
assuming it. Keep assigned queue authorization and human approval unchanged.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Does the actual served case load all required helpers? | depth | Open |
| Q2 | Is the briefing queue empty because of role/identity mapping or code? | depth | Open |
| Q3 | Which exact employee AI settings are required, and which are deployed? | depth | Open |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, component README and
owner conventions. Supplied VM success is a starting claim, not HTTP/browser
evidence. Source base f183ba39. No prior implementation evidence reused.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Starting areas: employee web assets/static allowlist and server routes, briefing
provider/queue, synthetic owner seeds, image lineage and safe configuration names.
Reflection: current static handler has no asset-name allowlist; installed wheel
includes web/*. Scripts are synchronous classic scripts. Queue and briefing use
exact owner_code, independently of permitted all-case reads.

#### Wave 2: Deeper

Started src/api real API through its existing browser-check harness, installed
isolated pip editable core/agents/API distributions after ModuleNotFoundError.
Renamed a public test case to ZF-2026-0597, without reading a private dataset.
Chromium loaded all eight scripts HTTP 200, qualityPanel was a function,
and the complete case rendered. No pageerror; service-worker controller null.
Expected unconfigured law (503), regulatory capability (403), and initial
signed-out /api/me (401) are separate from asset loading.

Read-only Azure show pins revision 0000006, created 2026-10-25T12:18:25Z,
to digest 0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e.
Public /app returns platform 401 without a signed-in browser. Private ACR
metadata was denied by existing network policy; no relaxation attempted.
Read-only, exact-file container exec used PTY after plain CLI failed ioctl.
No application imports, database reads, .env, environment values or secrets.
The installed index DOES include /ops.js before /app.js. Installed ops.js is
readable and SHA256 d28b705ffa88f386cb1b23ca4db9be93dd09d2bcbc6ea2fee3a4f12d0e466cd3,
byte-identical to current source. panels/assistants/chat/timecapture also match.
Installed app.js matches git 7e95f022 (2026-10-20). Its index predates only the
new role-screens wiring, not ops.js. Installed server static handler matches the
current routing: /app -> index, / -> welcome, exact existing files, protected
scripts require a valid principal; no named ops denylist.
Reflection: old-image-missing-ops wiring is disproved for this serving revision.

#### Wave 3: Contrarian

Challenged the stale-image, service-worker, static allowlist and CSP hypotheses:
the serving image already wires matching ops bytes; source has no service worker,
same-origin scripts are permitted and static responses use no-store/nosniff.
EasyAuth excluded paths are health/ready/welcome/style/logo/sign-in, not employee
scripts. Authenticated browser request outcomes remain unavailable, so neither
transient request denial nor client blocking/parse failure can be asserted.
Current "Try again" only reruns route(), never refetching failed scripts.
Thus missing-script recovery is a real reproducible source defect even though
the owner's original exact HTTP/execution failure is not conclusively diagnosed.

Challenged "no programme work": briefing selects only exact assigned open cases;
all-case permission does not imply assignment. identity.bind uses unique
tenant+OID roster continuity, never email or role inference. Historical seed
merge deliberately inserted NO staff. That supports unbound Entra users having
no assigned cases, but does not prove this owner's current live mapping:
no private/live dataset was read. Synthetic bound/unbound tests will demonstrate.

Challenged "AI code broken": deployed env NAMES omit AI_ENDPOINT and both
AI_DEPLOYMENT names. Ai.configured is bool(AI_ENDPOINT); the displayed reason
therefore matches missing employee configuration. Resident assistant variables
are separate. Endpoint settings do not satisfy release/activation/identity gates.
Reflection: improve honest empty-assignment wording and document exact settings;
do not grant ownership, call a model or change release controls.

#### Parent Synthesis and Disposition

| Claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Image predates ops wiring | W1, W2 | Rejected | Exact serving index wires ops; bytes match source |
| Current case always fails | C1, W3 | Rejected | Real synthetic browser case renders |
| Retry recovers missing ops | C2 | Rejected | route-only retry never fetches missing dependency |
| Empty briefing means no programme cases | C3, C4 | Rejected | Scope is personal assignment only |
| AI absent due to employee settings | C5, W1 | Accepted | No AI_ENDPOINT configured |
| Exact original authenticated asset failure known | W3 | Deferred | Need owner's authenticated network/console evidence |

#### Cycle Re-entry Evaluation

No further in-scope source search can establish the unavailable authenticated
browser request. Local failure injection and regression tests can verify the
recovery defect. Ready for bounded implementation; live diagnosis remains an
explicit residual, not an invented root cause.

## Evidence Log

| ID | Location | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/index.html:34-41; server.py:234-250 | Classic script order, same shell, exact-file handler, no-store, same-origin CSP |
| C2 | src/api/src/zava_forward/api/web/app.js:182-186,453 | ReferenceError bubbles to route retry that cannot reload scripts |
| C3 | src/core/src/zava_forward/core/store.py:249-259,726-753 | Mine and briefing select owner_code == user.code and not closed |
| C4 | src/core/src/zava_forward/core/identity.py:169-223; .copilot-tracking/changes/2026-10-25/seed-demo-baseline-360-changes.md | Tenant+OID-only continuity; historical merge omitted staff |
| C5 | src/core/src/zava_forward/core/ai.py:24-39,46-62,128-129 | Employee endpoint/deployment/model-version and managed-identity settings |
| W1 | Azure management read, ca-cutover-test-demo-api in ama, 2026-10-27 | Exact revision/digest; environment names omit employee AI settings |
| W2 | Exact static files via read-only container exec, 2026-10-27 | ops/index/server evidence above; no data or secret access |
| W3 | Local Chromium through checks.design_system_browser_check.main, 2026-10-27 | Constructed ZF-2026-0597 renders; missing live authenticated evidence |
| W4 | Read-only Azure Cognitive Services account/deployment metadata in ama, 2026-10-27 | Employee account aif-cutover-test-rzsrg advertises https://aif-cutover-test-rzsrg.openai.azure.com/ but deployment list returns []; resident account aoai-resident-469 is separate, not an authorized fallback |

Delegation: inline; one tightly coupled evidence trace.

## Findings, Alternatives and Decision State

Selected: detect missing required scripts before rendering a workspace and offer
full-page reload preserving the deep link. Add actual HTTP/browser tests for
healthy and missing ops loads, plus bound/unbound identity briefing tests.
Change misleading "No open cases." to explicit assignment scope. Document
employee AI settings and safe redeploy checks in the component README.
Rejected: duplicate qualityPanel, make static assets public, loosen CSP/auth,
auto-assign seeded work by role/email, auto-enable AI, or deploy.
Residuals: exact live failed request and current owner mapping unobserved.
W4 acquired while preparing exact configuration instructions: approved employee
model deployments are absent, not merely environment names. Setting the endpoint
alone would not restore inference. No provider task was called or provisioned.
No user/human/WCAG, deployed regression, real inference or whole-issue acceptance.

## Planning Readiness

Ready for scoped source work. Research disposition: executed, complete.
Self-check: all questions mapped; unobserved live data is explicit; wider,
deeper and contrarian waves completed. Existing source/read-only metadata are
adequate for the scoped plan; no further deployment or private-data access.
