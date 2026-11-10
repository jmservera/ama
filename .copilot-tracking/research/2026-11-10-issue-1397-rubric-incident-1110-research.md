<!-- markdownlint-disable-file -->
# Research: issue 1397 criterion-set rejection at run 42838857558

Date: 2026-11-10. Task `issue-1397-rubric-incident-1110`. Research disposition: executed. Planning Readiness: Ready.

## Scope and limits

Initial bounded documentary diagnosis of the new incident #1397 only. It is not a source-feature or correction grant for the scoring lineage. No scorer, workflow, prompt, adapter, test or config edit, no score repair, no model or provider call, no workflow rerun and no weakened validation. #1383 diagnosed a different placeholder incident; its failure, recovery and process qualifications stay as recorded. No agent execution log, sandbox or provider trace was read.

Permitted evidence read (all supplied by Root, plus read-only repository and `gh` metadata):

* `incident1397-run-1910.json`, `incident1397-artifacts-1910.json`, `incident1397-record-job-1911.log`.
* `incident1397-fallback-1911/safeoutputs.jsonl` (submitted tool inputs only; the other files in that folder were not read).
* `incident1397-context-1911/context.json` (trusted context, baseline and template).
* Repository sources at `6cc59776`, `901fea60` (the #1383 failing commit) and `eff05737`, and `backlog-ready-refinement-1903.md` as a proposal, not evidence.

## Run identity

* Run 42838857558, attempt 1, event `push`, head `6cc59776666620309fb6b67ad2fdafb343d40998` (main), conclusion `success`. All eight jobs concluded `success`: `pre_activation`, `activation`, `rubric_prepare`, `agent`, `detection`, `record_rubric_score` (job 129913684497), `safe_outputs`, `conclusion`.
* #1397 ("Rubric scoring failed on main") was created by `github-actions` at 2026-11-10T15:03:33Z, still `OPEN` with no comments when read. Its body is `FAILED`, "details must contain exactly the 20 rubric criterion IDs", that run URL and the commit.
* Artifacts present, none expired: `safe-outputs-items` (386 bytes), `agent-output-fallback` (6495), `detection`, `usage`, `aic-usage-scan-v2`, `agent`, `activation`, `rubric-context`, `info`. No `decision.json` or `report.md` artifact exists.

## Record job behaviour (log)

* Downloaded artifacts `agent` and `agent-output-fallback` with `merge-multiple: true` into one directory; `GH_AW_AGENT_OUTPUT` is `.../safe-jobs/agent_output.json`. Which artifact supplied that file is not shown.
* `Verify scored commit`: `HEAD_STATE: eligible`, checkout equals `6cc59776`.
* `Load trusted rubric tools`: with `BASE_REF: HEAD` (push event) the tools are copied from the checked-out scored commit itself, not from an earlier base.
* `Run deterministic gate` (`--model claude-sonnet-5`, no `--force`) printed `valid: false`, `passed: false`, `bootstrap: false`, `calibration: false`, `total: null`, `baseline_total: 78`, `outcome: null`, `error: "details must contain exactly the 20 rubric criterion IDs"`.
* `Refresh baseline on main`: notice "No passing score to record; the baseline is unchanged." No refresh branch or pull request was created.
* The enclosing job and workflow concluded `success` because the gate step reports a rejection as data and exits normally; the verdict step then reports the failure.

## Consumed identities (git blobs, identical at `901fea60`, `6cc59776` and `eff05737`)

| Path | Blob |
| --- | --- |
| `.github/rubric/rubric.json` (registry, 20 IDs A1-A7, B1-B7, C1-C3, D1-D3) | `059efb2efa0a3bcc7de18002c54af49e04a8f02d` |
| `.github/rubric/scripts/gate.py` | `5ca9ad44e9d45accc32ea5aa0508472512124f62` |
| `.github/rubric/scripts/scorecard_adapter.py` | `7d496f30abfbdd59c50b6aa604256b1395cc40e7` |
| `.github/rubric/scripts/prepare.py` | `53641ee8057b2e192713a04ed5a0d1a7fb6a1718` |
| `.github/workflows/rubric-score.md` | `af87853f182d13d50c72cb0b76949ac0a5875053` |
| `.github/workflows/rubric-score.lock.yml` | `1667c08e4fbc423aa3c59b11d709d9a983c4f72e` |

Baseline consumed: `.github/rubric/scores/latest.json` at `6cc59776` (blob `3bb822e09a532a1612891c6771cffd3326b260d8`) records scored commit `111847191d1fde5e8ea18c30c999e99f33721aff`, run 42830696796, total 78. Trusted `context.json`: event `push`, baseline source `workflow`, total 78, not bootstrap, not calibration, instrument unchanged, diff base `111847191d1f`, 686 changed files, changed artifact `solution-code`, open criteria A1, A3, A4, A5, A6, A7, B6, live criteria B1-B5 and C2, no unmet requirements.

## Submitted tool inputs (file order of `safeoutputs.jsonl`, two lines, no timestamps)

Both calls are `record_rubric_score` with all 20 `<ID>_score` strings, `details` and `summary`; the key set of each call is the complete 22 input keys.

| Call | `details` | `summary` | Detail key set versus the 20 registry IDs |
| --- | --- | --- | --- |
| 1 | `{}` (2 characters) | `placeholder - will be replaced` | zero keys: all 20 missing, none extra |
| 2 | JSON object, 6340 characters | non-placeholder evidence summary | exactly the 20 registry IDs, each entry has exactly `evidence`, `rationale`, `change_reason` |

Call 1's score strings differ from the trusted `tool_inputs_template` for nine criteria (B1, B3, B4, B5, B7, C1, C2, D2, D3), so it is not a verbatim template copy. Call 2's 20 score strings equal the template (the baseline). No grade was reconstructed, and call 2 was not run through the gate here; only its key sets were compared.

## Which call the gate judged

The adapter message is raised only by `set(details) != set(criterion_ids)`. The gate's own count check ("expected exactly one record_rubric_score call, found N") did not fire, so exactly one item reached the adapter. Call 2 has exactly the registry key set, so it cannot raise this message; call 1 does (missing all 20 IDs). Conclusion by deduction: the item judged was call 1, the placeholder. The consumed `agent_output.json` bytes were not read, so this is a deduction from the job log, the code at the consumed identities and the submitted inputs, not direct observation.

Not shown by the permitted evidence: whether call 2 was rejected at submission (as #1383's retained output showed with `Maximum allowed: 1`) or appended and dropped before the gate; how the 386-byte `safe-outputs-items` artifact relates to the two submitted inputs.

## Source versus the observed behaviour

* `scorecard_adapter.from_inputs` parses `details` with duplicate-key rejection and requires `set(details) == set(criterion_ids)`; `{}` is a valid JSON object, so it passes the JSON and object checks and fails the key-set rule. This differs from #1383, where the literal text failed JSON parsing. Existing adapter tests cover missing-ID and extra-ID mutations; the all-missing `{}` case is the same set inequality and is not a separate test.
* `rubric-score.md` (identical blob at `901fea60`) says the pinned custom-job handler validates required parameters, string type and choices before append, does not validate `details` contents, and "does not enforce a one-call quota", while also telling the agent not to submit a second card after a call succeeds. The README's #1383 record reports the second call there was rejected with `Maximum allowed: 1`. These statements are not reconciled by the evidence here; flag, do not resolve.
* Because only the first schema-valid call is the accepted one and contents are validated downstream, a placeholder first call cannot be corrected afterwards.

## Publication and recovery (read-only GitHub metadata and git)

* This run's baseline publication: none. The baseline was unchanged and `6cc59776` never received a score of its own.
* Later push run 42841391974 (attempt 1, head `eff05737e8eaed584f3c269754d45bc5e44d0168`, conclusion `success`; all eight jobs `success`) is followed by merged baseline refresh pull request #1398 (merged 2026-11-10T15:16:43Z, squash `c66370042eb08f07839d054433f4483078703cf2`, trailer "Scored commit: eff05737..."). `latest.json` at `c66370042` records commit `eff05737`, that run URL, total 78, 20 criteria, scored at 2026-11-10T15:16:29Z.
* The refresh step only commits when the gate decision is `valid` and `passed` and `latest.json` exists, so the merged refresh implies a valid passing gate decision for `eff05737`; the job log and decision were not read.
* The diff of `latest.json` against its previous version changes only `scored_at`, `commit`, `run_url` and the `solution-code` fingerprint. The criteria content is identical to the earlier baseline, so it does not show whether the solution-code changes of `6cc59776` were assessed freshly or carried forward.
* Classification: successor baseline publication observed for a descendant under byte-identical tools; recovery of `6cc59776` itself and fresh-versus-carried scoring are UNKNOWN. #1397 remains open; closure is an owner decision.

## Classification

* Causal failure: a model-produced first `record_rubric_score` call carrying a placeholder summary and empty `details` object became the sole item the gate judged; the trusted adapter correctly rejected it. Fail-closed rejection of invalid input is the intended behaviour.
* Recurrence of the #1383 class (placeholder first call accepted as the single call), same day, with a different payload and adapter branch. It is not a new adapter defect: gate, adapter, registry, workflow source and lock are byte-identical to the #1383 failing commit. It does not show that the #1383 documentation fixed the producer; that change was documentation only and the prompt blob is unchanged.
* Not established: why the placeholder was submitted, whether the second call was rejected or dropped, and recurrence beyond #1383 and #1397.

## Smallest future engineering action (owner question, not authorized here)

Two evidence gaps made this diagnosis rely on deduction: the consumed accepted-item list and the gate `decision.json` are not retained as artifacts. The smallest candidate is a separately authorized change to retain those two files from the record job. Whether to additionally refuse placeholder-only `details` before append, or reconcile the prompt statement on the call quota, is a design question for the owner. No waiver, grade repair or validation relaxation is proposed.

## Follow-ups (ranked)

1. Owner decision whether to authorize the minimal artifact-retention change (ease high, value high for the next incident).
2. Reconcile the prompt statement about the one-call quota with the observed `Maximum allowed: 1` behaviour.
3. Read-only recurrence search across rubric-score incident issues.
