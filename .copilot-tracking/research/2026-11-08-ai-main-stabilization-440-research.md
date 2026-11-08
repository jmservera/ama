<!-- markdownlint-disable-file -->
# Research: AI and employee chat current-main stabilization checkpoint (#440)

* Date: 2026-11-08, native session `9dfa8bcc-4468-4888-be6a-d543c459c94f`
* Task: `440-ai-main-stabilization-checkpoint`; branch `docs/ai-main-stabilization-440`, worktree `issue-440-ai-main-checkpoint`
* Research disposition: executed. Planning Readiness: Ready.

## Scope and trigger

Bounded docs-only checkpoint in the existing `docs/architecture/cutover-evidence-pack.md`. Trigger: merged #1275 (actionlint installer), #1271 (restart regression) and #1273 (SQL and controlled browser validation), plus #157 and #159 status-paragraph drift that the coordinator corrected (not a new adoption).

## Reading order completed

* `docs/case_study_48_original.md` (blob `0aec2d80`), addendum (`888d9ff7`), `docs/reference/README.md` (`1f5f310d`), `memory.md` (context only, ms.date 2026-09-30).
* Tracking retention policy, the existing cutover pack (3090 lines, 15 earlier #440 sections; the latest is the ranking checkpoint with a currency note, whose structure this record follows), BRD 0.21.0, PRD 0.21.0, ADR 0002, 0003, 0004, 0006.
* Coordinator scoped summaries `review-530-c162`, `review-107-0639`, `review-1274-4db` (read only those three files; no raw inspect, env or private data).
* GitHub: #157 and #159 updated bodies, #158 (CLOSED 2026-10-15T14:19:00Z), #160 and #161 CLOSED, #162 to #164, #104, #107, #116, #121, #432, #1274, #440 OPEN.

## Source pin

| Item | Value |
| --- | --- |
| Start and observed main | `608c98e639c874b127b3a4e8f9fdb335673c22c6`, tree `b518fcbc0fbd5f96d834c405a8b853f39d07cc7c`; `origin/main` equal at fetch |
| Newest main change | generated rubric commit; `.github/rubric/scores/latest.json` blob `7e10826b967a9d530dc45f75fb1df8ec9524cb09` |
| #1275 | `4bc1e3f3361a762cc9f0c187d394fdab9a11b033`, tree `85ef5852bcdd17ce73d1684e76f96b70f8d2274f` (equals the reviewed `4db31928` tree), merged 2026-11-08T10:51:51Z, `Refs #1274 #118 #138` |
| #1271 | `457a0c824972f318e41cafae635563d252f8b0ef`, tree `31d67a841b5f0884eef85115222fe56a72717117`, merged 2026-11-08T11:09:27Z, `Refs #107 #104` |
| #1273 | `a5295c45209ecc25206c79566a07191921700cfe`, tree `a6f392d4201bc75d6dfcd235805050803b0be740`, merged 2026-11-08T11:17:13Z, `Refs #530` |
| Open, excluded | PR 1278 (`6d7b52fd`, sensor analysis), PR 1243 (`eddc7d71`, complaints), PR 1240 (`c5edb320`, parent) are OPEN and not in main |

Document blobs: BRD `34d88395de861e9799eb9e24121a21c92c7a5adc` (0.21.0, draft), PRD `c788b917bafaede215f326f0efc71e071a687f1c` (0.21.0, in-review), ADR 0004 `9406c2e747ced91e5ba7be4072f9482293c0c38f` (Accepted 2026-10-15), ADR 0002 `cbe21530043ff15432cc6dce1086d080f5eb15b4` (Proposed), ADR 0003 `d60645397b20fb70ac3d1dc47c7a6c8671201306`, ADR 0006 `956da1a3b804c803041fe2e8a312bd9f400273ae`, cutover pack at start `81c183ed555a244c1072cff72b6a27a1e168a62b`.

Source blobs read: `core/assistants.py` `0f1db5ad`, `chat_panel.py` `5f7c5786`, `chat_isolation.py` `b8a33880`, `chat_privacy.py` `fa4ecb76`, `chatthreads.py` `a62aedca`, `ai.py` `8c3c3c83`, `ai_registry.py` `534dbf14`; `agents/chat.py` `634fdb0b`, `dispatch.py` `15332c12`; `api/server.py` `05a9539a`.

## Where AI is invoked (source observation, main `608c98e6`)

* Provider boundary for the five assistants and employee chat (the resident demo has separate, inventoried call sites in `test_ai_call_site_inventory.py`): `Ai._request` (`src/core/src/zava_forward/core/ai.py:88`). It refuses under a data-protection dispatch hold, requires a financial meter (`financial-meter-unavailable` otherwise), reserves, dispatch-checks and completes the consumption ledger. `Ai.evidence` (line 137) is the bounded envelope used by assistants and chat; it never falls back and records no raw output. `Ai.run` and `look_at` serve the retained legacy tasks in `ai_tasks.py` and `store.py:962` (not the five assistants).
* Five proposal assistants: `REGISTRY` in `assistants.py:36` has exactly `stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`, each with fixed roles, data categories and purpose. SQL owns eligibility (`eligible`), snapshots, claim and lease, release admission, continuity suspension, review and ledger; the model call is one per attempt (`MODEL_CALLS_PER_ATTEMPT = 1`), one agent, no tools, at most `ATTEMPT_CEILING = 3` attempts, inside `Assistants.execute` (line 1024) after `suspended`, `admission` and `release_reference` re-checks. Provider is `AgentWorker(...).provider_call`, which never raises.
* Employee chat, stored: `ChatPanel._ask` (`chat_panel.py:508`), via `/api/chat/threads/{id}/ask`. Model call only when permitted case sources exist and a model is injected; `ChatModel` (`agents/chat.py`) denies by default unless `admission` returns None, checks admission before and after the call, and signals any failure as `ModelUnavailable`. Server `chat_admission` (`server.py:49`) requires `ai_registry.authorizes_live(CHAT_TASK)` (named personal authority, or the exact owner demo-only switch plus demo profile), a gate, then SQL release (non-demo) and continuity.
* Employee chat, unstored: `ask_unstored` (`chat_panel.py:454`) via `/api/chat/unstored-ask` when storage is unapproved: rules-only `chat_case_answers.answer`, `model_calls=0`, audited `chat.turn.unstored`.
* Fallback ladder in `_ask`: refusal of approve, decide, consent, diagnose, contact asks before any call; abstain with no sources; model failure becomes `FALLBACK` text, then rules-only grounded answer with `RULES_NOTE`; replies must cite permitted facts, unsupported status words or numbers are withheld, action claims withheld.
* Proposal from chat: `/api/chat/threads/{id}/proposals` calls `Assistants.invoke`, so chat can only queue the existing independent-review proposal path (HTTP 202); `Assistants.review` enforces current role and scope, explicit human source verification, accept by the same reviewer who verified, additional independence checks for `quality-evidence`, and no general requester-differs rule; it writes only task state and events, never a domain record.
* Regulatory chat: `agents/regulatory_chat.py` is offline extractive (`model="offline-extractive"`), no provider call; separate synthetic-demo route and role rule.
* Not model inference: all controlled browser chat answers, FixtureModel evaluation and model-unavailable exercises. No actual-provider response is observed in this checkpoint.

## Authority ceiling

* AI and rules can recommend, draft, explain and flag. No assistant or chat channel writes a controlled record, approves, certifies, records consent, diagnoses or contacts a resident (`chat_panel.out_of_scope`, `ACTION_CLAIM`, `chat_isolation.TOOLISH`, `assistants` docstring "No domain write is available to the provider or this service").
* Role and scope: `ChatIsolation.current_user` on every turn verifies the supplied Entra principal through `identity.verified` (non-Entra principals re-read the staff register) and requires the `chat` projection (seven staff roles; contractors excluded); case context comes through the caller's own `detail` projection; `Assistants.authorize` re-reads role, disabled flag and case or area scope.
* Persistence: `chatthreads.py` `SqlRepo` (Azure SQL or SQLite) owner-filtered queries; `chat_privacy` refuses storage until DPIA, lawful basis and staff notice references exist (`ChatNotApproved`); retention is Unknown until a reference and day count exist.
* Owner demo-only activation: `ai_registry.DEMO_ACTIVATION` (owner `jmservera`, decision 2026-11-03) honoured only with the exact switch and `ZF_DEPLOYMENT_PROFILE=demo`; it states DPO, Legal and RAI approval outstanding. ADR 0004 option C staged adoption (2026-10-15) is the owner's architectural decision; it is not DPO, Legal, HR, control-owner or live personal-data acceptance.
* Memory: items are stored, listed, edited and deleted with per-task and global switches, but `ChatPanel._ask` builds its own prompt without memory and `status` reports `memory_used: False`. The only prompt builder that adds memory (`ChatIsolation.build_prompt`) is used by `chat_eval` isolation probes and tests.

## Requirements and decisions in play

BRD (0.21.0 draft): BG-013, FR-049, FR-050, RULE-025, RULE-026, NFR-010, NFR-011, OD-44 to OD-49 (OD-44 decided via ADR 0004), OD-51, NFR-012, FR-052, RULE-018, CON-003, CON-007. PRD (0.21.0 in-review): FR-025 to FR-028, FR-036, FR-044, FR-047, FR-055 to FR-059, NFR-015, NFR-016, NFR-003, PR-007, PR-008, SA-004, AC-091 to AC-103. ADR 0004 decisions 5 and 6; ADR 0002 decision 4 and five-assistant runtime; ADR 0003 decision 3. All IDs are document-qualified in the record. Draft, in-review and Proposed items are not approved by this checkpoint.

## Existing evidence and owners

* Coordinator-reported historical (source-qualified, not fresh at main): #1273 executed head `b02f4492` 21 actual SQL cases (privacy 13, projection 4, meter 4), zero skips, three controlled employee Chromium states with 20 axe passes and zero violations each; #1271 restart regression `0639b6e3` (3 MSSQL methods, 0 skips); #1275 `4db31928` (12 installer, 19 CI-selection, 86 runner tests; AWF checksum 504 remains #1274).
* Existing open owners: #157, #159 (screen-reader and tokenomics criteria unticked), #162, #163, #164, #104, #107, #116, #121, #432, #530, #619 (production-build assistive technology, consent and Fluent acceptance for the widget), #1274 (AWF).

## Candidate findings (to be deduplicated in the record)

* F1 (confirmed, Low, refactor): `ChatIsolation.turn` (`chat_isolation.py:133`) has no static callers in `src` or `tools` (reproduce against the pinned checkout with `grep -rn "\bturn(" src tools --include=*.py`; dynamic dispatch is not excluded by grep). It and its `_ask` (line 147) call `Ai._chat` directly with no `chat_admission`, release or continuity check, and stay a latent bypass of the admission boundary if wired by mistake. `_request` still applies the data-protection hold and the financial meter. No existing open issue matches (searches for ChatIsolation turn, legacy and dead code, memory prompt). Existing owner family: #162 (isolation) or #164; not filed here.
* F2 (traceability gap, not a defect): eval `isolation_contains` probes use `build_prompt`, a prompt that differs from the live `ChatPanel._ask` prompt (no memory there). Memory-in-prompt behaviour is therefore not evaluated on the live path; consistent with `memory_used: False` and with #164 and #163 remaining open scope (#161 is closed; any remaining memory scope is not asserted here).

## Planned validation (no execution yet)

Narrow existing selectors only, in a fresh venv under `/tmp/ai-main-440-1108` from `git archive HEAD src`, synthetic empty `ZF_DATA`, `PYTHONDONTWRITEBYTECODE=1`, `timeout`-bounded, no Docker, no provider, no Azure, no private data. No MSSQL or browser rerun; #1273 evidence stays source-qualified.

## Critique corrections applied (2026-11-08, one critique, verdict Revise)

Applied directly: role revalidation wording, review independence wording, provider-boundary qualification, F1 static-caller qualification and checkout scope, #161 closed status. Validation setup corrected in details: `ZF_CHAT_GOLDEN` points at the archived `src/agents/evals/chat_golden.json`; agents tests add `core/tests` to `PYTHONPATH`.
