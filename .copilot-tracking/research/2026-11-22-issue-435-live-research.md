# Issue 435 live research (2026-11-22)

Research disposition: executed (read-only). Planning Readiness: Ready.

Scope: synthetic demo, desktop only, docs only. Four earlier notes cover the same criteria (research notes dated 2026-11-18 and 2026-11-20 under docs/reference/research/). This pass re-reads the deck and the live demo API on 2026-11-22 and records one fifth note.

Fresh observations (2026-11-22):

* python-pptx read of docs/capstone/deck/zava-forward-cowork-v2-draft.pptx: 55 slides, last changed by commit 05e94d3036. Slide 16 is "Adopt without a big-bang replacement." (S14, not Tokenomics). Slide 22 is the Tokenomics segment (S18, E21 assumed workload, E19 usage only). Slide 53 is B25 (CFO card), slide 55 is B27.
* `az containerapp show -g ama -n ca-cutover-test-demo-api`: provisioning Succeeded, running Running, latest revision ca-cutover-test-demo-api--0000053. No Azure resource created; none to delete.
* Batch records for #432 exist in docs/reference/research/evaluation/heldout-batch-432-live-2026-11-18/ (authorization.json, report-live.json).

Unticked criteria: 1 placement and rebuild, 2 mentor confirmation, 4 batch decision. Criterion 2 cannot be proven (needs the mentor). Issue text "slide 16" is stale: Tokenomics sits on slide 22.
