<!-- markdownlint-disable-file -->

# Task Research: activate-scoped-initializer-360

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md |

## Research Brief

* What: verify merged #375 RBAC, prior #360 review/receipts/runbook and existing Azure initializer/API/job metadata.
* Why/audience: exact, owner-authorized live permission activation and independently reviewable evidence for #360.
* Scope: existing initializer MI and actual demo API in resource group ama; reviewed role definitions/assignments only.
* Non-goals: Graph, SQL, Key Vault secret reads, payloads, restarts, browser acceptance, image publication, networking, spending, deletion, old-stack changes or broader roles.
* Criteria: enumerate exact permission actions, principal and scopes; compare approval; exact what-if before any authorized deployment; capture real denials sanitized.
* Requested output: scoped recommendation and readiness for full ordered RPI.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Does reviewed RBAC fit exact approval? Which actual resources/principal? Can exact permitted roles be activated? |
| Codebase scope | infra/staff-initializer-rbac.bicep, linked guards/runbook and prior #360 artifacts |
| External scope | Existing Azure ARM metadata in current subscription/resource group ama; no secrets |
| Initial internal candidates | Reviewed template, runbook, prior review and receipts |
| Initial external candidates | Azure CLI ARM read-only metadata |
| Research posture / provenance | Focused; bounded owner request |
| Limits | No scope widening; unapproved existing-job tag grant excluded |
| Completion basis | Material questions answered or concrete missing evidence/blocker recorded |
| Edits during research | Evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Authority / disposition |
| --- | --- | --- |
| Instruction | Repository copilot instructions | Selected: safe topic branch, evidence/runbook/index/log, local privacy-safe author |
| Skill | rpi-research | Selected: three ordered inline waves and canonical evidence |
| Specialist | RPI Researcher | Skipped: tightly coupled bounded trace handled inline |
| Skill | Security planning / architecture diagrams | Skipped: no new security architecture or diagram required |

## User Participation and Research Decisions

Owner explicitly requests full ordered lifecycle and boolean approval for limited live deployment. No routine phase confirmation needed. Exact approval excludes assumptions about tag relay or broader grants. Stop at live outcome/authorization blocker, not an automatic child task.

## Scope and Success Criteria

Latest main verified as e065ecd2; clean requested worktree/branch already present. Prior implementation must not be duplicated. Every live claim requires filtered ARM evidence; inventory must never include secret values or job tags.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| API ca-cutover-test-demo-api, not old API | Owner 2026-10-17 | Verify actual target |
| Reviewed API read/restart and temporary staff-job lifecycle only | Owner boolean true | No implicit existing-job tag-write approval |
| No live runtime execution or infrastructure expansion | Owner | Permission activation only |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What exact grants does merged template contain? | depth | answered C1 |
| Q2 | Which existing principal/API/job and current grants are present? | depth | answered W1-W3 |
| Q3 | Is the template deployable within exact approval without source changes? | depth | answered C1/W4: no |

## Prior Knowledge Gate

Read original case study, relevant addendum framing, KB index and owner memory. Historical #375 and #360 claims are starting evidence, not live acceptance. No private datasets used.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline review found two roles, not a temporary-job lifecycle role. C1 contains
API read/restart and existing-job tags/read + tags/write. C2 separates the
operator's temporary-job permissions from the worker MI's grants. C3 records
historical unapplied IAM and blocked image publication.

Reflection: operator lifecycle permission does not imply MI tags/write on an
existing job. Prior four-Create preview is not authority to deploy all four.

#### Wave 2: Deeper

Live filtered ARM reads confirmed W1 principal/client ID, W2 demo serving
revision/environment and deny-all ingress, W3 initializer job/identity and
existing AcrPull. Current custom Staff initializer roles are absent. Deployer
RG permission metadata has actions ["*"], no exclusions or dataActions; this
is capability, not consent. Initial assignment-list syntax combined --all
with --scope and was rejected locally; corrected --all object-ID query
succeeded without directory discovery.

Reflection: grant only to MI 3830883a-f4af-44f8-bff8-8859b78fc2f8 at the demo
API; do not grant to old ca-cutover-test-api or API runtime MI. No temporary
job needs to be created or granted new broad rights in this activation.

#### Wave 3: Contrarian

Unchanged-template exact what-if W4 succeeded with four Creates: two roles
and two assignments. Existing-job relay tags are outside the exact approval.
The previous runbook's proposed blanket authorization must not be reused as
the new owner's approval. A safe subset needs a source amendment and standard
independent source review before live apply. Do not edit generated JSON or
deploy hand-filtered what-if output. No permission denial was observed.

Reflection: preserve merged default behavior; add an explicit opt-out for the
relay role/assignment, prove compiled output exclusion, and obtain independent
review before the API-only two-Create what-if/apply. If review or exact preview
fails, stop deployment and document that blocker.

### Parent Synthesis and Disposition

| Claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Full merged template is approved | C1/W4 | Rejected | Existing-job tags not clearly authorized |
| API-only activation is possible without broad roles | C1/W1-W4 | Accepted conditionally | Small reviewed conditional amendment and exact two-Create preview required |
| Need new MI lifecycle role | C2/W3 | Rejected | Temporary lifecycle belongs to operator, not worker MI; no runtime execution authorized |
| IAM inability prevents activation | W3 | Rejected | No denial observed; capability metadata is not consent |
| Private worker publication still blocked | C2/C3 | Retained prior finding | No approved existing publisher supplied; no build attempted |

### Cycle Re-entry Evaluation

No second cycle: material questions covered; remaining source review and
deployment/readback are Plan/Implement gates, not missing research.

## Evidence Log

Initial Git evidence: clean branch chore/activate-scoped-initializer-360; origin/main and HEAD equal e065ecd2c5b09b0f4bc22bfbfdb343e41910189b; no matching open PR.

| ID | Source | Finding |
| --- | --- | --- |
| C1 | infra/staff-initializer-rbac.bicep:1-105 at e065ecd2 | Exact four API actions and two existing-job tag actions, resource-scoped assignments |
| C2 | infra/README.md:1632-1695,1796-1820 | Operator lifecycle vs worker MI roles, private publisher and historical approval boundary |
| C3 | .copilot-tracking/reviews/logs/2026-10-17/demo-setup-readiness-360-review.md:145-179 and prior resource/publication receipts | IAM/publisher/live-human dependencies; prior review does not close d/e |
| C4 | infra/tests/test_identity_rbac.py:94-121 | Existing custom-role matrix and no broad jobs/write guard |
| W1 | Azure ARM identity show, 2026-10-17 | id-cutover-test-init; principal 3830883a-f4af-44f8-bff8-8859b78fc2f8; client 8fd2cb23-cc1c-4ee5-ab8d-4b6fdff4564e |
| W2 | Azure ARM demo API show, 2026-10-17 | ca-cutover-test-demo-api in cae-cutover-test-demo, latest/ready ca-cutover-test-demo-api--wncofr9; external ingress remains deny-all |
| W3 | Azure ARM job/role/permissions reads, 2026-10-17 | job-cutover-test-init in cae-cutover-test, correct MI; only AcrPull assignment returned; no Staff initializer custom roles; deployer metadata ["*"] |
| W4 | Azure group what-if staff-iam-360-research-20261017, 2026-10-17 | Four Creates, exact IDs below; no deploy invoked |

ARM endpoint root for W1-W4:
https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama .
Only metadata and role definitions were inventoried. No Graph/SQL/vault secret
read, job-tag listing, image build, restart or browser operation was performed.
What-if initially included unrelated Ignore payloads; no payload is retained
in committed evidence and its oversized temporary tool output was removed.
Subsequent previews must project only actionable role metadata.

W4 exact definitions under resource group ama:
`0d8c4586-d46e-514c-9c19-680d9f068755` (API restart) and
`64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c` (result tags).
Assignments: API child `3a7e0803-3997-5cbe-af9c-c9776b37f3a7`;
initializer-job child `8e9a497e-3b90-50e2-a783-93e58755165b`.

## Alternatives and Decision State

Select API-only source amendment with independent predeployment review.
Reject full template (unapproved relay); reject new broad role or job lifecycle
grant to MI (not needed); reject hand-edited compiled template (unreviewed
drift); retain no-deployment as fallback if review/what-if cannot pass.

## Open Questions, Risks and Residual Uncertainty

Existing-job result relay remains unapproved. API permission activation alone
cannot enable end-to-end staff setup. Private publisher and human tenant/runtime
acceptance remain separate blockers; d/e remain UNMET. Readback proves assigned
actions/principal/scope, not execution by the MI or token propagation.

## Planning Readiness

Ready for bounded source amendment and gated API-only activation. Research
disposition: executed. All three ordered waves and parent synthesis completed
inline; no research worker ran. Source, Graph, SQL and runtime remained
unchanged. Evidence IDs and explicit unresolved authorization are recorded.
