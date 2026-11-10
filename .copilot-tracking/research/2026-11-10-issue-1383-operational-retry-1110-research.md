<!-- markdownlint-disable-file -->
# Task Research: issue 1383 operational retry (process qualification)

Date: 2026-11-10. Task `1383-operational-retry-1110`, parent `1383-incident-d1-1110`. Mode manual. Research disposition: executed (local re-inspection; no GitHub download, rerun or model call).
Start: branch `docs/demo-rubric-incident-1383-1110`, HEAD `5c8a856c2dbee53d1aa8f7030524afa9569e7451`, clean.

## Question

The original D1 witness chain ended with a refused `commit-complete`. What exactly happened, does the diagnosis stand, and what bounded documentation qualification is warranted?

## Findings

* Original chain (`phase1383-incident-d1-evidence-1110/issue-1383/events.jsonl`, SHA-256 `e1fe1900ccc3e895...c764bb`): seq 1-6 `launch`, `research-open`, `plan-done`, `implement-start`, `implement-done`, `review-done` are `ok` with empty reasons; seq 7 `commit-complete` is `refused` with reason `commit claim does not match the actual HEAD`, recorded at 14:23:52Z with git head `5c8a856c`.
* Cause: the caller passed the literal string `HEAD` to `--claim-commit`, not the 40-hex commit. This is a caller error, not a defect in the diagnosis or the committed content. The old chain is preserved unmodified and is not repaired, appended to or relabelled here.
* Original direct evidence is intact: all 21 entries of `checks-1383-incident-d1-1418/MANIFEST.sha256` verify (0 mismatches), covering run 42812941091 and 42815865163 metadata, jobs, record-job logs, PR #1386, `latest.json` at `9724a471` and the agent outputs. No new download was needed or made.
* Source identities unchanged: workflow, lock, adapter and gate blobs at `901fea60` and current HEAD match (`abd5aabf...`, `dd28eee0...`, `9e5cff7a...`, `15748752...`).
* The diagnosis stands as committed: historical invalid scoring input (28-character `PLACEHOLDER_WILL_BE_REPLACED` accepted first; complete second call rejected `Maximum allowed: 1`) with recovery in run 42815865163 (decision valid/passed/78, baseline PR #1386, `latest.json` at `9724a471`). Limits remain: log-only decision/report evidence, `901fea60` never scored itself, no recurrence search, no persistent code defect established.
* The README incident note does not mention that the original witness chain ended in a refusal. A reader trusting only the README or commit could assume a complete witnessed chain.

## Disposition

Add a short dated process qualification to the existing incident note: the last original witness event was refused for the caller's non-hex `HEAD` claim; the original evidence is kept; this separately recorded prospective operational retry does not repair that chain and is not host or model attestation. No change to incident meaning, scores, source or authority.

Planning Readiness: Ready. Not a scorer fix, not a new correction pool, no second retry permitted.
