---
title: Issue360 bounded RG publisher changes
description: Actual ordered implementation evidence and outcomes
ms.date: 2026-10-19
---

## Implementation Scope and Opening

## P04 Opening: Additional Owner-Authorized Rubric Recovery

Owner2026-10-19 explicitly lifts the previous two-cycle stop for this bounded
rubric-only recovery. Original research/critique/Review unchanged; active scope
is supplemental P04, not blocked publisher/cloud/tenant work. Clean branch was
fast-forwarded from e879 to7e810dc9 after exact ancestry and score-only diff.
Fresh main remains634a024d. Actual failed record log and report retained:
/tmp/issue360-rubric-original-record.log and
/tmp/issue360-rubric-original-report.md. Report shows48 vs48 PASS; lifecycle
status nevertheless failed. Do not inflate score or equate workflow success
with gate acceptance.

Supplemental focused research C1-C5/W1-W2 and plan/details recorded before
source changes. Root predicate established from actual NEW_SHA, empty MOVED,
eligible record recheck and success outcomes: immediate publication API head
did not equal known pushed SHA. Its exact returned SHA was not logged.
Reproduce old-source visibility and distinguish true movement before correction.
Baseline existing lifecycle suite:159 passed. Only existing rubric harness and
canonical workflow publication will change; lock generated with gh-aw.
No original critique or Review repeated, no remote/cloud/model write.

### P04-T01 Reproduction, Repair and Coverage

Actual sticky report verifies48/100 against baseline48/100 PASS. No numeric
regression established. Given actual record-job inputs, the only true moved
predicate was current API head != successful pushed NEW_SHA. The prior API
response is unavailable; stale scored-head visibility is reproduced, not
invented as an observed response.

New harness cases against unchanged source/compiled code fail24 cases with179
passing. Corrected source/lock retry at most five reads with1/2/4/8-second
delays only after successful guarded self-append, only while API returns scored
source SHA. Final head must equal NEW_SHA; unrelated movement stops immediately.
Closed PR, malformed/error responses, prior movement, failed/skipped record,
gate/verification failure and exhausted visibility cannot pass.
Safe diagnostic prints only public SHA and attempt counts. No change to
scoring, baseline, provenance, main writes, credential or push semantics.

Six added parameterized tests plus integrated real Git race assertions exercise
transient/persistent old head, first/last permitted retry, true movement,
closure/malformed response, valid regression denial, actual gate.evaluate
comparison, and real failed score push. Existing before/after advertised-ref
movement/deletion checks remain. No original test or module removed.

| Actual command boundary | Result and external evidence |
| --- | --- |
| Original lifecycle baseline |159 passed; original suite before source changes |
| New reproduction against unchanged source/lock |24 failed/179 passed, before.log |
| Corrected lifecycle including real deterministic comparison |207 passed, focused-final.log combined below |
| Actual pinned MCP stdio/HTTP, blob hashes and compiled schema |12 passed/12 unrelated trigger cases deselected, pinned-runtime.log |
| Combined corrected lifecycle plus runtime/schema |219 passed/12 unrelated trigger cases deselected, focused-final.log |
| Full wider suite before runtime restoration |21 failed/320 passed/7 runtime skips, rubric-all.log |
| Untouched7e810dc9 archived rubric/workflow baseline |21 failed/276 passed/7 runtime skips, baseline-all.log |
| Current full suite after restoring pinned runtime |21 failed/331 passed/no skips, rubric-all-final.log |
| Exact pre-existing failure-ID comparison |Identical21 IDs, preexisting-failure-comparison-normalized.diff empty |
| gh aw compile rubric-score --actionlint --shellcheck --no-check-update |Pass; actual emitted scanner execution, compile-native-scanners.log |
| git diff --check |Pass |

All named files are under /tmp/issue360-rubric-recovery-20261019/.
Runtime restored only after existing harness reported missing runtime, from
official immutable gh-aw-actions924af5fdc64061cfbf66fb584c8b07e2ac230c60.
Existing test validates ten pinned source blob hashes; no runtime code fork,
model call or package install needed. Wider21 failures are inherited hardcoded
seed/adapter assumptions and outdated trigger expectations, not new failures.
They remain visible and are not fixed/suppressed in this bounded recovery.

Partial/failed tooling attempts retained: gh aw lint initially received a
workflow ID instead of a lock path; corrected native path passes. A no-emit
compile with scanner flags did not actually invoke them; final emitted command
does. Direct PATH actionlint1.7.7 rejected pre-existing ubuntu-slim/copilot/
queue syntax; compiler-provided1.7.12 with ShellCheck checks the full lock and
passes without ignored findings. Gate's mandated PATH/tool identities remain.

### P04-T02 Documentation and Frozen-Candidate Preparation

Prior cycle2 final e879 full17group/187-command pass and independent bounded
source assessment by84baed3f-578f-4ab8-9a61-3da35b0efc69 are historical evidence:
/tmp/ama-issue360-correction2-final-20261019-e8796758/receipt.json.
That receipt does not cover appended7e810dc9 or this recovery candidate.
Original live360 acceptance and the original adverse Review remain unmet.

Existing rubric guide now documents actual versus inferred failure evidence,
bounded retry limitations and finite one-append/final-head validation sequence.
KB index routes there and log is append-only. Existing src-ci dispatch supports
all image checks; workflow_run infra-plan rejects dispatch events, so this
mechanism is non-deploying and does not authorize Azure activity. Required
PR-only/protected checks, permissions, reviews and owner merge remain separate.
No dispatch performed here, no manually green context or review dismissal.

Every later bot commit invalidates this candidate's receipt: coordinator must
fast-forward final remote head, run full gate in fresh external output and
independently assess that exact final head without another source push.
Persistent publication failure stops; no paid rerun loop or empty commit.
Current 19th-October recovery must freeze/commit source and all tracking before
actual17group gate. Authoritative final receipt and post-freeze state remain
external to avoid self-reference. No postgate commit/push/PR update authorized.

Full approved plan issue360-rg-loop P01-P03. Research executed first, Plan then
one original independent critique Revise, five direct dispositions recorded
before implementation. No prior adverse/historical artifact overwritten.
P01-T01 complete: standalone no-IAM publisher template and one compiled-security
test module. Native Bicep build passes; 233 focused publisher/proof/IAM/setup/
staff/auth tests pass, zero skips, before any cloud write. Initial missing
zava_forward failure restored only task-owned external pip venv distributions.
Native Bicep argument and repository linter failures were corrected before the
passing precloud run. Log: /tmp/issue360-operator/focused.log.
No cloud mutation yet. Active P01-T02.

## Amendments and Divergences

P01-T02 exact actual preflight rejected B2als_v2 with SkuNotAvailable/capacity
restriction despite the fresh unrestricted SKU result and quota. No resources
allocated. Local judgment within researched alternatives: use D2as_v5, already
unrestricted with family quota0/100 and regular Linux retail USD0.10/hour.
Two-hour VM/IP/disk estimate becomes about USD0.217 before IO/transfer/tax,
not an account invoice. Recompile and rerun focused tests before new preview;
if researched D2as_v5 also fails capacity, stop rather than size escalation.

Original critique resolved the IAM parser concern by separating the runtime
registry assignment from no-IAM Bicep. No production parser/matrix exclusion.
Cloud, tenant, browser and local complete-gate evidence remain distinct.

## Validation and Remaining Work

## P01-T02: Actual Capacity Refusal, No Allocation

Both exact provider-preflight attempts failed InvalidTemplateDeployment /
SkuNotAvailable for capacity restrictions in UK South, first B2als_v2 then
researched D2as_v5. Neither produced a successful what-if change list. No
deployment create, VM, NIC, disk, subnet, PIP, NSG, MI or AcrPush assignment
was created. Final candidate fixes D2as_v5, but is explicitly undeployed and
must not be described as currently allocatable. Quota/SKU-read evidence is
weaker than provider-preflight availability, and the contradiction is retained.

Private inventory, two-hour cleanup deadline, exact intended IDs, input hashes,
and original failed responses remain external under /tmp/issue360-operator,
mode0600 files in mode0700 directory. No raw credentials/application payload.
No watchdog was armed because allocation never began. There is no claimed
runtime lifetime/billing proof and no new resource charge is asserted.

## P02: Blocked Publication and Actual Available Probes

P02-T01/P02-T02 cannot execute without a valid publisher. No login/build/push,
new image/digest, exact digest pull/run, initializer pin/rollback, SQL initialization
or app restart was attempted. Current initializer still uses
ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72,
not a verified fresh worker. Existing API digest remains111b2622.
No stale proof image was republished or relabelled.

P02-T03 executed bounded existing-credential and direct HTTPS probes only.
Existing service-principal Graph token has no delegated scopes/application
roles; application-read probe failed. Authorized tenant administrator must
provide/approve the intended single-tenant registration, provisioning permissions,
private credential and staff roster, then an interactive authorized person must
complete the real browser/role checks. No tenant authority inferred from RG.
Direct '/', '/healthz', '/api/me', '/app' each returned403 with no redirects
followed. This is deny-all restriction evidence, not health200/auth acceptance.
No unknown/private SQL data or real AI call was read/executed.

## P03-T01: Cleanup and Preservation Readback

2026-10-19T08:22:24Z independent resource inventory found zero owned temporary
resources. Existing subnet objects equal the prewrite baseline; registry
public access/bypass/policies equal baseline. SQL, vault, storage, Foundry and
IoT publicNetworkAccess are all Disabled. Registry remains Disabled/bypass None.
Old API/Front Door and RG ama retained. No cloud deletion was necessary or run.
Private planned-resource inventory and sanitized receipt retained externally.
This is no-allocation verification, not successful temporary-publisher cleanup.

## Validation and Remaining Work

233 focused tests pass after each final template update, zero skips; native
Bicep build passes. Original failed local attempts retained outside git.
P01-T02 and dependent publication/pin remain BLOCKED. Complete infra discovery
initially failed missing yaml; restored pinned PyYAML6.0.3 from existing
workflow/tool manifest in the external venv. Actual complete suite then passed
363tests, zero skips, under /tmp/ama-rpi-heavy.lock.

P03-T02 complete: updated existing runbook/ADR/evidence/index and appended log
without altering prior entries or memory; added sanitized actual live receipt.
Unused external task-owned SSH keypair removed, no cloud resources to delete.
Implementation/plan/details/blockers reconciled for the single original Review.
Final candidate commit and complete gate will follow that Review.

## P03-T03: Original Review and Frozen-Candidate Handoff

Exactly one original independent Review executed after implementation.
Execution Complete; implementation Partial; outcome **Not accepted**.
Canonical record:
.copilot-tracking/reviews/logs/2026-10-19/issue360-rg-loop-review.md.
RV-001 Medium finds missing compiled resource-relationship/negative guard
test coverage, while inspecting current template as correctly wired.
RV-002/003 High retain actual publication and tenant/live acceptance blockers.
Route RV-001 to later rpi-implement; do not correct source or repeat Review in
this completed loop. Preserve original critique/Review unchanged.

Reviewer did not independently inspect external primary files due to its own
execution restrictions. It used candidate sanitized receipt/source/artifacts
and reported test results; coordinator must independently compare primary
failure responses, test logs and private inventory. No final exact-head
approval or full-gate result is inferred from that Review.

Final clean commit/full17gate remain mandatory after this record is frozen.
Authoritative receipt and full command log will stay in a fresh external
directory, not committed here. This record intentionally cannot contain the
later self-referential final HEAD or claim a not-yet-executed gate pass.

## P01-T04: Coordinator-Selected RV-001 Continuation (Correction Cycle1)

The original process exited0 and returned frozen clean HEAD
8f996e6ffc0a7e6a4953fff4523d1cbe01190522 before this continuation started.
Coordinator explicitly routes RV-001 to Implement in this same task; this
supersedes only the prior no-source-correction handoff direction, not its
historical adverse assessment. No new research, critique or Review.
Starting boundary: existing compiled test module, exact guard/refusal and
resource connections, with bounded actual negative mutations before/after.
Plan/details/state updated before source edits. No Bicep/guard/parser/matrix
change, Azure attempt, publication, tenant or operational approval.
Both provider capacity failures and RV-002/003 remain actual blockers.

Original Review SHA256:
686fd0bed206e904e32b985b8f9945116b44ef54e7ed53ff52c7223d3063d2ba.
Original critique SHA256:
9c6c3a32e97746bb688e21bec5a3fa85a4ee3634a8d811bb84760c09ba48726a.
These will be checked unchanged before the frozen handoff.

### P01-T04 Implementation and Concrete Mutation Results

Only infra/tests/test_private_proof_publisher.py changed outside these current
RPI artifacts. Replaced substring/nonempty dependency checks with exact compiled
guard expression (both name and case-normalized exact ID, successful actual
scope and empty refusal), nested string/minLength1, and exact guard dependencies.
Asserted actual NSG attachment, existing-VNet child target, NIC subnet/public-IP,
VM NIC and each dependency chain. Original Bicep, guard, parser and IAM matrix
remain unchanged.

The fifth test exercises16 deep-copied compiled negative fixtures against the
same positive assertions. An independent external harness actually compiled
the unchanged Bicep, loaded original tests from frozen8f996e6f and current tests,
then ran each four-test baseline suite on identical mutated compiled ARM.
This is executed failure evidence, not an assertion-only claim of sensitivity.

| Compiled mutation | Original four tests | Corrected four tests |
| --- | --- | --- |
| Detached NSG attachment | Passed incorrectly | Failed attachment assertion |
| Wrong NSG resource ID | Passed incorrectly | Failed attachment assertion |
| Wrong existing-VNet child name | Passed incorrectly | Failed exact child target |
| Wrong NIC subnet ID | Passed incorrectly | Failed exact NIC subnet |
| Wrong NIC public-IP ID | Passed incorrectly | Failed exact public-IP reference |
| Wrong VM NIC ID | Passed incorrectly | Failed exact VM NIC |
| Unrelated NSG dependency instead of guard | Passed incorrectly | Failed exact guard dependency |
| Unrelated public-IP dependency instead of guard | Passed incorrectly | Failed exact guard dependency |
| Missing subnet dependency | Passed incorrectly | Failed NSG prerequisite |
| Missing NIC dependencies | Passed incorrectly | Failed subnet/public-IP prerequisites |
| Missing VM dependency | Passed incorrectly | Failed NIC prerequisite |
| Accept refused scope instead of empty branch | Passed incorrectly | Failed exact refusal expression |
| Wrong approved scope branch | Passed incorrectly | Failed exact approval expression |
| Empty scope allowed by nested minLength0 | Passed incorrectly | Failed nonempty guard input |
| Missing RG-name check | Failed already | Failed, retained protection |
| Missing exact RG-ID check | Failed already | Failed, retained protection |

Both unmutated baselines passed4/4. Original14/16 mutants survived; corrected
0/16 survived,16/16 rejected by real assertion failures, no errors or skips.
Detailed cases, failed test IDs and before/after logs:
/tmp/issue360-rg-correction1/mutation-evidence.json,
/tmp/issue360-rg-correction1/before-<mutation>.log and
/tmp/issue360-rg-correction1/after-<mutation>.log.
Reproduction harness and exact compiled fixtures are beside that evidence.
No credential environment inherited; heavy work used /tmp/ama-rpi-heavy.lock.

Five focused tests pass (16 negative subtests); complete infra discovery
passes364 tests, zero skips. Logs: /tmp/issue360-rg-correction1/focused.log and
/tmp/issue360-rg-correction1/infra-all.log. git diff --check passes.
P01-T04 checked with this completion evidence; historical P01-T01 and original
Review findings are preserved, not retroactively converted to acceptance.
No new research/critique/Review, cloud writes or provider attempts; both original
capacity failures, no-allocation receipt and RV-002/003 remain unchanged.
Assertions/mutations do not prove cloud security, machine-checked live preview,
runtime assignment, publication/pin, browser/tenant/SQL/AI or human approval.

### Frozen-Candidate Preparation and Remaining Gate

Authenticated gh api user returned id8036360/login jmservera. Repository-local
author/committer email is8036360+jmservera@users.noreply.github.com.
Fresh origin/main remains reviewed634a024d97d2da7168b8a7d5f343ab26e6108cf3.
The corrected candidate and this evidence will be committed before running all17
groups with caller PATH, fresh external output and fixed heavy lock.
Final exact HEAD/receipt/group totals and post-freeze state must stay external;
no later commit, push, PR, repeated Review or live acceptance is authorized.

## P01-T05: Coordinator-Selected Outbound Continuation (Cycle2)

Starting clean HEAD9f552eda3efd83443e36384febfda4cf538df023 and freshly fetched
unchanged base634a024d97d2da7168b8a7d5f343ab26e6108cf3. Original/cycle1
processes exited; no concurrent implementation. Independent exacthead reviewer
84baed3f-578f-4ab8-9a61-3da35b0efc69 verified RV-001 closed and actual prior
full receipt, then found a new Medium blocker: no explicit outbound restrictions.
This later disposition does not rewrite the original Not accepted Review.

Plan/details reconciled before source changes. Approved boundary is the
publisher Bicep, existing compiled test module, directly related documentation
and current RPI artifacts. First execution is explicit private-ACR/platform
egress plus deny-all, without changing exact-RG/relationship guards.
No safe package FQDN enforcement exists in NSGs; retain blocked package
bootstrap rather than broad Internet/Storage/AzureCloud access or new complex
infrastructure. Retain public-IP relationship but deny general Internet use.
Planned validation: compiled flow contracts and actual before/after mutations,
focused/full infra externally, then frozen commit and fresh isolated17group gate.
Previous receipt becomes historical/invalid for changed source. No Azure
writes/deploy/what-if/capacity attempts or new Review. Original capacity/Graph/
live403/tenant/privacy/human boundaries persist.

Immutable Research SHA256:
379ec0676976abe5b4ee52aa24e4d334ee747ebeeefb5411e58e8fe29038c315.
Original critique/Review hashes above remain authoritative and unchanged.

### P01-T05 Implemented Boundary and Actual Mutation Evidence

Bicep now permits only TCP443 to recorded private ACR10.40.4.20/.21,
AzurePlatformDNS TCP/UDP53, WireServer TCP80/32526 and AzurePlatformIMDS TCP80.
Explicit platform DNS/IMDS denials and priority200 deny-all outbound precede
default VNet/Internet allows. No public package/Storage/AzureCloud/ARM/Entra
allow. Existing exact-RG guard, all resource connections, inbound denial and
private backing remain intact. Retained PIP cannot override the deny.

Relevant current-state clarification preserves the coordinator's approved
intent: NSGs cannot filter package FQDNs; package/bootstrap is blocked pending
a separately reviewed private/offline tool route. No new firewall/proxy/image
service is justified or created. Supported-agent WireServer redirection is
officially documented but unverified here, and agent WireServer traffic is
NSG-exempt. DNS/registry payloads and authorized push misuse are not filtered.
Runbook/ADR/evidence/index/log explicitly retain those limitations and future
private endpoint/DNS identity revalidation. Original adverse history retained.

Actual source compilation before/after:

| Executed boundary | Result |
| --- | --- |
| Original9f552eda template with its original suite | 5/5 pass, reproducing inadequate outbound protection |
| Original template with new2 policy/flow checks | Both reject,18 assertion failures including flow subtests; no runner errors/skips |
| Corrected compiled template with full corrected suite | 8/8 pass, including original16 guard/relationship and new18 outbound mutation subtests |
| Same compiled remove-all-outbound mutant | Original5 tests pass; corrected policy2 checks reject |
| All18 corrected compiled outbound mutants | 18 rejected,0 survivors,0 errors/skips |
| Focused infra / complete infra discovery | 8 /367 tests pass,0 skips, shared fixed heavy lock |

Mutations cover absent/late/allow/TCP-only/wrong-target/wrong-source deny,
whole-subnet/Internet registry widening, wildcard ports/protocols, arbitrary
DNS/agent/IMDS endpoints, missing explicit platform denials/registry permit,
all outbound rules removed and inserted Internet allow. Tests inspect compiled
rules and bounded first-match flows including default65000/65001 allows,
private lateral access, public80/443/53/22/UDP, IPv6, exact ACR/platform ports
and wrong source. This is not an Azure platform emulator or live security proof.

Concrete compiled fixtures, original source bytes, individual assertion logs
and reproduction harness are external:
/tmp/issue360-rg-correction2/mutation-evidence.json and mutation-evidence.py.
Focused/full logs: focused.log and infra-all.log in that directory.
P01-T05 checked with this evidence. Original Research/critique/Review SHA256
rechecked unchanged. P01-T02/P02-T01/P02-T02 remain blocked; both actual
SkuNotAvailable preflights/no allocations, Graph403/direct403 and human gates
are unchanged. No cloud attempt, no repeated critique/Review or acceptance.

### Cycle2 Frozen-Candidate Preparation

Authenticated gh api user resolved id8036360/login jmservera for repository-local
noreply author and committer. Fresh main must remain reviewed634a024d before
commit/gate and on final receipt verification; stop for coordinator if changed.
Commit this source and dated evidence, then run actual17group gate in a new
external output with env credential isolation, full host Node PATH plus
/tmp/rpi-413-tools first, pip/no uv and /tmp/ama-rpi-heavy.lock. No outside
heavy concurrency. No postgate source/commit, push/PR/merge/settings/issue
change. Final receipt, matrix counts/limits and post-freeze state stay external
to avoid self-reference. Earlier gate is not valid for this corrected source.
