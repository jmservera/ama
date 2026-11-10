<!-- markdownlint-disable-file -->
# Research: issue 1397 documentary qualification

Date: 2026-11-10. Task `issue-1397-documentary-qualification-1110`, child of `issue-1397-rubric-incident-1110`. Research disposition: executed. Planning Readiness: Ready.

## Scope and limits

One bounded documentary correction after independent Readiness (approve_with_comments, one Medium finding at line 66 of the original research record, commit `ac4177b5`). It is not source repair, not a fresh source grant and not a reset of the original cycle. No scorer, workflow, prompt, adapter, test or config edit, no rerun, no model or provider call, no score or grade reconstruction, no gate relaxation, no choosing a last valid payload. The original `ac4177b5` records and handoff are preserved unchanged.

## Finding under correction

The original research record states: "Because only the first schema-valid call is the accepted one and contents are validated downstream, a placeholder first call cannot be corrected afterwards." This asserts a general acceptance rule. It conflicts with the preceding paragraph, which leaves the quota contradiction unresolved, and with the README Scorer execution section, which says multiple schema-valid items can append and that the gate rejects multiple items. The Readiness review is correct.

Two nearby statements carry the same overreach in weaker form: original research line 79 ("placeholder first call accepted as the single call") and README line 269 ("a placeholder first call that became the only judged call"). The record elsewhere calls the judged item a deduction, so these are shorthand for the deduction and need the same qualification.

## Permitted evidence re-read

* The permitted index archive was listed with the standard library only. Only the root `safeoutputs.jsonl` was extracted, to `ROOT/incident1397-agent-safeoutputs-1958/`. No agent execution, internal reasoning, sandbox, provider or other archive member was opened.
* SHA-256 of the extracted file equals that of `incident1397-fallback-1911/safeoutputs.jsonl`: `2b82d5c63abf1fd15b209b9baec64781fb65da6d4932a53201e52a391b421e48`. It is the same two submitted inputs already analysed. It adds no new fact about acceptance, refusal or the consumed item.
* Successor artifact metadata (`incident1397-successor-artifacts-1936.json`) lists `agent` 13777211143, `agent-output-fallback` 13777176269 and `safe-outputs-items` 13776916975 (386 bytes) for run 42841391974, none expired. Only identifiers and sizes were read; no successor payload or log was read. Fresh versus carried scoring of the successor stays UNKNOWN.

## Corrected statement of what is established for this incident only

* Two submitted tool inputs exist, in file order: a placeholder with empty `details`, then a complete 20-key card.
* The gate error is a key-set rejection that only the placeholder can raise, so the placeholder is deduced to have been the sole judged item.
* No successful correction is evidenced.
* Whether the second call was refused at submission or appended and dropped, and the runtime acceptance policy responsible, are UNKNOWN. No general first-call-acceptance or quota rule is claimed.
* Recovery of `6cc59776` and fresh-versus-carried scoring of the successor stay UNKNOWN.

## Follow-ups

1. Owner decision on retaining the accepted-item list and gate `decision.json` as run artifacts (smallest action that would settle the acceptance question next time).
2. Reconcile the prompt's one-call quota statement with the observed behaviour.
3. Read-only recurrence search.

No further proof is available from permitted evidence; UNKNOWN items are retained.
