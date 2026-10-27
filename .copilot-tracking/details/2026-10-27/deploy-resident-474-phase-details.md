<!-- markdownlint-disable-file -->
# RPI Phase Details: deploy-resident-474

## Metadata

Task ID/slug: deploy-resident-474. Date: 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/deploy-resident-474-plan.md.
Research: .copilot-tracking/research/2026-10-27/deploy-resident-474-research.md.

## Phase Index

| Phase | Status | Tasks |
|---|---|---|
| P01 Release | Completed, including exact merged-view deployment | P01-T01, P01-T02 |
| P02 Live tests | Available checks complete; authenticated/expiry criteria blocked | P02-T01, P02-T02 |
| P03 Publication | Ready for original Review, commit and scoped gate | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Release merged image

<!-- rpi:task id=P01-T01 -->
### P01-T01: Snapshot and build/push

Current registry crcutovertestrzsrg is private, exports disabled, network
defaultAction Allow with no IP rules. Prior push3 route temporarily enables
exports/public access, default Deny and exactly the VM /32, then restores.
Capture actual prior state, not just these expected values. Trap restoration
before the first mutation; do not print token, credential files or command traces.
Use docker login --password-stdin with az acr login --expose-token captured solely
for authentication. Token retrieval is the explicitly authorized ACR route, not
permission to inspect any resident, vault or .env secret.

Image context src/ with src/api/Dockerfile.resident-demo and its dockerignore.
Hold timeout-zero /tmp/ama-rpi-heavy.lock during remote/local image build.
Admission reserves <=USD1 for bounded build/test within fresh USD30 allocation.
Stop a remote build after 600 seconds. Local build has no new Azure resource.
After push use registry digest, never mutable tag in deployment.

Evidence: source SHA, build result/log, push digest and exact ACR policy equality.

Critique corrections PC-001/003/007/008: establish default Deny and the exact VM
rule before enabling public access. Cleanup disables public access first, removes
only the newly added rule in its actual read-back form (Azure may normalize /32),
then restores captured default/export/bypass/rules, re-enabling public access only
if originally enabled after restrictions are restored. Bound retries to three;
preserve original failure separately and require exact policy equality, otherwise
stop deployment/publication. No broad reset of network rules.

Remote build admission requires a verified current rate/600-second quantity bound
and at most one run. If that cannot be established, use local build rather than
queue unknown spending. Record run ID and confirm cancellation/terminal state
before fallback after timeout. App compute bound uses 0.25 CPU/0.5GiB, at most two
startup-overlapping revisions, <=30 minutes test plus <=10 minutes startup/cooldown,
and bounded API operations. Record pricing provenance; unknown ancillary billing
is explicit, not actual-zero. Stop if no conservative admission is supportable.

Before deploying, run pinned Trivy0.76.0 with src/trivy.yaml, scanners vuln,
ignore-unfixed true, HIGH/CRITICAL exit1 on the exact artifact; retain full report,
DB identity and image linkage. Apply existing non-root/no-data/config-refusal
contracts on the same image without resident secrets. Real SQL fixture/image
journeys are historical merged-code evidence, not fresh live acceptance.

Safe preservation queries select only names/IDs/identities, image/resources/scale,
ingress/traffic, job trigger, SQL SKU, secret-reference names and URI metadata.
Do not capture full env/configuration then redact; exclude unapproved inline
environment values in the retrieval projection. Expected resident deltas are
image/generated revision and temporary ingress only. Other app metadata must
match; employee hidden settings and interactive login remain unproved.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Deploy compatible resident projection and image

Existing ca-resident-demo has min0/max1, identity id-resident-demo and existing
Key Vault references. Update image only with az containerapp update; preserve
all runtime settings, references, expiry and workload identity. Do not list secrets.
No new role needed for this deterministic image. If startup fails, record failure,
keep ingress off and restore old digest if necessary.

Implementation amendment: real startup fails with SQL ProgrammingError because
the merged SELECT adds sensor_home_id/sensors_json. Completing the already merged
release requires the exact merged view batch, not a new source/data migration.
One execution override of existing job-cutover-test-init may use its existing SQL
admin MI, min0/Manual definition unchanged, <=600 seconds/0.5CPU/1GiB, <=USD0.0126
compute reservation inside ancillary release allowance. No principal/grant/table/
case/allowlist or sensor-row mutation. Before DDL require original fourteen
column names and unchanged dedicated resident identity/permissions; transact exact
third batch, assert sixteen names and permission equality, otherwise rollback.
Use safe counts/metadata only. Keep the failed live attempt and original plan
critique; do not claim initial ARM Healthy proved application health.

Evidence: ready/latest revision, deployed digest and unchanged resident config.

<!-- rpi:phase id=P02 -->
## P02: Live verification and closure

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run bounded live checks

Resident FQDN: ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io.
Enable target port8089 external HTTP ingress with insecure traffic disallowed.
Bound window to 30 minutes; arm cleanup before exposure and always disable ingress.
Browser receives only invalid synthetic credentials, no owner secret. Actual
positive login and session expiry cannot be claimed without one.

Check /healthz, sign-in accessibility landmarks/labels, no case before login,
generic wrong/unknown login denial with valid CSRF, cross-origin/missing CSRF,
forged session denial and staff-route denial. Compare served JS/CSS/HTML hashes
to merged source to establish deployed feature identity, not rendered-authenticated
acceptance. Capture only unauthenticated screenshots.

PC-002: before opening, start an owned independent watchdog process with an
absolute deadline <=30 minutes and verify its PID is alive. It disables ingress
at the deadline with bounded retries and requires ARM ingress-null readback.
Use bounded browser/CLI timeouts. Main cleanup also disables and verifies, then
terminates only that watchdog PID. If closure fails, preserve the watchdog,
stop all other work and attempt only bounded closure recovery; publication blocks.
Record open/close UTC, HTTPS enforcement, revision and external non-service after
closure. No new Azure watchdog resource or job schedule is authorized.

Natural 1800-second expiry, registered own-case content, gauges/history, assistant
interaction and real sign-out remain Blocked, not simulated or skipped-pass.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Verify restoration and cost ledger

Ingress null after disable. Compare all non-resident app templates/configurations
without retrieving secret values, job triggers, SQL Standard/10 DTU, resident
min0/max1 and runtime env refs. There are four actual apps, so preserve all four.
No claim of employee interactive login based solely on unchanged config.
Record fresh operation estimates separately from delayed charges, previous ledger
and the ama baseline USD309.49076053371493.

Completion: two ingress windows closed and ARM null/external404 verified. After
closure, min0 alone still left one resident replica running. Deactivated only
ca-resident-demo--0000002; final readback active false, replicas0, Stopped.
Future authorized testing must reactivate that revision before opening ingress.
All four app minima, eight job triggers, non-resident safe app metadata, SQL SKU
and exact ACR policies match their preflight snapshots.

<!-- rpi:phase id=P03 -->
## P03: Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review and scoped gate

Independent reviewer assesses plan, implementation evidence and actual diff once.
Preserve adverse outcomes and exact boundary; do not iterate Review. Findings
become later selected work, not permission to weaken requirements.

Before commit use gh api user id/login to configure local privacy-safe identity
8036360+jmservera@users.noreply.github.com for both author/committer. Required
Copilot coauthor trailer. No closing keywords in commit or PR.

Commit dated evidence before --changed gate, external fresh output, timeout0.
Gate runner itself owns the heavy lock: do not wrap it in another flock and
deadlock it. Verify external receipt immediately before push after fetching main;
any new commit invalidates it. PR to main includes URL, final ingress, digest,
partial outcomes, original Review and the fact hosted/human approval is separate.

PC-004/005/006: use --changed --lock-timeout 0 --base <current-main-sha> --out
<new-external-directory>; verify with --required-scope partial. Require current
main ancestor of HEAD; otherwise stop publication without implicit merge/rebase.
After final candidate commit and passing scoped gate, obtain an independent
bounded exact-head publication assessment with verified receipt and matching
head/base. Preserve the one original RPI Review, not a repeat Review loop.
