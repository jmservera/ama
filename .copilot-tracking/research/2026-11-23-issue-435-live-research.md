# Issue 435 live research (2026-11-23)

Disposition: executed (opening). Scope: unticked criteria 1, 2 and 4 of #435; synthetic demo, desktop only.

## Observations

* main and HEAD are both 342fad401d (git rev-parse).
* Live, read-only via existing Azure CLI login: ca-cutover-test-demo-api active revision 0000054 (Healthy, 100% traffic, created 2026-11-22T23:14:23Z); ca-resident-demo active revision 0000026 (Healthy, 100%, 2026-11-22T23:14:37Z).
* Deck docs/capstone/deck/zava-forward-cowork-v2-draft.pptx: 55 slides; slide 22 "Model inference. Measure accepted value.", slide 53 B25 CFO card, slide 55 B27 card; last changed 05e94d3036.
* Prior five passes (2026-11-18 to 2026-11-22) found no src gap; criteria are decisions and documents, not application behaviour, so the live apps carry no Tokenomics acceptance evidence.

## Planning Readiness

Ready. Pending: re-run the held-out batch adapter tests (src/agents) as the code-path evidence for criterion 4.
