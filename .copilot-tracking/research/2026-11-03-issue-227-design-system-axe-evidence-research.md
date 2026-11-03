# Research: issue #227 design-system and axe evidence

Disposition: reused (prior research 2026-11-01 to 2026-11-03). Planning Readiness: Ready.

* Merged for #227: #653 per-home screens, #776 per-home browser and axe check, #806 cross-home referral table, #831 cross-home browser check (axe reported not run), #866 rendered table tests. #488 closed unmerged.
* Criteria 1-4 are met in code and browser-evidenced. Open: 5 (WCAG 2.2 baseline; automated axe for the cross-home table not yet recorded; no AT or human acceptance, #151/#155) and 6 (design-system components; #150 is closed, but no safety-screen-specific proof of component use).
* Pinned axe 4.10.3 file exists outside the workspace (sha256 880970c0...a68bb, matches AXE_SHA256 in the check).
* Slice: run the existing browser check with axe for both roles and per-home and cross-home views; add a rendered-class test tying safety screen classes to the CSS and the design-system document.
* Desk research is hypothesis, not observed behaviour; validation remains #155.
