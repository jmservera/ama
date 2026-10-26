<!-- markdownlint-disable-file -->

# Task Research: issue-350-demo-feedback-harness

| Field              | Value                                                                                  |
|--------------------|----------------------------------------------------------------------------------------|
| Date               | 2026-10-22                                                                             |
| Researcher / agent | rpi-research (RPI Agent, Sonnet 5.5, automatic single-task run)                        |
| Status             | Complete                                                                               |
| Artifact path      | .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md      |

## Research Brief

* What to research: Whether existing harnesses can already check the #350 "minimum owner-feedback release" prerequisites offline from explicitly supplied synthetic evidence, and if not, the narrowest contract for a new checker built on actual runtime schemas.
* Why it matters: Deployment is blocked on #349 (tenant/staff) and #360 (private transport). Offline work should reduce later live-acceptance effort without implying acceptance.
* Audience or intended use: Plan, implement and review phases of this task; later live-acceptance owners.
* Scope: `src/api/checks/`, `infra/scripts/`, `tools/`, `src/core` and `src/api` runtime schemas, the gate in `tools/rpi-checks.py`, the parity matrix and #350 body/comments.
* Non-goals: Live or authenticated execution, Azure/tenant/RBAC/staff/ingress writes, paid inference, credentials, API/web/core/infra changes, edits to `tools/rpi-checks.py`, workflows, knowledge-base index/log, addendum or parity matrix. Not closing or claiming any #350 criterion.
* Criteria: Every claim cites a `path:line`; no invented API shapes; pass/fail/blocked/not-run kept distinct.
* Requested outputs: Reuse-versus-gap decision and a contract for the new checker.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                   |
|----------------------------------|-----------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q6 below                                                                             |
| Codebase scope                   | `src/api`, `src/core`, `infra/scripts`, `infra/tests`, `tools`, `docs/architecture`     |
| External scope                   | #350 issue body and the 2026-10-22 owner comment                                        |
| Initial internal candidate areas | `src/api/checks/*.py`, `infra/scripts/private-cutover-proof.py`, `tools/rpi-checks.py`  |
| Initial external candidate areas | GitHub issue #350                                                                       |
| Research posture                 | focused                                                                                 |
| Posture provenance               | caller-specified (narrow offline harness, named sources)                                |
| Explicit limits / deadline       | Offline only; owned-file boundary; retained cost authorisation expires 2026-10-25T16:02Z (irrelevant to offline work) |
| Posture-specific completion basis| Scope and materiality: named source targets covered, material claims evidence-backed    |
| Edits allowed during research?   | no, research-only (tracking artifacts only)                                             |
| Resolved evidence root           | .copilot-tracking/                                                                      |
| Known constraints / excluded sources | Private datasets, deployed endpoints and credentials are excluded                   |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions; rpi-research contract; domain skills and specialists.

| Kind                | Candidate                                   | Match and provenance                                          | Scoped authority or output contract                       | Selected / skipped reason                                   |
|---------------------|---------------------------------------------|---------------------------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------------|
| Instruction         | AMA repository instructions (`applyTo: **`) | Matches every path                                            | Branch/PR, regulatory, evidence and gate conventions      | Selected                                                    |
| Skill               | web-design-guidelines, design-taste-*       | Web skills; this slice has no web files                       | Web design review                                         | Skipped: backend/tooling-only, exempt per repository text   |
| Skill               | rpi-research                                | Caller-requested phase                                        | Research artifact contract                                | Selected                                                    |
| Research specialist | RPI Researcher                              | Lanes are small, tightly coupled, low volume                  | Delegated lane artifacts                                  | Skipped: inline fallback, no independent lane justified     |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                      | Answers / unanswered | Resulting decision or selected further research |
|------------------|--------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------|
| Intake           | Non-interactive run; the prompt fixes scope, ownership, offline boundary and deliverables  | n/a                  | Proceed with focused posture                     |
| Direction change | None                                                                                       | n/a                  | None                                             |
| Convergence      | Non-interactive; remaining items are deferred, none blocks planning                        | n/a                  | Stop after one complete cycle                    |

## Scope and Success Criteria

* Scope: see Research Brief.
* Assumptions to verify: "chosen feedback minimum" is the "Minimum owner-feedback release" section of the 2026-10-22 owner comment on #350 (verified, W1). The 980-case programme and 60,000-home stock are distinct baselines (verified, C14).
* Success criteria: each question answered or blocked with named missing evidence; self-check passes.

## Task Research Requests

* Explicit requests: search existing checks first; build a narrow checker only if the existing harness cannot do this; otherwise execute the offline tests and document reuse/gap.
* Inferred research questions: Q1-Q6.
* Caller constraints and non-goals: as in the brief.

## Direction Controls

| Control type | Direction or boundary                                                  | Source / checkpoint | Effect                                  |
|--------------|-------------------------------------------------------------------------|---------------------|------------------------------------------|
| narrow       | Offline from explicit evidence only; no live execution                  | User request        | Evidence is supplied JSON, never fetched |
| exclude      | No edits to API/web/core/infra, `rpi-checks.py`, workflows, KB files    | User request        | Gate integration limited to documented run |
| narrow       | Reuse runtime schemas; do not invent API shapes                         | User request        | Import installed packages and constants  |

## Research Questions

|  # | Sub-question                                                                                       | Type            | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What is the "minimum" and which of its prerequisites are offline-measurable?                       | straightforward | H        | answered |
| Q2 | Can an existing check or proof script already do this offline from supplied evidence?              | breadth         | H        | answered |
| Q3 | What are the actual runtime schemas for `/api/me`, case write/reload and bounded AI evidence?      | depth           | H        | answered |
| Q4 | How can template/mock output be distinguished from a real model result?                            | depth           | H        | answered |
| Q5 | How are the 980-case programme and 60,000-home stock distinguished?                                | straightforward | M        | answered |
| Q6 | How can the new files be validated by the existing complete gate without editing it?               | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: the 2026-10-22 owner forecast comment on #350; #350 body; parity matrix audit section; `src/README.md` local gate section.
* Reused (verified) findings: the digest `sha256:111b...` in the parity matrix is a 2026-10-16 audit, recorded as older than any current feedback release (W1 states the deployed API serves the older digest and is not a usable feedback release).
* Superseded / stale: none relied on without re-reading source.

## Research Cycle Log

### Cycle 1

* Active direction controls: all three above
* Active research posture and completion basis: focused; scope and materiality
* Explicit limits or deadline effect: none on research

#### Wave 1: Wider

* Plan and independent lanes: inline (low volume, coupled). Surveyed `src/api/checks`, `infra/scripts`, `tools`, `infra/tests`, the gate matrix and docs for any evidence-bundle or live-acceptance checker.
* Worker evidence relationships or inline fallback: inline fallback; Q2 -> C1, C2, C3, C4.
* Reflection: all `src/api/checks/*browser_check*.py` start a local server with the shared-password provider and drive Chromium; none validates a supplied evidence file or deployed capture. Image identity regexes exist only inside deploy tooling, not as a standalone checker.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: `/api/me`, case action POST/detail, AI priority record, ledger, image digest form, baselines.
* Plan and independent lanes: inline reading of handlers and core modules.
* Worker evidence relationships or inline fallback: Q3 -> C5-C9; Q4 -> C10-C12; Q5 -> C14; Q6 -> C15, C16.
* Reflection: Runtime schemas are concrete and importable: `projection.me_payload`, `workbench.navigation`, `taskqueues.contract`, `ledger.verify_entries`, store `_rec_view`. The AI record carries `source` ("ai" or "template"), `model`, `validated`, `fallback_reason`, `mode`, `release{id,version,digest}` and per-item `cites`.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: (a) existing browser checks already suffice; (b) a fresh `GET` after a `POST` proves persistence; (c) `/api/cases` total equals the 980 programme; (d) a 200 on `/api/ai/priority` proves AI.
* Plan and independent lanes: inline.
* Worker evidence relationships or inline fallback: (a) weakened by C1/C2: local server, password provider, live Chromium, not evidence validation. (b) weakened by C8: an in-memory store would also return the write; only a restart between write and read separates persistence. (c) weakened by C13: `view=all` totals open cases only, closed excluded. (d) disproved by C10/C11: the same route returns `source: "template"` for workflow-only, unconfigured, failed or invalid output.
* Reflection: All four challenges narrow the contract: require a restart marker, label the case total as open permitted cases, and treat template/workflow-only as a failed AI-evidence check, never a pass. Spend boundedness has no runtime field, so it stays not-run.

#### Parent Synthesis and Disposition

| Material / claim                                              | Evidence IDs      | Parent disposition | Evidence-based rationale                                                       | Primary-artifact treatment                  |
|---------------------------------------------------------------|-------------------|--------------------|--------------------------------------------------------------------------------|---------------------------------------------|
| Existing browser checks cover the offline contract            | C1, C2            | rejected           | They run local servers/password auth; they validate no supplied evidence       | Gap: new checker justified                  |
| Rebuild schemas by hand in the checker                        | C5-C9             | rejected           | Would invent shapes and drift; runtime modules are importable                  | Import installed packages instead           |
| Import runtime modules and validate evidence bundle           | C5-C12            | accepted           | Reuses actual schemas; offline; deterministic                                  | Selected recommendation                     |
| Fixture evidence may yield an overall pass                    | W1, C2            | rejected           | Offline fixture is not deployed acceptance; #349/#360 unmet                    | Fixture origin caps overall at blocked      |
| Treat 3xx/401/403 in positive slots as success                | W1 (#350 AC1, AC10)| rejected          | Issue forbids redirect/denial/source existence as functional pass              | Such evidence fails the check               |
| Spend bound as a check                                        | C10               | deferred           | No runtime field carries spend; inventing one is forbidden                     | Reported not-run with reason                |
| Gate integration via `rpi-checks.py` edit                     | C15               | rejected           | Forbidden by ownership; gate matrix is fixed                                   | Run new tests directly; run full gate as is |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: scope covered; source targets saturated; remaining unknowns need live access
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: all lanes were small and tightly coupled; no worker artifacts exist.

### Codebase Evidence

| ID  | Claim / finding                                                                                                          | Location (`path:line`)                                                   | Tool | Confidence | Notes                                              |
|-----|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|------|------------|----------------------------------------------------|
| C1  | Browser check is manual, needs Playwright, starts the real server on scratch state with a shared password                | src/api/checks/browser_check.py:1-30                                     | read | high       | Eight other `*_check.py` files follow the same model |
| C2  | Checks directory holds only local-server browser/SQL scripts; none consumes a supplied evidence file                     | src/api/checks (listing)                                                 | glob | high       | `workbench-manifest.json` is a UI manifest         |
| C3  | Cut-over proof script and pipeline verify digests inside deploy flows, not as a standalone feedback checker              | infra/scripts/pipeline.py:162-168                                        | read | high       | Digest form `server/zava-forward-<project>@sha256:<64hex>` |
| C4  | `tools/` holds migration, climate bounds and the RPI gate only                                                           | tools (listing); tools/rpi-checks.py:47                                  | glob | high       | No feedback checker exists                         |
| C5  | `/api/me` returns `me_payload` plus `account`, `map`, `navigation` and, for non-contractors, `work_queues`               | src/api/src/zava_forward/api/server.py:365-372                           | read | high       |                                                    |
| C6  | `me_payload`: contractor gets `user{name,role,contractor}`, `counts={}`, `staff=[]`; others `user`, `counts`, `staff`    | src/core/src/zava_forward/core/projection.py:192-195                     | read | high       |                                                    |
| C7  | Role constants `STAFF_ROLES`, `CONTRACTOR`, `FINANCE_VIEW`, `NOTE_HELD`; `workbench.navigation(user)` derives role links | src/core/src/zava_forward/core/projection.py:25-30; src/api/src/zava_forward/api/workbench.py:15-50 | read | high | Navigation never grants access |
| C7b | `taskqueues.contract(policy)` shape; default role map and `account` shape (`name`,`email`,`provider`)                    | src/core/src/zava_forward/core/taskqueues.py:58-79; src/api/src/zava_forward/api/auth.py:90-91,165-170 | read | high | Trusted-proxy provider name is `trusted-proxy` |
| C8  | Case actions `POST /api/cases/{id}/call` append a contact and audit `log_contact`, then return `detail` (+`rule_checks`) | src/api/src/zava_forward/api/server.py:911-914,1012-1015; src/core/src/zava_forward/core/store.py:481-493 | read | high | Contact `outcome` is held (`NOTE_HELD`) for roles without a need (projection.py:134-140) |
| C9  | Ledger report: `intact`, `entries`, `head`, `problem`, `digests_checked`, `digest_mismatches`; `/api/audit-check` returns it | src/core/src/zava_forward/core/ledger.py:32-55; src/api/src/zava_forward/api/server.py:485-486 | read | high | |
| C10 | `AI.run` returns `source` "ai" only after a configured, released, validated model call; otherwise `source: "template"` with a reason (workflow-only, not configured, held, failure, invalid, quarantined) | src/core/src/zava_forward/core/ai.py:101-140 | read | high | |
| C11 | Priority record fields: `source`, `model`, `validated`, `fallback_reason`, `latency_ms`, `release`, `mode`, `quarantine`, `status`, per-item `cites`; label `AI suggestion, not approved` | src/core/src/zava_forward/core/store.py:757,760-781,816-826 | read | high | `POST /api/ai/priority` returns this view (server.py:887-888) |
| C12 | `release_current` requires release `{id, version, digest}` non-empty strings and exact current match                      | src/core/src/zava_forward/core/store.py:84-94                            | read | high | |
| C13 | `/api/cases` returns `items,total,limit,offset,...`; `view=all` lists open cases only                                    | src/core/src/zava_forward/core/store.py:246-259,308-309                  | read | high | |
| C14 | 980-case retained programme on real SQL on 2026-10-12; generated stock stays 60,000 homes and is not 60,000 SQL programme cases | src/api/README.md:2348-2352                                         | read | high | |
| C15 | Complete gate: `rpi-checks.py --all --base --out`, `--verify-receipt`; `--extra-test` accepts only tracked project unittest selectors | src/README.md:48-100; tools/rpi-checks.py:1699-1707 | read | high | Tools-folder tests are not gate-discovered except `test_rpi_checks.py` (tools/rpi-checks.py:47,95) |
| C16 | Parity matrix 2026-10-16 audit digest recorded as the then-serving immutable image                                       | docs/architecture/mvp-to-src-parity-matrix.md:46-49                      | read | high | Historical; not a current feedback image |

### External Evidence

| ID | Claim / finding                                                                                                                                                                                       | Source (title)                       | URL                                                      | Retrieved  | Version/date | Confidence |
|----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|----------------------------------------------------------|------------|--------------|------------|
| W1 | Minimum owner-feedback release: Entra sign-in, role-scoped queue, continuing synthetic homes, one persistent SQL journey with audit, one real-model assistant task with failure/manual path and bounded spend; static/mock is not AI acceptance; deployed API still serves the older digest and Foundry lists no deployments | Issue #350, owner comment 2026-10-22 | https://github.com/jmservera/ama/issues/350              | 2026-10-22 | 2026-10-22   | high       |
| W2 | #350 criteria: no redirect or source-file existence is a functional pass; browser-style anonymous API requests must return 401; no private data                                                        | Issue #350 body                      | https://github.com/jmservera/ama/issues/350              | 2026-10-22 | 2026-10-16   | high       |

### Contradictions / Conflicts

* none material. W1 mentions fixed administrator account and bounded spend; neither has a runtime schema field, so they are not checked (see Decision State).

## Findings Mapped to Questions and Evidence

| Question | Finding                                                                                                                                                         | Evidence IDs        | Confidence | Decision or readiness implication                          |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|------------|-------------------------------------------------------------|
| Q1       | Offline-measurable prerequisites: immutable image identity, `/api/me` role contract, case write/reload persistence evidence, real-AI evidence, baseline counts   | W1, W2, C5-C14      | high       | Four check groups plus a baseline check                     |
| Q2       | No existing harness validates supplied deployed evidence; browser checks use local servers and password auth                                                      | C1-C4               | high       | Gap justifies new standalone checker                        |
| Q3       | Schemas are concrete and importable from installed `zava_forward.core`/`api`                                                                                     | C5-C9, C13          | high       | Import constants and builders; do not copy shapes           |
| Q4       | `source` and `model`/`release` fields distinguish real from template                                                                                             | C10-C12             | high       | `source=="ai"` plus validated model/release is the minimum  |
| Q5       | 980 programme cases vs 60,000 generated homes; list total counts open cases only                                                                                 | C13, C14            | high       | Claiming 60,000 as cases fails; mismatch with 980 fails     |
| Q6       | Gate cannot discover `tools/test_check_demo_feedback.py`; run it directly and the full gate unchanged                                                           | C15                 | high       | No gate edit; record direct unittest run                    |

## Key Discoveries

* Existing prior art validates local servers, not supplied deployed evidence; the gap is real.
* Runtime modules already expose every needed schema constant or builder.
* A write followed by a fresh read does not prove persistence without a restart marker (in-memory store would also pass).
* The priority route returns HTTP 200 for template results too, so only `source`/`model`/`release` establish AI.
* Contact outcomes are held for some roles, so write/reload evidence for those roles is blocked, not passed.
* Spend boundedness and the fixed administrator account have no runtime field; they stay not-run.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: A standalone `tools/check-demo-feedback.py` that reads one explicitly supplied JSON evidence bundle (no network, no env credentials, no implicit paths), imports installed runtime modules for constants and expected role navigation/work queues, and reports per-check `pass | fail | blocked | not-run` plus an overall verdict that is never `pass` for fixture-origin evidence. `tools/test_check_demo_feedback.py` covers each state with synthetic fixtures built from the real runtime builders.
* Rationale: reuses actual schemas, keeps determinism, forbids success-shaped fallbacks, and stays inside owned files.
* Evidence refs: C1-C16, W1, W2
* Implementation impact: two new tools files plus tracking artifacts; no change to API/web/core/infra, gate or workflows.
* Confidence: medium-high; would rise with a reviewed live capture once #349/#360 land.

File tree:

```text
tools/check-demo-feedback.py
tools/test_check_demo_feedback.py
```

### Alternative: extend an existing browser check

* Approach: add a mode to `src/api/checks/browser_check.py`.
* Trade-offs: reuses Chromium flow but edits shared API-project files (contention with other lanes) and still checks a local server.
* Evidence refs: C1, C2
* Rejection rationale: ownership boundary and wrong evidence source.

### Alternative: hand-written JSON-schema copies

* Approach: encode schemas in the checker.
* Trade-offs: no package dependency but invents shapes and drifts.
* Evidence refs: C5-C12
* Rejection rationale: caller forbids invented shapes.

### Alternative: checklist document only

* Approach: another markdown acceptance list.
* Trade-offs: cheap, but not deterministic or reusable.
* Evidence refs: W1
* Rejection rationale: caller requires executable harness.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none for the offline slice.
* Important: the evidence-bundle format is a new contract of this tool, not a runtime API; later live capture must be produced by a reviewed procedure outside this slice.
* Follow-up: spend-bound and fixed-administrator evidence need runtime fields or a separate approved evidence path.
* Residual uncertainty: current deployed digest, model availability and costs are unknown offline; `/api/cases` total is open-only so 980 equality is an assumption stated in the report.

## Current Decisions

| Decision                                         | Status    | Owner / source | Rationale                      | Evidence IDs | Implications                             |
|--------------------------------------------------|-----------|----------------|--------------------------------|--------------|------------------------------------------|
| Build new checker (existing harness insufficient) | confirmed | evidence       | No prior art consumes evidence | C1-C4        | Two owned files                          |
| Import installed runtime modules                 | confirmed | constraint     | No invented shapes             | C5-C12       | Requires installed core/api packages     |
| Fixture evidence never yields overall pass       | confirmed | constraint     | Not deployed acceptance        | W1, W2       | Overall caps at blocked                  |
| Run new tests directly, gate unchanged           | confirmed | constraint     | Cannot edit gate               | C15          | Document direct run in changes/review    |

## Unresolved Decisions

| Decision                                  | Smallest evidence or answer needed    | Owner            | Impact | Blocker status |
|-------------------------------------------|----------------------------------------|------------------|--------|----------------|
| Spend-bound and admin-account checks      | A runtime or approved evidence field   | downstream owner | low    | follow-up      |
| Live capture procedure                    | #349 and #360 completion               | downstream owner | high   | blocking live  |

## Potential Next Research

| Priority | Research item                                 | Expected value        | Trigger                   | Selected? | Related questions / evidence |
|----------|-----------------------------------------------|-----------------------|---------------------------|-----------|------------------------------|
| M        | Reviewed live-capture procedure for bundles   | Converts offline to live | #349/#360 complete     | deferred  | Q1; W1                       |

## Planning Readiness

* Status: Ready
* Decision state: convergence selection recorded above
* Evidence basis: C1-C16, W1, W2
* Preconditions met: all research questions answered; ownership and offline boundaries recorded
* Blockers: none for planning
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                    |
|----------------------------------|---------------------------------------------------------------------------|
| Research execution status        | Complete                                                                  |
| Completed waves                  | Wider, Deeper, Contrarian (cycle 1)                                       |
| Lane evidence or inline fallback | Inline fallback; low-volume coupled lanes                                 |
| Research disposition             | executed                                                                  |
| Planning Readiness               | Ready (C1-C16, W1, W2)                                                    |
| Blockers                         | none for offline slice; live acceptance blocked by #349/#360              |
| Continuation owner and state     | Confirmed automatic RPI Agent; continue to Plan                           |

## Advisory Next Step

| Field                            | Record                                                                            |
|----------------------------------|-----------------------------------------------------------------------------------|
| Research disposition             | executed                                                                          |
| Planning Readiness               | Ready (C1-C16)                                                                    |
| Output mode and planning support | convergence; yes                                                                  |
| Acting owner                     | confirmed automatic RPI Agent                                                     |
| Required gates or confirmations  | Research gates passed; no exceptional confirmation required                       |
| Continuation result              | automatic continuation to Plan                                                    |
| Primary evidence file            | .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md |
| Notes for planning or re-entry   | Plan must carry the restart-marker, template-fail and open-total decisions        |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion basis: further research would need live access, which is out of scope.

## Sources

* W1 - Issue #350 owner comment, 2026-10-22 - https://github.com/jmservera/ama/issues/350 (retrieved 2026-10-22, comment dated 2026-10-22)
* W2 - Issue #350 body - https://github.com/jmservera/ama/issues/350 (retrieved 2026-10-22, body dated 2026-10-16)
