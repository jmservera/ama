---
title: Issue 440 checkpoint triage, epic gating and verdicts (live demo, 2026-11-18)
description: Deduplicated issue drafts from confirmed checkpoint findings, the epics each blocking finding gates, and a continue, fix or pivot verdict per open epic
ms.date: 2026-11-18
ms.topic: reference
---

Scope: synthetic demo, desktop only, on `main` at `d7d7fdee3c2a123e777c1c6ad1496610a6a80502` (the branch base; main has moved since). Owner decisions of 2026-11-18 apply: live Azure authorised in resource group `ama`, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. This note creates no issue, changes no source and mutates no Azure resource. Refs #440.

## Evidence base

* Prior checkpoint records in `docs/architecture/cutover-evidence-pack.md` (first checkpoint 2026-10-28 and the dated checkpoints through the scoped Epic #89 and #100 records of 2026-11-15) and `.copilot-tracking/research/*440*`.
* The 2026-11-18 live demo notes under this folder, for example `deployed-parity-live-2026-11-18.md`, `public-browser-access-live-demo-2026-11-18.md`, `cutover-gate-live-2026-11-18.md` and `issue-109-live-device-monitoring-evidence-2026-11-18.md`.
* Fresh observations from this task, in `.copilot-tracking/evidence/2026-11-18/issue-440-live/` (script, JSON result, redacted container log lines; no credentials, cookies or identity claims).
* GitHub issue and sub-issue state read with `gh` on 2026-11-18 (16 open epics, 97 open issues).

Fresh observations (this task, 2026-11-18, employee account signed in through Entra with Playwright, desktop viewport 1366x900):

| Observation | Result |
| --- | --- |
| Anonymous `fetch('/api/me', {redirect: 'manual'})` in the page, default and `Accept: application/json` | Opaque redirect in both cases (not 401); `/healthz` 200 |
| Signed-in `GET /api/time/status` | HTTP 500 |
| Container console log for that request | `http-error GET /api/time/status status=500 exc=ProgrammingError` (log line retained in `container_log_time_status.txt`) |
| Signed-in `/api/me`, `/api/ai/report`, `/api/continuity`, `/api/audit-check` | 200 each |
| Signed-in `/api/law`, `/api/account/photo` | 503 each (known: law store not configured, photo token store disabled) |
| `/api/ai/report` consumption block | present; `token_cost` is `Unknown`, not zero |
| Running revisions | API `ca-cutover-test-demo-api--0000031`, resident `ca-resident-demo--0000012` (digest-pinned images, read with `az containerapp show`) |
| Local `python3 tools/check-legacy-references.py` at head | 11 violations in three `tools/test_*` files, exit non-zero |
| Static: callers of `ChatIsolation.turn` outside tests | none (`grep` over `src`) |

Classes used below: local observed, Azure observed, implemented but unverified, deferred, blocked, unknown. A merged issue count is not acceptance.

## Part 1. Findings and deduplicated issue drafts

A finding is blocking for an epic only when it is a confirmed defect on that epic's implemented surface and contradicts a stated acceptance criterion or requirement. Everything else is non-blocking and independent work continues. Candidate findings were drawn from the checkpoint records, the live notes and the fresh probes above, then compared with the 97 open issues.

### Not filed: already owned or not reproduced

| Finding | Disposition | Existing owner |
| --- | --- | --- |
| Anonymous browser-style API requests get a 302 to Entra, not 401 (reproduced live today) | Duplicate; no new issue | #350 criterion 1 and #349, an edge auth setting needing an owner decision |
| Narrow-viewport home summary covers map controls | Already filed; out of scope for the desktop demo | #1844 |
| Standalone nomination acknowledgement, correction and challenge submissions | Already filed | #1837 |
| Ranking archive durability and unusable-path reporting | Already filed | #1258, #1259 |
| Old-image test execution classified as sufficient | Already filed | #1840 |
| Hosted CI release download resilience | Already filed | #1274 |
| Rubric scoring failed on main | Already filed; original failure preserved | #1397 |
| Coordinator idle tick and stale handoff | Delivered on main by #1903; issue still open for its own criteria | #1204 |
| Storage account has no queue log category, so a poison-queue alert has no source | Duplicate; infrastructure change outside the demo remit | #146 |
| `map_fullscreen_browser_check.py` strict-mode failure of 2026-11-17 | Not reproduced on current main (the failing run used a different checkout); retained as adverse evidence, no issue | #440 comment of 2026-11-17 |
| Memory-in-prompt behaviour not covered by isolation evaluation | Traceability gap, not a defect | #164, #163 |
| `BRD::FR-016/017` and other `FR-*` numbering collisions with the PRD | Requirements governance, owner decision | none new |
| Human-review panel scores (default accept 0 of 4 detected) | Expected gate failure by design, not a defect | #223 |

### Draft D1: staff time capture status returns HTTP 500 on Azure SQL

* Title: `fix(api): return the gated "not enabled" status from /api/time/status on Azure SQL`
* Severity: Medium for the demo (a visible error where a gated explanation is specified); Low blast radius (time capture is deliberately off and case work is independent).
* Reproduction: sign in to the deployed demo as the employee test account; `GET /api/time/status` returns 500; the console log records `exc=ProgrammingError`. `TimeCapture.status` (`src/api/src/zava_forward/api/timecapture.py:151`) calls `self.request()` and `self.activation()` before building the reason, so a missing or mismatched time table or column in the demo database fails the whole status instead of reporting "switched off". Cause is a static hypothesis; the SQL error text was not retrieved because the Log Analytics workspace denies query from this host. Reproduction on SQLite or a local SQL Server container is not yet established, and the store normally attempts table creation, so the cause may differ.
* Requirement and decision links: #120 (staff time capture gated on DPIA), PRD time-capture gating requirements as mapped in `docs/architecture/mvp-to-src-parity-matrix.md`, `ADR-0002` (Azure SQL), #350 criterion 9.
* Acceptance criteria: (1) the actual SQL failure is diagnosed first (error text from the deployed database or a SQL Server container) and a failing regression reproduces that failure; (2) status returns 200 with `enabled: false` and the existing reason text when the flag is off, even when the tables are absent or unreadable; (3) a storage failure when capture is switched on fails closed and visibly, never as enabled; (4) a live check on the demo shows the gated explanation on the screen; (5) no change to DPIA, consultation, notice or dual-role activation rules.
* Dependencies: touches SQL, so the FULL validation tier applies; needs a SQL Server container check; independent of #349.
* Gates: the #350 parity criterion 9, which explicitly requires the unavailable explanation (confirmed). Impact on #113 through #120 is unconfirmed: #120's stated criteria do not name this explanation, so treat #113 as gated only if the owner or the #120 criteria adopt it.

### Draft D2: repair the legacy-reference guard allowlist

* Title: `fix(tools): add the epic retirement tests to the legacy-reference guard allowlist`
* Severity: Low for runtime, Medium for delivery (the cut-over gate check fails at head, 11 violations, reproduced today).
* Reproduction: `python3 tools/check-legacy-references.py` from the repository root exits non-zero and lists `tools/test_epic_legacy_path_retirement.py`, `tools/test_epic_parity_matrix_old_paths.py` and `tools/test_private_mvp_data_exclusion.py`. These files assert on retired paths on purpose and belong in `GUARD_FILES` (`tools/check-legacy-references.py:38`). It was first recorded in the 2026-11-15 Epic #89 and #100 checkpoints and again in `cutover-gate-live-2026-11-18.md`.
* Requirement and decision links: `ADR-0006` (src layout and cut-over, archive tag `v0.21.0`), #201, #203.
* Acceptance criteria: the three files are allowlisted with a reason, the check exits 0 at head, each intentional historical reference names archive tag `v0.21.0` (as #203 requires), any exemption is scoped to the specific lines and not the whole file where practicable, and new tests show that an added unrelated retired path in those same files still fails. Whole-file allowlisting would suppress future violations, so it is acceptable only if the owner accepts that trade-off.
* Dependencies: none; `tools/` only, but a gate tool edit is classified by impact and may need the full tier if gate semantics change.
* Gates: #195 closure (children #201 and #203). Blocking for those two only.

### Draft D3: remove or wire the unreachable ChatIsolation turn path

* Title: `refactor(core): remove or properly gate ChatIsolation.turn and its _ask`
* Severity: Low; no behaviour defect today because nothing calls it.
* Reproduction: `grep -rn "\.turn(" src --include=*.py` outside tests finds no caller. `ChatIsolation.turn` (`src/core/src/zava_forward/core/chat_isolation.py:173`) and `_ask` (line 187) would call the model without `chat_admission`, release or continuity checks if wired. Recorded as F1 in the cut-over evidence pack; still unowned and unfiled at head.
* Requirement and decision links: `ADR-0004` decisions 5 and 6, #162.
* Acceptance criteria: either the path is deleted with tests moved to the live `ChatPanel` route, or it is wired through the same admission checks with a test that a denied admission never reaches the model; the isolation and evaluation suites still pass.
* Dependencies: none; sequence after #164 evaluation work to avoid conflicts.
* Gates: nothing. Non-blocking for #157.

### Draft D4: make the AI golden fixture path independent of the source tree

* Title: `fix(agents): package the priority golden file or fail with a named configuration error`
* Severity: Low.
* Reproduction: `GOLDEN` in `src/agents/src/zava_forward/agents/ai_eval.py:41` resolves to `parents[3]/evals/ai_priority_golden.json`, so a non-editable install looks outside site-packages and the file is absent. Observed in the 2026-11-13 and 2026-11-14 checkpoints.
* Requirement and decision links: #108, `ADR-0006`.
* Acceptance criteria: a test installs the package non-editable (or simulates the layout) and the evaluation either finds the packaged fixture or raises one clear configuration error naming `ZF_AI_GOLDEN`.
* Dependencies: none.
* Gates: nothing. Non-blocking for #104.

### Observation not drafted

The 302 versus 401 behaviour for anonymous browser API requests is recorded above as a duplicate of #350. If the owner wants the Easy Auth change split from #350 it needs an owner-approved infrastructure decision first; no draft is written because a draft cannot choose that decision.

## Part 2. Which epics each blocking finding gates

| Finding | Blocking | Gated epics and children | Not gated |
| --- | --- | --- | --- |
| D1 time status 500 | Yes for #350 criterion 9; #113 only if adopted | #350 criterion 9; #113 (through #120) conditional | #73, #81, #89, #93, #100 and the rest |
| D2 guard allowlist | Yes, for cut-over | #195 (through #201 and #203) | all other epics |
| #1837 nomination submissions (existing) | Yes | #81 (through #130) | #73 |
| #1258, #1259 ranking archive (existing) | No, partially delivered hardening | none; #79 and #73 continue | |
| #1840 old-image classification (existing) | No | none | #104 |
| D3, D4, #1844, #1274, #1397, #1204 | No | none | |

Epic #89 and Epic #100 have no blocking finding and no open child. No finding is blocking for #93, #109, #123, #136, #149, #157, #165, #208 or #218.

## Part 3. Per-epic checkpoint verdicts

Verdicts are proposals from merged and live evidence, not owner decisions. No pivot is proposed for any epic; a pivot needs owner approval and no evidence here supports one. Open children were read from the GitHub sub-issue lists on 2026-11-18.

| Epic | Open children | Blocking finding | Verdict | Basis and what would change it |
| --- | --- | --- | --- | --- |
| #73 Home case and role-based workbench | #76, #79, #80 | none | Continue | Ranking hardening #1258 and #1259 are independent; closure waits on the three children and their acceptance checks |
| #81 Safety, consent, lifecycle | #130 | #1837 | Fix | Nomination submissions defect gates #130 and the epic; consent and approval boundaries are otherwise unchanged |
| #89 Provider capacity, work orders, quality | none | none | Continue; no open child, the tick waits on the listed prerequisites | All seven children closed (#90, #91, #92, #132, #133, #1384, #1402); 2026-11-15 scoped checkpoint recommended continue and no defect was confirmed; live API reads for the epic surfaces answer 200 today; PR #1641 merged 2026-11-18. The tick waits on this: the 2026-11-15 record requires the checkpoint to merge to main, exact-head hosted CI and independent review, then an owner tick |
| #93 Finance, grants, form-assisted evidence | #96 | none | Continue | #96 open |
| #100 Management insight, forecasting, export | none | none | Continue; closure waits on merge, hosted CI, independent review and owner tick | Live `/api/ai/report` shows the consumption block with `token_cost` Unknown rather than zero, which is partial support only: management views and explicit denominators for the AI-economics criterion were not verified here and stay unproven. Provisional tariff approval stays an owner item under #432 |
| #104 Bounded AI assistance with human review | #107, #108, #435 | none | Continue | Human-effectiveness and independence evidence needs people and is not provable in the demo; #1840 is independent |
| #109 In-use monitoring (IoT Hub, simulated) | #110, #111 | none | Continue | Device connectivity evidence exists; ingestion and analysis children open |
| #113 Azure platform, security, data protection | #114, #116 to #122 | D1 (through #120) | Continue, with D1 gating #113 only if adopted (see D1) | Time status 500 contradicts the #350 gated explanation; production-claim criterion is out of demo scope |
| #123 Discovery, evaluation, release governance | #124, #125, #126, #128, #129, #440 | none | Continue | This note and the changes record advance #440; the epic cannot close before #440 |
| #136 Bicep IaC and deployment pipeline | #138, #142 to #146 | none | Continue | OIDC environments and image provenance are unproven in the live notes; #142 rotation excluded by owner decision |
| #149 UX, accessibility, usability | #151, #153, #154, #155 | none | Continue | Person-run assistive-technology and usability testing are waived for the demo, which makes #155 an owner deferral decision |
| #157 Per-user chat and memory | #159, #162, #164 | none (D3 is non-blocking) | Continue | Isolation and evaluation work open |
| #165 Synthetic data: needs, generator, sensor simulator | #184 | none | Continue | Needs inventory owner approval is an owner item; #184 streaming evidenced on the demo hub for weather schema |
| #195 Repository restructure and cut-over | #198, #200, #201, #202, #203, #344, #350 | D2 | Fix | Guard allowlist failure at head blocks the cut-over gate; image-from-`src/` provenance is unproven (registry private) |
| #208 Regulatory compliance assistant (proposed) | #215, #216 | none | Continue | Decision and phase-order criteria need the owner; no evidence for a pivot |
| #218 Responsible AI release, challenge, incident control | #220 to #224 | none | Continue | Open children need Legal and human-run evidence; Legal approval is waived for the demo, so #224 needs an owner deferral decision |

Counts: 14 continue (#113 conditional on D1 adoption), 2 fix (#81, #195), 0 pivot. Epics #89 and #100 have no open child (their closure prerequisites are in the rows above) and no blocking finding.

## Limits

* Not re-run: full local suites (the heavy gate lock was held by another job and `rpi-checks.py --all` is not permitted here), SQL Server and browser harnesses, and the Entra browser flow beyond the single probe above. The prior 2026-11-15 test counts are historical.
* D1 root cause is unproven (no SQL error text); D2 to D4 are static or tool reproductions.
* No issue was created; the drafts above need owner or coordinator filing. No epic criterion is ticked and no issue is closed by this note.

## Evidence limits

* `.copilot-tracking/evidence/2026-11-18/issue-440-live/time-capture-screen.png` shows the signed-out landing page, not a time-capture screen; the probe's `time_screen_text` is empty. It is not time-capture evidence.
