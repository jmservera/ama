<!-- markdownlint-disable-file -->
# Details: issue 1383 incident disposition documentation

Plan: [plan](../plans/2026-11-10-issue-1383-incident-d1-1110-plan.md).

## Phase 1 details

* File: `.github/rubric/README.md`. Insert after the paragraph ending "...remain separate from this submission repair." and before `## Files`.
* Heading level `###`, matching `### PR #423 invalid D1 details (2026-10-30, Refs #360)`.
* Content, plain ASCII, `*` lists, no em dashes, no bolded prefixes:
  * Failure: run 42812941091 (attempt 1, push to main, commit `901fea60e06348fa11915c8cc0cebc56a2d78216`) concluded `success`, but its gate decision was `valid:false`, `total:null`, baseline 78, error `details is not valid JSON: Expecting value: line 1 column 1 (char 0)`. The agent's first `record_rubric_score` call, the only one accepted, carried the literal `PLACEHOLDER_WILL_BE_REPLACED` (28 characters, non-empty) as `details` and `PLACEHOLDER` as summary; its second, complete call was rejected (`Maximum allowed: 1`). Gate, refresh and publish steps ran as designed: no baseline change and incident #1383.
  * Not established: empty payload, truncation, transport or schema fault, adapter defect. Strict JSON rejection is intended.
  * Recovery: run 42815865163 (commit `caaf989148aff21ed8ecb5b71eb0be75b29c16de`) made one call, decision `valid:true`, `passed:true`, total 78 against 78, verified the scored commit, and merged baseline refresh PR #1386. `latest.json` at `9724a471f69b4545a051047b58d9e0e9d8326755` records commit `caaf9891`, that run URL, total 78 and 20 criteria summing to 78. Fresh computation: the content differs from the previous baseline.
  * Source: workflow, lock, adapter and gate are byte-identical at `901fea60`, `caaf9891` and `06374dfca`, so no source change separates failure from recovery and no persistent defect is established.
  * Remaining uncertainty list as in the plan.
* Verification after edit: `git diff --stat` shows only the README and RPI records; every link target exists; line wrap consistent with neighbours.

## Phase 2 details

* Changes record lists files, witness boundaries and qualifications (research file was observed by the witness only after it was written).
* One self-review, outcome recorded, independent assessment is Root's.
* Commit with the GitHub-resolved noreply identity set repository-locally and the Copilot trailer.
