<!-- markdownlint-disable-file -->
# Plan: fresh full behavior run, discriminating controls first (issue 1204)

* Task: 1204-behavior-fresh-full. Written 2026-11-05 after the research update and before any scratch-copy, model or storage action. Research: [update](../../research/2026-11-05/coordinator-behavior-fresh-full-1204-research-update.md). Details: [details](../../details/2026-11-05/coordinator-behavior-fresh-full-1204-details.md).
* Source acefb44a4d254ede6d86413343127b763dec42cb, frontmatter and tools configuration unchanged and opaque.

## Phases

| Phase | Work | Gate to continue |
| --- | --- | --- |
| 0 | Write the finite raw-storage manifest as evidence (read-only compute; no move) | Manifest committed; root reviews later |
| 1 | No-model identity probe: strace openat filter on an owned scratch agent copy | Open of exactly the intended file observed, else stop and report the missing mechanism |
| 2 | Fresh independent design (content only), lead persists, expectations frozen in run-state before any executor call | Design Complete, black-box self-check clean |
| 3 | Build opaque-named scratch cwds: real copy (blob acefb) and coherent mutants M1, M2, M3; record diffs and remaining-clause check | Mutants internally consistent |
| 4 | Execute discriminating pairs first (P1, P2 with backend sibling, P3), each real and mutant, sequentially with trace and exit | Expected directions observed, else stop with cause |
| 5 | Only if Phase 4 discriminates: execute remaining real-source scenarios of the full design | All executed |
| 6 | Independent fresh grader (content only); mutants graded against the original contract as separate findings | Review verdict |
| 7 | Durable promotion of gradeable raw output, report, Changes, one dedicated RPI Review, state, commit | Commit |

## Decisions

* D1 reuse: ineligible (003 Revise). D2 scope: full. D3 early failure yields Partial, Deferred or Blocked. D4 no source change. D5 range diff check remains an open gate until an approved lossless replacement. D6 97-test rerun only after the final tracked candidate exists.

## Self-critique (single pass)

* Risk: strace may not follow the CLI's child or may fail ptrace under restrictions. Mitigation: the probe is Phase 1; failure stops the lane with the exact mechanism.
* Risk: Auto routing differs per run; recorded per run.
* Risk: mutants leave residual contradictory clauses; Phase 3 check is mandatory.
* No conflict with a confirmed decision found.

## Resume point

Phase 0 then Phase 1.
