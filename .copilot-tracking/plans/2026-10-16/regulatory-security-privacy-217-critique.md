<!-- markdownlint-disable-file -->
# RPI Plan Critique: Regulatory security and privacy implementation plan

## Metadata

* Task ID: 217 / regulatory-security-privacy-217
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-security-privacy-217-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/regulatory-security-privacy-217-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: full synthetic implementation of issue 217
  on a clean `feat/regulatory-security-privacy-217` branch atop merged PRs
  328/331/348; no operational/DPO approval; draft (never approve) the DPIA for
  Juan Manuel Servera; code changes limited to `src/` and `infra/`; no private
  data, environment files, or cloud actions; max 20 added tests, no removals;
  owners and validation locked in the plan.
* Research and evidence considered:
  `.copilot-tracking/research/2026-10-16/regulatory-security-privacy-217-research.md`,
  the plan and phase-details files above, and direct inspection of
  `src/core/src/zava_forward/core/regulatory_chat.py`,
  `src/core/src/zava_forward/core/rule_engine.py` (+ `test_rule_engine.py`),
  `src/core/src/zava_forward/core/chat_privacy.py`,
  `src/core/src/zava_forward/core/chatthreads.py`,
  `src/api/src/zava_forward/api/auth.py`,
  `infra/entra/app-registration.json`, `infra/scripts/create-api-app-registration.sh`,
  `infra/tests/test_identity_rbac.py`, `infra/role-assignments.json`,
  `docs/reference/research/chat-memory-dpia.md`.
* Decisions, dependencies, and acceptance criteria considered: the 2026-10-16
  user decisions block in the plan (synthetic-only ADR 0005, draft-not-approve
  DPIA, `src/` + `infra/` only, no private data/cloud, PR with `Refs #217`); the
  Phase Checklist (P01-T01, P02-T01, P02-T02); the Acceptance Criteria section;
  the "Critique Disposition" gate blocking implementation until this critique.
* Assessment boundary: this critique can confirm or refute claims the plan and
  research make about the *current* merged baseline (328/331/348) by reading
  that baseline directly. It cannot predict the quality of code not yet written,
  and it defers to confirmed user direction (synthetic-only scope, draft DPIA,
  `src/`+`infra/` boundary, 20-test ceiling) as already-resolved rather than
  re-litigating it.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Research: "significant-decision check currently accepts evidence without recorded reasons" | Partial/Contradicted | `rule_engine.py` `_text()`/`evaluate()` (merged in PR #328, `0f9ba37`) already requires nonempty `evidence` before returning `clear` for both the automated-decision-safeguard and hazard-hold-release paths; `test_rule_engine.py::test_significant_decision_missing_evidence_pending_and_human_record` already asserts this end-to-end. See PC-001. |
| FR: "RegulatoryChat separately from author and owner roles ... unique object binding ... including generic thread reads" | Partial | Generic per-thread object binding via `user_key` ownership already exists in `chatthreads.py::_chat_owned`/`chat_resume`, used by `regulatory_chat.py::thread()`. The genuinely new piece is an auxiliary Entra capability (`ZavaForward.RegulatoryChat`-style claim in `auth.py`, parallel to `RULE_ROLE_MAP`) — this is accurately scoped as new work, but the plan's prose conflates an already-solved problem (object binding) with the actual gap (capability-claim separation), which risks mis-scoped test writing. See PC-002. |
| FR: "SQL turn and referral writes and metadata audit must commit or roll back together" | Covered (gap confirmed) | `regulatory_chat.py::ask()`/`doubt()` call `self.store._chat_event(...)` *after* the `with repo.txn(): ... repo.commit()` block closes, so a process crash between commit and the audit call can leave a turn without an audit event, exactly as the research states. This is a real, correctly identified gap. |
| FR: "Register all three auxiliary roles in infra" | Covered (gap confirmed) | `RULE_ROLE_MAP` in `auth.py` defines `ZavaForward.RuleAuthor`/`ZavaForward.RuleOwner`, but neither appears in `infra/entra/app-registration.json` `appRoles` nor in `infra/scripts/create-api-app-registration.sh`'s `roles` array; `infra/tests/test_identity_rbac.py` only checks the primary `DEFAULT_ROLE_MAP` parity, so the gap is untested today. Plan P01-T01/"infra" ownership line is correctly targeting a real, currently-unregistered pair plus the new RegulatoryChat role. |
| FR: "checks/alerts/source/audit retention classes without inventing periods" | Covered (gap confirmed) | `ChatPrivacy.decision()`/`MEMORY_CLASSES` only cover chat/memory retention; no existing per-class surface for checks/alerts/source/audit. This is genuinely new, bounded work consistent with "do not invent periods." |
| Acceptance Criteria: 20-test ceiling and ownership split (core/API/agents/infra) | Partial | The ceiling is a hard cap, not a budget guarantee; see PC-001's effect on test allocation. Ownership split itself is coherent with the files touched. |
| Non-Goals: "No generative model, new SQL authority, destructive retention worker or operational activation" | Covered | Consistent with everything read; no contradicting evidence found. |
| DPIA: draft-only, extend existing record | Covered | `docs/reference/research/chat-memory-dpia.md` already exists as the base document to extend; P02-T02 correctly scopes this as an extension, not a new document. |

## Verdict

* Verdict: Revise
* Rationale: The plan is well-bounded on scope, authorization, and honesty
  framing (synthetic-only, draft DPIA, explicit unmet/partial acceptance
  criteria), and three of its four P01-T01 sub-items target real, confirmed
  gaps in the merged baseline. However, one sub-item — requiring nonempty
  reasons before the significant-decision evaluator returns `clear` — describes
  work that is already implemented and already tested in the merged baseline
  (PR #328). Proceeding to implement and test this sub-item as stated would
  produce no functional change, would consume part of the fixed 20-test ceiling
  on a non-gap, and would make the "Critique Disposition" and acceptance
  evidence inaccurate about what is genuinely new versus pre-existing. This is
  a planner-correctable research/plan inaccuracy, not a user-decision item, and
  should be fixed before P01-T01 execution begins.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: "Significant-decision reasons" sub-item targets an already-implemented, already-tested control

* Related IDs: Functional Requirements ("A significant-decision check cannot be
  clear without reasons"), P01-T01, P02-T01 (20-test budget)
* Evidence: `src/core/src/zava_forward/core/rule_engine.py` lines ~78-115
  (`_text()` gate on `item.get("evidence")`, used for both the
  `automated-decision-safeguard` "clear" branch and the hazard hold-release
  "clear" branch) and `src/core/tests/test_rule_engine.py::test_significant_decision_missing_evidence_pending_and_human_record`
  (asserts `unknown` → `attention` → `clear` only once `evidence="SYN-HUMAN"` is
  present). `git log` confirms both were introduced in PR #328 (`0f9ba37`,
  "deterministic rule engine and scoped step alerts"), which the plan's own
  baseline (merged 328/331/348) already includes.
* Concern: The research document and phase details state this behavior is
  currently missing ("currently accepts evidence without recorded reasons")
  and direct P01-T01 to add it plus bump `ENGINE_VERSION`. Direct inspection
  shows the nonempty-reason requirement, and a passing regression test for it,
  already exist on the stated starting branch.
* Impact: Implementing this sub-item as currently written either (a) produces
  no behavior change and wastes part of the fixed 20-added-test ceiling on
  tests that duplicate existing coverage, shrinking the budget available for
  the genuinely new gaps (RegulatoryChat capability separation, audit atomicity,
  per-class retention), or (b) prompts an unnecessary `ENGINE_VERSION` bump that
  invalidates currently-valid checkpoints for no corresponding control change,
  which is a confusing, unjustified operational side effect to document in the
  changes/acceptance evidence. Either way, the final acceptance record would
  misrepresent what issue 217 actually added.
* Smallest useful change: Before starting P01-T01, re-verify against the actual
  checked-out branch whether a distinct gap remains in this area (e.g., some
  other code path that bypasses `evaluate()`'s reason gate, or a currently
  untested boundary such as whitespace-only reasons). If none remains, drop the
  "require nonempty reasons" sub-item and its implied `ENGINE_VERSION` bump from
  P01-T01, and reallocate any test budget earmarked for it to the confirmed
  gaps (PC-002, audit atomicity, per-class retention). If a narrower, real gap
  is found (for example, a path where `evidence` is accepted as a non-string
  truthy value, or where callers can bypass `evaluate()`), restate the P01-T01
  item to name that exact gap instead of the already-closed one.
* Action owner: Planning parent (direct correction to phase details and plan
  before P01-T01 execution).
* Exact resolving evidence: Updated phase-details P01-T01 text that either
  removes the already-satisfied reason-gate item or names the specific residual
  gap it targets, with the revision checked against `rule_engine.py`/`test_rule_engine.py`
  on the actual implementation branch.
* Decision route: Direct planner correction — this is a factual re-check against
  already-readable source, not a user policy choice.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: RegulatoryChat "unique object binding" wording conflates existing generic ownership with the actual new capability gap

* Related IDs: Functional Requirements ("Map RegulatoryChat separately from
  author and owner roles, requiring unique object binding at trusted-proxy
  boundaries, including generic thread reads"), P01-T01, P02-T01 ("negative
  role/object binding, direct and generic HTTP access")
* Evidence: `src/core/src/zava_forward/core/chatthreads.py::_chat_owned`/`chat_resume`
  already enforce per-thread ownership by `user_key` for every chat thread,
  generic or regulatory, and `regulatory_chat.py::thread()` already calls into
  that path plus an additional `owner_role` check. The one piece that does not
  yet exist is a distinct Entra app-role/claim for regulatory-chat access,
  analogous to `RULE_ROLE_MAP`'s `ZavaForward.RuleAuthor`/`RuleOwner`, in
  `src/api/src/zava_forward/api/auth.py`.
* Concern: The FR wording ("requiring unique object binding ... including
  generic thread reads") reads as if object-level binding for generic thread
  reads is new work, when it is already generic, pre-existing behavior. The
  real novel surface is the auxiliary capability claim at the auth-provider
  layer, which the phase details correctly separate out ("existing auxiliary
  capability map, not the mutually exclusive staff-role map") but the FR
  summary does not make this distinction explicit.
* Impact: Low risk of wasted implementation effort (the phase details are
  already more precise than the FR summary), but a moderate risk that P02-T01's
  negative test set re-tests already-covered generic ownership denial instead of
  covering the actually-new capability-claim boundary, again competing for the
  fixed 20-test ceiling.
* Smallest useful change: Tighten the FR bullet (or add a one-line clarifying
  note) to state that per-thread ownership binding already exists generically,
  and that the new control is the auxiliary RegulatoryChat capability claim at
  the trusted-proxy boundary, so P02-T01 test writers target the new capability
  check and its denial paths rather than re-asserting already-covered generic
  ownership.
* Action owner: Planning parent (direct wording correction; no user decision
  needed).
* Exact resolving evidence: Revised FR/phase-details text distinguishing
  pre-existing generic ownership from the new capability-claim gap, consistent
  with the already-correct P01-T01 phase-details language.
* Decision route: Direct planner correction.

## Strengths and Residual Risk

* The audit-atomicity gap (SQL turn/referral commit vs. a separate, later
  `_chat_event` call) is correctly identified and is a credible, well-scoped
  target for a locally provable fix and test.
* The infra auxiliary-role registration gap (`RuleAuthor`/`RuleOwner` absent
  from `app-registration.json` and the registration script, with no test
  catching it) is correctly identified and real; folding the new
  `RegulatoryChat` role into the same registration fix is a reasonable,
  minimal-surface-area approach.
* The per-class (checks/alerts/source/audit) retention-unknown surface is
  genuinely new, bounded, and explicitly declines to invent numeric periods,
  which matches the "no DPO approval" constraint honestly.
* The plan's acceptance-criteria section already distinguishes locally provable
  claims from explicitly partial/unmet DPO- and operational-dependent criteria;
  this residual gap (DPO completion, tenant provisioning, live Azure SQL
  evidence) is explicitly accepted by the user's stated decisions and does not
  need further findings here.
* Scope discipline (`src/` + `infra/` only, no mvp/prototype changes, no new
  dependencies, no destructive retention worker) is consistent throughout the
  plan, phase details, and research, with no contradicting evidence found in
  source.

## Questions or Blocking Evidence Gaps

* None that block disposition. PC-001 is resolvable by the planning parent
  re-checking the stated gap against source before P01-T01 begins; it does not
  require a new user decision because the user's authorization already covers
  "full synthetic implementation" of genuine gaps within the locked scope, and
  this finding only narrows what counts as a genuine gap.

## Limitations

* This critique read the merged baseline at the current worktree HEAD
  (`feat/regulatory-security-privacy-217`-equivalent state including PRs
  328/331/348) and the plan/phase-details/research artifacts; it did not run
  the test suite or execute any code, and it did not review `src/agents` or
  `src/api` test files exhaustively beyond the auth, regulatory-chat, and
  identity-RBAC files cited above. Any additional gap in those unreviewed test
  files is outside this critique's evidence boundary.
* No DPIA, DPO, tenant, or Azure artifacts were available or relevant to review
  per the stated synthetic-only, no-cloud boundary, consistent with the plan's
  own stated boundary.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: Revise P01-T01 (and the research note it is based on)
  to drop or re-target the "significant-decision reasons" sub-item per PC-001
  before starting implementation; fold in the PC-002 wording tightening at the
  same time since it touches the same phase-details section.
* User response required: No — both findings are direct, evidence-backed
  planner corrections resolvable by re-checking already-readable source; they
  do not require a new user decision given the user's existing authorization
  and locked scope/ownership/test-ceiling constraints.

## Related Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-16/regulatory-security-privacy-217-plan.md](.copilot-tracking/plans/2026-10-16/regulatory-security-privacy-217-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-16/regulatory-security-privacy-217-phase-details.md](.copilot-tracking/details/2026-10-16/regulatory-security-privacy-217-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-10-16/regulatory-security-privacy-217-research.md](.copilot-tracking/research/2026-10-16/regulatory-security-privacy-217-research.md) | Research basis containing the PC-001 inaccuracy |
| [.copilot-tracking/changes/2026-10-16/regulatory-security-privacy-217-changes.md](.copilot-tracking/changes/2026-10-16/regulatory-security-privacy-217-changes.md) | Scope/validation-intent record |
| [src/core/src/zava_forward/core/rule_engine.py](src/core/src/zava_forward/core/rule_engine.py) | Evidence for PC-001 (existing reason gate) |
| [src/core/tests/test_rule_engine.py](src/core/tests/test_rule_engine.py) | Evidence for PC-001 (existing passing test) |
| [src/core/src/zava_forward/core/regulatory_chat.py](src/core/src/zava_forward/core/regulatory_chat.py) | Evidence for PC-002 and the confirmed audit-atomicity gap |
| [src/api/src/zava_forward/api/auth.py](src/api/src/zava_forward/api/auth.py) | Evidence for PC-002 and the confirmed infra auxiliary-role registration gap |
| [infra/entra/app-registration.json](infra/entra/app-registration.json) | Evidence for the confirmed infra registration gap |

## Next Steps

Run `/rpi-plan` to apply the PC-001 and PC-002 corrections to the phase details
(and, if needed, the research note) before P01-T01 execution begins; no other
user action is required.
