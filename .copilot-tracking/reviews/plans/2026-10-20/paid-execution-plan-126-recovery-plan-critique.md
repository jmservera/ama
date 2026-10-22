<!-- markdownlint-disable-file -->
# RPI Plan Critique: Finite costed execution plan for #126 (recovery run)

## Metadata

* Task ID: 126-paid-plan-recovery
* Critique date: 2026-10-20
* Plan: .copilot-tracking/plans/2026-10-20/paid-execution-plan-126-recovery-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: documentation-only finite costed plan for #126 as an addendum subsection, index row and append-only log entry; USD 500 TOTAL monthly cap including accrued charges; expiry 2026-10-25T16:02Z; unknown spend or prices block execution; no IDs or secrets; preserve RG `ama` and identities; no retry of known capacity failures; no acceptance inferred; edit boundaries per the brief.
* Research and evidence considered: .copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md; pre-RPI critique .copilot-tracking/reviews/2026-10-20/paid-execution-plan-126-plan-critique.md (unverified input); /tmp/ama-wave-20261020-2113-common.md.
* Decisions, dependencies, and acceptance criteria considered: plan Acceptance Criteria, Functional and Non-Functional Requirements, P01/P02 task details. Arithmetic was recomputed independently (S0 535.41, S1 418.37, S2 384.79 all reproduce). Existence of the referenced commands (setup-entra.py flags, initialize-workbench-staff.py --check/--apply/--restart, infra/public-edge-existing.bicep, src/api `zava_forward` package) was spot-checked in the repository.
* Assessment boundary: the plan and details only. No Azure access, no price re-verification, no check of the addendum text (not yet written).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| USD 500 total cap, projected month end | Partial | Formula omits non-RG-`ama` spend (PC-001); thresholds contradict eligibility (PC-002) |
| Arithmetic reproduces | Covered | S0/S1/S2 and eligibility sums recompute exactly; S2 uses a rejected assumption (PC-003) |
| Hard expiry gate / do-not-start | Partial | Fixed 10:00Z conflicts with T1 template rule (PC-004) |
| T1 approval fields, commands, preconditions, browser/roles/SQL/AI checks | Partial | AI check contradicts "no new resources"; mutations hidden; checks lack pass evidence (PC-005, PC-006) |
| T3 bill of materials | Partial | No prices, lifetimes, named scripts or retention liabilities (PC-007) |
| T2 model/token bounds | Covered | Versions, counts, bound 4.61; minor gap (PC-009) |
| Local-first vs Azure-only | Covered | T1 stage 0 and Azure-only list |
| Liabilities, blockers, no retry, RG/identity preservation | Covered | P01-T03; no retries stated |
| Transport design generic | Covered | T3 |
| Scope boundaries | Partial | Appending to the four draft files conflicts with "preserved unchanged" (PC-008) |
| 403/redirect not sign-in | Partial | Stated, but positive pass evidence not defined (PC-006) |
| No acceptance inferred | Covered | Non-goals |

## Verdict

* Verdict: Revise
* Rationale: The arithmetic is sound, but the gating design is not yet hard or internally consistent: eligibility ignores the pause and review thresholds, the cap formula excludes unknown subscription spend, the do-not-start time is arbitrary and in conflict with the T1 rule, T1 needs an AI call that no allowed-resource tranche can supply, and T3 has no priced bill of materials. All items are planner-correctable; none needs a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Projection formula excludes unknown subscription-scope spend

* Related IDs: P01-T01, Acceptance Criteria, research C16
* Evidence: phase details P01-T01 formula `P = 172.47 + ...`; plan lists unknown spend as blocking only in prose.
* Concern: P is RG `ama` only, yet the cap is a TOTAL. Credits, tax, support and other-RG charges are absent, so every threshold is computed on a partial base and could be "eligible" while the true total exceeds 500.
* Impact: the headline gate can pass without proof of 500 USD compliance.
* Smallest useful change: add an owner-supplied term U (other charges accrued to date and expected, with date, scope, currency, source) to P; state P is undefined, so all paid tranches are blocked, until U is recorded with a timestamp no older than one day at tranche start.
* Action owner: planning parent
* Exact resolving evidence: addendum formula includes U; eligibility rule and hard-gate list both name "U unrecorded or stale = blocked"; arithmetic script prints results with U = 0 labelled "illustrative, RG only".
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Eligibility rule contradicts the review and pause thresholds

* Related IDs: P01-T01, Functional Requirements (options, thresholds)
* Evidence: thresholds review 400, pause new tranches 450, stop 475; eligibility compares to 475. S1 alone is 418.37 (above review 400); S1 + T1 + T2 + R = 466.37 (above pause 450); S2 all tranches 447.79 sits within 3 USD of pause.
* Concern: a set deemed eligible would trigger "pause new tranches" at once, so the rule is not hard or coherent. R = 30 is also unevidenced and the run rate is a two-day sample after a 17 Oct step change, with no margin for it.
* Impact: owner approval could be requested for sets the plan itself would halt; stop at 475 leaves only 25 USD against a possibly wrong burn rate.
* Smallest useful change: make eligibility use the pause threshold (P_option + ceilings + R at or below 450) or restate the thresholds as one ladder with defined actions (who acts, what stops); recompute the eligible sets and the S1 T3 and S2 cases; justify R or label it an owner-replaceable assumption with a rule for what lower or higher R does; add a rule that review at 400 requires an owner decision before the next tranche.
* Action owner: planning parent
* Exact resolving evidence: one table of thresholds with actions; eligibility numbers recomputed by the script and matching addendum text; no eligible set exceeds the pause threshold.
* Decision route: direct planner correction (R remains labelled an owner-replaceable assumption)

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: S2 relies on the 50 percent saving that research rejected, and mislabels it as optimistic

* Related IDs: P01-T01, research Wave 3 (a) and disposition table
* Evidence: details say S2 assumes "50 percent of 10.66 over 6.3 days: 384.79" and call it "the optimistic bound"; research rejected 50 percent and replaced it with a 0 to 10.66/day range requiring a measured check. 6.3 days is 25 Oct 16:02Z to month end but is not explained.
* Concern: 50 percent is a midpoint, not an optimistic bound (100 percent gives about 351); the 447.79 eligibility figure depends on it; why SQL is idled only after expiry is not explained, and stopping the schedule may not idle SQL (replicas and demo API hold connections).
* Impact: unsupported claim in an approval document.
* Smallest useful change: show S2 as a range (0 percent equals S1 418.37; 100 percent about 351) with no baseline credit; make S2 eligibility use the 0 percent case until a measured post-change daily cost exists; state the 6.3 day derivation and the connection caveat.
* Action owner: planning parent
* Exact resolving evidence: addendum S2 row with both bounds and derivation, 447.79 replaced by the conservative figure, script output matching.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Do-not-start time is arbitrary and conflicts with the T1 template rule

* Related IDs: P01-T02 (hard gates, T1 approval fields), Acceptance Criteria
* Evidence: hard gate "2026-10-25T10:00Z, a fixed six hours before expiry"; T1 template says start must precede expiry minus tranche duration minus margin; no tranche duration is stated for T1 to T3; the owner and executors needed are private-connected humans, and 25 Oct 2026 is a Sunday.
* Concern: two different rules; six hours is unsupported by any duration; cleanup is required before expiry but its duration is not budgeted; T2 and T3 durations are open ("hours"). A fixed 10:00Z could allow a start with insufficient time to clean up, or needlessly forbid short tranches.
* Impact: the single most consequential gate is not demonstrably sound.
* Smallest useful change: state per-tranche maximum execution plus cleanup duration (T1, T2, T3), define do-not-start = expiry minus (duration + cleanup + margin) per tranche, with 10:00Z only as the latest for the longest tranche if the numbers support it; add that any unfinished tranche at expiry is stopped and its leftovers listed as liabilities; add that tranches run sequentially and T2 and T3 require T1 and cost re-check; require the approval to name an executor and the day-of availability (Sunday).
* Action owner: planning parent
* Exact resolving evidence: addendum table of durations and per-tranche do-not-start times, consistent with the T1 template and the hard-gate list.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: T1 "no new resources" cannot supply the AI check, and its mutations are understated

* Related IDs: P01-T02 (T1), research C13, C14
* Evidence: T1 expects "one AI call returns a bounded response"; research states no model deployments exist and quota is Unknown, and T2 is what creates deployments. T1 preconditions include tenant registration and consent, private roster apply with restart, and changing the deny-all restriction.
* Concern: the AI check is unachievable in T1 as scoped; the tenant, roster and ingress changes are identity or access mutations that the ceiling of 8 USD (itself unjustified) does not describe, and "preserve identities" needs explicit boundaries.
* Impact: T1 would be approved as no-new-resource yet either fail its own check or silently require T2.
* Smallest useful change: move the AI check to T2 (or make T1 AI pass conditional on T2 and mark it "not testable in T1"); list T1 mutations explicitly as owner or tenant-operator actions outside Azure resource creation, each with rollback (re-apply deny-all, remove roster rows) and the statement that no existing identity is altered or deleted; replace the 8 USD with a stated basis or label it as an owner-replaceable ceiling.
* Action owner: planning parent
* Exact resolving evidence: T1 table with check-by-check "testable in T1: yes or no", a mutation list with rollback, and a ceiling basis.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: T1 pass or fail checks lack positive evidence, so a redirect or 403 could be misread as success

* Related IDs: P01-T02 (T1), research C9, requirement on real evidence
* Evidence: the plan states "a 3xx redirect or 403 does not count as sign-in" but the checks are stated only as results ("reaching /app", "expected role", "expected rows").
* Concern: no per-check pass rule (e.g. final URL, authenticated 200, identity displayed, role shown by the application not by a login page), no capture format that avoids IDs, no ordering with the cost check before and after, no fail outcome (stop, do not retry, record). Commands are named but not given as a sequence with `--check` before `--apply` and read-only first; "valid managed-identity client sentinel" has no defined source.
* Impact: the owner cannot tell a real pass from the known 403 or a redirect to a login page.
* Smallest useful change: for each of browser, roles, SQL, AI give pass criterion, fail criterion (including 3xx, 401, 403 and login-page content), evidence to record with IDs redacted, and the stop rule; order the commands; state the sentinel source as an owner-supplied precondition.
* Action owner: planning parent
* Exact resolving evidence: T1 checks table with pass, fail, evidence, stop columns; command list order consistent with infra/README usage.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [High]: T3 is not a priced, finite bill of materials

* Related IDs: P01-T02 (T3), requirement for count/SKU/region/lifetime and price provenance
* Evidence: T3 gives counts, "Standard", "UK South", lifetimes "in hours" and "ceiling 15" with no unit prices, dates, currency or script names (research prices only token costs, W1); "existing scripts" are not named.
* Concern: ceiling 15 USD is unsupported; "unknown prices block execution" applies to T3 as written. Retention liabilities are not accounted for: a vault with soft-delete or purge protection persists after deletion; storage retention or immutability tests may not be deletable on schedule; malware scanning may be metered per GB; SQL restore drill depends on a backup source and minimum storage.
* Impact: the paid tranche most likely to leave residual liability is the least bounded.
* Smallest useful change: per resource give count, SKU, region, numeric lifetime hours, unit price with retrieval date, currency and source class (or "Unknown, blocks"), the exact script or command reference, and a post-deletion liability line; state that T3 is blocked until each price is recorded and that the ceiling is the sum plus a stated margin.
* Action owner: planning parent (prices to be retrieved read-only from public retail data; if a price cannot be retrieved it is stated Unknown)
* Exact resolving evidence: T3 table with dated priced rows and script references whose names exist in the repository; ceiling equals the table sum plus margin; script output checks it.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Appending to the four pre-RPI draft files conflicts with "preserved unchanged" and the edit boundary

* Related IDs: plan Scope, P02-T01, research Recovery Disclosure
* Evidence: research and plan metadata say the drafts are preserved unchanged; P02-T01 appends a clarification to them; the brief restricts edits to the addendum, index and log (recovery artifacts excepted).
* Concern: self-contradictory and an unnecessary touch of unverified material, and the plan Non-Goals list does not mention it.
* Impact: scope-diff check ambiguity and altered provenance.
* Smallest useful change: drop the draft-append step; record the disclosure only in the recovery artifacts and changes record (already present in the plan and research).
* Action owner: planning parent
* Exact resolving evidence: P02-T01 and the scope list no longer name the draft files; git diff shows them untouched.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: T2 residual gaps

* Related IDs: P01-T02 (T2), research C14
* Evidence: models are Legacy with unknown quota; capacity 10 each; no statement on failure handling; token pricing date and currency are not restated in the plan.
* Concern: a failed deployment due to capacity or legacy restriction needs the no-retry rule and a "T2 does not proceed" outcome; the 4.61 figure needs price date, currency and a statement that it excludes deployment-hours (zero for GlobalStandard, to be confirmed).
* Impact: minor; could cause a speculative retry.
* Smallest useful change: add one failure rule (first capacity or quota error stops T2, no retry, not counted as a pass) and price provenance for 4.61.
* Action owner: planning parent
* Exact resolving evidence: T2 row contains the failure rule and dated, currency-labelled price basis.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-010 -->
### PC-010 [Low]: Front Door retirement effective date and rollback cost are not in the S1 hard gate

* Related IDs: P01-T01 (S1), P01-T02 (T0)
* Evidence: S1 assumes retirement effective 21 Oct while T0 requires owner choice, inventory, and separate retirement approval; recreation via public-edge-existing.bicep would re-add about 10.64 USD/day.
* Concern: the 418.37 figure holds only if the change occurs on 21 Oct; the delay sensitivity exists but is not tied to the eligibility rule or to a recompute at the actual effective date, and the recreation cost is not shown.
* Impact: S1 headroom overstated if the owner acts later.
* Smallest useful change: state that S1 and eligibility are recomputed with the actual effective date, include a row for 22, 23 and 25 Oct, and note the rollback cost.
* Action owner: planning parent
* Exact resolving evidence: sensitivity rows in the addendum matching the script.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Arithmetic recomputes exactly; unknown subscription spend is promoted to a gating item; the recovery provenance is disclosed; commands named in T0 and T1 exist in the repository; identity and RG preservation, no-retry and no-acceptance boundaries are stated.
* Residual risk accepted by the owner in any case: R, the run rate and the SQL saving are assumptions; subscription spend remains owner-only; T1 preconditions (sentinel, tenant consent, roster, private executor) may not be met before expiry, so the plan may yield no executed tranche.

## Questions or Blocking Evidence Gaps

* None blocking the critique. Owner-only execution inputs (U, R, S1 or S2 choice, executor) remain outside the planning scope.

## Limitations

* Addendum text, prices and Azure state were not re-verified; the analysis rests on the supplied research. The pre-RPI critique was used only as an unverified concern list.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-002 and PC-004 as the same gating design)
* Action owner: planning parent
* Smallest next action: direct revision of the details for P01-T01 and P01-T02 (U term, one threshold ladder, per-tranche do-not-start, T1 and T3 tables), then drop the draft-append step; finalize without another critique
* User response required: no

## Related Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-20/paid-execution-plan-126-recovery-plan.md](.copilot-tracking/plans/2026-10-20/paid-execution-plan-126-recovery-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md](.copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md](.copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md) | Supporting research |

## Next Steps

* Return the verdict to the planning parent, which applies PC-001 to PC-010 directly and finalizes. No user action is required.
