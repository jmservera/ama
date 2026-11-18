<!-- markdownlint-disable-file -->
# RPI Phase Details: Rebase #215 regulatory alerts and home chat suites onto PR #1641

## Metadata

* Task ID: 215-rebase-1641-0511
* Task slug: 215-rebase-1641-0511
* Related plan: .copilot-tracking/plans/2026-11-15/215-rebase-1641-0511-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/215-rebase-1641-0511-research.md, src/core/src/zava_forward/core/chat_case_answers.py, src/core/src/zava_forward/core/chat_panel.py, src/api/src/zava_forward/api/web/chat.js

## Phase Index

| Phase ID | Name                                                                               | Status   | Detail sections        |
|----------|------------------------------------------------------------------------------------|----------|------------------------|
| P01      | Fetch target ref, isolate Python environment, and rebase unmerged #215 stack       | Complete | P01, P01-T01, P01-T02  |
| P02      | Reconcile #215 test contracts, add stable alias modules, validate, and commit src/ | Complete | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Fetch target ref, isolate Python environment, and rebase unmerged #215 stack

### Context

Branch `test/demo-215-visit-schedule-consent-boundary-0600` (`d273b99d6`) diverged from `0578458d4` with 22 commits: 10 commits (`a3a9030be..680ca9a87`) already squash-merged as PR #1576 (`c42fceed7`) on `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`), followed by 12 unmerged `#215` commits (`799909e72..d273b99d6`). Meanwhile, shared user site-packages currently link `zava_forward` editable distributions to a deleted sibling worktree.

### Intent

Rebase only the unmerged `#215` commits (`799909e72..d273b99d6`) cleanly onto `d8cb35d25` with privacy-safe git committer identity, and set up workspace-local `.venv-215-0600` pointing to this worktree's `src/{core,agents,api}` packages ahead of `~/.local` user site-packages.

### Boundaries

* Included: `git fetch`, `git config --local user.email`, `git rebase --onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87`, resolving `chat_case_answers.py` in `83957d33e`, and creating `.venv-215-0600`.
* Excluded: Rewriting upstream commits on `d8cb35d25`, mutating shared `~/.local` editable installs, or pushing to `origin`.

### Likely Targets

* `src/core/src/zava_forward/core/chat_case_answers.py`: Conflict resolution during replay of `83957d33e`.
* `.venv-215-0600`: Workspace-local scratch virtualenv created after rebase completes and deleted at the end of `P02-T02`.

### Dependencies

* None.

### Validation Expectations

* `git merge-base HEAD origin/feat/demo-164-chat-grounding-provenance-0900` equals `08c36e4dc807a44e493b40cc080c5d865c22d93f` (immediate child of `d8cb35d25445b19b0533e30aec39842e992474a3`), so both `d8cb35d25` and `08c36e4dc` are ancestors of `HEAD`.
* `.venv-215-0600/bin/python -c "import fastapi, pydantic, httpx, zava_forward.api, zava_forward.core; print(zava_forward.core.__file__)"` prints paths inside `/home/azureuser/source/ama-demo-wt/test-215-visit-consent-0600/src/`.

### Completion Evidence

* Completed rebase history (`535515c18..0c016aa66`) on `test/demo-215-visit-schedule-consent-boundary-0600` atop `08c36e4dc` (`origin/feat/demo-164-chat-grounding-provenance-0900`) and verified editable + third-party imports in `.venv-215-0600`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure privacy-safe git identity, fetch target branch, and rebase 680ca9a87..d273b99d6 onto d8cb35d25

#### Context

Replaying `83957d33e` onto `d8cb35d25` encounters one conflict in `src/core/src/zava_forward/core/chat_case_answers.py` where PR #1641 replaced inline `_unblock` text with `RULES[CHAT_BOUNDARY]`, `RULES[SAFETY_SEQUENCE]`, and `RULES[VISIT_CONSENT]`.

#### Intent

Configure repository-local `{id}+{login}@users.noreply.github.com` via `gh api user`, fetch `origin/feat/demo-164-chat-grounding-provenance-0900`, inspect `d8cb35d25`'s verbatim `RULES[VISIT_CONSENT]` and `src/core/tests/test_chat_case_answers.py`, and run `git rebase --onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87`, extending `RULES[VISIT_CONSENT]` in `chat_case_answers.py` to preserve PR #1641's tested phrases (`"the resident's consent is recorded by the named officer using the case consent control"`) while adding `"resident consent and access"` confirmation (`"Before a non-emergency visit to a home, resident consent and access must be confirmed with the resident, and the resident's consent is recorded by the named officer using the case consent control. Chat cannot record or assume either."`), retaining `[VISIT_CONSENT]` citation and excluding `UnblockTests.BANNED` words.

#### Boundaries

* Included: Local git config, `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase --onto`, and `chat_case_answers.py` conflict resolution.
* Excluded: Modifying `CHAT_BOUNDARY` or `SAFETY_SEQUENCE` strings relied upon by `test_chat_panel.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/chat_case_answers.py`: `RULES[VISIT_CONSENT]` and `_unblock(r)`.

#### Dependencies

* None.

#### Validation Expectations

* Rebase finishes with zero remaining conflict markers (`git diff --check` clean) and `d8cb35d25` as merge-base.

#### Completion Evidence

* `git log --oneline d8cb35d25..HEAD` shows the 12 rebased commits cleanly atop `d8cb35d25`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Provision workspace-local scratch virtualenv with editable local distributions

#### Context

Shared `~/.local` site-packages point `zava_forward` at a removed sibling worktree; modifying `~/.local` could interfere with concurrent sessions in other worktrees, and Python `venv --system-site-packages` sets `ENABLE_USER_SITE = False` by default.

#### Intent

Create `.venv-215-0600` with `python3 -m venv --system-site-packages .venv-215-0600`, write a tail `zzz_user_site_fallback.pth` inside `.venv-215-0600/lib/python*/site-packages/` pointing to the user site-packages directory so third-party libraries remain importable behind editable installs, and run `.venv-215-0600/bin/pip install --no-build-isolation --no-deps -e src/core -e src/agents -e src/api` so `unittest` and `mypy` resolve `zava_forward.*` directly from this worktree.

#### Boundaries

* Included: Creating `.venv-215-0600`, adding tail user-site `.pth` fallback, and editable no-deps installation of `src/{core,agents,api}`.
* Excluded: Network package downloads, `/tmp` writes, or global/user site-package edits.

#### Likely Targets

* `.venv-215-0600`: Workspace-local scratch Python environment.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Importing `fastapi`, `pydantic`, `httpx`, `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api` succeeds and resolves `zava_forward.*` to `/home/azureuser/source/ama-demo-wt/test-215-visit-consent-0600/src/`.

#### Completion Evidence

* Verified import paths from `.venv-215-0600/bin/python`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Reconcile #215 test contracts, add stable alias modules, validate, and commit reconciled src/ edits

### Context

On `d8cb35d25`:
1. `RULES_FIRST = frozenset({"unblock", "claim", "pas2035", "sensor"})` causes unblock/visit questions (`"what can I do to unblock this case?"`, `"how can we fix this safety? Should we schedule a visit?"`) to execute rules-first (`answer_source == "decision-rules"`, `answer_origin == "decision_rule"`, `model == "workflow-only"`, 0 model calls) and return both `ZF-4/*` and `workflow/*` citations (`workflow/chat-boundary`, `workflow/safety-sequence`, `workflow/visit-consent`). Non-`RULES_FIRST` prompts (`"review what is blocking it"`, `"Please summarise this case"`) exercise `generative-grounded`, `decision-rules-fallback`, and `withheld`.
2. `SOURCE_LABELS` in `chat_panel.py` and `RULE_LABEL` / `MODEL_LABEL` / `WITHHELD_LABEL` in `chat.js` use standardized origin-prefixed labels, `regulatoryPlainMode` uses `<div class="regulatory-mode">` wrapping `<label for={id}>` + polite state span and passes `plain_language: plainMode.checked` in `employeeChat`, `<article class="regulatory-alert">` includes `"aria-labelledby"` and `regulatoryStateLabel(alert.result)`, and alert model copy says `"No AI model is used for any role."`.
3. Caller task 2 specifies `test_alert_chat_doubt_held_parity_215.py` and `test_alert_chat_owner_clock_safe_action_215.py`, whose implementations currently live in `test_epic215_doubt_route_held_state_wcag_parity.py` and `test_epic215_role_alert_owner_clock_safe_action_matrix.py`.

### Intent

Update the rebased `#215` tests to assert PR #1641's stronger contracts, create the two thin re-export alias modules, and pass all 8 named `#215` suites, sibling `#215`/`#164` suites, `ruff check src/api/tests`, and `mypy` inside `src/api`.

### Boundaries

* Included: Targeted test updates in `src/api/tests/`, adding `src/api/tests/test_alert_chat_doubt_held_parity_215.py` and `src/api/tests/test_alert_chat_owner_clock_safe_action_215.py`, and running `unittest`, `ruff`, and `mypy`.
* Excluded: Weakening consent/safety/provenance/WCAG assertions or changing `src/api/src/zava_forward/api/web/chat.js`.

### Likely Targets

* `src/api/tests/test_alert_chat_unblock_visit_grounding_215.py`: Align unblock/visit prompts with `RULES_FIRST` (`decision-rules`, `workflow/*` + `ZF-4/*` citations) and keep grounded/fallback coverage via non-`RULES_FIRST` `"review what is blocking it"`, plus updated `chat.js` `RULE_LABEL`/`MODEL_LABEL`/`WITHHELD_LABEL` strings.
* `src/api/tests/test_alert_chat_visit_consent_boundary_215.py`: Align `unblock`/visit-schedule assertions with `RULES_FIRST` (`decision-rules`, `workflow/visit-consent` citation, zero case mutation) and test generative consent-assumption withholding on a non-`RULES_FIRST` case prompt (e.g., `"What is the status of this case?"` or `"review what is blocking it"`).
* `src/api/tests/test_alert_chat_end_to_end_stabilization_215.py`: Align `chat.js` `plain_language` / `plain_summary` / `RULE_LABEL` / `MODEL_LABEL` / `WITHHELD_LABEL` strings and distinguish `RULES_FIRST` unblock (`decision-rules`) from generative grounded (`"review what is blocking it"` -> `generative-grounded`), fallback (`"review what is blocking it"` with unsupported claim -> `decision-rules-fallback`), and pure `withheld` (`"Please summarise this case"` with unsupported claim -> `withheld`).
* `src/api/tests/test_alert_chat_provenance_audit_contract_215.py`: Align `SOURCE_LABELS["generative-grounded"]` (`"Generative model suggestion..."`), allow `workflow/*` rule citations alongside `ZF-4/*`, and exercise `generative-grounded` + `decision-rules-fallback` on `"review what is blocking it"` while additionally verifying `RULES_FIRST` `decision-rules` on unblock/visit prompts.
* `src/api/tests/test_epic215_role_alert_owner_clock_safe_action_matrix.py`, `src/api/tests/test_alert_chat_escape_disclosure_semantics.py`, `src/api/tests/test_alert_chat_input_label_pii_notice_a11y.py`, `src/api/tests/test_alert_chat_provenance_badge_contrast_tokens.py`, `src/api/tests/test_alert_chat_citation_source_attribution_215.py`, `src/api/tests/test_alert_chat_plain_language_noncolour_215.py`: Align static `chat.js` substring checks with `d8cb35d25`.
* `src/api/tests/test_alert_chat_doubt_held_parity_215.py` and `src/api/tests/test_alert_chat_owner_clock_safe_action_215.py`: Thin re-export alias modules matching `src/api/tests/test_alert_chat_keyboard_provenance.py`.

### Dependencies

* P01.

### Validation Expectations

* All 8 caller-specified suites in `src/api/tests`, all sibling `#215`/`#164` suites (`test_chat_case_answers.py`, `test_chat_panel.py`, and the static web suites), `ruff check src/api/tests`, and `mypy` inside `src/api` exit `0`.

### Completion Evidence

* Recorded command outputs and exact test/lint/type counts in `.copilot-tracking/changes/2026-11-15/215-rebase-1641-0511-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Reconcile #215 API/provenance tests and static web tests with PR #1641 contracts and add module aliases

#### Context

Each updated test assertion maps 1-to-1 to a deliberate PR #1641 improvement on `d8cb35d25` (`RULES_FIRST`, `workflow/*` citations, `SOURCE_LABELS`, `regulatoryPlainMode`, `regulatoryStateLabel`, `"aria-labelledby"`).

#### Intent

Apply minimal, surgical updates to the affected `#215` test modules in `src/api/tests/` and create `test_alert_chat_doubt_held_parity_215.py` and `test_alert_chat_owner_clock_safe_action_215.py` as typed, `ruff`-clean re-export modules.

#### Boundaries

* Included: `src/api/tests/test_*215*.py` and the 4 unnumbered `#215` static web test modules (`escape_disclosure`, `input_label_pii_notice`, `provenance_badge_contrast`, plus `epic215_*`).
* Excluded: Production web assets (`chat.js`, `style.css`) and merged `#1576` tests unless needed (already green on `d8cb35d25`).

#### Likely Targets

* `src/api/tests/test_alert_chat_*.py` and `src/api/tests/test_epic215_*.py`.

#### Dependencies

* P01-T02.

#### Validation Expectations

* Zero test failures and zero `ruff`/`mypy` diagnostics across `src/api/tests`.

#### Completion Evidence

* Clean diff across reconciled test files and two added alias modules.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Execute the 8 named #215 suites, sibling suites, ruff check, and mypy, clean scratch venv, and commit validated src/ reconciliation

#### Context

Caller tasks 2 and 3 require running the 8 `#215` test suites in `src/api/tests`, `ruff check src/api/tests`, and `mypy` inside `src/api`; `PC-001` and `PC-003` require removing `.venv-215-0600` and committing validated `src/` reconciliation before `rpi-review`.

#### Intent

Run all 8 named suites, sibling `#215`/`#164` regression suites (`src/core/tests/test_chat_case_answers.py`, `src/api/tests/test_chat_panel.py`, and the remaining `#215` web tests), `ruff check src/api/tests src/core/src/zava_forward/core/chat_case_answers.py`, and `mypy` inside `src/api`, delete `.venv-215-0600`, commit validated `src/` changes locally with the Copilot trailer, and record exact commands, outputs, and committed implementation SHA in `.copilot-tracking/changes/2026-11-15/215-rebase-1641-0511-changes.md`.

#### Boundaries

* Included: Focused local validation commands, `.venv-215-0600` cleanup, local `src/` reconciliation commit with trailer, and changes-record creation.
* Excluded: Hosted CI triggers or `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/215-rebase-1641-0511-changes.md`: Implementation evidence record.

#### Dependencies

* P02-T01.

#### Validation Expectations

* Every validation command returns exit code `0`, `.venv-215-0600` is removed, and `git diff HEAD -- src` is empty before `rpi-review`.

#### Completion Evidence

* Populated `.copilot-tracking/changes/2026-11-15/215-rebase-1641-0511-changes.md`, committed `src/` SHA `f0556155a`, and synchronized `[x]` markers in plan and details ahead of the parent RPI Agent's Review and `.copilot-tracking/` freeze commit.

#### Unresolved Items

* None.
