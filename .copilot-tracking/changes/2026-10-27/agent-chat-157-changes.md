<!-- markdownlint-disable-file -->
# Changes: agent-chat-157

Task 157; 2026-10-27; full P01-P03 scope.
Plan/details and original Revise critique are preserved in their dated paths.
Status: implementation in progress; P01 starts first.

## P01: Runtime

Implemented: shared cited HTTP turn path, default-deny adapter admission and
post-call admission, permission/case/source checks; per-invocation usage
validation and one metadata-only chat.turn event including rejected completions.
Complete source JSON, <=16,000 system+prompt chars, <=4,000 history chars/12
user messages, <=1,000-character new question. No memory activation.
Exact ceiling values are engineering safeguards, not approved
per-role token/budget/expiry authority. No real model calls authorized.

## P02: Warning and evaluation

Implemented: server canonical warning/status, described disabled-until-loaded
question input, explicit loading/registry errors and accurate refusal status.
Offline evaluator aggregates turn/scenario/answer consumption with actual
calls zero and token/cost Unknown. Random thread identifiers removed from
exported report so repeated evaluations remain deterministic.
Existing known grounding failure remains visible.
Final recorded report: agent-chat-157-eval.json, 24 synthetic development
scenarios / 61 turns, 33 scripted invocations, zero actual model calls,
19 answers passing runtime filters, two critical check failures in the single
known unsupported-claim/valid-citation scenario; enablement fail/disabled.
The comparator covers 18 expected answer turns (all answerable by the case
card). The nineteenth runtime answer is the known unsupported claim, not a
benefit or human-accepted outcome.

Chromium 156.0.8078.4 actually exercised warning fetch failure, keyboard
disclosure/submission, focus return, refusal/manual status, live-log attributes
and 390px visibility over loopback synthetic HTTP. This is not a screen-reader
announcement/comprehension or complete zoom/reflow conformance test.

## P03: Validation and acceptance

Initial targeted test failed with ModuleNotFoundError for zava_forward.
Installed editable core/agents/api and declared dev tools via pip in isolated
/tmp/ama-chat157-venv after that failure. No dependency manifest changes.
No Azure, private data, secrets, uv, full gate or heavy gate run.
Focused core chat/privacy tests: 73 passed. Agents chat suites: 43 passed.
Core and agents full Ruff/mypy passed; API Ruff/mypy and JS syntax passed.
Full core/API unit discovery is in progress.
Final source candidate targeted API suite including Chromium:
`ZF_BROWSER_TESTS=1 PYTHONPATH=tests:../core/tests:../agents/tests
/tmp/ama-chat157-venv/bin/python -m unittest test_chat_panel
test_chat_isolation test_role_endpoint_inventory -q` from src/api:
80 passed in 39.519s, no skips. This final run includes unsent-input preservation
and navigation guard DOM checks after a network failure.
Final all-package Ruff check/format check/mypy passed (core 153 source files,
agents 23, API 88); `node --check` chat.js passed.
Migration regression first failed seven missing Pillow/python-pptx imports in
system Python. After pip installing tools/rename-zava-requirements.txt in the
isolated venv, all 25 tests passed. No source correction required.
Complete agents discovery: 109 tests passed. Final role-history regression
passes: prior-role questions are omitted after role change; system prompt
states current sources alone are evidence. Browser preserves unsent input and
uses the existing application unsaved-form navigation guard.

## Scoped web-guideline review

Current full guideline source refreshed from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Read changed staff chat controls against all rules; no new scoped defect found.
Unchanged regulatory panel and application-wide styling are not a conformance
assessment. Repository plain-language/ASCII/Fluent conventions take precedence
over cosmetic Title Case/curly-quote preferences.

### src/api/src/zava_forward/api/web/chat.js

src/api/src/zava_forward/api/web/chat.js:34 - canonical warning, native labelled
input, fail-closed loading and explicit manual-route error; scoped pass.
src/api/src/zava_forward/api/web/chat.js:91 - existing unsaved-form guard wired;
Chromium keyboard/focus/refusal/live-log/390px and network failure checks pass.
Screen-reader announcement/comprehension evidence remains unavailable.

Initial regression attempts and corrections: evaluator report included random
thread IDs (removed from report only); decoded tool-call text escaped in JSON
bypassed raw lexical check (now checked after parsing too); API test import
precedence initially selected the same-named core module (corrected selectors);
admission test initially wrapped its own mock (now retains original function).
All original failures are recorded here, not claimed as earlier passes.

## Amendments, Divergences and Blockers

PC-001/002 incorporated; PC-003 rejected as unsupported environment claim;
PC-004 one-pass Review/publication boundary clarified. Related current-state
amendment: legacy /messages intentionally no longer sends memory. Its lifecycle
tests still exercise existing isolated memory assembly directly, and both HTTP
turns stay memory-free until the human decision. No test method removed.
Human activation/privacy/access/evaluation/accessibility/stabilization criteria
remain blocked and issue checkboxes remain unchanged.

## Issue-by-issue acceptance disposition

No new GitHub criterion is ticked and no issue receives a Closes reference.
Previously checked criteria are not reinterpreted as operational acceptance.

| Issue / criterion | Evidence and current boundary |
| --- | --- |
| #157 scoped #440 stabilization | Bounded local integration/traceability here, not the complete recurring stabilization checkpoint; remains open. |
| #157 decision accepted | Owner #158 comments and accepted ADR 0004 prove direction only. |
| #157 child acceptance | Not complete: named human gates below remain. |
| #157 memory not controlled evidence | Both HTTP turns omit memory; memory IDs rejected by existing storage tests; no new authority or controlled-write path. |
| #157 consumption before activation | Engineering caps and receipts implemented; finite owner-approved role call/token/budget/expiry limits absent, so activation blocked. |
| #162 server owner key, all route denial | Existing authenticated role/isolation suites plus new status inventory and legacy-route parity. Owner supplied only by session/current_user. |
| #162 field projection and cross-user prompt isolation | Same current case projection; current sources rechecked after completion; own user history only and dropped after role change. Existing canary tests preserved. |
| #162 injection cannot execute tools/writes | No tool executor; existing attack set, now decoded output syntax checked too. Lexical/paraphrase and actual-model assurance remain limited. |
| #162 administrator/break-glass policy | Existing metadata-only audited default deny remains; OD-46 policy is not decided by this PR. Criterion remains open. |
| #159 optional permitted panel | Existing workbench integration and role matrix; manual case controls independent. |
| #159 cited/labelled answers and abstention | API regression/golden sources and fixed label. Citation resolution is not claim entailment; known grounding failure preserved. |
| #159 follow-up case permissions | Existing per-turn tests plus post-call revocation/disappearance/source and role-history regressions. |
| #159 proposals only / independent review | Existing Assistants.invoke path retained, no controlled record tool added. |
| #159 failure/manual route | Denied admission, provider failure, oversized input and browser fetch failure evidence. |
| #159 keyboard, screen reader, announcements | Actual Chromium keyboard/focus and live-log DOM checks; no named human screen-reader/announcement test. Whole criterion remains open. |
| #159 tokenomics turn and bounds | Content-free receipts and context caps implemented. Token values Unknown for scripted provider; actual owner limits/activation not approved. |
| #164 golden multi-turn/source/refusal coverage | 24 development scenarios; source changes and revoked permissions, lexical refusal before calls, current permission/source completion checks. No independent held-out set. |
| #164 poisoning/injection before enablement | Existing scripted scenarios pass, including isolated memory assembly; no actual-model proof and known critical grounding failure. No enablement. |
| #164 thresholds, task/reviewer/state | Missing approved thresholds/reviewer/conversational registry/release; runtime denies dispatch and report remains fail/disabled. No invented reviewer. |
| #164 non-AI comparison / failures | Case card comparator and exact failures retained in generated report; no observed benefit. |
| #164 independently labelled frozen held-out | Not available; golden file/version hashes are development evidence only, not held-out approval. |
| #164 unsupported/stale/conflicting/ambiguous/source-revoked evidence | Development cases cover stale/conflicting/permissions; unsupported-claim known failure remains. Whole criterion unproven. |
| #164 memory poisoning across all inputs | Scripted attacks and no-memory HTTP boundary do not prove semantic real-model behavior. Whole criterion unproven. |
| #164 no manufactured consent/approval/contact | Existing refusal/no-write tests preserved; no contact or consent tool added. Human qualification remains external. |
| #164 actual serving/control version, thresholds and review | Development bindings updated; actual serving version and qualified release approvals unavailable. |
| #164 competent human seeded-error exercises | Not run, consent/accessibility/privacy approvals unavailable. |
| #164 shared harness/non-AI/review effort | Shared harness reused; human review effort Unknown, no single-turn pass inherited. |
| #164 finite approved actual calls/provider handling | Zero actual calls. No payload/provider/budget/expiry approval assumed. |
| #164 criteria do not authorize implementation/live use | Explicit owner request authorizes this independent local work only; no criterion itself grants live authority. |
| #164 tokenomics per-scenario/per-answer | Scripted call totals and runtime-answer denominator reported; tokens/cost Unknown with missing inputs. Quality-floor failure cannot become a saving. |
| #163 data map | Existing synthesis updated to distinguish current HTTP prompt and logical deployment target; no observed Azure/provider claim. |
| #163 DPO/Legal lawful basis, notice, DPIA, retention | All unrecorded; no retention number selected. Human blocker. |
| #163 rights locate/delete | Existing JSON/SQLite lifecycle/privacy tests; no claim that ledger/backups/provider erasure workflow is complete. |
| #163 diagnostic/performance exclusion | Receipt contains ids/counts/status only; content not added to diagnostics/performance. Linkable metadata still needs DPO retention/use decision. |
| #163 provider handling/region position | Architecture says uksouth; current provider terms/transfer evidence not retrieved or approved. Whole criterion open. |
| #163 free-text warning/redaction | Canonical server warning beside described staff input, fail-closed fetch, masking policy documented; browser DOM/keyboard evidence, not comprehension. Other free-text surfaces unassessed. |

## Handoff

Implementation P01-P03 and evidence preparation complete. The subsequent
lifecycle Review is read-only and runs once. Supplemental core/API discoveries
are still running; targeted final candidate and static evidence above are
complete. No broad-suite pass or whole-issue acceptance is implied.
No heavy --changed gate chosen; no full --all gate permitted by owner.

Source candidate is frozen for Review at baseline
0ded682bab690d24eb59b78e704be82d337bf6cd plus the src diff SHA-256
2e616b6c2242ffbe37022a78409948e34c5ea7c8d6fef48050ba8623d1d43cf7.
Later publication/state/validation-only artifact updates do not imply a second
independent assessment or exact-head approval.

## Post-Review Validation and Delivery Record

The one independent Review completed with original outcome Not accepted.
RV-001 is a Medium implementation defect: the report contains 59 consumption
entries for 61 turns because two pre-dispatch permission denials emit no receipt.
They incur zero calls, so the 33 scripted-call total is not understated, but
the per-turn reporting criterion is not met. No correction or second Review
was performed. P02 reporting completion is qualified by this finding.

Supplemental local discoveries subsequently finished:

| Command (isolated venv Python) | Final result |
| --- | --- |
| From src/core: python -m unittest discover -s tests -q | OK, 1429 tests in 802.993s; 186 skipped |
| From src/api: PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q | OK, 1128 tests in 893.244s; 315 skipped |
| From src/agents: python -m unittest discover -s tests -q | OK, 109 tests in 74.652s |

These are package discoveries, not the full RPI gate or hosted/human approval.
Existing opt-in/environment prerequisites account for skipped checks; SQL,
cloud and other skipped paths are not claimed tested. The final targeted
80-test API/Chromium run separately includes the late source changes.
The Review's then-pending broad-suite wording remains original historical
evidence; these subsequent results do not change its outcome.

Delivery decision: the owner's explicit task requires pushing a branch and
opening an evidence-backed PR using Refs for unproven criteria. Deliver a
non-accepted draft, not a ready final candidate, prominently disclosing RV-001,
the known grounding failure and all human blockers. This is a declared departure
from the self-imposed plan/Review prohibition on even draft publication, not
an override or rewrite of independent acceptance. No issue closure, merge,
activation, human decision, full/changed gate or exact-head approval is claimed.
The original assessed source diff is unchanged. Later work must address RV-001;
this one-pass task does not silently enter another implementation/Review loop.

Commit tooling note: the installed git-commit skill's get_changed_files tool
is unavailable in this CLI. Use the already inspected branch/status/diff and
independently frozen source boundary rather than inventing a tool result.
Its instruction file moved from instructions/ to rules/ and was located/read.
