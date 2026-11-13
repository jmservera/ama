<!-- markdownlint-disable-file -->
# Details: issue #108 offline evaluation coverage record

## Design

* `observe(store, observed)`: wraps `store.ai.run` and `store.ai.look_at`. For each call it appends `dict(task=<returned task>, via="run"|"look_at", source=<returned source>, model_called=<scripted _chat reached>)`. `_chat` is wrapped per call, so the harness's own later `_chat` overrides still count.
* `task_coverage(observed)`: for each id of `ai_registry.tasks()` (registry-derived, cannot drift):
  * retained path (`kind == "retained-path"`): `exercised offline` when at least one observation has `model_called` and `source == "ai"`; `template fallback only` when observed but never; else `not evaluated by this harness`.
  * every other kind (assistant, chat, proposal-pack): `not evaluated by this harness`, fixed by kind. The assistants dispatch through the core planner, not `Ai.run` or `Ai.look_at`.
  * `namespace_errors`: observed task ids that are not retained ids (assistant ids, `legacy:` prefixed ids, unknown names). Any error fails the run.
* `evidence_gate(raw, summary, scripted=True, observed=None, namespace_errors=())` adds `task_coverage` with the per-task statuses, a count summary and a note: offline dispatch and control checks only, never held-out semantic accuracy or provider behaviour.
* `run_task_checks(workdir, observed=None)` and `run_scenario(sc, workdir, observed=None)` pass the list through `_scripted`. Funding draft checks: cited answer verified and Unverified controls, uncited Unverified, workflow-only returns the template without calling the model, comparison record, status becomes Draft ready, review controls. Read document checks with a constructed public text fixture: cited `Document:` label, comparison record, workflow-only no model call, non-text type stored but not read (template, no model call).
* A failing funding or document check, or a task that is only `template fallback only`, fails the run.

## Amendments from the critique ([critique](../reviews/plans/2026-11-13-108-offline-coverage-0008-plan-critique.md))

* Observations are of two kinds: `dispatch` (spy; `model_called`) and `final` (recorded by the harness from the returned view: `source`, `mode`, status, financial attribution). A retained task is `exercised offline` only with a model-called dispatch AND an eligible final (source ai, mode ai, not Quarantined or Hold, no financial attribution). Anything observed otherwise is `template fallback only`.
* `run_eval` fails when any retained id is not `exercised offline` (missing or fallback-only), or when a namespace error exists.
* Funding and document checks use isolated stores (`run_funding_checks`, `run_document_checks`), called from `run_task_checks`, which keeps the 11-result and 14-run denominators. Baselines: ranking and all case state except the intended `funding` or `documents` fields.
* `observe` is installed regardless of `_scripted`, wraps the current `_chat` per call with `try/finally`, and passes `run`/`look_at` arguments unchanged.
* The briefing check uses a distinctive cited answer and asserts final AI source, text, citations and record.

## Tests (failing first)

* Registry-derived exact coverage: keys equal `ai_registry.tasks()`; six retained exercised; assistants, chat, pack not evaluated.
* Template-only is not coverage: `Ai.look_at` patched to return the template gives `template fallback only` and a failed run.
* Namespace: a spy observation named like an assistant or `legacy:` id is a namespace error and fails the run.
* Discriminating funding and document checks: disabling `ai_tasks.workflow_only` or the citation resolver makes the named funding or document failure appear.
