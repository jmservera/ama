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
