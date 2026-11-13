# Research: #203 inventory refresh and owner decision recording (2026-11-13)

Disposition: executed. Planning Readiness: Ready.

## Findings

* Generator and verifier: `src/core/src/zava_forward/core/synthetic/cutover_audit.py` (`--write` regenerates, default checks) writes `docs/architecture/cutover-reference-inventory.tsv` and the parity TSV; tests in `src/core/tests/test_cutover_audit.py`.
* Base `da0d5af97`; inventory has 1463 lines and is stale after the Wave-1222 tracking merge.
* Pitch drafts: `tokenomics-placement-draft.md` says "54-slide" and places Tokenomics at page 21 S18 and B25/B26/B27 at pages 52-54; the current deck has 55 slides, Slide 22 on the main route, B25/B27 at pages 53/55.
* Evidence pack last section: Wave-1222 (line 8222); log is append-only.

## Owner decisions to record (2026-11-13, supplied in the brief)

* #201/#202/#198: approve prototype parity mapping, `v0.21.0` retirement, current `src-ci` and `rubric-score` checks; live deployed parity and private-data backup stay pending.
* #228 AC3: staff-mediated capture plus acknowledgement plus independent QA satisfies AC3 for demo scope; OD-47 supplier portal deferred.
* #435 AC1/AC4: Slide 22 plus B25/B27 Q&A cards; USD 0.44/home kept as labelled scenario; up to USD 5 held-out token batch authorised, not yet run; rehearsal timing unperformed.
