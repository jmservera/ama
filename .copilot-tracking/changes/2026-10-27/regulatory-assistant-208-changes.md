<!-- markdownlint-disable-file -->
# RPI Changes: regulatory-assistant-208

## Metadata

* Task: 208; regulatory-assistant-208
* Date: 2026-10-27
* Scope: full independent synthetic plan P01-P03, not full issue acceptance.
* Plan: .copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md
* Details: .copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md
* Original critique: Revise; six compatible direct planner corrections applied.
* Status: P01-P03 implementation/evidence complete; ready for one Review.

## P01: Durable conflicts and consumption

Implemented automatic supported-conflict referral with exact selected
question/both cited versions, owner-isolated inbox and sender receipt inside
the existing transaction. Manual doubt uses the same writer. Dedupe is the
stored thread/turn, not equal text or a new ask retry. Sender role/thread and
named owner's case scope are rechecked under lock; trusted authenticated role
survives repeated admission. Missing owner/capability fails closed.

Added regulatory_usage's closed task/schema/day/outcome/zero-call contract,
metadata in chat audit/checks/alerts, and guarded own-role/day status/usage
read model. SQL projects foreign detail as NULL across at most 1,000 audit
positions; JSON reads at most 256 KiB and 1,000 complete lines. Coverage is
audit-only or partial, never exact daily turn totals. No question/source/home
content enters usage. Draft privacy inventory retains unknown DPO periods.

SQL audit/turn/referral is atomic, including an actual COMMIT-before-effect
failure test. JSON pre-save rollback and post-save separate-audit failure
are distinguished: saved turns stay saved and errors require history reload.
No lost-acknowledgement or whole-request idempotency is claimed.

## P02: Evaluation and presentation

Extended comparator with explicit Unknown service/accepted-check costs,
missing denominator/price/billing/review effort and zero enabled inference,
tokens and paid authority. Independently authored fixture and forged-usage
negative controls retain separate citation/answer/refusal/hazard checks.
Regenerated the existing stateless 60,000-home seed-174 report. Cards_only
remains the ship recommendation, not an actual release approval.

Existing Fluent/native alert/chat UI shows zero calls, current-role/day
recorded outcomes, Unknown cost and automatic referral/restored receipt state.
The usage paragraph has aria-live but no second status role, preserving the
established single status selector. Touched question field has name and
autocomplete; new summary dates/numbers use Intl formatters. No redesign,
framework, dependency, workflow/check-name or safety route changed.

## P03: Validation and acceptance

Updated core/API/agents guides, existing regulatory-literacy synthesis and
draft DPIA, reference index and append-only log. Prior dated acceptance audits,
original critique verdict and all human checkboxes are preserved.

### Executed local evidence

Commands used the session's external files/venv after the actual missing-import
failure; only existing editable core/agents/API dev extras were installed
with pip. PYTHONPATH names test directories, never retired code or data.

| Check | Command/scope | Observed result |
| --- | --- | --- |
| Initial relevant baseline | unittest test_regulatory_chat test_regulatory_answers test_regulatory_chat_api | 31 tests, OK |
| Expanded routing/usage regression | Core/API chat, core privacy/usage, development gate method | 37 tests, OK after corrections below |
| Affected core suites | From src/core: PYTHONPATH=tests python -m unittest test_regulatory_chat test_regulatory_usage test_regulatory_privacy test_rule_engine test_rulecards test_source_freshness test_chatthreads test_chat_privacy -q | 114 tests, OK |
| Agents discovery | From src/agents: PYTHONPATH=../core/tests python -m unittest discover -s tests -q | 106 tests, OK |
| API discovery | From src/api: PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q | 1,122 run in 797.893s; OK, 314 skipped (808 passed) |
| Core quality | ruff check .; ruff format --check .; mypy | Passed; 102 formatted files, 155 typed source files |
| Agents quality | ruff check .; ruff format --check .; mypy | Passed; 19 formatted files, 23 typed source files |
| API quality | ruff check .; ruff format --check .; mypy; node --check src/zava_forward/api/web/chat.js | Passed; 46 formatted files, 88 typed source files |
| Frozen evaluation | src/agents/evals/run_regulatory_gates.py --record src/agents/evals/regulatory_gates_results.json | Process completed; separate check outcomes, no overall acceptance |
| Real browser | src/api/checks/regulatory_ux_check.py --axe external/axe-4.10.3.min.js --out external/reg208-browser-attempt2.json | Passed, 21 states; axe 4.10.3 executed, Chromium 156.0.8078.4 |
| Migration guard | python tools/rename-zava-tests.py in prepared venv | 25 tests, OK after missing declared dependencies installed |
| Whitespace / links | git diff --check; manual review of changed relative links/headings | Passed at implementation reconciliation |

The browser used constructed loopback fixtures, blocked non-loopback requests,
and measured native target sizes, seven staff roles/supplier denial, widths,
keyboard, enlarged text, reduced motion, conflict/receipt restoration,
usage and errors. Axe digest:
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
No participant study or full WCAG/assistive-technology acceptance follows.
API skipped tests are not executed passes; no cloud/platform/opt-in acceptance
is inferred. The expected unavailable-law-store tracebacks are explicit
unknown-state diagnostics in successful negative tests.

Evaluation measured citation validity 7/7; answer/refusal contract 24/24,
including 17 refusal cases; expected rule hits 78,000/78,000; state agreement
120,000/120,000; seeded hazards 42,000 with zero misses. Small SQLite integration
also ran. Thresholds remain provisional; 60,000 stateless identities are not a
continuing-stock pipeline, held-out human grading or actual-model evaluation.

External session logs: reg208-core-tests.log, reg208-agents-tests.log,
reg208-api-tests.log, reg208-migration-tests.log, reg208-evaluation-run.json,
reg208-browser.log and reg208-browser-attempt2.{log,json}. These are local
execution evidence, not publication receipts or cloud results.

### Original adverse results and direct corrections

* System-Python import failed with ModuleNotFoundError; installed existing dev
  extras in an external venv. No manifest or namespace workaround was added.
* First expanded unit run exposed an unbound created flag on ask rollback and
  loss of trusted authenticated-role marker on re-admission. Corrected both;
  subsequent expanded and affected suites passed.
* Initial Ruff runs found test closure/long-line formatting issues; corrected
  using existing formatter and explicit capture. Initial core mypy found an
  inferred object result; added the precise list[dict[str, Any]] annotation.
* First browser attempt failed because the new usage status created two
  role=status matches. Retained aria-live and removed the redundant role;
  original failed browser log remains, second attempt passed all 21 states.
* System-Python migration guard ran 25 tests with seven missing pptx/PIL
  errors. Installed existing tools/rename-zava-requirements.txt in the venv;
  recovered run passed 25 tests. Its broken.pptx diagnostic is the expected
  negative fixture, not an unhandled failure.

### Changed-web review

Fetched the complete current web-interface-guidelines source before edits and
refreshed it on 2026-10-27 before reading the complete changed chat.js. New
content uses native semantics, text status, polite live updates, Intl formatting,
bounded lists and existing keyboard/Fluent styles. Repository ASCII and
plain-language rules override generic curly-quote/title-case suggestions.

#### src/api/src/zava_forward/api/web/chat.js

* src/api/src/zava_forward/api/web/chat.js:196 - inherited question drafts have
  no navigation-loss warning; distinct nonblocking UX follow-up, not newly
  introduced. Do not equate the scoped axe result with every guideline passed.
* Existing source/alert timestamp displays remain raw provenance strings.
  New usage-period display is localized; no unrelated date/UI overhaul.

## Criterion-Level Evidence and Unmet Boundaries

Keys match the plan allocation and original issue text; T denotes appended
tokenomics criteria. No issue checkbox was changed. All five issues are Refs,
not Closes; no aggregate acceptance is claimed.

| Criterion | Actual evidence | Full-acceptance boundary |
| --- | --- | --- |
| 208.1 | Research read #440 and architecture stabilization dependencies | #440 checkpoint unmet, coordinator |
| 208.2 | Existing ADR 0005 accepted synthetic development, dated 2026-10-16 | Not operational/legal acceptance |
| 208.3 | Existing cards/checks/chat/monitor implementation and affected regressions | Child acceptance/order ratification unmet, owner |
| 208.4 | Closed exact-excerpt/refusal fixture, mutation tests and independent engine tests | Actual Legal/held-out grading absent |
| 208.5 | Synthetic admission/capability/privacy denial tests | Actual appointments and live approvals absent |
| 214.1 | Exact fixed sections, provision/fact metadata; 7/7 citation cases and mutation controls | Not semantic/legal validation of generated prose |
| 214.2 | Core role projection/minimisation and API trusted-role/capability denial tests | No actual Foundry request or tenant acceptance |
| 214.3 | 17 refusal cases and unsafe/mixed/future/terms negative controls | Human Legal/held-out acceptance absent |
| 214.4 | New core automatic conflict tests, HTTP referral, browser conflict/restored receipt | Synthetic named exercise owner, not operational appointment |
| 214.5 | Existing selected-turn route and new shared per-turn referral writer | No operational appointment or received human decision |
| 214.6 | Inert exact source quotes; hostile-source/question fixture and privacy assertions | No actual-model adversarial assurance |
| 214.7 | Engine isolation tests; hostile chat leaves cards/alerts/holds unchanged | No model introduced or model-negative study |
| 214.8 | SQL/JSON restart, exact stored pair/referral, real COMMIT rollback and HTTP history | JSON audit remains separately committed |
| 214.T1 | Closed usage tests, bounded current-role/day HTTP summary, UI and check/alert metadata | Zero inference only; not a nonzero owner budget or exact turn total |
| 216.1 | Independent fixture, 24 contract cases, citation/refusal mutations and separate report | Owner-agreed targets/graded held-out set absent |
| 216.2 | Hazard omission/identity negative controls, critical miss classification | Synthetic engineering baseline only |
| 216.3 | Reproduced 60,000 stateless identities, 78,000 rule hits, small SQL check | Continuing-stock ingestion and owner baseline review absent |
| 216.4 | Same-source comparator and cards_only without staff value | Paired staff trial/measured benefit absent |
| 216.5 | Source-freshness suites/API history/browser stale states | Live monitoring/legal currentness not performed |
| 216.6 | Separate named check outcomes/counts/failures; no overall pass | No aggregate acceptance inferred |
| 216.T1 | Unknown accepted-check/service cost, four missing-input groups and cards_only | Staff-accepted denominator/prices/billing absent |
| 216.T2 | Closed zero calls/tokens/paid authority, explicit absent expiry | No paid model run authorized or executed |
| 215.1 | Existing seven-role guidance, supplier denial, browser role states | Actual role-needs validation absent |
| 215.2 | Alert source/status/action/owner/clock and browser assertions | Fictional clocks are not statutory/legal acceptance |
| 215.3 | Native controls, non-colour labels, keyboard/plain mode, 21 browser/axe states | Full WCAG/manual assistive-tech acceptance not established |
| 215.4 | Refusal/no-source/manual doubt and automatic conflict/restoration browser states | Human route is an exercise, not legal approval |
| 215.5 | Explicit Not evaluated in development evidence | Repairs/housing/grants participants required |
| 217.1 | Existing and updated DPIA draft; actual/live mode denied | Completed DPO assessment absent |
| 217.2 | Unknown/simulated periods and metadata-only review; usage inventory updated | DPO periods/disposal/hold/rights decisions absent |
| 217.3 | Bounded allowlisted retrieval with no provider call, content canaries excluded | Actual Foundry privacy/terms evidence absent |
| 217.4 | Separate capability mapping and HTTP denial, trusted-role preservation | Actual Entra assignments/ingress unverified |
| 217.5 | Append-only lifecycle/check/alert stores; new atomic turn/referral SQL tests | JSON audit separate; DPO retention unresolved |
| 217.6 | Cross-role/home/injection suites and new transaction-time revocation tests | No deployed security acceptance |
| 217.7 | Named-human/reasons safeguard exercised in core engine suites | Legal applicability/actual appointments not decided |
| 217.T1 | Metadata-only scoped usage, SQL audit/rollback, bounded reads and DPIA inventory | Actual DPO periods/rights/assessment remain unmet |

## Amendments and Divergences

No material divergence. Critique clarified bounded audit-only aggregates,
transaction-time authorization, per-turn idempotency, actual COMMIT testing and
the JSON post-save separate-ledger limitation.

Implementation-time corrections above preserve the approved plan. P01/P02
markers and details are reconciled with current code/evidence. P03's completed
implementation marker covers validation/documentation and Review handoff, not
the future independent Review execution itself. New test-method
budget is retained: 11 added methods, zero removed, within 20-method maximum.
No second critique or Review is planned.

## Blockers and Remaining Work

Human criteria and #440 remain unmet. Mandatory full publication gate is not
authorized by caller; do not invoke it or substitute a scoped claim. No issue
checkboxes changed. Publication remains blocked.

Neither --all nor --changed was invoked. The optional scoped gate cannot
resolve the higher-priority complete publication gate, so no heavy lock/run
was consumed. No Azure resource or private dataset was accessed. No model
call, paid run, new budget, live legal check or actual staff study occurred.

Distinct follow-ups remain outside P01-P03: owner threshold/paired-staff
measurement; Legal/Compliance/DPO appointments, DPIA, retention and rights;
coordinator #440 and legitimate publication-policy reconciliation; inherited
unsaved-draft navigation UX. Review must route these separately, not silently
expand or re-enter this implementation.

## Review Handoff

Assess the complete synthetic slice against the current plan/details, original
Revise critique and six direct dispositions, research and 35 criterion rows.
Retain this evidence and the original Review verdict. Do not repair source
during Review or run a second Review. Publication and human acceptance are
not satisfied by local tests or implementation completion.
