<!-- markdownlint-disable-file -->
# Research: post-153 integration checkpoint for #440 (2026-11-12)

* Session: native session UUID `d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b`; task slug `post153-integration-440-1112`; RPI Agent, manual-style sequential run, research executed.
* Research disposition: `executed`. Posture: `focused` (bounded internal task, named source targets). Provenance: caller direction. Delegation: none; all waves inline (a read-only diff review does not benefit from isolated context). Output mode: `convergence` limited to the evidence plan below.

## Research brief

* Topic: bounded integrated evidence for two inputs merged after the previous #440 checkpoint (PR #1478, merge `4074b44f3704b860dd4b890473cca620115d3dca`): PR #1470 (proposal-card plain-language source) and PR #1475 (five-home demo runbook).
* Purpose: record a new dated section in `docs/architecture/cutover-evidence-pack.md`, an index entry and an append-only log entry. Existing issue #440, newly due recurring checkpoint. Not a new issue, not a reopened correction campaign, no new correction allowance.
* Non-goals: repeating the 281-test campaign; coordinator, HVE or source corrections; product fixes; new issues; full gate, Docker, SQL, browser installation, Azure, model or cloud calls; push, PR, merge.
* Active controls (caller): work only in this worktree on `docs/post153-integration-checkpoint-440-1112`; do not touch the primary checkout; memory is context, not evidence; private data not read.

## Extensions selected

| Item | Provenance | Use |
| --- | --- | --- |
| Repository instructions (AMA, `applyTo **`) | system context | Markdown style, evidence classes, branch and commit rules, validation tiers |
| `docs/reference/method/tracking-retention-policy.md` | read | New dated files only; no deletion or rewrite of earlier artifacts |
| `rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review` skills | host skills | Phase protocols |
| Web design skills and web-design-guidelines | skipped | No web file is edited; the web portion is read-only static observation. Disclosed: no fresh Web Interface Guidelines fetch and no web review of changed files is claimed |
| Specialist subagents | skipped | Single continuous trace, fewer than five direct reads |

Start documents read: `docs/reference/README.md` (index), `docs/reference/memory.md` (context only), `docs/reference/log.md` tail, the previous checkpoint section (cutover pack from line 7387), `docs/reference/method/tracking-retention-policy.md`. The addendum and original case study were not read end to end; they are not needed for a source-link check. This is stated as a limit, not as coverage.

## Identities (read 2026-11-12, local git)

| Item | Identity |
| --- | --- |
| Worktree HEAD and freshly fetched `origin/main` | both `4074b44f3704b860dd4b890473cca620115d3dca` (PR #1478 merge); root tree `88a7ffbd1c88ecdaee5a3f538579fbcabfab5dd2`; `src` `b03b4c9d8ca1dbabc04a9032686a471bf300100c`; `docs` `99601f87116262eb1add72b7aeb3cf0271b9b461`; `infra` `a022907662e2a98374f36d8f641eefd29d0dc798`; `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9` |
| PR #1470 merge | `088e8c3c031be45b22422b91b3195b0988583ebd`, tree `68f0db875dfab4ad5b1f9fa4410a8b47c359148d`; 6 non-evidence paths: `assistants.js`, `assistants_browser_check.py`, `test_content_standard.py`, `test_case_journey.py`, `content-standard.md`, `log.md` (plus 16 tracking files) |
| PR #1475 merge | `38d3ed18703ee05c6795f715b6e62600d36225ec`, tree `cc219a7fc19c31b876144aa9ac783fd9863d6c5f`; documentation only: `runbook.md`, `docs/reference/README.md`, `log.md` (plus 7 tracking files) |
| Source delta from the previous tested pin `bbb1d20cc` | `src` tree `60d841010c4a` (pin) to `b03b4c9d8ca1` (now); 4 files, 554 insertions, 179 deletions (the 1470 files above minus docs). No other source change |
| Document blobs at HEAD | `assistants.js` `40cfc532cab0`; `test_content_standard.py` `029516bee815`; `test_case_journey.py` `f05d5eee41b7`; `runbook.md` `e15eef73925b`; `content-standard.md` `aa1cf210269f`; `cutover-evidence-pack.md` `9be680f41966`; `log.md` `30bacbe7309c` |
| Status documents (blob, status) | BRD 0.21.0 `draft` `34d88395de86`; PRD 0.21.0 `in-review` `c788b917bafa`; ADR 0003 `d60645397b20` and ADR 0006 `956da1a3b804` Accepted; ADR 0007 `541e0f72dd2c` Proposed. Unchanged by #1470 and #1475; draft, in-review and Proposed are not approval |
| Issue and PR states (live `gh`) | #440, #153, #132, #134, #184 OPEN; #1470 and #1475 MERGED |

Exclusions: the previous 281-test set (not rerun), `assistants_browser_check.py` execution (browser harness not installed or run), SQL Server, Docker, hosted CI, Azure, models, live endpoint, any private dataset, `support/`, sensors, resident consent and human approval.

## Wave 1 (wider): candidate evidence

Candidates considered for the smallest affected set: (a) `test_content_standard.py` (changed by #1470; copy audit and disclosure structure); (b) `test_case_journey.py` (changed line 1296 for the renamed edit label; node-based assistant-card fixtures); (c) `test_quality_sensors.py` (reads `assistants.js` and `ops.js` as text, the Quality tab that the five links target); (d) `test_workspace_scripts.py` (references `assistants.js` only as a route/script allowlist, not the card); (e) the browser check `assistants_browser_check.py` (changed by #1470; needs a browser: excluded, unverified); (f) a static runbook link check for #1475 (no existing test covers the runbook: `grep` of `src/*/tests` and `tools` finds no reference to the five-home section); (g) `node --check` on `assistants.js`.

## Wave 2 (deeper): code evidence

* C1 `src/api/src/zava_forward/api/web/assistants.js:130-135`: one `<details data-proposal-technical>` titled "Suggestion details (technical, for audit and support)" holds the permitted-source `pre` and the history `pre` with the "Earlier changes" button; warnings, reasons, unknowns and the review fieldset remain outside it (the fieldset follows at the next sibling).
* C2 `assistants.js:45,115-116`: edit label is "Edited proposal (technical JSON format)" with an explanatory paragraph; `src/api/tests/test_case_journey.py:1299` asserts the new label.
* C3 `assistants.js:103,133`: both technical `pre` elements gain `tabindex="0"` and an `aria-label` and carry no `role`.
* C4 `src/api/tests/test_content_standard.py` (new method `test_proposal_card_keeps_technical_evidence_in_one_labelled_disclosure` and the rest of the diff): static assertions on the disclosure and a formatting rewrite of the audit tuples.
* C5 `docs/capstone/demo/runbook.md:48-119` (new section): five-row table, provenance bullets, preflight list; every link has the form `<origin>/app#/case/<id>?tab=quality`.
* C6 `src/api/src/zava_forward/api/web/app.js:382-387,1146`: `#/case/<encoded id>` route, `tab` read from the hash query, and a `quality` tab definition ("Quality and handover"). The route syntax in C5 matches this source. Case id shape `ZF-<4 digits>-<4 digits>` is not defined by any public source rule found: `src/core/src/zava_forward/core/chat_case_answers.py:16` uses `ZF-\d+` only. The syntax check therefore tests the runbook against itself and the route source, not against an id contract.
* C7 `docs/reference/README.md` and `runbook.md` heading: the README anchor `#demo-operating-mode-and-five-homes-owner-selected-target-2026-11-12` equals the computed slug of the heading (observed locally, see raw output).
* C8 Origin host in every link equals the host the cutover pack documents from 2026-10-31 (`cutover-evidence-pack.md`; one mention). That is provenance of a string, not availability.

## Wave 3 (contrarian): challenges to the selected set

* A browser-observed claim would be stronger for #1470, but the browser harness may not be provisioned; running it is outside the admission and the task ("unavailable optional browser evidence stays explicitly unverified"). The node fixtures in `test_case_journey.py` and static tests are not equivalent to keyboard, focus or assistive-technology evidence.
* The five-home ids cannot be verified as existing in any build from public source; the generator replay lives under `support/`, which this task excludes. No public source contains the ids other than the runbook (`git grep` over `src` and `docs` excluding the runbook and tracking found none), so the ids are unverified by independent public evidence. This is recorded, not a defect.
* The #1470 `pre` elements: ARIA 1.2 prohibits naming on a role-less (`generic`) element, and the repository's own scrollable focusable regions use `role="region"` with `aria-label` (10 `role: "region"` occurrences in `src/api/src/zava_forward/api/web/*.js`, for example `app.js:853`). This is a static, unverified concern about accessible-name exposure, not an observed assistive-technology failure. `docs/reference/research/ux/design-system.md:94-95,109` defines named `role=region` focusable scroll areas, but only for wide data tables; it does not address text blocks such as `pre`, so no repository rule is shown to be breached (correction after critique PC-003; the earlier draft said no rule text exists). Candidate owner: #153 (content and design) or #132/#134 accessibility work; routed, not filed. No new issue is created (caller rule).
* `test_quality_sensors.py` skips 92 tests unless SQL Server is configured; its passing count is therefore not SQL evidence.

## Questions and findings

| Question | Answer | Evidence |
| --- | --- | --- |
| What exactly changed in the two merged inputs? | As in the identities table; no BRD, PRD, ADR, workflow or requirement change | C1-C5, git |
| Which smallest checks cover them? | `test_content_standard` (19 tests), `test_case_journey` (31 tests, needs node on PATH), `test_quality_sensors` (187 run, 92 skipped for SQL), `node --check`, static runbook check | Observed 2026-11-12, raw files in the external evidence directory below |
| Is the five-home link contract syntactically coherent against public source? | Yes for the five ids, uniqueness, link text, route and `tab=quality`, origin string, README anchor and relative links; not for existence or availability | `five-home-static-check.out` |
| New concrete findings? | F1: unexplained accessible-name pattern on two role-less `pre` elements (static, unverified, routed to #153/#132). F2: the proposal card's keyboard and disclosure behaviour is covered only by node fixtures and static tests here; the browser check changed by #1470 is not run (an omission, not a defect). F3: no repository test exercises the runbook link contract (a coverage gap; a tiny external static check was used and is retained outside the repository). No product defect confirmed | C3, C5, C6, wave 3 |

Raw observation directory (outside the repository): `/home/azureuser/.copilot/session-state/d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b/files/checkpoint-440-post153-1112/`.

## Evidence plan fixed by research

Environment: owned venv `/home/azureuser/.venvs/post153-440-1112` (`--system-site-packages`, `pip install --no-deps -e src/core -e src/agents -e src/api` from this worktree, no uv), `env -i` with an owned empty `HOME`, `PYTHONDONTWRITEBYTECODE=1`, an owned external working directory, `PYTHONPATH=<worktree>/src/core/tests:<worktree>/src/agents/tests:<worktree>/src/api`. Origin proof is the import `__file__` plus `git hash-object` equal to `git rev-parse HEAD:<path>`, never a namespace `None`.

## Decisions, readiness and limits

* Accepted: the five checks above. Rejected: the 281-test rerun, browser harness, full gate, hosted-CI claims. Deferred: browser keyboard check of the card, a live-endpoint preflight, SQL-backed tests.
* Planning Readiness: `Ready`. All applicable Research gates pass: scope fixed, identities pinned, adverse and contrarian items recorded.
* Limits: no live endpoint, deployed availability, paid model, sensor send, resident consent or human approval is observed or implied.

## Artifacts

| Path | Description |
| --- | --- |
| [.copilot-tracking/research/2026-11-12/post153-integration-440-1112-research.md](post153-integration-440-1112-research.md) | This research record |

## Next Steps

Plan phase (parent-owned): `.copilot-tracking/plans/2026-11-12/post153-integration-440-1112-plan.md`.
