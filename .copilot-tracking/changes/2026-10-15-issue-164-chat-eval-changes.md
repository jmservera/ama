---
title: Issue 164 chat evaluation changes
description: Changes, commands and results for the chat evaluation slice
ms.date: 2026-10-15
---

## Changes

### PR 307 review-fix continuation (P05-T01 to P05-T03)

The owner requested fixes before acceptance, on the existing branch only.
P05-T01 to P05-T03 are complete; source fix `2f6f73a` was committed and pushed
normally to the existing branch. The earlier results below are historical, not evidence for the review
fixes. No new critique or approval is claimed. Synthetic data only; ADR 0006 and
disabled enablement remain unchanged.

### Refusal, model output and history (P05-T01)

* `src/core/src/zava_forward/core/chat_panel.py` now NFKC-normalizes, removes
  Unicode format characters, folds common Greek/Cyrillic Latin confusables and
  collapses whitespace before lexical matching. Removed the clause-start
  restriction; added mark-X-as-consented and named contact targets.
* All assistant turns are excluded from model input, not just turns whose
  citation ids or role permissions changed. Current projected sources and
  untrusted user questions remain. Stored assistant messages are unchanged.
* Approval/consent action assertions in parsed model answers are lexically
  withheld with no citations. Tests include prose, confusables and zero-width
  text. This closes the seeded prose-action scenario, not semantic injection
  resistance: lexical checks are still paraphrase-bypassable; the model's own
  refusal behaviour is unmeasured.
* Core tests, API tests and the golden file cover the requested phrasings,
  no provider call for refusals, unchanged case records and preserved user
  follow-ups without assistant history. No database or dependency changes.

### Critical known gaps block acceptance (P05-T02)

* `chat_eval.py` now treats grounding as critical as well as refusal, injection,
  poisoning and permissions. Known gaps are not passes in any category or
  aggregate; their failed assertions contribute to failure/critical totals.
* `summary.open_critical_gaps` separately lists id, category and description;
  `enablement.blocking_gaps` carries those blockers even with approved
  thresholds. CLI output names them and exits 1. An otherwise successful,
  gap-free development report still has enablement `insufficient`, disabled.
* Golden version and registry now `chat-golden-2026-10-15-pr307`: 24 scenarios,
  61 turns, 23 passing scenarios, one critical known gap with two failed
  assertions (`kind`, `forbid`). Stale assistant history and lexical
  injection-obeyed approval/consent scenarios now genuinely pass and their gap
  markers were removed. Unsupported funding claims with a valid stage citation
  remain a blocker, not a fake pass or a claimed grounding verifier.
* Actual JSON CLI subprocess verified exit 1, `passed: false`, enablement
  `fail`, state `disabled`, and the named unsupported-claim blocker.
  Non-AI comparator: case card could answer 18/18 expected answer turns,
  scripted AI answered 18, workflow-only panel answered 0. No benefit claim.
* Policy version binds normalization mapping/steps, action regex and history
  policy as well as the existing refusal/tool patterns; golden hash changes too.

### Validation and reconciliation (P05-T03)

Existing `/tmp/zf164` environment, editable imports verified against this
worktree. No uv used. From each `src/<project>`:

| Project | unittest discover command suffix | Result | ruff check / format --check / mypy |
| --- | --- | --- | --- |
| core | `PYTHONPATH=tests python -m unittest discover -s tests -q` | 261 OK | All pass; mypy 62 files |
| agents | `PYTHONPATH=../core/tests python -m unittest discover -s tests -q` | 70 OK | All pass; mypy 16 files |
| api | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | 459 OK, 92 skipped | All pass; mypy 33 files |
| orchestrator | `PYTHONPATH=../core/tests python -m unittest discover -s tests -q` | 17 OK | All pass; mypy 8 files |
| importer | `python -m unittest discover -s tests -q` | 39 OK | All pass; mypy 10 files |

* All five suites include their ADR 0006 dependency-rule checks.
* Initial orchestrator/importer discovery failed because their distributions
  were not installed. Restored with
  `/tmp/zf164/bin/python -m pip install --quiet -e src/orchestrator -e src/importer`,
  verified local import paths, then reran both complete suites and tools.
* API skips are existing SQL integration/environment boundaries, not new
  acceptance evidence. Core emitted existing sensor-backfill unclosed-file
  ResourceWarnings; its suite passed. No live model, SQL Server, Docker image
  or human exercise was run for these fixes.
* Updated agents README, reference index/log and existing plan/details/state.
  Corrected the historical log's stale-history claim to describe its initial
  partial filtering, and appended current limitations/results without changing
  unrelated earlier entries. Existing critique and single Review stay historical;
  review artifact now records the fixes and remaining critical blocker.
* `git diff --check` passed. Source fix commit
  `2f6f73a190e82909dc1013af726fef9e990c0ebd` was pushed normally to
  `origin/feat/src-chat-eval-164` (`2fb276d..2f6f73a`). This delivery-record
  reconciliation follows as a documentation commit on the same branch.
* Authenticated account resolved with `gh api user`; repository-local
  privacy-safe noreply email used for author and committer, with the requested
  Copilot trailer. No force push, main push, merge, live inference or enablement.

* Added `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/evals/chat_golden.json`, `src/agents/tests/test_chat_eval.py`; registry entry `chat-golden`.
* Modified core `chat_panel.py` (refusal, history carry filter), core and api `test_chat_panel.py`, `web/chat.js`, agents README, reference index and log.
* No `mvp/` change; no SQL added; no enablement.
* Divergence: an existing api test asked "Approve the case and email the resident now." to test withheld output; that now correctly refuses first, so it asks a neutral question.

## Commands and results (venv /tmp/zf164, pip install -e src/core src/agents[dev] src/api)

* agents `PYTHONPATH=../core/tests python -m unittest discover -s tests -q`: 62 OK (baseline 47).
* core `PYTHONPATH=tests python -m unittest discover -s tests`: 258 OK.
* api `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q`: 458 run, 92 skipped, OK after the test fix (one failure first, the divergence above).
* ruff check, ruff format --check and mypy on agents, core and api: clean.
* `python -m zava_forward.agents.chat_eval`: 21 scenarios, 42 turns, 0 unexpected failures, 3 known gaps recorded; card answers 18 of 18 answer turns, AI 18, workflow-only 0; enablement insufficient, task disabled.
* Local app: `build_mvp_dataset.py --seed 20260901` (980 cases) then `python -m zava_forward.api.server`: `/` 200, `chat.js` serves the refusal handling, unauthenticated chat POST 401.
* `docker ps`: permission denied; image and mssql evidence rely on CI.

## Owner decisions and open criteria (unticked)

* [ ] Pass thresholds for grounding, refusal, injection and poisoning.
* [ ] Accountable reviewer and the enabled or disabled state of the chat task.
* [ ] Independently labelled held-out set.
* [ ] Live model run (payload, provider handling, budget).
* [ ] Human exercises (consent, accessibility, privacy) and review-effort comparison.
* [x] Exclude stale assistant answers from model history.
* [x] Withhold the seeded plain-prose approval/consent action claims (lexical only).
* [ ] Close the critical unsupported-claim-with-valid-citation gap; establish
  semantic grounding/injection resistance and measure actual-model refusal.

## PR 663 review and CI follow-up (2026-11-01)

* `assistants.py` `registry()` and `continuity.py` `candidate()` now list the
  disabled chat task with `binding` null, `release` null and the missing
  evidence reason instead of raising `KeyError`; disabled tasks do not make the
  serving candidate incomplete. Zero-call denial for enabled tasks is unchanged.
* Regressions: `test_assistant_release` (registry lists chat) and
  `test_continuity` (all-task candidate and suspension with chat registered).
