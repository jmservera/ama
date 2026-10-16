# Cut-over evidence phase details

Task: issue-201 / cutover-evidence-201.
Research: .copilot-tracking/research/2026-10-16/cutover-evidence-201-research.md.

<!-- P01 -->
## P01: Evidence execution

### P01-T01

Use session-local pip venv, install five editable projects with dev extras;
follow project-specific shared test fixture PYTHONPATH (not package workaround).
Capture commands, exit codes, counts, skipped integrations and tooling exemptions.
Run infra tests with compiled Bicep required, all Bicep build/lint, rename tests.
Do not inspect private working datasets.

### P01-T02

Ama exists and generic inventory was empty. Use infra/main.bicep and documented
two-stage deployment; first deployApplications=false, existing authenticated
Azure session, no group creation/deletion. Discover registry from outputs.
Use az acr build with each src workload Dockerfile and src context.
If authentication, service quota, policy or tenant dependency blocks progress,
capture exact safe error and failed smoke status, not fabricated deployed proof.
No live unauthenticated workbench. Cleanup only named run-created resources
when established owner cleanup pattern requires it; preserve group.

<!-- P02 -->
## P02: Durable report and guard

### P02-T01

Read existing stdlib CLI/test patterns before implementing. Source module under
src/core, tests beside package. Audit only tracked allowlisted text, never .env,
.vscode, github-issues or properwarm.json. Output path/line/token/reference class.
Check explicit matrix exceptions rather than pretending old proposed targets
are current. Fixtures prove mutation detection without editing real source.

### P02-T02

Pack distinguishes migrated code from acceptance, partial rebuild from pending,
intentional retirement from future deletion. Azure section includes baseline
commit, scope, commands, safe outputs, IDs and explicit missing proof. List
dependencies/open PR evidence, rubric caveat and owner-only backup. Rename plan
keeps old workflow names until owner-led single PR and protection transition.
Checklist is unchecked; no sign-off inferred.

<!-- P03 -->
## P03: One review and publication

### P03-T01

Review checks plan, details, critique, changes and actual outputs once.
Route remaining acceptance or implementation defects to future work; no second
review in this lifecycle.

### P03-T02

Resolve gh identity before commit, local noreply email for author and committer.
Conventional message and Copilot trailer. Push current clean topic ancestry;
PR against main with Refs #200 and Refs #201 only. No automatic merge.
