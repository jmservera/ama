# Research: #435 AC1 Tokenomics pitch and Q&A (1452)

Research disposition: executed. Planning Readiness: Ready. Base `1db0c4462c25266b9df4755a4453b612eef7a660`.

## Findings

* `docs/capstone/source/content.yaml` does not exist. The manifest is `docs/capstone/source/slides.json` (Slide 22 = S18, B25 = page 53, B27 = page 55). Not edited.
* S18 notes: one 50 s slot, labelled planning calculation (USD 0.44/home, USD 6,873 across 15,600 homes, dated secondary-source rate), accepted-outcome cost Unknown. Concise; meets "brief".
* B25 gives the CFO answer (workings, TCA denominator, controls, no saving or payback). B27 covers sprawl and call bounds. Both are long appendix cards, not a speakable 30 s answer.
* `validation.json` hashes: package candidate, manifest, asset catalog, builder, native helper, `pitch/speaker-script.md` and `pitch/questions-and-answers.md`. `docs/capstone/README.md` and `pitch/README.md` are not hashed, so a README link is safe. Do not edit the two hashed pitch files.
* `zava_forward.agents.heldout_batch` does NOT exist in this checkout (`src/agents/src/zava_forward/agents` has `heldout_freeze` and `chat_heldout` only). The brief must describe the USD 5 held-out batch as authorised by the owner on 2026-11-13 but not run and no runner present; no module claim.
* Ledger: `ai_consumption.batch_spread` labels recorded usage "not an authorised held-out batch"; cost, price and liability stay `Unknown` (src/core/README.md, src/api/README.md:60-66).
* Test paths in the brief are stale: real ones are `docs/capstone/history/cowork-main-presentation/test_build_assets.py` and `docs/capstone/source/diagrams/architecture/test-architecture.mjs`.

## Decision

Add `docs/capstone/tokenomics-qa-brief.md` (new, unhashed) and link it from `docs/capstone/README.md`; append a `docs/reference/log.md` entry. No deck, manifest or hashed file changes. AC1 is supported by the existing deck plus this sheet; no rehearsal, measurement or ticking claimed.
