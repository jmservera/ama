# Plan: integrate current main into the issue 144 branch (2026-11-09, Refs #144)

Recorded prospectively before the merge. Research: [research](../../research/2026-11-09-issue-144-current-main-research.md). Details: [details](../../details/2026-11-09/issue-144-current-main-details.md).

Pins: HEAD d2d9560694622441fc8b2ad146cccd9c765535c4; origin/main df8e858b2150198e5e22c73d224a0d3592c73daa; predicted merge tree 464ce9646f8c7ebc29a1a17d419fce6cc99e02c9 (prediction only).

## Phases

* [ ] P1: Re-fetch; stop on any main or owner-branch movement relative to the pins and re-plan.
* [ ] P2: One ordinary `git merge --no-ff origin/main`. No rebase, reset, stash or force.
* [ ] P3: Verify `docs/reference/log.md` is additions only versus HEAD and versus main, both entry sets and the 2026-11-09 header text retained; no original tracking record modified or deleted.
* [ ] P4: Verify `src/agents` equals approved 63d7f8c1 and equals HEAD; verify source, infra and tools equal main outside this branch's own paths.
* [ ] P5: Run the demo-targeted checks in the details (Agents queue set, Date positive and mutation-negative, ruff, format, mypy, impacted Core set), one immutable log per producer with its own exit.
* [ ] P6: Scoped whitespace and link checks on authored paths.
* [ ] P7: Self-review once, changes record, state, append KB log entry, commit a clean frozen local candidate.

## Critique (executed once, before the merge)

Verdict: proceed with amendments, all applied.

* Risk: target moved from the brief's 23e944c1 to df8e858b. Amendment: pin df8e858b, state the rubric-only difference, and stop if it moves again.
* Risk: `infra/README.md` and `log.md` both edited on both sides. Amendment: P3 and P4 check the merged row at the queue adapter line and the log additions; on a textual conflict keep both intents in append order, and stop and report if intent is unclear.
* Risk: masked exits (pipes to tail or tee). Amendment: run each producer with output redirected to its own unique file and capture `$?` directly; never pipe a producer.
* Risk: the Date negative proof is inherited. Amendment: mutate a copy outside the repository and assert failure, confirming the module path imported.
* Risk: Core and API tests that need SQL. Amendment: select only non-SQL Core modules; no SQL, browser, cloud or credentials.
* Risk: counting this validation as a review-correction cycle. Amendment: unchanged-source validation consumes no cycle; a material product fix would be reported with scope and budget first.

## Tier and limits

Owner demo-targeted tier. No `rpi-checks --all`. No push, PR, issue or board action. Independent exact-head review by the same reviewer and hosted CI of the published head remain required.
