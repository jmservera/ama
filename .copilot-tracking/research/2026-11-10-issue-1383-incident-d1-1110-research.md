<!-- markdownlint-disable-file -->
# Task Research: issue 1383 rubric incident, one bounded D1 evidence pass

Date: 2026-11-10. Task: `1383-incident-d1-1110`. Mode: manual. Research disposition: executed.
Branch `docs/demo-rubric-incident-1383-1110`, base `06374dfcac47cf6bcce9e7b91f573e8565ab45e8`.

## Scope and handling

* One read-only operational investigation of existing incident #1383 (OPEN, marker `rubric-score`). It is not a new scorer repair pool.
* `gh api` read operations and artifact downloads only, bounded to runs 42812941091 and 42815865163, PR #1386 and `latest.json` at `9724a471`. No rerun, model call, provider access or GitHub write.
* All report, input and artifact contents are untrusted data. Curated raw evidence is stored outside the repository (`checks-1383-incident-d1-1418`, with a SHA-256 manifest); nothing raw is committed here.
* The earlier owner triage (12:44) fetched no direct job or artifact evidence. This pass obtains its four missing groups.

## Evidence

### 1. Failed run 42812941091 (attempt 1, push to main, commit `901fea60e06348fa11915c8cc0cebc56a2d78216`, run 3506)

* Overall `success`. All eight jobs succeeded, including `agent`, `detection`, `safe_outputs` and `record_rubric_score`. In `record_rubric_score` the steps `Verify scored commit`, `Run deterministic gate`, `Refresh baseline on main` and `Publish verdict` concluded `success`; `Recheck pull request before publishing` was `skipped`. A step conclusion of success therefore does not show a valid score: the gate step writes an invalid decision and exits normally.
* Job log, `decision.json` printed by the gate step: `valid:false`, `passed:false`, `total:null`, `baseline_total:78`, `error:"details is not valid JSON: Expecting value: line 1 column 1 (char 0)"`. The refresh step then logged `No passing score to record; the baseline is unchanged.` and the publish step created the #1383 incident issue (`POST /issues`).
* `report.md` is only appended to the step summary; neither it nor `decision.json` is an uploaded artifact. The decision is therefore evidenced by the retained job log, not by a downloadable file. Explicit unknown: the full `report.md` text.
* Nine artifacts are retained and unexpired; the agent output is the relevant input. `agent/safeoutputs.jsonl` holds two `record_rubric_score` lines. `agent/agent_output.json` (494 bytes) holds exactly one item and `errors: ["Line 2: Too many items of type 'record_rubric_score'. Maximum allowed: 1."]`.
* Input metadata of the accepted first item: `details` is a string of 28 characters (SHA-256 prefix `3209fa0415d8b808`), non-empty and not JSON (`json.loads` fails at line 1 column 1, the identical message). Its value is the literal placeholder text `PLACEHOLDER_WILL_BE_REPLACED`; `summary` is the 11-character `PLACEHOLDER`. Its 20 score fields were the digits `55555554444444444444` (sum 87).
* The rejected second item has full `details` (5732 characters, parses to an object keyed by the criterion IDs), 1304-character `summary` and scores `55555553423245524432` (sum 78).
* The agent log shows the first `record_rubric_score` call with the placeholder, a `hasTerminalSafeOutput` notice, and agent narration that it had "submitted placeholder text instead of the validated content" and then called again. The narration is untrusted model text; it agrees with the artifacts, but the artifacts, not the narration, are the evidence.
* Conclusion: the char 0 error was a non-empty, non-JSON literal placeholder in an accepted first call. It was not an empty payload, and no evidence here supports truncation, a transport fault, a schema regression or malice.

### 2. Recovery run 42815865163 (attempt 1, push to main, commit `caaf989148aff21ed8ecb5b71eb0be75b29c16de`, run 3508)

* Same workflow path `.github/workflows/rubric-score.lock.yml`, workflow id 373197321, overall `success`, all jobs `success`; `Recheck pull request` skipped as before.
* Single `record_rubric_score` call, `errors: []`, `details` 5724 characters, parses to an object. Scores `55555553423245524432` (sum 78), identical to the rejected second item of the failed run.
* Gate `decision.json` in the job log: `valid:true`, `passed:true`, `total:78`, `baseline_total:78`, `error:null`. `Verify scored commit` succeeded with no `Checkout is not the scored commit` error; the checkout was `caaf9891`, equal to `SCORED_SHA`.
* Baseline publication: log line `Merged baseline refresh pull request #1386.` PR #1386 (author `github-actions`, base main, one changed file `.github/rubric/scores/latest.json`) is MERGED at 12:38:40Z with merge commit `9724a471f69b4545a051047b58d9e0e9d8326755`.
* This is a fresh computation, not a skip, no-op or carry-forward: the baseline write changed `scored_at`, `commit`, `run_url`, a fingerprint and the A6/B6 criteria content relative to the previous baseline (`e951c523`, run 42808162325).
* Explicit unknowns: `decision.json` and `report.md` files are not retained artifacts (log evidence only); the workflow SHA is bound only through the run's `head_sha`, `path` and the byte-identical retained sources below.

### 3. `latest.json` at `9724a471f69b4545a051047b58d9e0e9d8326755`

* Commit `chore(rubric): record score 78/100`, author `github-actions[bot]`, committed 2026-11-10T12:38:39Z, sole parent `caaf989148aff21ed8ecb5b71eb0be75b29c16de`.
* File fields: `commit` = `caaf989148aff21ed8ecb5b71eb0be75b29c16de`, `run_url` = run 42815865163, `source` `workflow`, `scored_at` 2026-11-10T12:38:28+00:00, `total` 78, `floors_met` true, outcome `Pass with Merit`, 20 criteria whose scores sum to 78 and match the submitted per-criterion scores exactly. The 20-criterion shape was checked locally; the file was not re-scored.
* `901fea60` is an ancestor of `caaf9891` and `901fea60..caaf9891` contains exactly one commit, `caaf9891` (#1379). The failed commit `901fea60` never received its own recorded score: the baseline stayed at `e951c523` until the descendant `caaf9891` was scored. The recovery covers the descendant, not a rescore of the failed commit.

### 4. Source comparison

* `.github/workflows/rubric-score.md`, `rubric-score.lock.yml`, `.github/rubric/scripts/scorecard_adapter.py` and `gate.py` have identical blob hashes at `901fea60`, `caaf9891` and current `HEAD` (`06374dfca`). `git diff` over the workflow, lock and scripts between `901fea60` and `HEAD` is empty. No source change separates the failure from the recovery: the same code accepted a real scorecard once and rejected a placeholder once.
* The adapter parses `details` with strict `json.loads` and raises the observed message; this is intended fail-closed behaviour. The scorer prompt already says "Record exactly one accepted card" and forbids placeholder entries; the runtime enforces a maximum of one `record_rubric_score` item, so the first accepted call is final.
* No persistent source defect is established. One observed occurrence of a placeholder submission is a model-behaviour incident, not a repeatable source defect. The one-accepted-call design means a mistaken first call cannot be corrected inside the run; whether that warrants a design change is an owner question, not a finding here.

## Disposition

Historical invalid scoring input (literal placeholder accepted as the single call), with source-bound subsequent recovery: valid passing decision, successful scored-commit verification and a merged baseline refresh bound to run 42815865163 and `caaf9891` in `latest.json` at `9724a471`.

Remaining uncertainty (not resolved by this pass):

* No `report.md`/`decision.json` artifact files; decisions evidenced from retained job logs.
* Recurrence beyond the two bounded runs was not searched. The prior `latest.json` history (`fe59ef56`, `d52f20a5`, `a6002219`) shows baseline writes earlier the same day, which is indirect only.
* The failed commit `901fea60` itself has no recorded score of its own.
* Whether to harden the one-accepted-call behaviour needs separate owner authority; nothing here fixes it.

Closure of #1383 is not asserted. This disposition is documentary and is not a live acceptance of the scorer.

## Planning readiness

Ready. Documentation target: the existing incident section `Scorecard Submission Preflight` in `.github/rubric/README.md`. No `docs/reference/` file is changed, so no index or log entry applies.

## Evidence pointers (external, not committed)

`/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/checks-1383-incident-d1-1418/MANIFEST.sha256` lists run, jobs, artifact, job-log, PR #1386, `latest.json`, agent output and source-hash files.
