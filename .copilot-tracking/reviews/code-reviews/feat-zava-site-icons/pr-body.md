## Summary

Add the supplied Z as a browser tab icon, using an outlined circle and the
owner-approved audience variants:

* Residents: black on white, with a 52-pixel mark.
* Employees: larger white on black, with a 60-pixel mark.
* Both PNGs are 64 pixels square. Employee welcome, workbench and law pages,
  and both resident surfaces link the appropriate icon.

The welcome page uses the existing inline-media path, so anonymous public
asset permissions are unchanged. Other pages use existing release-versioned
static assets. The owner approved appearance and publication in this session.
Unrelated concurrent paper PDF and TeX edits are excluded.

## Validation

Focused tier: branding and existing static/media registration only; no
authentication, CSP, infrastructure, dependencies, SQL, deployment or gate
semantics changed.

* 127 combined static-asset, welcome, accessibility-baseline, content-standard,
  authentication and resident-preview tests passed.
* Three resident static/host/method-boundary tests passed.
* Ruff lint passed; four non-exempt Python files passed format checks.
  The existing legacy authentication test remains format-exempt.
* API mypy passed on 383 source files.
* Headed Chromium selected and decoded favicons on all nine entry paths,
  with native favicon requests observed.
* Pixel checks confirmed correct opaque backgrounds, centering and a
  measurably larger employee mark.

## Independent review

`hve-core:code-review-functional` reviewed every changed hunk and both PNGs
at exact commit `f037bd977817c78940457146b6836330e6f1b746`, against
`337d3999d5f1113752873b129a52f95aae6623ba`, with adjacent serving, caching and
package-data context. Result: `approve`, zero findings at every severity.
The reviewer did not rerun tests.

The original local review artifacts remain in the repository working copy.
This PR preserves the exact commit, scope, result and validation record.
Hosted CI must still be read for this head; no deployment or post-merge
smoke test is claimed.

## Human review

- [ ] Reviewed and validated by a qualified human reviewer

Only a qualified human reviewer may check this box. Owner approval of icon
appearance and publication does not constitute engineering or accessibility
sign-off.
