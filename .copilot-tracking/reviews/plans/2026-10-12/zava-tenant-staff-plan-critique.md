---
title: Tenant Staff Initialization Final-Candidate Plan Critique
description: Single bounded credibility assessment of the locked initialization candidate
ms.date: 2026-10-12
---

## Metadata

* Task ID: zava-tenant-staff-2026-10-12
* Critique date: 2026-10-12
* Workspace: ama-wt-zava-challenge
* Plan: .copilot-tracking/plans/2026-10-12/zava-tenant-staff-plan.md
* Phase details: .copilot-tracking/details/2026-10-12/zava-tenant-staff-phase-details.md
* Critique execution status: Complete
* Execution: exactly one final-candidate critique; no second review, delegation, source edits or live Graph/Azure mutations.

## Inputs and Criterion Boundary

* Caller requirements: use tenant people under the owner's explicit authorization; preserve the main admin and existing Coordinator; eleven distinct enabled people covering ten stable staff/workload codes plus one supplier-scoped Contractor; add only missing assignments for this application; account for effective group roles; no directory administrative-role or group writes; keep directory identities outside Git.
* Preservation requirements: atomically change staff identity fields and current owner labels only, preserving historical attribution, workload ownership, supplier restrictions, the audit chain, shared write locking, meta sequence and rowversions; restart the cached roster.
* Test boundary: at most twelve new methods in infra/tests/test_initialize_workbench_staff.py, no removed methods or changed existing auth/projection assertions.
* Supplied evidence: .copilot-tracking/research/2026-10-12/zava-tenant-staff-research.md.
* Targeted implementation context: mvp/zavaforward_mvp/auth.py, the relevant loading/writing/audit portions of mvp/zavaforward_mvp/sqlstore.py, and mvp/zavaforward_mvp/ledger.py. These were read only to assess planning assumptions, not audited.
* Decisions and dependencies: continuing PR #65; Graph reconciliation precedes the SQL transaction; committed SQL precedes API restart; fresh-browser acceptance is unavailable and separately owner-verifiable.
* Assessment boundary: credibility of the supplied candidate, not proof of implemented behavior, live directory eligibility, current deployed configuration, or actual browser access. No additional project documents, directory inventories, test files or deployment adapters were inspected.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner authorization and application-only changes | Covered | Plan and research explicitly authorize tenant-person allocation, preserve admin/Coordinator, and forbid directory-role/group modifications. |
| Eleven people, stable codes, eight role kinds and Contractor scope | Covered | Plan and P01-T02 establish cardinality, code preservation, resource-account exclusion and an existing supplier scope. Live eligibility remains an implementation gate. |
| Effective roles, group assignments and add-only grants; P01-T01 | Partial | Runtime mapped-role semantics and completeness/failure behavior of directory reads are not specified; PC-001. |
| Atomic staff/current-owner changes, shared lock, sequence and rowversions; P01-T01 | Partial | Correct invariants are named, but the cross-process transaction and fresh-read protocol are not established; PC-002. |
| Cached roster restart and repeat execution; P01-T02 | Partial | SQL no-op retry and restart recovery are not joined into a complete convergence procedure; PC-003. |
| Historical attribution, ledger and workload preservation; P01-T01/P01-T02 | Partial | Commitments exist, but exact baseline comparisons and acceptance evidence are underspecified; PC-004. |
| Privacy and operator prerequisites; P01-T01/P01-T03 | Covered | Private roster/directory evidence, restrictive permissions, generic audit content and least-privilege guidance are explicit. |
| Test ownership and twelve-method limit | Partial | Limit and preservation of existing assertions are explicit; findings require a bounded assertion allocation rather than additional test files or weakened regressions. |
| Documentation, publication and browser-evidence limitations; P01-T03 | Covered | Existing routing/log and PR are reused; operator checks are not presented as personal browser acceptance. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 3; Medium 1; Low 0.
* Rationale: the approved direction is implementable, but four substantive protocol/evidence gaps need direct corrections before the candidate becomes an implementation contract. None requires changing the owner's persona decision, requesting broader directory privileges or performing another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Effective-role reconciliation lacks a runtime-equivalent completeness contract

* Related IDs: functional requirements for role validation/preservation; one-effective-role acceptance criterion; P01-T01; P01-T02.
* Evidence: phase details say to use a live role map and read group membership, but do not define the effective set or incomplete-read response. mvp/zavaforward_mvp/auth.py initializes DEFAULT_ROLE_MAP, overlays ZF_ROLE_MAP, and authenticates using the set of mapped internal role values. It then binds by oid; it does not require the stored staff role to equal the token-derived role. The research distinguishes the admin's unmapped Default Access from Programme Manager.
* Concern: registered/enabled Graph app roles alone do not define the deployed runtime mapping. Counting assignment records or raw role values is not equivalent to counting distinct mapped internal roles. The candidate also does not specify complete paginated assignment/membership reads, principal/resource matching, or failure on unreadable membership. It does not explicitly require the sole effective mapped role to match each selected stable position.
* Impact: a check could declare a roster valid while runtime denies access, grants a different workbench role than intended, or unnecessarily adds a direct grant already satisfied through an applicable group.
* Smallest useful change: define role evaluation from the deployed runtime's merged map and this service principal's enabled role definitions. Resolve all applicable direct/group assignments with complete reads, reject incomplete or ambiguous results before mutation, ignore unmapped Default Access in the mapped-role count while preserving it, and require the single mapped internal role to match the position. Add a direct grant only when the desired effective role is missing; re-read after grants with bounded retry and stop before SQL if the result is not confirmed.
* Action owner: planning parent, with initializer implementation owned by Primary.
* Exact resolving evidence: revised P01-T01 specifies the effective-set algorithm and fail-closed read rules. Within the twelve-method budget, synthetic assertions cover matching group-only access without a new grant, a group-inherited conflict, direct/group duplication of the same mapped role, an overridden runtime mapping, preserved Default Access, incomplete reads and a mismatched position role. Private live evidence confirms one matching effective mapped role for each of eleven identities.
* Decision route: direct planner correction; the owner already authorized application-scoped role reconciliation. No new user decision or directory/group write authority is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The shared SQL write protocol is named but not established

* Related IDs: atomic replacement and shared-write-lock requirements; preservation of meta seq and rowversions; P01-T01.
* Evidence: phase details promise the MssqlStore adapter/shared exclusive lock, rowversion/seq increments, rollback and a chained event. In mvp/zavaforward_mvp/sqlstore.py, Python dblock is process-local; database writes begin a transaction, read meta seq, check rowversions, append against audit_head, update meta seq and commit. Staff is keyed by email, not stable staff code. The deployed MssqlStore locking hook was not supplied within the allowed reading boundary.
* Concern: the candidate does not identify the database-scoped lock entrypoint or its transaction lifetime, distinguish it from local Python locking, or require roster/case/audit/seq reads to be refreshed after acquiring it. It leaves unspecified the expected-row checks and how email-key replacement, including swaps, avoids intermediate collisions. This is missing protocol evidence, not a finding that the deployed adapter is defective.
* Impact: using a stale preflight snapshot or a local lock could race an API writer, overwrite a newer case, lose a sequence advance, or append against the wrong chain head despite an otherwise atomic SQL batch.
* Smallest useful change: document the existing adapter/lock hook and require the same database-wide exclusive lock used by API writers for the entire transaction. Re-read staff, changed cases, meta seq and audit_head under that lock; revalidate protected bindings/codes; apply collision-safe email-key replacement; check expected case rowversions and affected-row counts; use one fresh sequence advance and one audit append for a changed roster; commit them together. A SQL no-op must change neither seq nor rowversions nor ledger.
* Action owner: planning parent, with Primary proving the existing adapter contract before apply.
* Exact resolving evidence: revised details identify the adapter/lock operation and transaction order without inventing a new locking mechanism. Synthetic assertions demonstrate rollback after an injected intermediate failure, refusal/retry on stale state, unchanged unrelated case fields, correct changed-case versions/seq and no-op stability. Before live apply, implementation evidence establishes that the selected hook shares the API's database lock and holds it through commit/rollback; an unverified hook blocks apply.
* Decision route: direct planner correction. If the existing adapter cannot provide the promised shared lock, stop and route that implementation blocker to the parent rather than weakening the preservation requirement.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: A successful SQL no-op must not bypass recovery of a failed roster restart

* Related IDs: cached-roster restart requirement; retry-safe execution; API readiness acceptance; P01-T01; P01-T02.
* Evidence: details promise no further SQL mutations for a fully matching roster and restarting all ready API replicas after successful SQL commit. mvp/zavaforward_mvp/sqlstore.py loads staff only when its in-memory staff dictionary is empty, even when database sequence advances.
* Concern: no recovery step is defined for SQL commit succeeding but restart/readiness verification failing. A retry can find matching SQL while old processes still hold the previous roster. Targeting only currently ready replicas does not establish coverage of every revision/instance that can subsequently serve traffic.
* Impact: a retry could report success while selected people remain denied by stale staff caches, or while mixed old/new roster processes produce inconsistent access.
* Smallest useful change: distinguish SQL reconciliation from runtime convergence. On apply, verify/re-establish convergence even after a SQL no-op; identify all traffic-serving revisions and how their replicas are replaced or otherwise proven fresh without changing image/configuration. Use bounded readiness checks and return incomplete/non-success on restart failure, retaining an explicit safe retry path. Keep check mode strictly read-only.
* Action owner: planning parent, with Primary owning restart execution and verification.
* Exact resolving evidence: revised P01-T02 states commit-success/restart-failure recovery, no-op apply behavior, serving-revision coverage and the runtime freshness signal. A synthetic failure/retry assertion proves no second grant/audit/seq mutation while restart is still required. Private operator evidence identifies successful SQL commit and serving revision/restart/readiness results, plus public-root 200 and blocked anonymous API. Do not substitute SQL roster reads for cache-refresh evidence or claim browser sign-in.
* Decision route: direct planner correction; restart is already authorized and cannot be silently skipped to preserve SQL idempotency.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Preservation acceptance needs a private baseline and explicit comparison targets

* Related IDs: immutable history and owner-label-only acceptance; workload/supplier preservation; test ownership/candidate lock; P01-T01; P01-T02.
* Evidence: the candidate calls for unchanged row/owner counts and prior ledger, one new generic initialization event, and preserved approvals/recommendations. mvp/zavaforward_mvp/ledger.py verifies chain structure and hashes; that alone does not prove all previously attributed records are unchanged. The plan specifies test themes but no bounded assertion allocation.
* Concern: counts alone can conceal ownership reassignment or changes to historical attribution. A valid post-operation chain alone does not prove the original audit prefix was preserved. No concrete baseline/comparison contract is given for current case bodies, historical embedded fields, recommendations, protected staff fields, or repeated execution.
* Impact: acceptance could miss a destructive rewrite while all counts and the ledger's internal validity still pass; failure-injection/concurrency coverage could also be squeezed out by the twelve-method ceiling.
* Smallest useful change: define a private before/after snapshot or fingerprint comparison keyed by stable case/staff codes. Allow only approved staff identity fields, intended current owner labels, specified changed-case versions/seq and the new generic event. Compare owner_code-to-case membership, supplier restrictions, all other case fields including historical attribution, recommendations and the entire prior audit prefix. Allocate these and PC-001 through PC-003 assertions across no more than twelve new methods, using subcases/helpers rather than extra methods or changed regressions.
* Action owner: planning parent, with Primary collecting private evidence and retaining existing assertions.
* Exact resolving evidence: revised acceptance details specify baseline capture under a consistent read, exact allowed deltas and a bounded test/assertion matrix. Private comparisons prove prior ledger prefix equality and correct head/count extension, one new generic event on change, unchanged approvals/recommendations/workload membership and no mutation on a matching retry. Git-safe results contain only generic outcomes, not identities or identity-derived baseline payloads; verification confirms no removed test methods and at most twelve new methods in the named test file.
* Decision route: direct planner correction; no significant user decision is required.

## Strengths and Residual Risk

* The candidate explicitly preserves tenant checks, role/staff separation, main admin, existing Coordinator, stable workload codes and contractor supplier scope without expanding application authority.
* Owner authorization resolves tenant-person selection and ordinary demo allocation. Job/title/group hints remain illustrative, not claims of professional qualification.
* Private roster permissions and the prohibition on directory identities in Git are concrete. Evidence requested by this critique stays private; committed summaries must remain generic.
* Cross-system Graph/SQL atomicity is unavailable by design. Add-only grants followed by SQL retry are a reasonable bounded strategy, but each retry must revalidate effective roles and protected bindings rather than rely on the previous run.
* Live directory/deployment state can change after preflight. Read/validate again at the defined mutation boundaries and fail closed on conflicts; do not remove existing grants to force success.
* Actual browser acceptance remains unavailable unless the owner separately verifies it. This limitation is disclosed, not treated as a reason to invent evidence or delay direct planning corrections.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice is required.
* Before live apply, effective-role read completeness and the database-scoped lock contract must be proven. If either cannot be established, Primary must stop apply and return the specific missing evidence to the parent.
* This is a Revise verdict, not a claim that live implementation is already blocked: the supplied candidate is sufficient to assess its planning gaps.

## Limitations

* No live reads/mutations, external research, implementation execution, source audit, security audit or second critique were performed.
* The Graph management-permission reference is supplied research, not independent proof of current operator authority.
* MssqlStore/deployment restart internals and the existing test suite were outside the permitted file-reading boundary. The critique does not assert defects in them or pretend to validate their behavior.
* Only the requested critique artifact was written; plan, phase details, research and source files remain unchanged by this execution.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly revise effective-role reconciliation and record dispositions for PC-001 through PC-004; finalize the candidate without another critique, then implement P01 subject to the defined pre-apply evidence gates.
* User response required: no.
* Complete disposition route: PC-001 direct planner correction; PC-002 direct planner correction with a lock-proof apply gate; PC-003 direct planner correction; PC-004 direct planner correction. No significant/divergent owner decision is presently indicated.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-12/zava-tenant-staff-plan.md](.copilot-tracking/plans/2026-10-12/zava-tenant-staff-plan.md) | Locked plan assessed once. |
| [.copilot-tracking/details/2026-10-12/zava-tenant-staff-phase-details.md](.copilot-tracking/details/2026-10-12/zava-tenant-staff-phase-details.md) | Phase protocols requiring direct correction. |
| [.copilot-tracking/research/2026-10-12/zava-tenant-staff-research.md](.copilot-tracking/research/2026-10-12/zava-tenant-staff-research.md) | Supplied evidence and owner decisions. |
| [.copilot-tracking/reviews/plans/2026-10-12/zava-tenant-staff-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-12/zava-tenant-staff-plan-critique.md) | Complete PC finding set and parent handoff. |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 directly, record dispositions, and finalize without another critique. No user action is required. This critique execution stops here.
