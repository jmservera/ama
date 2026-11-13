# Details: #440 demo feature-wave checkpoint (1531)

## Section content

* Pins: main `34b11967b93df40b653d384ab3b136bb1fb842f9`, tree `dfe71a6354772012d894bf1e9f3ddb92cbba1610`, previous checkpoint head `5cedff3f4`-era sections unchanged; merge commits per PR from the research table.
* Wave identity: label versus actual content per PR (1514 and 1515 and 1519 docs only, 1516 README, 1518 source, 1520 diagrams and capstone tooling, 1523 and 1525 agents source, 1527 aftercare source). 1519 closes nothing; no PR merged here closes #440.
* Documents: BRD 0.21.0 draft, PRD 0.21.0 in-review, ADR 0003 and 0006 Accepted, ADR 0007 Proposed, with blob prefixes; draft or in-review or Proposed is not approval; none of the nine PRs changes them (verify with `git diff` of docs/brds, docs/prds, docs/adrs between `3b05143179` and main).
* Traceability rows with classes `local observed`, `implemented-unverified`, `deferred`, `blocked`.
* Commands and exits: taken verbatim from each changes and review file, labelled as recorded, not rerun here. Only this checkpoint's own runs (audit check, `test_cutover_audit`, `git diff --check`) are current.
* Gates: PR 1517, PR 1521, #131 tenure owner decision, plus Azure sync items (live Azure OpenAI held-out batch not run, route/allowance for #144 worker, #184 mid-slot PR 1524, #1288 SQL).
* Recommendation: CONTINUE, bounded; epic closures (#440, #149, #144, #184, #432, #435, #133, #131, #891) held; the Azure demo sync may proceed once 1517 and 1521 merge and an exact-head read of hosted CI, under the owner admission already recorded for the sync.

## Critique amendments (applied before editing)

* Sync gate: cite the 2026-11-13 owner sign-offs section (batch up to USD 5, Azure sync authorised, batch waits for the live Azure OpenAI step) as the only admission recorded; require applicable successful exact-head hosted checks of 1517 and 1521 as merged; separate preflight gates (1517, 1521, #131 decision) from optional follow-ups (1524, 1528).
* Documents: PR 1519 changed one PRD link and one addendum line (PRD blob `c788b917bafa` to `a385d27481f8`); version, status and ms.date unchanged. BRD and ADRs unchanged.
* Each observation carries its tested head and scope; no claim of current-head equivalence.
* PR 1523 includes the Container Apps Bicep `serve` command; no route, allowance, image build or queue run.
* Adverse limits carried: 1520 stale catalog derivative hashes and drifted infra anchors, test-geometry and Test-SourceHashes not run; 1527 api mypy missing Playwright imports; 1523 bicep_policy 1 error in the first run.
* Commands are quoted where recorded; where a record gives only a summary the command or exit is marked not recorded.
