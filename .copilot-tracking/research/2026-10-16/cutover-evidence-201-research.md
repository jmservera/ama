<!-- markdownlint-disable-file -->
# Cut-over evidence research

## Research Brief

Task identity: `issue-201`, slug `cutover-evidence-201`. Prepare evidence for
issues #200 and #201, not owner approval or deletion. Audience: Juan Manuel
Servera. Output mode: audit preparing planning. Posture: focused, selected
because the caller names the matrix, ADR, Azure scope and delivery boundary.
Evidence root: `.copilot-tracking/research/2026-10-16/`.

## Research Parameters and Direction Controls

Read issue comments first. Preserve mvp/prototype, check names, private data,
tenant configuration and resource group ama. No Docker, uv, private dataset,
.env, .vscode or github-issues tracking access. Local pip venv; build only src;
tests outside packages. Azure writes only inside ama. No sign-off claim.
Caller explicitly requests implementation through PR, not a manual phase stop.

## Extension Registry and Participation

Repository instructions and ADR 0006 selected. RPI phase skills selected for
their respective evidence contracts. No domain specialist needed; source and
Azure inspection are tightly coupled. No interaction available; explicit
caller limits settle the decisions.

## Research Cycle 1

### Wider

Read #200/#201 comments, source index, matrix, architecture guide, deployment
guide and current resource inventory. Reflected: the historical matrix is not
a current gate report; Azure ama is empty, so this is a bootstrap, not an
update of an existing healthy revision.

### Deeper

Inspected src CI, API Dockerfile, deployment parameters and Container Apps
module. Reflected: ACR remote build is the documented Docker-free route.
Full template needs SQL administration and authenticated app setup; RG
ownership is not tenant permission. Do not provision a public unauthenticated
workbench as a shortcut.

### Contrarian

Challenged "all code migrated means cut-over accepted": agents/importer entry
points remain skeletons, worker transport is not deployed, matrix rebuilds
and owner-only private backup remain independent gates. Historical test
counts do not establish equal coverage or SQL integration success.

## Evidence Log

* C1 `docs/adrs/0006-src-layout-and-cutover.md:105`: src context, sibling core,
  external tests and isolated packages.
* C2 `docs/architecture/mvp-to-src-parity-matrix.md:137`: 719-test historical
  baseline, later 747 tests, 92 skips; per-file outcomes retained.
* C3 `infra/README.md:243`: source-image recipe; old checks retained.
* C4 `infra/modules/containerapps.bicep:135`: deployed API requires MSSQL;
  authentication conditional on Entra client ID.
* C5 `.github/workflows/src-ci.yml:62`: editable packages, local tools,
  Docker-based image assertions unavailable locally to this agent.
* W1 https://github.com/jmservera/ama/issues/200 (comments read 2026-10-16):
  old names retained until one post-cut-over PR.
* W2 https://github.com/jmservera/ama/issues/201 (comments read 2026-10-16):
  Juan Manuel Servera signs off; no minimum soak; private backup is owner-only.
* W3 Azure CLI inventory 2026-10-16: group ama in uksouth exists, resources [].

## Decisions, Alternatives and Uncertainty

Accepted: inspect current destinations, run local evidence, try the documented
bootstrap and ACR builds, report partial failures explicitly. Rejected:
deleting old folders, tenant writes, public unauthenticated substitute app,
claiming remote build as local Docker proof or owner acceptance.
Deployment failures do not prevent delivery of an honest evidence pack.

## Readiness and Continuation

Research disposition: executed. Planning Readiness: Ready for evidence
preparation and bounded deployment attempts, not cut-over. No additional
research cycle warranted until execution provides new failure evidence.
Parent rpi-quick owns continuation to Plan.
