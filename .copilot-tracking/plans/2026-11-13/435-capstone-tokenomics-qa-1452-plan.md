# Plan: #435 AC1 Tokenomics Q&A brief (1452)

Research: `.copilot-tracking/research/2026-11-13/435-capstone-tokenomics-qa-1452-research.md`

## Steps

1. Create `docs/capstone/tokenomics-qa-brief.md` (YAML frontmatter, `*` lists, ASCII): 30 s presenter answer; three-way table (labelled scenario, live consumption ledger, held-out batch); S18/B25/B27 pointers with page numbers; do-not-say list; honest status (not rehearsed, batch not run, `heldout_batch` module absent in this checkout).
2. Link it from the "Prepare the pitch" row of `docs/capstone/README.md`; bump nothing else.
3. Append `docs/reference/log.md` entry; update `docs/reference/README.md` index if it lists capstone files.
4. Validate: `validation.json` hashed files unchanged (git diff names), real test paths `test_build_assets.py` and `test-architecture.mjs`, link check, `git diff --check`.

## Details

* No edit to `slides.json`, `pitch/speaker-script.md`, `pitch/questions-and-answers.md`, deck, validation.json.
* Figures only as already sourced: USD 0.440576/home, USD 6,872.9856 across 15,600, USD 1.60/million on 2026-10-23, 6,884 tokens/5 runs, cap USD 5.00.
* Ledger: cost Unknown until settled and approved (Finance).

## Critique dispositions (rubber-duck, once)

* PC-001 applied: sha256 baseline of every tracked file under docs/capstone and tools/capstone taken before edits; compared after.
* PC-002 applied: brief states 10x tokens/task, 20 tasks/home, USD 1.60/million GPT-4.1-mini output-rate basis dated 2026-10-23; cites pages 22, 53, 55.
