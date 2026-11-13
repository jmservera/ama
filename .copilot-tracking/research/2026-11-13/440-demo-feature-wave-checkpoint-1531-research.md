# Research: #440 demo feature-wave checkpoint (1531)

Disposition: executed. Planning Readiness: Ready.

## Pins (read 2026-11-13)

* Branch `docs/demo-wave-stabilization-checkpoint-1531`, HEAD equals `origin/main` `34b11967b93df40b653d384ab3b136bb1fb842f9` (merge of PR 1527), root tree `dfe71a6354772012d894bf1e9f3ddb92cbba1610`.
* BRD 0.21.0 `draft` (`34d88395de86`), PRD zava-forward 0.21.0 `in-review` (`a385d27481f8`), ADR 0003 and 0006 Accepted, ADR 0007 Proposed (`541e0f72dd2c`).
* Open sibling PRs: 1517 (chat grounding, head `b3d4282c`, checks partly pending), 1521 (UX parent, head `aee55045`, checks partly pending), 1524 (IoT mid-slot exit), 1528 (Azure sync preflight docs). All excluded.
* Issue state (live): #440, #131, #1288, #184, #432, #144, #133, #435, #203, #441, #891, #149 OPEN.

## Merged wave (merge commit, content read from `git show --stat` and changes and review files)

| PR | Merge | Content | Recorded local validation and review |
| --- | --- | --- | --- |
| 1514 | `74a93a137` | docs, Wave-1045 section | historical child observations |
| 1515 | `dafed6a27` | docs, Waves 1105 and 1143 section | historical child observations |
| 1516 | `74cd8cb08` | `src/agents/README.md` field count nine to ten (#216) | test_paired_report_command 21 OK; review no significant issues |
| 1518 | `1db0c4462` | #184, #1288: cadence 1 and 5 minutes, five-home fail-closed Quality scope, handover guard (api and core) | ruff, format, mypy clean; core 24, 50, 40; api 102 and assistants 138 (59 MSSQL skips); review no significant issues |
| 1519 | `b605f78a3` | #203, #441, #201, #202, #228: inventory regenerated, PRD anchors, Wave-1222 section, sign-offs | audit check PASS, test_cutover_audit 9 OK; review approve after one fix |
| 1520 | `1ccfae438` | #435: regenerated diagrams, slide 52 qualifier | test-architecture 11/11, build-architecture --check 0, pytest 26/26; review approve; test-geometry and Test-SourceHashes not run |
| 1523 | `96da501c1` | #144: standalone worker runtime, safe standby entrypoint | agents 355 tests, infra container_contract, bicep_policy, deploy, pipeline 118 OK; review approve; no image build or queue run |
| 1525 | `0893bbcdb` | #432, #435: held-out token measurement and cost-cap runner | 34 new tests, agents suite 370; review approve; nothing run against a provider |
| 1527 | `34b11967b` | #133: evaluator outcomes column, stricter neutral text guard | core aftercare 111 (15 skipped), api aftercare OK; review two findings fixed |

## Gates before the live Azure demo sync

* PR 1517 (#891 chat grounding) and PR 1521 (UX parent, #149) unmerged, checks pending at read time.
* #131 tenure: owner product decision on universal routing; no criterion tick or Legal inference.
* Not claimed: Azure, SQL Server, browser, assistive technology, provider, resident, human acceptance.
