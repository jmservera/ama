---
title: Critique for issue 2186 integration gate
---

Executed once. Verdict: proceed.

* Risk: the post-gate evidence commit moves HEAD off the gated commit. Mitigation: keep it to .copilot-tracking/ paths, which are receipt-inert, and verify the receipt at the final HEAD with the current origin/main.
* Risk: add/add conflict resolution dropped content. Mitigation: kept the later commit's tracking files; the held commits stay recoverable by their -x trailers.
* Risk: gate failure unrelated to held commits. Mitigation: record the failure and failing check verbatim; do not bypass, relax or skip; use --resume only for the same head.
* Disposition: the generic brief ban on --all conflicts with the goal; the goal names the owner-approved run, so it is followed.
