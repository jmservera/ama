<!-- markdownlint-disable-file -->

# Task Research: mvp-cutover-201

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md |

## Research Brief

* Target: verify migration on origin/main for #199-#203 before retiring the legacy directories.
* Purpose/audience: evidence-backed maintenance PR for the owner.
* Scope: CI, Docker, Bicep, scripts, live docs, archive tag, knowledge-base index/log.
* Non-goals: deployment, private data inspection, tag publication, check-name changes, full gate, unrelated historical rewriting.
* Criteria: source-backed references, unchanged check names, exact tests, honest issue closure.
* Outputs: research evidence and planning handoff.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What is migrated? What remains live? Which acceptance criteria can this PR prove? |
| Codebase scope | jmservera/ama, fetched origin/main |
| External scope | Named GitHub issues and related PR evidence only |
| Internal candidates | src, infra, tools, workflows, rubric, docs, mvp, prototype |
| External candidates | #199, #200, #201, #202, #203 |
| Posture/provenance | Focused; bounded caller request |
| Explicit limits | No full gate, no uv, no main push, no tag push, no secrets/private datasets |
| Completion basis | Material scope coverage and contradictory evidence investigated |
| Source edits allowed | No |
| Resolved root | .copilot-tracking/research/2026-10-27/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | Supplied applyTo **; KB, branch, privacy and evidence requirements | Selected; owner explicitly authorizes scoped/no-full-gate maintenance |
| Skill | rpi-research | Active RPI phase | Selected |
| Skills | rpi-plan, rpi-implement, rpi-review | User requests full loop | Deferred to their phases |
| Specialist | hve-core-all:rpi-researcher | Registered independent research lanes | Skipped: one tightly coupled reference trace, handled inline |
| Skills | Web/design/security audit | No UI changes or vulnerability request | Not applicable |

## User Participation and Research Decisions

User explicitly requests the full ordered loop and publication on
chore/mvp-cutover-201. Treat as consent for this bounded automatic task, not
permission for additional child work. Owner SIGNED OFF #201 on 2026-10-27 in
the current request. The older issue comments are evidence of earlier state,
not grounds to erase or contradict the later owner direction.
No interaction is needed or available.

## Scope and Success Criteria

Preserve all original historical records; change only live guidance and links.
Confirm archive BRD version and last pre-deletion commit. Never inspect private
datasets. Distinguish owner sign-off from independently measured deployment.

## Task Research Requests and Direction Controls

* Retire residual mvp/ and prototype/ after source migration verification.
* Record owner sign-off in the PR.
* Create archive tag only if locally absent; give owner exact push command.
* Keep workflow/check names unchanged, even if an old issue suggests renaming.
* Use Closes only with complete acceptance evidence; otherwise Refs.
* Run requested existing tests; no full gate.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is present/migrated on origin/main? | Depth | Answered |
| Q2 | Which remaining references are live rather than dated history? | Depth | Answered |
| Q3 | What archive version/target and issue dispositions are justified? | Straightforward | Answered |

## Prior Knowledge Gate

Read original case study, addendum baseline, KB index and owner memory.
Memory is context, not evidence. Fetched origin/main equals current HEAD
65a514ed20e97816dbf47e9fb981ab4cfe40597d; worktree initially clean, correct
topic branch, no open PR for that branch. Issue checkboxes are not assumed
current; verify against actual files.

## Research Cycle Log

### Cycle 1

Focused, inline research; no independent lane warrants delegation.

#### Wave 1: Wider

Initial issue retrieval: mvp contains only README on origin/main; prototype
has no tracked files. #199-#203 retain substantial unticked acceptance criteria.
Inspected active build surfaces, migration ADR/parity and evidence pack.
Reflection: current owner sign-off does not itself prove all historical
engineering or hosted acceptance criteria.

#### Wave 2: Deeper

Inline inspection verifies per-project editable installs, src Docker contexts,
new Bicep job module paths, migrated initializer imports and rename tool roots.
Archive version is v0.21.0 from current BRD frontmatter. There are no local
archive tags or matching remote version tags. mvp contains only its pointer,
with no private data present in this worktree; prototype is absent.
Live stale prose remains in src index, repository agent instructions, capstone
registry table, active PRD build-baseline statement and rubric registry summary.
One mutable parity-document link still targets the pointer.
Reflection: no application migration is needed. Retain legacy-path data guards
and test fixtures: these protect against accidental reintroduction rather than
directing builds to deleted code.

#### Wave 3: Contrarian

Challenged literal zero-token search and whole-issue closure. Historical ADRs,
dated report copies, pinned URLs, original audits and append-only log necessarily
retain old paths. Four old log links must remain byte-exact; add a repair map
in the new log entry instead of rewriting them. Rubric registry already has
no mvp include globs, contrary to its current prose; legacy excludes are
defensive, not live inputs. Dispatch-only workflows are already src-based.
Current src CI owns retained mssql and image checks; do not rename/remove them.
Source-image success and owner sign-off are not proof of fresh deployed health,
all-suite baseline parity, release publication or post-merge rubric comparison.
Reflection: all five issues require Refs, not Closes. Owner-authorized bounded
retirement can proceed without manufacturing their broader acceptance.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Surgical pointer deletion and live-prose repairs | C1-C8 | Accepted | Executable migration already complete on fetched main |
| Rewrite historical evidence to eliminate tokens | C4, C9 | Rejected | Violates dated evidence and append-only policy |
| Rename workflows or remove legacy data protections | C2, C7 | Rejected | Owner requires unchanged checks; guards prevent regression |
| Close #199-#203 now | W1-W5, C4 | Rejected | Unproven hosted/whole-issue criteria |
| Broader acceptance follow-up | W1-W5 | Deferred | Requires later hosted/owner evidence, outside maintenance |

#### Cycle Re-entry Evaluation

No further cycle required. Focused source coverage is complete; additional
cloud probing would widen scope and cannot change the surgical deletion plan.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Per-project distribution migration M1-M6 and current scoped gate policy documented | src/README.md:10, src/README.md:47 | Read | High |
| C2 | Dispatch-only legacy CI installs packages, tests and builds exclusively from src | .github/workflows/mvp-ci.yml:30, .github/workflows/mvp-validation.yml:25 | git grep/read at origin/main | High |
| C3 | Bicep uses orchestrator image and new token/digest modules | infra/modules/containerapps.bicep:260, infra/modules/containerapps.bicep:400 | git grep at origin/main | High |
| C4 | Original evidence preserves blocked human/deployment gates; prototype retired previously | docs/architecture/cutover-evidence-pack.md:9, docs/architecture/cutover-evidence-pack.md:23 | Read | High |
| C5 | Archive version current at cut-over is 0.21.0 | docs/brds/agentic-retrofit-programme-brd.md:9 | Read | High |
| C6 | Mutable parity link still targets soon-deleted pointer | docs/architecture/mvp-to-src-parity-matrix.md:610 | git grep | High |
| C7 | No active mvp scoring includes; obsolete data/vendor excludes remain defensive | .github/rubric/artifacts.json:35, .github/rubric/README.md:374 | Read | High |
| C8 | Live PRD and capstone still name old build/scoring locations | docs/prds/zava-forward-retrofit-programme-demonstrator.md:476, docs/capstone/README.md:23 | git grep | High |
| C9 | Immutable log links to old README anchors require additive navigation repair | docs/reference/log.md:1888, docs/reference/log.md:1907, docs/reference/log.md:1973, docs/reference/log.md:2166 | git grep | High |
| C10 | Migration regression tests deliberately retain historical name/path assertions | tools/rename-zava-tests.py:19, src/core/tests/test_cutover_audit.py:32 | Read | High |
| C11 | Infra initializers import installed namespace, not legacy code | infra/scripts/initialize-workbench-staff.py:184, infra/scripts/create-sql-users.py:11 | git grep | High |

### External Evidence

| ID | Finding | URL | Retrieved |
| --- | --- | --- | --- |
| W1 | Issues have additional CI/deployment/rubric acceptance beyond deletion | https://github.com/jmservera/ama/issues/201 | 2026-10-27 |
| W2 | Archive name must follow cut-over BRD version; preserve check continuity per current user | https://github.com/jmservera/ama/issues/202 | 2026-10-27 |
| W3 | #199 still requires full-suite baseline parity, SQL/image checks and hashed requirements evidence | https://github.com/jmservera/ama/issues/199 | 2026-10-27 |
| W4 | #200 includes deployed image health beyond source repointing | https://github.com/jmservera/ama/issues/200 | 2026-10-27 |
| W5 | #203 requires post-merge rubric comparison and deployed/CI health | https://github.com/jmservera/ama/issues/203 | 2026-10-27 |

## Findings, Alternatives and Decision State

Q1 answered by C1-C4/C11: migration is already present on origin/main.
Q2 answered by C6-C10: fix mutable instructions/navigation, preserve historic
paths and negative guards with an explicit reference policy and archive pointer.
Q3 answered by C5/W1-W5: create absent local annotated v0.21.0 at the last
commit containing the pointer (initially 65a514ed20e97816dbf47e9fb981ab4cfe40597d),
before deletion commit; do not move an existing tag. Use Refs for all five issues.
Recommend the surgical option; broad historical rewrite is rejected.

## Open Questions, Risks and Residual Uncertainty

All material maintenance questions answered. Historical/append-only tokens will
remain; the literal whole-repository criterion in #203 is not claimed complete.
No new Azure/deployment, all-suite SQL/browser/image or rubric result is supplied.
If main moves before publication, record any new last pre-deletion baseline.

## Current Decisions

Use the existing clean main-based topic branch. Honor owner sign-off and
bounded publication request. Do not push tags or rename checks.

## Planning Readiness

Ready. Research disposition: executed. Focused cycle completed in order, inline.
No source edits during research. Evidence IDs resolve to verified sources;
external issue evidence is dated; current owner direction is labelled separately.
Parent RPI Agent should transition to Plan; no additional research needed.
