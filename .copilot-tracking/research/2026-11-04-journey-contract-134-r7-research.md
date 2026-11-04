# Research: #134 slice 3 (R7)

Merged for #134: #872 (trace) and #1010 (AC register). Unmet and locally testable: RV-001 real-store journey. Finding: trace ignored the real `resident_decision_record` action (only legacy `resident_decision`), so a store-driven journey would never show a resident decision. Not implementable here: perspective screens, keyboard and announcement evidence (need browser and owner). Planning readiness: Ready. See [review](../reviews/2026-11-04-journey-contract-134-r7-review.md).
