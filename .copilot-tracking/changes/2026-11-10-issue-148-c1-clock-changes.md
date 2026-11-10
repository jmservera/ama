<!-- markdownlint-disable-file -->
# Changes: issue 148 C1 clock erratum

Plan: [C1 plan](../plans/2026-11-10-issue-148-c1-clock-plan.md). Original records and adverse finding preserved: [original changes](2026-11-10-issue-148-four-images-changes.md), [original review](../reviews/2026-11-10-issue-148-four-images-review.md).

* Added [erratum](2026-11-10-issue-148-c1-clock-erratum.md) (additive, documentation only).
* Updated only the current state file and added the C1 research, plan, details, critique, changes and review records.
* Verification (tool output): `git diff --check` clean; staged paths all under `.copilot-tracking/`; `git diff d305d0f90 HEAD -- src infra docs .github` empty; `git rev-parse d305d0f90:src HEAD:src` both `300d3183f7de68f079ce317fa772abc4891ac80b`; `infra` trees both `d94040329d5497aee252300972cb3c7497689d25`; erratum links resolve.
* No runtime test rerun. The d305 targeted results apply only with the product tree unchanged.
* Actual `date -u` readings: start `Tue Nov 10 01:31:50 UTC 2026`; during verification `Tue Nov 10 01:32:27 UTC 2026`. Prospective C1 commit `7715f2f426e5a9245da102602b4fb3a247d212dc` has Git time 2026-11-10T01:32:09+00:00 (provenance only).
