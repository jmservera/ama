---
title: Demo setup readiness phase details
description: Evidence and completion expectations for issue 360
ms.date: 2026-10-17
---

Task: issue-360 / demo-setup-readiness-360.
Plan: `.copilot-tracking/plans/2026-10-17/demo-setup-readiness-360-plan.md`.

<!-- phase: P01 -->
## P01 - Implement laptop-safe transports

### P01-T01

C1/C2/W3/W4: retain existing AES-GCM protocol, but bounded frames fit ARM tag
values and total tags. Read/publish through the generic tags endpoint at the
existing initializer, not app config or stdout. Worker gets source target as
nonsecret environment configuration, validates request binding; only ciphertext
can leave it. Tag-count/size/collision checks precede SQL transfer when possible.
Client deletes only this run's keys after job absence/stop proof. Existing
cross-host serialized operator window remains; no new lock service.
Same-VNet alternative to exact environment equality requires both environments
and subnet resource IDs in ama and matching VNet, not merely a matching prefix.

### P01-T02

C4/W1/W2: adapter owns only storage transport. `--run-in-azure` preflights the
selected private vault by ARM metadata and deploys exactly one child secret
using secureString, fixed management host and private captured body file.
What-if accepts only exact intended Create; reject deletes/modifications of
unrelated resources, expansion, missing/partial validation or failure.
Never return a credential from the template. Check deployment completion and
vault secret metadata (enabled, matching expiry and versionless URI).
Do not change credential reuse/expiry selection or existing secret rebuilding.
PC-001: add a storage compatibility guard before reconciliation/directory
writes, rejecting explicit/recorded app storage and existing app-backed
credential references in Azure mode. Do not migrate existing credentials.

### P01-T03

New tag permissions read/write at existing initializer only, no jobs/write,
listSecrets, resource-group assignment, wildcard or directory permission.
Existing restart role retained. Definition/what-if do not imply activation.
#358 surgical boundary: only replace vault preflight/write calls on Azure mode;
no edits to valid credential selection, preserved secrets or configuration PATCH.
Coordinator reads this artifact as overlap notice.

<!-- phase: P02 -->
## P02 - Validate and execute authorized readiness actions

### P02-T01

Observed missing zava_forward import justifies pip-only isolated installation.
Run focused tests first, then existing full infra suite with local Bicep required.
Run existing Ruff/format/mypy checks plus new modules and pip check.
No host privilege changes or private dataset lookup.

### P02-T02

Existing external environment is ready. Build is blocked: private ACR, no
agent pool/tasks, no local Docker. Do not open networking or add a paid pool.
For API migration only, retain its deployed immutable image, identity, complete
read-visible configuration/template/auth, private backing references and old app.
Create only the demo API and auth child in existing external environment.
PC-002: initial ingress has Deny 0.0.0.0/0, with retained runtime auth denial;
verify auth child and a real single-tenant UUID before separately reviewing
removal. Missing registration blocks exposure; leave new app restricted on
failure. This preserves the future FQDN for laptop setup (external=false
would change it to an internal hostname). Never infer deletion permission.
If exact preserving payload cannot be formed, record blocker rather than infer
redacted values. Inspect what-if before every allowed apply; no role writes.
Probe direct welcome/health/anonymous API with no redirects; no browser login
claim without actual user. No model inference without required release gates.

### P02-T03

Runbook replaces private-console prerequisite with explicit image/tag-role gates,
ARM Key Vault path and actual resource audit. Preserve historical evidence.
Append knowledge log; update index without erasing other workstreams.

<!-- phase: P03 -->
## P03 - Review and publish

### P03-T01

One canonical post-implementation rpi-review, assess diff, evidence and gates.
Record execution/outcome separately from critique; open material findings route
to distinct later work, not another implementation/review cycle in this task.
PC-003: unresolved material findings block readiness and ordinary publication;
only a clearly blocked draft PR or concrete blocker receipt is permissible.
No further live action on a materially failed candidate.

### P03-T02

Commit dated phase artifacts and persistent completion entries. Use repository
local GitHub noreply identity and Conventional Commit/Copilot trailer. Push
topic only; Refs #360, not Closes. Report actual head/actions/a-f status and
exact human action without waiting for login. Do not merge or close issues.

<!-- phase: P04 -->
## P04 - Same-session integration continuation

Owner explicitly authorizes rebase onto latest origin/main and force-with-lease
of the run-owned topic only. Upstream #374 expiry tests, inventory reconciliation,
pending-handoff digest/readback and legacy CLI behavior must remain exact.
Integrate only Azure-mode ARM/no-app-store wiring; add combination tests in
test_staff_azure.py. Preserve both knowledge histories and reviewer 4536f9cc's
material findings; report changed candidate SHA rather than implying old review
covers the new head. No new critique/Review/delivery loop.

Research actual existing private build/import paths and GitHub image retention.
Do not infer missing permission from unattempted actions. No new paid services,
credentials, broad grants, network exposure or privilege escalation. Live scoped
IAM stays approval-bound; state precise minimum human action if no safe route.
Stop after rebase/integration/validation/push and concrete blocker evidence.

Completion: P04-T01/T02/T03/T04 executed; integration63aea64 pushed with exact
lease on prior662c11b. All upstream contracts/tests/evidence preserved; focused
37, setup101, full infra329/no skips, API563/110 skips, core546/1 skip,
orchestrator22, rename25 and relevant quality gates recorded in changes.
No extra Review; reviewer-agent delivery unavailable, so durable PR comment
reports exact final completion head. No live resource writes in continuation.

<!-- phase: P05 -->
## P05 - Independent-review selected reuse guard correction

User supplied independent Revise against662c11b: Key Vault requested but an
unreferenced/untagged generated future-valid app-backed credential is selected,
then record_credential_store writes app. Apply the storage rule to the actual
selected candidate, not merely named/tagged references. Pre-reconciliation must
use equivalent selection before any directory writes. No silent conversion,
rotation or loss of unrelated app/KV secrets. Preserve #374 expiry conditions,
inventory/digest/handoff helpers/tests and legacy CLI, plus sensor/evidence work.
Prove regression fails first, then focused variants and full relevant gates.
Append correction disposition to existing Review, retaining historical text;
external Revise remains pending independent verification. Normal topic push,
no merge, no Azure write or extra delivery/Review loop.

Correction evidence:11 failing-before-fix subcases; selected-candidate guard
and read-only reuse-only preflight now share exact existing expiry/selection.
Final focused41/setup101/full infra333/no skips and existing lint/format/type/
pip gates passed. Upstream inventory/digest/readback/legacy helpers and tests
remain exact. No independent acceptance inferred: external Revise requires
reviewer verification after the normal same-topic publication.
