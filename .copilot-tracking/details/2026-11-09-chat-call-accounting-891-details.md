---
title: Issue 891 chat call accounting details
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109
---

## Step 1 regression first (red)

* File `src/agents/tests/test_chat_model.py`. Add a helper that builds a real `Ai` (endpoint `https://synthetic.invalid`, `_token` and `urllib.request.urlopen` patched, a counting urlopen) and a minimal ledger stub with `reserve`, `dispatch_check` and `complete`, each optionally raising `DispatchHeld`.
* Test A pre-dispatch: meter absent, and `reserve` held. Assert counted transport 0, `ModelUnavailable.calls == 0`, outcome `provider-unavailable`.
* Test B post-dispatch: transport returns, `complete` raises `DispatchHeld("meter-capacity-reached")`; and transport raises then `complete` raises. Assert transport 1 and `calls == 1`; the envelope carries `meter_id`.
* Test C conservative: `dispatch_check` hold with reservation keeps 1 (documented limitation) so that a later core marker has to change this deliberately.
* Test D panel: real `ChatPanel` with the synthetic store pattern of `test_callback_exception_receipts_match_provider_and_audit`; for the meter-missing and the post-dispatch cases assert `answer["consumption"]["model_calls"]` equals the counted transport, kind `fallback`, no private text, and the `chat.turn` audit detail equals the receipt.
* Test E (added 22:37Z after critique) `input-refused` envelope: transport 0, `calls == 0`.
* Run: `cd src/agents; PYTHONPATH=tests:../core/tests <venv>/bin/python -m unittest test_chat_model -v`. Expected red: tests A and the A part of D fail with `1 != 0`; B, C pass. Preserve the raw output in `/home/azureuser/source/ama-demo-wt/logs-891-fresh-accounting-1109/`.

## Step 2 correction

* File `src/agents/src/zava_forward/agents/chat.py`. Replace `calls = 0 if envelope.get("outcome") == "disabled" else 1` with a small private function `provider_calls(envelope)` returning 0 for `disabled` and for `financial-held` without `meter_id`, else 1, with a one-line comment that a reservation exists only before the transport and a later ledger hold can follow a real call.
* Re-run Step 1 command: expect green.

## Step 3 documentation

* `src/agents/README.md` consumption provenance section: three or four plain sentences (rule, why not blanket zero, the F3/F4 limitation, core marker follow-up). ASCII, `*` lists, no em dashes.

## Step 4 validation (commands, run from `src/agents` unless noted, venv `/home/azureuser/source/ama-demo-wt/venv-891-1109`)

* `PYTHONPATH=tests:../core/tests python -m unittest test_chat_model test_dispatch test_worker -q`
* `PYTHONPATH=../core/tests python -m unittest discover -s tests -p 'test_chat_*.py' -q`
* Agents full: `PYTHONPATH="$PWD/tests:$PWD/../core/tests" python -m unittest discover -s tests -q` (README line 212).
* Core impacted (corrected 22:37Z): from `src/core`, `PYTHONPATH=tests python -m unittest discover -s tests -p 'test_chat_panel.py' -q` and `-p 'test_ai_consumption*.py'`.
* API impacted (corrected 22:37Z): `pip install -e src/api` only after an observed missing-dependency failure; from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_chat_panel.py' -q`, `-p 'test_continuity.py'`, `-p 'test_ai_call_site_inventory.py'`, and `test_ai_consumption_api` if its owned loopback stub runs. Any exclusion, skip or failure is reported with raw output.
* `ruff check .`, `ruff format --check .`, `mypy` in `src/agents`.
* Scope proof: `git diff --name-only a04668ae9..HEAD`.

## Step 5 records and commit

* Changes record, state update, review (one only), handoff. Commit tracking separately from source so process order is visible; author and committer from `git config --local` noreply, trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`. No push.
