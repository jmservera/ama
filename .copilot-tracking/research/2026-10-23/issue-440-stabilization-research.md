<!-- markdownlint-disable-file -->

# Task Research: issue-440-stabilization

| Field | Value |
| --- | --- |
| Date | 2026-10-23 |
| Researcher / agent | RPI Agent / activated rpi-research |
| Status | Complete (research only; checkpoint execution blocked) |
| Artifact path | .copilot-tracking/research/2026-10-23/issue-440-stabilization-research.md |

## Research Brief

* What to research: issue #440 recurring stabilization behavior and the first bounded current-main checkpoint.
* Why it matters: prevent merged-child counts from obscuring failing journeys and requirements drift.
* Audience or intended use: owner and backlog coordinator; prepare planning.
* Scope: existing coordinator, delivery/parity evidence, BRD/PRD/ADRs, component guides and local gate.
* Non-goals: source feature changes, unrelated fixes, private data, Azure/Entra/Graph writes, paid inference, other worktrees.
* Criteria: genuine phased evidence, pinned source and versions, scoped closure gates, no invented acceptance.
* Requested outputs: research, plan/details and independent critique; implementation/checkpoint and Review only when prerequisites permit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1: checkpoint insertion and retained safeguards; Q2: traceability and bounded test ladder; Q3: concurrency and execution readiness |
| Codebase scope | THIS worktree, existing coordinator and directly related evidence |
| External scope | GitHub issue/PR metadata only |
| Initial internal candidate areas | .github/agents/ama-backlog-delivery-coordinator.agent.md; docs/architecture/; docs/brds/; docs/prds/; src/*/README.md; tools/rpi-checks.py |
| Initial external candidate areas | jmservera/ama#440 and existing open related issues |
| Research posture | focused |
| Posture provenance | named targets and bounded caller scope |
| Explicit limits / deadline | No heavy tests while #349 owns the lock; finish research/plan and stop, without polling |
| Posture-specific completion basis | Named scope and materiality |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints / excluded sources | No other worktrees or private datasets; no dependency installation absent manifest change or missing-dependency failure |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Supplied repository guidance | Branch, KB, evidence, local gate | Selected |
| Skill | rpi-research | Explicit user direction; activated | Three ordered research waves | Selected |
| Skill | hve-builder | Coordinator action/gate change; activated | Major, improve; workflow contract read | Selected; author/static/behavior/host stages pending candidate |
| Research specialist | hve-core-all:rpi-researcher | Available registration | Independent lane evidence only | Skipped: continuous bounded trace handled inline |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit request to run full ordered loop, with busy-lock stop condition | No clarification needed | Execute eligible phases; do not invent later phases |

## Scope and Success Criteria

* Preserve original case study, memory, frontmatter/capability surfaces and all existing issue criteria.
* Separate main assessment from candidate-policy validation.
* Every outcome must resolve to observed evidence or an explicit unmet gate.

## Task Research Requests

* Recurring checkpoints before epic closure, after each wave (cap eight, not fill), earlier on material drift/regression.
* Local-first focused fix loops; final exact-head full gate remains mandatory.
* Existing #349/#350/#360 acceptance gaps stay open.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
| --- | --- | --- | --- |
| narrow | Use only supplied isolated worktree and branch | Caller | No checkout/worktree mutations elsewhere |
| exclude | No concurrent gate, cloud actions, paid inference or private data | Caller | Busy lock blocks execution and publication |
| add | HVE Major improve with independent static, tester and host validation | Caller | No prose-only pass |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Where must recurring checkpoints integrate without weakening existing safeguards? | depth | H | answered |
| Q2 | Which existing evidence, requirement IDs and local tests bound the first checkpoint? | depth | H | answered for planning; runtime outcomes unavailable |
| Q3 | Can execution and publication proceed without conflicting with #349? | straightforward | H | answered: no |

## Prior Knowledge Gate

* Verified clean branch test/stabilization-checkpoints-440, HEAD and freshly fetched origin/main both 140d8f494482c78e84d15f3d46b9223d3c487af0.
* gh issue view 440 --repo jmservera/ama --json number,title,body,state,url returned the complete current issue body; OPEN.
* No existing PR for this branch (all states).
* Read memory and original case study; addendum and index reading in progress.
* ps/stat/lslocks independently confirm supplied gate ownership: PID 3256519 running tools/rpi-checks.py --all at the supplied main base, holding WRITE FLOCK /tmp/ama-rpi-heavy.lock. Its output is not read or reused.

## Research Cycle Log

### Cycle 1

* Active controls: focused, local-only, busy-lock stop.

#### Wave 1: Wider

* Inline: establish issue, branch/base, canonical context, coordinator baseline and HVE workflow.
* Reflection: existing per-issue RPI and exact-head safeguards already exist. Recurring integration checkpoints must complement rather than replace them. Busy lock prohibits first-checkpoint execution now.

#### Wave 2: Deeper

* Parent-prioritized Q1/Q2: read coordinator through workflow completion, BRD/PRD status and requirement rows, ADR 0001 to 0006 status and applicable runtime sections, parity matrix and component guides, Source CI and actual runner control paths.
* Inline evidence: C4-C13 below. BRD v0.19.0 is draft and PRD v0.18.0 is a candidate, not the accepted historical v0.12.0. Requirement IDs must be document-qualified.
* Existing auth tests use actual loopback HTTP but constructed platform principals. Existing package/importer/orchestrator tests can cover structural boundaries without claiming deployed workers.
* Reflection: add checkpoints around wave/closure selection and loop continuation, not a new per-edit full-gate requirement. Reuse cutover evidence pack for dated current-main checkpoint results, with package guidance and KB index/log updates only as directly necessary.

#### Wave 3: Contrarian

* Challenge: can old welcome 200, a merged migration, or local auth tests establish current deployed success? Read the parity matrix's dated failures, complete current #349/#350/#360 bodies, and auth tests' constructed principal setup after the Deeper wave. No: source-level HTTP checks bypass the actual platform/tenant and cannot reproduce or dismiss the documented browser API 302 gap.
* Challenge: does USD700 permit Azure residual execution? Read addendum lines 326-443. No: outside-group term U and post-change forecast remain unknown; expiry is unchanged. Local readiness must not become a paid-action prerequisite or paid authority.
* Challenge: does a smaller/core refactor follow automatically from a large shared core? ADR 0006 explicitly accepts the cohesive core and maintenance trade-off; no demonstrated behavior defect justifies a manufactured refactor.
* Challenge: run a queued full gate while #349 proceeds? Actual runner defaults to up to 600s waiting, so even invocation would violate caller's no-enqueue/no-poll direction. Do not run it.
* Reflection: preserve all original adverse evidence and classifications. No confirmed new code defect from static planning; no follow-up bug issue warranted yet.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Disposition | Rationale | Treatment |
| --- | --- | --- | --- | --- |
| Add recurring scoped checkpoint | C1, C4, W1 | accepted | Existing per-PR gates do not provide wave/epic reconciliation | Plan existing-agent mutation |
| Pin requirements and architecture as versioned source, not approval | C5-C8 | accepted | Candidate/proposed and accepted status differ | Plan explicit traceability rows |
| Old deployed observations prove current main | C9, W2-W4 | rejected | Historical source/image/session boundaries differ | Preserve gaps, no total pass |
| Azure unknown blocks all local work | C10, W1 | rejected | Only paid/live residuals blocked | Independent local lanes continue |
| Mandatory new refactor | C8 | rejected | No reproduced defect or demonstrated boundary failure | No manufactured code issues |
| First checkpoint runtime execution | W1, preflight log | deferred | PID3256519 owns lock | Stop after Plan/critique |

#### Cycle Re-entry Evaluation

* Another complete cycle needed: no for the bounded policy plan.
* Stop basis: named contracts and test mechanisms sufficient for planning; actual behavior evidence is an execution prerequisite, not a question solved by more source reading.
* Re-entry trigger: changed main/requirements/approved source scope that invalidates this plan.
* Readiness effect: Ready for Plan, not execution or publication.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Existing coordinator requires per-issue RPI artifacts and external exact-head full receipt | .github/agents/ama-backlog-delivery-coordinator.agent.md:16; :210 | view | high | Preserve |
| C2 | Original business brief retains human investment and resident-consent boundaries | docs/case_study_48_original.md:24 | view | high | Immutable |
| C3 | Local fixtures are not delivered real-AI/SQL/Azure acceptance | docs/case_study_48_addendum.md:185 | view | high | Preserve separation |
| C4 | Wave selection and loop continuation currently lack explicit recurring stabilization decision | .github/agents/ama-backlog-delivery-coordinator.agent.md:172; :306 | view | high | Existing issue/merge safeguards remain mandatory |
| C5 | BRD draft v0.19.0 adds unmet Tokenomics metering/value requirements | docs/brds/agentic-retrofit-programme-brd.md:7; :30; :1496 | view/rg | high | BRD FR-052/NFR-012; existing #432, not a new bug |
| C6 | PRD candidate v0.18.0 distinguishes optional assistance/manual path from accepted real-AI build | docs/prds/zava-forward-retrofit-programme-demonstrator.md:7; :865; :881 | view/rg | high | PRD FR-003/028/044/045/046/047 |
| C7 | ADR 0001 proposed estate differs from ADR 0002 shared API realization | docs/adrs/0001-azure-architecture.md:11; docs/adrs/0002-pilot-readiness-architecture.md:135 | view | high | Do not call worker skeletons full integration |
| C8 | ADR0006 accepted split permits temporary API->agents and cohesive core; forbids workload->API | docs/adrs/0006-src-layout-and-cutover.md:11; :132 | view | high | Structural tests in all five packages |
| C9 | Deployed row audit remains bounded with many unverified features | docs/architecture/mvp-to-src-parity-matrix.md:45; :89 | view | high | Old 200/redirect is not current acceptance |
| C10 | Replacement all-in ceiling expires unchanged; U/post-change forecast unknown | docs/case_study_48_addendum.md:335; :395 | view | high | No cloud inquiry/action performed |
| C11 | Current commands install distributions and use test-fixture-only paths; complete runner owns local disposable resources | src/README.md:35; :47; :75 | view | high | No private default data, no mvp workaround |
| C12 | Auth HTTP tests use synthetic trusted principals, check public welcome/protected app and API denial | src/api/tests/test_auth.py:289; :310; :402 | view | high | Source inspected, not executed |
| C13 | Runner uses offline Bicep, local SQL/browser/images, --extra-test selectors and shared-lock wait | tools/rpi-checks.py:1142; :1676; .github/workflows/src-ci.yml:270 | view | high | Do not invoke busy gate |
| C14 | ADR0003 accepted with IoT amendment; ADR0004 accepted staged; ADR0005 synthetic development only | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:9; docs/adrs/0004-per-user-agent-chat-and-memory.md:9; docs/adrs/0005-regulatory-compliance-assistant.md:9 | view | high | No live/human approval inferred |
| C15 | Import transport, queue/workload deployment and approvals remain unbuilt/unverified separately from local library | src/importer/README.md:9; src/orchestrator/README.md:9; src/agents/README.md:39 | view | high | Execute existing local tests, retain deferred classification |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| W1 | Current acceptance and concurrency boundary | Issue #440, full body via gh | https://github.com/jmservera/ama/issues/440 | 2026-10-23 | current | high |
| W2 | Tenant/session and role acceptance remain open | Issue #349 full body via gh | https://github.com/jmservera/ama/issues/349 | 2026-10-23 | current | high |
| W3 | Browser JSON API302 and deployed parity gaps already tracked | Issue #350 full body via gh | https://github.com/jmservera/ama/issues/350 | 2026-10-23 | current | high |
| W4 | Direct demo live criterion d unmet; documentation f ticked only | Issue #360 full body via gh | https://github.com/jmservera/ama/issues/360 | 2026-10-23 | current | high |

### Contradictions / Conflicts

* API guide retains historical deployed successes and later parity audit records unresolved deployment gaps. Preserve their dates; do not silently resolve the apparent conflict by treating historical successes as fresh observations (C9, W2-W4).
* ADR0001 future per-workload identities are not the implemented ADR0002 shared-process realization (C7, C8); assess each against its own status.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Readiness implication |
| --- | --- | --- | --- | --- |
| Q3 | Heavy execution blocked by actual #349 lock holder | W1; direct ps/lslocks observation | high | Research/plan only until lock released |
| Q1 | Integrate recurring reconciliation at wave and epic boundaries while retaining per-issue gates | C1, C4, W1 | high | Ready to plan narrowly scoped agent change |
| Q2 | Existing component and Source CI contracts supply ladder; no runtime results available now | C5-C15, W2-W4 | high | Pin exact source and report Not run/Blocked |

## Key Discoveries

* Lock ownership is verified, not inferred from file existence.
* No current-main test, browser, SQL, Docker or candidate-policy validation has run.
* Open-issue dedup inventory is persisted in issue-440-open-issues.json; #349/#350/#360 and #432 already own named gaps. No new issue created.

## Alternatives and Decision State

* Preserve per-issue gates and add scoped checkpoints, rather than replace receipts or freeze the entire repository.
* Selected recommendation: improve existing coordinator with operational pinned checkpoint records and a local-first ladder; execute only after lock release. Add dated actual results to existing cutover evidence pack, not a competing acceptance document.
* Rejected alternatives: new coordinator/feature architecture (unnecessary); whole-repository freeze (violates scoped gate); per-edit full gates (defeats local fix ladder); historic receipt reuse (wrong source identity).

## Open Questions, Risks, and Residual Uncertainty

* No new tests run; no current-main product acceptance established.
* First checkpoint and candidate validation are distinct future evidence boundaries.

## Current Decisions

* Finish eligible research and plan/critique under explicit caller busy-lock direction.

## Unresolved Decisions

* Owner alone may approve pivots or requirements relaxation.

## Potential Next Research

* Complete named requirement/ADR/README inspection, not unrelated backlog discovery.

## Planning Readiness

* Status: Ready for Plan.
* Research disposition: executed; Wider, Deeper and Contrarian completed in order.
* Basis: C1, C4-C15 and W1-W4.
* Implementation/checkpoint blocker: heavy-lock-349, confirmed active; no tests scheduled.
* Current-main pinned source: 140d8f494482c78e84d15f3d46b9223d3c487af0, same as candidate branch HEAD before evidence writes.

## Pinned Document Identities

Git blob identities at pinned main, in command order from git rev-parse origin/main:path:

| Document | Status/version at source | Git blob |
| --- | --- | --- |
| docs/brds/agentic-retrofit-programme-brd.md | draft 0.19.0, 2026-10-22 | e96c4b16010f47a8ce01b29a9c208e4b3bb34319 |
| docs/prds/zava-forward-retrofit-programme-demonstrator.md | candidate 0.18.0, 2026-10-22 | a1fa17ab39924bb4bed7cd92c7bf2c8c79772410 |
| docs/adrs/0001-azure-architecture.md | proposed, dated amendments | 9f53b5b6ee36ff0a21854c3058e10c55e3bd7835 |
| docs/adrs/0002-pilot-readiness-architecture.md | proposed, dated realization | e6c8ce004e04dd0aeda3beafc01719ebe81c927a |
| docs/adrs/0003-journey-derived-capabilities-runtime-fit.md | accepted with amendment | 6044e1061f45964393e649aefa80b2293644d58f |
| docs/adrs/0004-per-user-agent-chat-and-memory.md | accepted staged | 259358e53e37ddeade73f9ee3aafd8dcacea20f9 |
| docs/adrs/0005-regulatory-compliance-assistant.md | accepted synthetic development only | 4d610335a5a18bb282e29c6cb3053404beda995d |
| docs/adrs/0006-src-layout-and-cutover.md | accepted | a5063f8f31c79044137b529145fbef7667841305 |

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete for bounded planning |
| Completed waves | Cycle1 Wider, Deeper, Contrarian |
| Lane evidence / inline fallback | Inline; tightly coupled known-source trace, no research worker needed |
| Research disposition | executed |
| Planning Readiness | Ready |
| Blockers | heavy-lock-349 prevents checkpoint execution/publication, not Plan |
| Continuation owner | Owner-directed full-loop RPI Agent; next Plan/details and one independent critique |

## Advisory Next Step

Activate rpi-plan with C1/C4-C15, W1-W4 and the explicit busy-lock stop. Plan implementation/HVE/checkpoint honestly as future work; do not create changes or Review artifacts before those phases execute.

## Sources

Repository paths and W1 above. No public web or regulatory-currentness claims.

## Self-check

Opening state persisted during Research, before deeper exploration. Ordered cycle complete. Evidence IDs resolve to named paths/lines or full GitHub bodies. No implementation, runtime check, total acceptance claim, new bug, or fabricated phase result.

## Actual Command Ledger and Pause Boundary

| Command / action actually executed | Result | Evidence classification / limitation |
| --- | --- | --- |
| gh issue view 440 --repo jmservera/ama --json number,title,body,state,url | exit0; complete OPEN issue body persisted in issue-440-current-issue.json | Local observed retrieval, not delivered tests |
| git status --short; git branch --show-current; git rev-parse HEAD | initial clean; supplied topic branch; head140d8f494482c78e84d15f3d46b9223d3c487af0 | Local observed metadata |
| git fetch origin main; git rev-parse origin/main | exit0 at intake and final planning validation; main remains140d8f494482c78e84d15f3d46b9223d3c487af0 | Source pin unchanged |
| gh pr list --head test/stabilization-checkpoints-440 --state all --json number,state,url,baseRefName | exit0; empty list | No PR for branch |
| ps -p 3256519 -o pid,ppid,etime,stat,args; stat /tmp/ama-rpi-heavy.lock; lslocks filtered for exact lock | PID3256519 running --all at pinned base, WRITE FLOCK; own persisted preflight timestamp2026-10-23T12:29:30Z | Local observed ownership; no release inferred, no later polling |
| gh issue list --state open --limit 200 --json number,title | exit0; persisted issue-440-open-issues.json | Dedup inventory, no new confirmed bug |
| gh issue view 349/350/360 --json title,body | exit0; complete current bodies inspected | Existing live gaps retained; no acceptance ticks |
| git log -12 origin/main; gh pr list --state merged --base main --limit 12 --json number,title,mergeCommit,mergedAt | exit0; merge candidates persisted | Scope inputs, not an executed checkpoint coverage claim |
| git rev-parse origin/main:<BRD/PRD/ADR path> | exit0; eight identities in pinned table | Local observed source versions, not approval |
| Python3 stdlib JSON/path/marker validation on own tracking files | exit0; state parses, all four pointers exist, plan/detail phase/task IDs match; changes/review pointers null | Tracking-only check, not application test |
| git diff --check | exit0 | Tracked-diff whitespace check only; new tracking files remain untracked |

First integrated current-main checkpoint: **Blocked / Not run**. No package
installation, application unit/static suite, HTTP/browser execution, SQL,
Docker, scanner, HVE candidate static/behavior/host validation, original RPI
Review or receipt execution occurred. No Azure observed result is asserted.
No new code bug/refactor was confirmed and no GitHub issue was created.

Research and plan/details are genuine completed phase evidence; the independent
plan critique is genuine and retains its original Revise verdict. Planner
resolved its two findings directly in the plan/details, not by changing the
critique or repeating it. Implementation and final Review remain absent.
All writes are this issue's tracking files in this worktree, uncommitted and
preserved. No KB/project/policy/source file was edited, so no material KB
change or corresponding index/log mutation occurred.

Resume: coordinator waits for #349 release, then P01-T01 checks actual lock
ownership and fresh main/ancestry before activating rpi-implement. Later
HVE/full-gate/publication stages remain unmet; no receipt path/hash or PR exists.
