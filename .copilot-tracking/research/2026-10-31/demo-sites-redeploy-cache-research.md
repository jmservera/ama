<!-- markdownlint-disable-file -->

# Task Research: demo-sites-redeploy-cache

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md |

## Research Brief

* What to research: reuse redeploy 7 procedure for immutable-cache redeploy 8.
* Why it matters: put merged #597 asset cache policy live without changing identity, SQL, AI or safety controls.
* Audience or intended use: owner and independent RPI reviewer.
* Scope: exact main d20bc50c, retained redeploy executors, both ama demos, private ACR, anonymous HTTP/browser receipts.
* Non-goals: signing in, model activation, source repairs, push, RBAC, endpoints, public SQL, RG deletion, private datasets or .env.
* Criteria: exact source/image binding, protected config/backups, short IP-only ACR window and exact restoration, both healthy, immutable asset headers and no-store HTML.
* Requested outputs: dated full-loop artifacts, command/result evidence and local Conventional Commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Safe reuse; SQL delta; cache verification and rollback boundary |
| Codebase scope | src/api, infra, named dated redeploy artifacts |
| External scope | Existing Azure resources only; no web research needed |
| Initial internal candidate areas | #596 changes and retained helper scripts; #597 source delta |
| Initial external candidate areas | Existing app/ACR readbacks |
| Research posture | focused |
| Posture provenance | Default for named operational procedure and failure evidence |
| Explicit limits / deadline | Owner deployment authority through 2026-11-15; local commits only |
| Posture-specific completion basis | Focused scope and materiality |
| Edits allowed during research? | No, except research and required workflow tracking |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | Secret-free artifacts; private config never printed; no .env |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository guidance | Supplied applyTo ** | Topic branch, private backups, local publication gates | Selected |
| Skill | rpi-research | Full loop explicitly requested | Focused three-wave evidence | Selected |
| Skill | rpi-plan / rpi-implement / rpi-review | Later phases | Canonical plan, critique, changes, single Review | Deferred to respective phase |
| Research specialist | RPI Researcher | Registered | Independent research lane | Skipped: tightly coupled retained-procedure trace |
| Skill | Web design skills | No web edits or design audit | Not a design/conformance task | Skipped |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit full-loop and deployment authority, no questions necessary | Owner supplied all material controls | Manual full-loop progression authorized; not automatic follow-up |

## Scope and Success Criteria

* Build tracked current-main source only; distinct tag, immutable target digests.
* Preserve both app auth/protected configuration, history, min0, all eight Manual jobs and full ACR private baseline.
* No SQL execution unless verified source delta touches SQL.
* Local image proof precedes live mutation and cannot trigger live compensation.
* Health warm-up uses long timeouts/retries; cold-start timeout alone is not failed deployment.
* Anonymous asset/header and dock evidence is not signed-in acceptance.

## Task Research Requests

* Current request and redeploy 8 addendum control the task.
* Original and #596 procedures are starting evidence, not permission to repeat SQL or faulty compensation.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| change | Use #596 corrected procedure | Owner addendum | Inspect concrete resource-relative verifier |
| narrow | SQL only if diff touches SQL | Owner addendum | Source-delta gate |
| exclude | Resident AI, sign-in, push, .env, RBAC and public SQL | Owner request | Hard boundaries |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Can retained executors safely target this source/release? | depth | H | answered |
| Q2 | Does source delta touch SQL? | straightforward | H | answered |
| Q3 | Can anonymous cache/dock evidence prove scoped acceptance without sign-in? | depth | H | answered with signed-in limit |

## Prior Knowledge Gate

* Required original/addendum, index and memory read; index first 90 lines.
* Original 2026-10-30 and #596 2026-10-31 changes read.
* Clean topic chore/ops-redeploy-cache, no open PR; fetched HEAD=origin/main=d20bc50c4b664521f72446e5d0c85cc576ef0850.
* Delta from 4cb5964f lists cache source/docs/tests only, no infra paths; inspect full diff before SQL disposition.
* Previous no-cache versioned assets and local-proof-triggered recovery are superseded behavior to verify, not repeat.

## Research Cycle Log

### Cycle 1

* Active direction controls: all above.
* Active research posture and completion basis: focused; source/procedure verification.
* Explicit limits or deadline effect: no push, no source repair or SQL without delta.

#### Wave 1: Wider

* Inline: identify prior outcomes, exact source delta, operational tools and helper dependencies.
* Reflection: cache policy is only expected live change; retained transitive helpers need inspection.

#### Wave 2: Deeper

* Inline retained ops/build/publish/pair-rollout/verify/compensate/preflight/export read, including all transitive executed function bodies.
* C1: src/api/src/zava_forward/api/static_assets.py:20-29 returns exact-current-version public,max-age=31536000,immutable; HTML always no-store.
* C2: src/api/src/zava_forward/api/server.py:259-276 protects employee chat/workbench resources; anonymous employee widget200 is not expected or permissible to create here.
* C3: .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md:121-146 documents concrete-subdirectory correction and local-proof/live-compensation separation, confirmed in retained verify.py.
* Reflection: build/image proof can be evaluated before registry/app writes; new exporter must not reuse historical SQL/recovery assertions.

#### Wave 3: Contrarian

* Full src/infra diff from 4cb5964f examined; no SQL/schema/migration/DDL changes. Q2 answered: skip init entirely, retain fresh eight-job config equality instead.
* Employee public shell has only authorized public assets; shared widget200 can be proven in packaged image, but live signed-in widget200 is unproven. Do not widen anonymous permissions.
* Cold-start curl28/124 has explicit 900s read-only convergence; local/admin/browser-tool defects cannot justify healthy-app compensation.
* ACR public window requires temporary exports enable in the retained supported procedure; restore exact baseline including exports/admin/default-action/rules after closing public first. Old/new config/index/platform chains verified during window.
* Reflection: one scoped deployment is supported; fallback/recovery paths remain unexercised unless genuinely needed.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Reuse guarded publisher and rollout | Retained #596 procedures / C3 | accepted | Same resources and controls, new source/root/tag only |
| Skip SQL | Actual full 4cb5964f..d20bc50c src/infra diff | accepted | No SQL touch; addendum overrides prior mandatory-init step |
| Immutable live versioned assets | C1 | accepted for verification | Exact actual headers must pass; HTML remains no-store |
| Anonymous employee widget200 | C2 | rejected as acceptance claim | Preserve auth; image bytes do not prove signed-in live access |
| Repeat broad compensation | C3 | rejected | Local proof outside live guard; diagnostic auth/nonconformance separate |

#### Cycle Re-entry Evaluation

* Another cycle needed: no; named scope and material questions covered.
* Q1/Q2/Q3 answered. Remaining live outcomes belong to implementation.

## Evidence Log

| ID | Evidence and retrieval | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/static_assets.py:20-29, read 2026-10-31 | Current-version immutable caching; HTML no-store |
| C2 | src/api/src/zava_forward/api/server.py:259-276, read 2026-10-31 | Employee widget resources remain protected |
| C3 | .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md:121-146, read 2026-10-31 | Known verifier corrections |

## Alternatives and Current Decisions

Use guarded local Docker build/push with shortest /32 window. Only if window impossible, evaluate owner-authorized az acr build within private baseline; never create networking/RBAC to enable it.
No source repair, init, AI enablement or signed-in exercise selected.

## Risks and Residual Uncertainty

Live startup/header outcomes are unmeasured until implementation. Prior raw config/backups stay private; no secret/body dumps to terminal or Git. No regulatory claim or public web source used.
Financial authorization is owner standing operational authority, not measured all-in headroom. Full local publication gate, hosted/human approval remain distinct and not claimed; no push requested.

## Planning Readiness

Ready. Research disposition: executed. Self-check: all three waves completed in order; scope, provenance, decisions, evidence and honest limits recorded. Canonical template sections condensed for this focused retained-procedure task.
