---
title: "#521 unified evidence pack integration research"
ms.date: 2026-11-13
---

## Scope

Integrate commits 85b49947c (#521/#133/#152), 0f3710e12 (#189/#435) and e4b47e767 (#435 Slide 22 tokenomics Q&A) onto 8ca5685b7 on `docs/demo-unified-evidence-pack-1509`.

## Findings

* None of the three commits descends from 8ca5685b7; 85b49947c is based on 1ccfae438, the other two on 1db0c4462. Cherry-pick in order.
* 85b49947c changes `infra/README.md` (+14/-3 near line 4618), which may shift cutover inventory line numbers.
* e4b47e767 changes `docs/capstone/README.md` and adds `docs/capstone/tokenomics-qa-brief.md`; capstone assets and `validation.json` may hash docs.
* Review finding 1: the #152 plan line 3 links `../research/...` and `../details/...` resolve wrongly from `plans/2026-11-13/`; they need `../../research/2026-11-13/` and `../../details/2026-11-13/`.

## Planning Readiness

Ready. Research disposition: executed (git inspection only).
