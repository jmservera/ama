# Research: issue-201-private-mvp-data-exclusion (Refs #201)

Date: 2026-11-14. Tier: Focused. Disposition: executed. Planning Readiness: Ready.

Evidence inspected (no private dataset read):
* .gitignore lines 10-13 ignore /mvp/data/ and /src/**/data/.
* git ls-files -- mvp/data returns nothing.
* src/core/src/zava_forward/core/data_paths.py defaults ZF_DATA to ~/.zava-forward/data/zavaforward.json.
* src/README.md (lines ~631, ~690) documents data outside src/ and disclaims private backup evidence.

Finding: repository-side guard holds; no test existed. Owner backup confirmation is an external human gate and stays unverified.
