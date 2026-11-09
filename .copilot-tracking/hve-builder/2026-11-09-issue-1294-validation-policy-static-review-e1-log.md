# Static review E1: issue 1294 validation policy (PROXY)

* Executor: fresh-context rubber-duck subagent, read-only, host cannot bind intended hve-builder static profiles; proxy, not canonical host-bound. Two passes: full review of ALL current targets, then targeted closure.
* Scope actually read by pass 1 (reported by the reviewer): `.github/copilot-instructions.md` 50-202; coordinator agent 35-100, 130-142, 165-180, 233-255, 360-376, 430-530, 568-585, 600-660, 680-805; `src/README.md` 55-410, 510-532, 634-657; `docs/reference/method/tracking-retention-policy.md` 1-106; `.github/rubric/README.md` 325-370; `docs/reference/log.md` 10940-10966; plus verification reads of `src-ci.yml` 1-329, `tools/ci-affected.py` 1-148 and `tools/rpi-checks.py` ranges. Source tier: focused; no workflow or tool edit.

## Pass 1 findings and dispositions

| # | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | High | Stack procedure lets one tip receipt cover intermediate PRs (coordinator ~512-516, 727-729) | Not accepted for this issue: pre-existing #470 gate-speed design (`--stack-member` verifies each PR; each member keeps its own exact-head review and hosted CI); not changed by #1294. Recorded as a residual observation for the coordinator |
| 2 | Med | "Every changed base requires refreshed validation" versus `BASE RELAXED` | Fixed (coordinator ~642-646) |
| 3 | Med | Receipt scope described as always partial for `--changed` | Fixed (src/README.md scoped-skips bullet) |
| 4 | Med | Sensor discovery-skip tolerance implied the SQL group always runs | Fixed (README local-only bullet) |
| 5 | Low | Historical research called the blanket gate "current" | Fixed by dated supersession note in D4 |

## Pass 2 (targeted closure) findings and dispositions

| # | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Med | README said every `--changed` receipt is partial | Fixed ("when groups are skipped") |
| 2 | Med | Rubric step 3 read hosted checks before step 4 runs them | Fixed (hosted checks follow in step 4) |
| 3 | Med | Coordinator step 8 required hosted checks before a push | Fixed (local before push, hosted after) |
| 4 | Low | "Always runs the final verification" conflicted with the no-receipt path | Fixed (any receipt it uses) |

Verdict pass 1: Revise. Verdict pass 2: Revise. The pass 2 fixes were verified by the lead (not a third independent pass); the coordinator's independent exact-head assessment must cover them. Hosted CI: not observed.

## Pass 3 (independent closure at commit ad2160d4e)

* Fresh rubber-duck subagent, read-only, proxy. Verified the four pass-2 fixes; one Medium: coordinator line 496 required verifying every focused partial receipt while the new step 8 sentence says only a cited receipt. Fixed: "that is used or cited as evidence". This single-line fix was verified by the lead only; no fourth pass. The behavior run graded the coordinator file before this one-line edit (hash fc104010...); the edit narrows a receipt-verification condition and does not alter any scenario answer (S10 already reasoned from the cited-receipt rule). Coordinator independent exact-head assessment must cover it.
* Static stage status: Revise findings all dispositioned; final state not independently re-passed after the pass-3 fix. Not a canonical Pass.
