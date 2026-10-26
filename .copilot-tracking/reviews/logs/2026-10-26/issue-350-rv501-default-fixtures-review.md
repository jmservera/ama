<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 default fixture correction review
description: Independent review of correction cycle 1, outcome preserved as returned
ms.date: 2026-10-26
---

Single independent read-only `rubber-duck` review, 2026-10-26, run on the uncommitted change. The earlier RV-001 review (RV-501, Non-conformant) is unchanged and not relabelled.

Verdict as returned: Non-conformant; RV-501 not resolved at the reviewed state. 88 tests OK at review time.

* RV-601 (blocking): the cached runtime functions returned their mutable cached dicts, so a caller could poison later fixtures.
* RV-602 (blocking): the spy regression only proved the runtime methods ran, not that the bundle sections were their returned evidence.

Disposition: both were fixed after the review without a second review: baselines are cached as private immutable JSON text and deserialised per call (RV-601); the regression captures the real runtime returns and asserts the bundle sections equal them while being distinct objects (RV-602). 88 tests OK after the fixes. These fixes are not independently re-verified, and the review outcome is not converted to Conformant. Under the two-cycle limit this was cycle 1; a coordinator decision is needed before any re-review (cycle 2).

Reviewer-confirmed: no `src` or checker change; 980 baseline, 40-contact cap, non-acceptance, Application Administrator and RecursionError coverage unchanged; no `__pycache__` left.
