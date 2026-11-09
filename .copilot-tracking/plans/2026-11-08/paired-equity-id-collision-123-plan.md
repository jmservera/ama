<!-- markdownlint-disable-file -->
# Plan: paired-equity anchor ID collision correction (#128, Refs #123 #440), 2026-11-08

Research: [research](../../research/2026-11-08/paired-equity-id-collision-123-research.md). Details: [details](../../details/2026-11-08/paired-equity-id-collision-123-details.md). Critique: [critique](paired-equity-id-collision-123-critique.md).

Tier: FOCUSED (prospectively selected). Stop for coordinator disposition if any full-tier category appears.

## Phases

* [ ] Phase 1: commit this planning (prospective) with the fresh `gh api user` noreply email, Conventional Commit and Copilot trailer, before editing source.
* [ ] Phase 2: add focused regression tests to `src/core/tests/test_paired_equity.py` only; run red against unmodified code with installed-distribution or explicit current-source imports, external caches, bytecode off; preserve command, exit and output in Changes.
* [ ] Phase 3: if the finding example reproduces (silent pass), apply the minimal `paired_equity.py` fix; otherwise stop with the evidence and a clean freeze for disposition.
* [ ] Phase 4: run focused tests green, then the 171-test coupled selection, core Ruff, format check, mypy, JSON and link checks for changed files, `git diff --check`; confirm only `paired_equity.py`, its test and records changed.
* [ ] Phase 5: Changes, one author Review, state; commit implementation and RPI records; fresh fetch; freeze ignored-clean.
* [ ] Phase 6: check RAM, CPU, disk, physical and logical lock holder; run `python3 tools/rpi-checks.py --changed --jobs 2 --lock-timeout 0 --base <fresh origin/main> --out /home/azureuser/.local/share/ama/gates/c123-f15-collision1-1108 < /dev/null`; verify with `--verify-receipt --required-scope partial --base <current main>`. Results go to the external handoff; no later source commit.

## Critique dispositions

Applied: IC-001 and IC-002 extend the test set (non-string and empty IDs, differing IDs with a colliding anchor keep `pair_ids_differ`, multiple matching anchors, seeded defect on a blocked collision stays undetected, `_comparability` precedence for a confounded collision, unchanged `input_digest`). IC-003 accepted: unrelated duplicate anchors are not guarded.

## Stop conditions

* Not reproduced: no production edit. Main moved: plan and normally merge before the gate. Lock held, missing prerequisite, failed or unexpectedly skipped group: return the scoped failure, no reruns, fixes after sealing, cloud fallback or skip token.

## Boundaries

* Do not touch `ranking.py`, store, publisher or runner, API or auth, ranking policy, thresholds, fixture semantics. Keep `fairness_evidence=False`, `activation_allowed=False`. No push, PR mutation, merge, ticking, cleanup or cloud work. Preserve the f14 receipt (sha256 `040871816ad118e055c73f02ed74b343d72f176f33839de9886d6ad4466f8f83`), images and logs. Refs only.
