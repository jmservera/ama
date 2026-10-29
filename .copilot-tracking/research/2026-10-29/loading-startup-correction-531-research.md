<!-- markdownlint-disable-file -->

# Task Research: loading-startup-correction-531

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/loading-startup-correction-531-research.md |

## Research Brief

* What: audit all async feedback consumers, index script failure paths, and helper-loading pages before source edits.
* Why: correct retry residue and startup dependency failure without sibling regressions.
* Audience: correction implementation and independent review for PR #538, refs #531.
* Scope: src web assets, related tests/browser checks, manifest pins and component documentation.
* Non-goals: redesign, Azure operations, push, merge, issue closure.
* Criteria: sequential and overlapping attempts; blocked script downloads must reach an explicit terminal startup outcome.
* Requested outputs: complete audit, correction recommendation and regression design.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which controls and scripts share lifecycle failure risks? Which tests exercise real browser failures? |
| Codebase scope | src/api web and tests; tools browser checks; related manifests |
| External scope | Current Web Interface Guidelines only |
| Initial internal candidate areas | async-action.js, index.html, workspace-shell.js, other HTML pages and browser checks |
| Research posture | focused |
| Posture provenance | Default for explicit bounded correction |
| Explicit limits | No az, no push, no force-push; nonblocking heavy-suite lock |
| Completion basis | Full caller-specified loading surface covered with code evidence |
| Edits allowed during research | Evidence and workflow tracking only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and scoped authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository Copilot instructions | Project evidence, branch, validation and publication boundaries | Selected |
| Skill | web-design-guidelines | Current rules fetched before web changes | Selected |
| Skill | rpi-* | Requested complete correction loop | Selected per phase |
| Specialist | RPI Researcher | No isolated uncertainty warrants separate context | Skipped; continuous trace inline |
| Skill | redesign-existing-projects | No design or styling improvement requested | Skipped |

## User Participation and Research Decisions

Caller explicitly requests the full loop and local commits; treated as task-scoped automatic execution. No prior manual session is being switched. No routine phase prompts; noninteractive execution. Branch is clean, open PR matches work, and requested git pull --rebase completed first.

## Direction Controls

Audit before editing source. Source stays in src. Preserve existing approval boundaries. Commit original dated evidence; no publication is authorized.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How do every helper consumer and overlapping attempts settle status and controls? | depth | open |
| Q2 | What happens when each index script or helper script on another page fails? | depth | open |
| Q3 | Which existing validation and pins must change? | straightforward | open |

## Prior Knowledge Gate

Read original specification, addendum, knowledge-base index and owner memory. Supplied review findings are hypotheses to verify. Cross-session lookup found no recent matching session. Existing tracking and component guides will be checked against current code.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read every HTML script list under src/api/src and enumerated every AsyncAction
reference and h() click/submit/change binding. Read bootstrap, route guard,
watchdog, law entry point, helper and unit/browser harnesses. No research worker:
this is one continuous lifecycle trace. Reflection: the reported defects are
present; law.js itself also has no independent failed-download recovery.

#### Wave 2: Deeper

Helper keeps only pending promises, not settled notices. run() suppresses
same-control overlap but distinct controls and null-control reads overlap.
Sync throws create errors too; synchronous successes currently never clear them.
Direct feedback consumers (API and map) finish without retaining errors.
Central h() wrapping covers all companion action surfaces. Role/function checks
defer non-auth dependencies and keep bounded retry budgets. CaseWorkspace is
optional and already renders plain case sections when absent.

Reflection: retain promise deduplication and per-operation cleanup; track only
helper-owned notice disposal by control. Cleanup must happen before invoking
the next task, including synchronous outcomes. Main bootstrap must remove its
own static startup node as well as dispatching the existing ready event.

#### Wave 3: Contrarian

Challenged global-status removal: it would erase unrelated pending operations
and inline/action-owned errors. Reject it. Challenged adding workspace-shell to
the required dependency loader: startup should not depend on a watchdog that
has already failed; reject that in favour of independent main cleanup. Checked
other pages: law.html is the only other AsyncAction consumer, and law.js failure
leaves Loading sources forever. Reuse the existing independent watchdog for a
static law startup region and let law show() replace that region independently.
welcome.html has no scripts. Resident sites use separate helper contracts,
not AsyncAction/workspace-shell; no changes to those independent workstreams.

Reflection: cover one failed script at a time plus failed-watchdog and service
failure together, without claiming resilience if all independent entry scripts
fail simultaneously.

### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Per-control notice disposal | C1-C3 | Accepted | Does not conflate distinct control or null-control attempts |
| Independent main startup cleanup | C4-C5 | Accepted | Keeps successful/error outcomes independent of watchdog download |
| Law entry-point watchdog sibling | C6 | Accepted | Only other helper-loading page has same startup dead end |
| Reload watchdog as required dependency | C4-C5 | Rejected | Adds unnecessary dependency and fails to solve main ownership |
| Resident UI expansion | C7 | Deferred/outside scope | Separate apps, no shared helper, no caller-selected redesign |

Cycle re-entry: no. All requested surfaces are inventoried and material
questions answered. Contrarian checks introduced the law entry-point case,
resolved within the same bounded shared-watchdog contract.

## Evidence Log

| ID | Claim / finding | Workspace-relative location | Confidence |
| --- | --- | --- | --- |
| C1 | Settled errors are unowned; only pending promises are tracked | src/api/src/zava_forward/api/web/async-action.js:3 | High |
| C2 | All native factory click/submit/change consumers share helper lifecycle | src/api/src/zava_forward/api/web/app.js:15 | High |
| C3 | Direct read/map feedback owns separate completion and no retained errors | src/api/src/zava_forward/api/web/app.js:48; src/api/src/zava_forward/api/web/app.js:1631 | High |
| C4 | Main ready/error/login dispatch events but never removes startup itself | src/api/src/zava_forward/api/web/app.js:93; src/api/src/zava_forward/api/web/app.js:137; src/api/src/zava_forward/api/web/app.js:1538 | High |
| C5 | Watchdog alone removes startup and supplies deadlines when main fails | src/api/src/zava_forward/api/web/workspace-shell.js:3; src/api/src/zava_forward/api/web/index.html:18 | High |
| C6 | Law is only other helper-loading page; missing helper handled, missing law.js not handled | src/api/src/zava_forward/api/web/law.html:22; src/api/src/zava_forward/api/web/law.js:69 | High |
| C7 | Resident apps and welcome do not load shared loading helpers | src/api/src/zava_forward/api/resident_demo/web/index.html:57; src/api/src/zava_forward/api/resident_preview/web/index.html:36; src/api/src/zava_forward/api/web/welcome.html:1 | High |
| C8 | Existing script matrix and optional case fallback | src/api/src/zava_forward/api/web/app.js:221; src/api/src/zava_forward/api/web/app.js:938 | High |
| C9 | Existing browser and VM harnesses can extend coverage without new tooling | src/api/tests/test_loading_feedback.py:10; src/api/tests/test_workspace_scripts.py:11; src/api/checks/loading_briefing_browser_check.py:26 | High |
| C10 | Pins cover workbench recipe/fixture/navigation, not correction targets | docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:45 | High |
| W1 | Current interface rules retrieved, repository native/ASCII standards take precedence | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (2026-10-29) | High |

## Complete Startup Script Failure Inventory

| Page / script | Initial download failure and current terminal outcome | Correction / regression |
| --- | --- | --- |
| index: workspace-shell.js | Main works; stale static startup forever | Main-owned cleanup for signed-out, signed-in and error paths; blocked watchdog browser matrix |
| index: async-action.js | Bootstrap retries twice, checks all methods, native reload on exhaustion before API start | Preserve existing unit/browser failure matrix |
| index: vendor/leaflet.js | Route-gated retry on overview/coordinator, explicit reload on exhaustion | Include failed-download terminal matrix |
| index: panels.js | Case/finance route-gated retry then explicit reload | Include failed-download terminal matrix |
| index: ops.js | Case/capacity/contractor route-gated retry then explicit reload | Include failed-download terminal matrix |
| index: assistants.js | Case/assistant queue route-gated retry then explicit reload | Include failed-download terminal matrix |
| index: chat.js | Staff case route-gated retry then explicit reload | Include failed-download terminal matrix |
| index: timecapture.js | Time route-gated retry then explicit reload | Include failed-download terminal matrix |
| index: role-screens.js | Screens route-gated retry then explicit reload | Include failed-download terminal matrix |
| index: case-workspace.js | Optional enhancement, plain sections and explicit status remain available | Assert fallback with blocked script |
| index: app.js | Independent shell gives slow/deadline and native reload | Preserve existing failed/held script case |
| law: async-action.js | law.js validates interface before bindings/reads, native reload on failure | Preserve blocked/missing/partial interface cases |
| law: law.js | Static loading never settles | Reuse watchdog and native reload; blocked entry-point browser regression |
| law: watchdog (proposed shared reuse) | law show() replaces static region itself | Block watchdog and verify sources render without stale startup |

## Complete Helper Consumer Inventory

* Factory h(): login; route/startup retry; AI accept/edit/reject/cancel;
  briefing mode/refresh/dismiss; suggestions; queue load/reset; handover;
  case contact, message, summary and visit drafts; safety actions; return/reopen;
  documents/funding; coordinator/map filters and list navigation.
* Companion h() consumers: panels (stock/technical/resident/challenges/finance/
  grant forms and pagination), ops (quality/work orders/capacity/appointments),
  assistants (proposal requests/reviews/history/queue), chat (questions,
  proposals, regulatory alerts/chat), timecapture (request/enable/ack/save),
  case-workspace tabs/jumps. role-screens defines views via h() without direct
  helper ownership.
* Explicit handler(): queue filters/sort, CSV import, sign-out/switch-account;
  law source/provision/result/all/search actions.
* Explicit run(): debounced queue search and initial law read use null control,
  retaining independent overlapping operation notices.
* Explicit feedback(): api() and map draw, always settled in finally.
* Synchronous actions and handled errors retain their existing return/inline
  error contracts. Same-control async duplicate attempts return the same promise.

## Findings, Alternatives and Current Decisions

Q1 answered by C1-C3/C9: introduce per-control helper-owned disposal only;
preserve unrelated errors, independent operations and handler-owned states.
Q2 answered by C4-C8: main cleanup plus shared law watchdog addresses both
entry-point/watchdog halves; all other scripts already have explicit fallback.
Q3 answered by C9-C10: extend current VM/browser harnesses, run required
API/core strict/unit checks, update API guide; no pinned files need edits.

Risks: real screen-reader/voice, staff usability and hosted/live acceptance
remain unproven. Complete publication gate is not run because no publication
is requested and az is prohibited. Full suites require nonblocking heavy lock.

## Self-check and Handoff

Brief, three ordered waves, all script/consumer inventories, alternatives,
source IDs, constraints and evidence-backed readiness recorded. No source
edits during research. No material unresolved planning decisions.

## Planning Readiness

Ready. Research disposition: executed, Complete. Parent next action: Plan.
