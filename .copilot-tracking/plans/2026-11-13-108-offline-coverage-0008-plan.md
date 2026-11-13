<!-- markdownlint-disable-file -->
# Plan: issue #108 offline evaluation coverage record

* Task: `108-offline-coverage-0008`; research: [research](../research/2026-11-13-108-offline-coverage-0008-research.md); details: [details](../details/2026-11-13-108-offline-coverage-0008-details.md)
* Tier: focused (agents-only offline harness, tests and README; no gate, workflow, dependency, Dockerfile or tool file)

## Phases

* [ ] Phase 1: failing-first tests in `src/agents/tests/test_ai_eval.py`
* [ ] Phase 2: observation layer, `task_coverage`, funding and document checks in `ai_eval.py`
* [ ] Phase 3: truthful docstring, module header and `src/agents/README.md` note; docs log
* [ ] Phase 4: focused validation (agents unit tests, integrity, ruff, mypy)
* [ ] Phase 5: one independent Review; local candidate commit with noreply identity and trailer

## Constraints

* No provider, model, network, Azure, budget, threshold, independent label, human acceptance, push or PR.
* The PR #1495 head `bbdacadcb` must not change. If #1495 merges during work, freeze the local branch and let the root re-evaluate lineage; no retarget or push here.
* Unfavourable original raw results are retained in the evidence root.

## Amendment 2026-11-13: main alignment (prospective, append-only)

* #1495 merged to main as `e44de171e` (main now `bb9f450fd`). The Constraints entry above that froze the branch is satisfied; the root declared lineage: this is a new bounded AI-harness follow-up intended for `main`. #1495 is not updated or reopened, no parent is published and nothing is retargeted silently. The old #1495 branch ref is unchanged.
* Alignment is a normal merge of fresh `origin/main` into this branch. No amend, rebase, squash, source correction or new candidate pool. Original RPI artifacts, adverse failures, Review and append-only docs are preserved; conflicts keep both sides, and unclear conflicts stop the work.
* Preview showed no conflicts. Source behaviour and Low follow-ups are unchanged.
* Validation after merge: the 28 planned focused units and the offline harness in an isolated pip install (no uv, no source-package PYTHONPATH), Ruff on touched files and the configured mypy; exclusions are recorded. The full agents suite (336, previously green) is re-run only if new source conflicts appear.
* No push or PR until the root's independent exact-head assessment.
