<!-- markdownlint-disable-file -->
# Discovery CLI checkpoint 440 research (2026-11-10)

Task `440-discovery-checkpoint-1110`. Research disposition: executed. Prospective: written at 2026-11-10T04:28Z (tool `date -u`) before any observation run or document edit. This is a NEW periodic checkpoint after a completed feature increment (issue 125 CLI, PR 1355). It is not a correction: the #440 ledger C3 of five stays as recorded (two left, no reset, none spent here). Source artifact unchanged, so no new Major coordinator HVE mutation.

## Evidence read

* Issue #440 (OPEN) criteria 1 to 6 ticked, 7 and 8 open; issue #125 (OPEN) three criteria unticked. Latest #125 comment: PR 1355 merged after independent exact-head APPROVE/0 and 19 actual hosted checks SUCCESS (read via `gh pr view 1355`; not re-run here), no criterion ticked.
* Fresh `origin/main` at 2026-11-10T04:27:31Z (`git fetch`, `git ls-remote`): `0d262beee2dfa6feca27680aa1d596111154c8d9`, equal to the pin. `0d262beee` changes only `.github/rubric/scores/latest.json` (4 lines); the delivered source is `a0f7cf182` (PR 1355, merged 03:42:37Z), 12 paths: Core `discovery_assistant_demo.py` (204 lines), `__main__.py` (+7), `test_discovery_assistant_demo.py` (190, 14 cases), a README section (+29) and the 125 RPI records.
* Prior checkpoint a61bebe6b (PR 1354) is the previous recorded point; its C3 of five stays historical and is not re-observed.
* Delivered behaviour read from source: `python -m zava_forward.core discovery-demo` takes no argument (extra argument exits 2), reads no environment, path or store, composes the boundary, drafting and evaluation helpers over a fictional in-module fixture, and prints sorted JSON. Exit 1 on expectation mismatch or repeatability failure. Without an argument the package still prints its version.
* Affected contracts: Core boundary (`authorise_tool`, `assess_readiness`), drafting (`calculate_stage_durations`, `draft_evidence`), evaluation (`check_repeatability`, `compare_methods`), `__main__` dispatch, README slice 4 text, discovery brief readiness and evaluation sections (blob `fee5a6e48`, ms.date 2026-11-04).
* Open pull requests list contains no discovery change. Excluded by instruction: unmerged 135 C4, 1300 C2, retained 185 and 132; the current-live R10/Nov4 image is not current-main acceptance.

## Findings and limits

* The CLI makes the delivered helpers executable as a design-hypothesis illustration only. Expected figures are constructed from the fixture, the conventional table reuses the same calculation, the fallback text is deterministic code, and the human comparison is empty.
* Whole #125 criteria stay unmet: readiness list satisfied before company data (all ten items missing by design), no write access observed on a real operational system (policy decisions only, no tool is registered), no actual manual or conventional comparison. Current Azure model and UI acceptance stay unmet; no model is bundled or called.
* Not claimed: Phase 0 or any privacy, access or human approval; whole #440 or #125; hosted CI for the exact main head; independent exact-head assessment.

## Planning Readiness

Ready.
