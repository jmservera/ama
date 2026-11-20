---
title: Research issue 1837 live
ms.date: 2026-11-20
---

## Opening

* Issue #1837 (nomination route forms HTTP 400). Source at HEAD 6af67fa8c already posts JSON via nomination-routes.js (PR 2110 lineage) and has browser regression and native-encoding refusal tests.
* Gap candidate: negative tests (missing CSRF header, unauthorized role, case isolation, malformed input) for criterion 3.

## Findings

* Source already posts JSON with CSRF header from `/nomination-routes.js`; native URL-encoded posts are refused with 400 and write nothing (`test_native_form_encoding_is_refused_and_writes_nothing`).
* Browser regression `test_standalone_route_forms_submit_in_browser` covers all three forms with a constructed priority target and passes (`resident_post_statuses` 200,200,200).
* Gap: no negative tests for unauthenticated, unpermitted role, malformed body, stale version, bad id or cross-case writes on these actions. Buildable: criterion 3.
* Axe 4.10.3 (npm pack, sha256 matches the repository pin) runs `checks.nomination_route_forms_browser_check`: passed, zero violations.
* Adverse: `checks.nomination_browser_check` fails at the `nomination_review` step (HTTP 200 expected, got unexpected-error body) in this worktree; law store not loaded locally. Not caused by this change; not investigated further.

## Critique

One pass: keep the test additive in the existing file, no src change; FOCUSED tier basis is test-only change. Missing-CSRF header cannot be asserted because the test provider is not trusted-proxy; recorded as unproven here.
