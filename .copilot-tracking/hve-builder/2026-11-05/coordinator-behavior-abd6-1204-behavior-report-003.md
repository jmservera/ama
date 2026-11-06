---
title: Behavior report, coordinator agent at abd6b3f5f (issue 1204)
---

## Summary

* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md, blob acefb44a4d254ede6d86413343127b763dec42cb, commit abd6b3f5fea1c3618f79feb813555b866bccd60d, tree 93c4137d24e3b3602365f4f294f72702c295b778 (unchanged by this run).
* Run type: full (prior 11cfb run is historical, not reused). Fidelity: native activation of the registered agent in an isolated byte-identical copy, text-only (read-only tools; shell/merge/cleanup/Graph actions emulated text).
* Profile: requested `--model auto` (owner-approved intended Automatic profile). Auto selected GPT-6.1 Sol (most runs) and GPT-6 Luna (SC-14, SC-21); autoTier unknown; no model pinned. Lead is Sonnet 5.5. Designer and grader used harness defaults.
* Execution status: Complete (21 real runs + 7 + 6 control runs, all exit 0).
* Verdict: Revise. Real runs 20 Pass, 1 Partial, 0 Fail (independent grader). Negative-control discrimination not established.
* Evidence: sandbox .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/ (run-state, test-design, test-log, raw outputs with sha256 manifest, grade-report, test-review, both control copies).

## Findings

| ID | Severity | Finding |
| --- | --- | --- |
| B1 | Medium | Negative controls did not flip decisions; 20 Pass cannot be attributed to S01/S02 clauses (other target text lets the model infer the behavior). |
| B2 | Low | SC-14 Partial: omits that independent, hosted and human gates still apply; says native evidence "still required". |
| B3 | Low | R4 provenance expectation is inferred; SC-01 does not name the third no-progress check; SC-21 omits that delivery continues. |

## Coverage

Requirements R1-R10, R12-R16 covered; R11 partial. All scenario families requested (idle/unknown closure, blocked lane with independent work, approvals/one question, provenance, stacks and gates, cleanup, exited-worker slot, published-only pause, unknown upstream, HVE evidence gate, no proxy-to-native upgrade, HVE not-applicable, 15/18/21 PR thresholds, no double count, tier and single heavy holder, ignored-file provenance) have a scenario.

## Limits

* One run per scenario; no variance estimate; router-selected model varies.
* Text-only emulation; not native shell, merge, cleanup or Graph behavior.
* Schedules, rebase mechanics, tmux syntax and the live schedules were not tested.
* Agent tools frontmatter is opaque and not graded.
* Simulation evidence is not native-host or stronger-profile acceptance.
* Pass 5 committed transcripts are whitespace-normalized, not byte-exact; raw originals remain in /tmp/h1204 and commit cbebe58ef.
* Raw outputs in this run are byte-exact and not normalized, so `git diff --check` is not applied to them (documented exemption).

## Human review

- [ ] Human reviewer has accepted or rejected this report.
