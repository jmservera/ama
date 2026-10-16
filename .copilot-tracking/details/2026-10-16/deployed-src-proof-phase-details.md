---
title: Deployed src proof phase details
ms.date: 2026-10-16
---

Task: issues-200-201-deployed-src-proof.

## P01

P01-T01: `infra/main.bicep` currently ORs development with public access.
Use profile AND explicit switch so production remains private and dev defaults
stay unchanged. Compile/regress true/false/profile combinations.

P01-T02: In-VNet runner uses installed core/SQL driver and managed identity only.
Use runtime synthetic fixture solely for infrastructure, refuse populated
unexpected database, retain a unique non-personal marker, validate private DNS.
No CLI dependency or token transport in the runtime. Package runner with a
dedicated image derived from the remotely built API, using infra build context.
Unit tests mock external services; actual SQL/job success is separate evidence.

P01-T03: Bearer-only EasyAuth is opt-in and must reject missing audience.
Do not create fake credentials, trust unverified headers or bind MI as human.
Use current known application audience if directory enumeration is unavailable.

## P02

P02-T01: ACR tasks run before public ACR access is disabled. Pin digests in
what-if/apply; preserve identity and budget scopes. Reject Delete or writes
outside ama. Bootstrap uses deployApplications=false.

P02-T02: Dedicated MI is SQL Entra administrator for initialization. Identity
assignment and ACR pull roles are within ama. Environment uses existing delegated
subnet and internal VNet DNS. Grant api/import users by known client SID.
Do not overwrite a private/real workload. All data-plane commands run as a job.
Create environment/DNS first through deployEnvironmentOnly=true and
deployApplications=false. The application module owns both staged configurations.
Use sys.tables and a dedicated proof sentinel to reject unknown state before
constructing Store. API/import contained SIDs use client UUID little-endian;
administrator binding uses principal ID, never interchange them.
API gets reader/writer/ddladmin for existing startup behavior; import gets only
reader/writer. Dedicated initializer remains recorded admin for this proof stack.

P02-T03: Use main.bicep to deploy all four images. Inspect actual skeleton/CLI
workload behavior separately from API readiness. Internal HTTPS health must be
200 and unauthenticated protected API 401. Optional bearer attempt must never
log its token; unauthorized staff result is not a pass. Restart serving revision
and rerun SQL marker and health checks, without reseeding.
The nonempty synthetic case and meta marker must reload with API MI and a
nonexistent seed path; initializer-only marker reads cannot pass persistence.
Build runner and all workload images before ACR isolation; after isolation use
only captured digests and MI pulls. Stop unavailable repair builds, do not reopen
networking. Bearer-only negative probes include malformed JWT and forged proxy
principal; absent tenant staff means authorized HTTP remains independently blocked.

## P03

P03-T01: Preserve historical failures, add dated continuation and current summary.
Keep owner checkboxes unchecked. Redact all identifier/secret-bearing output
before persistence in repository, including RPI artifacts and PR body.

P03-T02: Infra unittest discovery, Bicep build/lint, runner tests and secret/ID
scan of staged diff. Review once against plan/evidence and route residual owner
actions. Set verified GitHub noreply email and required Copilot trailer.
Implementation completion is the review-ready source/evidence handoff; publish
the reviewed result afterwards without another implementation/review cycle.
Runtime amendment: expected API assistant tables derive from installed DDL.
First post-restart instrument failed closed; corrected tracked runner is deployed
as a hashed job-template Python command on the immutable proof image, not a
post-isolation registry rebuild. Metadata-only diagnosis and corrected execution
are retained. No initialization/reseeding follows restart.
