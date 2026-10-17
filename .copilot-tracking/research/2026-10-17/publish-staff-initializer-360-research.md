<!-- markdownlint-disable-file -->
# Task Research: publish-staff-initializer-360

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/publish-staff-initializer-360-research.md |

## Research Brief

Publish the merged staff initializer proof image to the existing private ACR
and pin only the existing manual initializer job image if safe. Audience:
owner and deployment reviewers. Output mode: convergence preparing planning.
Scope: exact issue #360, image packaging, existing private route, safe image-only
update and sanitized evidence. Non-goals: initialization, Graph, SQL/private
data, secret payloads, API restart, infrastructure deployment, new resources,
roles, spend, network changes, browser acceptance or retirement.

## Research Parameters

Focused posture, selected from caller's tightly bounded named targets.
Evidence root: .copilot-tracking/. Research edits only evidence and required
workflow state. Questions: is packaging safe and current; does the existing
private publisher route work; can an image-only pin preserve every other setting?
Initial internal candidates: infra/README.md, infra/cutover-proof.Dockerfile,
infra/.dockerignore, image tests, previous #375/#379 receipts.
External candidates: existing Azure ARM and ACR read-only configuration.
No deadline or additional research ceiling imposed.

## Extension Registry and Provenance

| Kind | Candidate | Disposition and scoped authority |
| --- | --- | --- |
| Instructions | Repository copilot instructions | Selected: branch, evidence, secrets and documentation rules |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian evidence |
| Skills | rpi-plan, rpi-implement, rpi-review | Deferred to explicitly requested later phases |
| Specialists | RPI researcher | Skipped: one tightly coupled bounded investigation, inline |
| Skills | Web/design | Skipped: no web edits |

## User Participation and Research Decisions

Caller explicitly requests FULL ordered RPI, authorizes normal Docker,
private image publication and image-only existing-job pin if validated.
This is automatic continuation authorized at intake, not inferred migration
or tenant approval. No routine phase questions necessary.

## Direction Controls

Only existing private DNS/network, identity and registry; stop at a concrete
network or authorization blocker rather than widening access. No ACR Tasks,
import, pools, temporary VMs or unrelated source upload. No workload execution.

## Prior Knowledge Gate

Clean specified topic branch at b15f2f0 (#379), no open matching PR.
Issue #360 read with comments: #375 merged, #379 grants activated, d/e unmet.
Normal Docker verified 29.9.0 with docker group membership; historical socket
blocker is superseded, not proof of private registry connectivity.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Exact packaging and smoke-test contract? | Answered: C1-C3 |
| Q2 | Existing private registry route/auth available? | Answered: W2-W4, blocked route; auth not tested |
| Q3 | Safe manual job image-only update and preservation? | Answered conditionally: W1/C4; no pin without validated image |

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read exact runbook, Dockerfile/ignore, existing image/worker tests, previous
#375/#379 receipts and sanitized current ARM job/registry. Reflection:
Docker access is fixed, but ordinary registry DNS still resolves publicly
and HTTPS returns 403. A private route must be demonstrated independently.

#### Wave 2: Deeper

The retained API base is immutable sha256:111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d.
Proof context is infra/, an allowlist of six Python scripts/manifest assets,
with inherited nonroot user and original proof ENTRYPOINT. Existing job has
one container proof, Manual trigger, args ["initialize"], retry 1, timeout 600,
one replica/completion, MI registry pull, no declared secrets or volumes.
Image-only update must not run that historical initialization argument.
Private endpoint NIC and private DNS zone agree on 10.40.4.21 login and
10.40.4.20 UK South data endpoints. Host is 172.16.0.4, not the AMA VNet.
Reflection: test those exact existing endpoints without DNS, hosts, routing
or registry settings changes; do not mistake public 403 for failed AcrPush.

#### Wave 3: Contrarian

Exact private login and data HTTPS probes both time out after 10 seconds
(curl exit 28, status 000). They use --resolve, --noproxy '*', normal TLS,
no credentials and no system configuration edits. Both routes use the host's
existing 172.16.0.1 default gateway; no working private path is demonstrated.
The local integrated-118 API digest is ee757c29..., not the retained deployed
111b2622... base. It cannot supply a truthful retained-base publication.
Reflection: Docker permission resolution did not resolve private publishing.
No evidence supports changing networks or trying public build alternatives.

#### Parent Synthesis and Disposition

Accept C1-C4 and W1-W4. Reject local substitute base and public registry path.
Defer build/push/pin until an existing private-connected authorized publisher
can reach both endpoints. Research is complete; another cycle cannot remove
the demonstrated route blocker within caller constraints. Planning can cover
offline checks, an exact blocked-build attempt and durable truthful evidence,
without falsely claiming successful package smoke or an immutable new digest.

## Evidence Log

| ID | Claim | Location or source | Confidence |
| --- | --- | --- | --- |
| C1 | Proof uses retained API, explicit copies and unchanged ENTRYPOINT | infra/cutover-proof.Dockerfile:1-6 | High |
| C2 | Recipe intends file-only context; native semantics not yet verified in Research | infra/.dockerignore:1-10 at starting commit | Medium; Implement later found directory-wide reinclusion |
| C3 | Existing image, private transport and context tests | infra/tests/test_staff_azure.py:1204-1281; infra/tests/test_container_contract.py:75-99 | High |
| C4 | Historical publication example and gates | infra/README.md:1642-1692, 1781-1835 | High |
| W1 | Current job Manual with original initialization args, old proof digest, exact identity | Azure ARM job metadata, read 2026-10-17, https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.App/jobs/job-cutover-test-init | High |
| W2 | ACR public Disabled, bypass None, admin false, approved private endpoint | Azure ARM registry read 2026-10-17, https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.ContainerRegistry/registries/crcutovertestrzsrg | High |
| W3 | Private endpoint NIC and private zone agree on login .21/data .20 | Existing pe-crcutovertestrzsrg NIC and privatelink.azurecr.io records, read 2026-10-17 via az network | High |
| W4 | Host public DNS/403, private login and data timeouts | Normal host getent/ip route/curl probes 2026-10-17; HTTPS registry URLs tested with actual existing private IP overrides | High |

## Findings Mapped to Questions and Evidence

Q1: C1-C3 establish the correct packaging and existing test contracts; actual
retained-base image smoke requires a successful build, currently unavailable.
Q2: W2-W4 establish a concrete endpoint reachability blocker, not an IAM denial.
Q3: W1/C4 permit conditional image-only update, but no validated new image exists.

## Alternatives and Decision State

Selected: preserve private registry/job; run bounded offline checks and record
the exact normal-login/build outcome in Implement, with no push/pin if blocked.
Rejected: public ACR Tasks/import, bypass, new pool/VM/role, local unrelated base,
replacing the full container spec, or starting a Manual job. Caller excludes these.

## Open Questions, Risks, and Residual Uncertainty

Existing publisher push authorization is untested; no AcrPush denial claimed.
No new digest, successful image build/import/CLI/package smoke, runtime or
human acceptance may be claimed. Existing job args would initialize if started:
do not start it or change its args to manufacture acceptance.

## Current Decisions

Caller-approved image-only operation remains conditional on validation.
Existing private connectivity fails; preserve all resources and credentials.

## Potential Next Research

Re-enter only after an already existing approved private publisher route is
supplied or demonstrated. No broader inventory or network discovery needed.

## Planning Readiness

Ready for bounded evidence/validation plan, not ready for live publication.
Research disposition: executed. Completed all three ordered waves inline;
no independent lane warranted. Concrete private-route blocker must persist
through Plan/Implement/Review. Parent owns automatic continuation.

## Closeout Record and Self-Check

Complete; ordered waves, evidence IDs, alternatives, owner boundaries and
remaining uncertainty recorded. Sources use exact repository locations and
dated live probes; no secret/data payloads retained. Next action: Plan the
bounded permitted attempt, validation and factual documentation.
