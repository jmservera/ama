<!-- markdownlint-disable-file -->
# Details: AI and employee chat current-main stabilization checkpoint (#440)

Plan: `.copilot-tracking/plans/2026-11-08-ai-main-stabilization-440-plan.md`

## Phase 1: focused local reproduction (prospective)

* Scratch: `/tmp/ai-main-440-1108` (19 GB free on `/`); `git archive HEAD src` already exported; venv `/tmp/ai-main-440-1108/venv`; `pip install` of `src/core`, `src/agents`, `src/api` (non-editable); `pip check`.
* Environment: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR`, `HOME` and `ZF_DATA` under the scratch directory; no `.env`, no provider variables, `ZF_CHAT_DEMO_ACTIVATION` unset. Per-command `timeout 600`, sequential, `nice`.
* Selectors (existing tests only):
  * core: `test_chat_panel.py`, `test_chat_privacy.py`, `test_chatthreads.py`, `test_chat_memory.py`, `test_chat_case_answers.py`
  * agents (`PYTHONPATH=../core/tests`, `ZF_CHAT_GOLDEN=<scratch>/src/agents/evals/chat_golden.json`): `test_chat_model.py`, `test_chat_eval.py`
  * api (`PYTHONPATH=../core/tests:../agents/tests`): `test_chat_panel.py`, `test_chat_isolation.py`, `test_ai_boundary.py`, `test_ai_call_site_inventory.py`, `test_assistants.py`
* Import identity: confirm modules resolve under the venv `site-packages`, not the checkout.
* F1 reproduction against the pinned checkout (the archive holds only `src`): `grep -rn "\bturn(" src tools --include=*.py` and the `chat_isolation.py` source lines.
* Not run: MSSQL (needs Docker), Chromium and axe, real provider, Azure, FULL gate.

## Phase 2: pack section

Heading: `## AI and employee chat current-main stabilization checkpoint (2026-11-08, Refs #440 #157 #159 #104 #107)`. Subsections: source and document identities; status-drift correction; retained historical evidence; where AI is invoked and the authority ceiling; actual local commands; traceability table; existing owners and findings; not run and exclusions; classification, recommendation and gates.

## Phase 3: index and log

Append one `docs/reference/log.md` entry. Check `docs/reference/README.md` for the established pack link pattern before any edit.

## Phase 4 and 5

`git diff --check`, relative-link and heading review, `git diff --stat` limited to docs and tracking; changes record; author Review; repository-local noreply email from `gh api user`; Conventional Commit `docs(arch): ...` with Copilot trailer.
