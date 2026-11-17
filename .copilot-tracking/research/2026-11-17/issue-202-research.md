---
title: Issue 202 research, archive tag and legacy deletion status
date: 2026-11-17
base: eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4
---

Research disposition: executed. Planning readiness: Ready. Evidence only; no deletion or remote write.

## Measurements against main eb51af5c

* `git ls-tree -r HEAD | grep -cE '^(mvp|prototype)/'` returns 0. Criteria 2 and 5 of the issue hold (prototype and mvp absent).
* Tag `v0.21.0` is an annotated tag object `0096b113`, targeting `65a514ed2` (2026-10-27), which contains exactly one `mvp/` file (`mvp/README.md`) and no `prototype/` files; it is an ancestor of HEAD.
* `git ls-remote --tags origin v0.21.0` and `gh api .../git/ref/tags/v0.21.0` both return `0096b113`: the tag IS published on origin.
* `gh release list` and `gh release view v0.21.0` return no release. The owner decided on 2026-10-15 that a release accompanies the tag; this is unmet and needs the owner (externally visible action).
* `gh api .../branches/main/protection` returns 404 "Branch not protected": no required checks exist, so the "branch protection updated" clause has nothing to update; the owner should confirm. `mvp-ci.yml` and `mvp-validation.yml` remain as dispatch-only workflows (`on: workflow_dispatch`), deliberately retained by owner direction (no silent rename or removal).
* `.github/rubric/README.md` records that mvp globs were removed from the registry in steps; no dedicated final registry PR exists, as the 2026-10-31 audit says.

## Defect found

README.md "Source cut-over archive" (lines 45-51) says the tag is local, not pushed, and tells the owner to push it. That is stale: the tag is on origin. The dated cut-over evidence pack and log keep the historical statement and stay untouched.

## Not deleting

Workflow removal and release creation are owner-gated and outside this evidence task.

## Follow-ups

1. Owner: publish GitHub release for v0.21.0.
2. Owner: decide removal of dispatch-only mvp-ci/mvp-validation, given no branch protection.
3. Owner: decide whether the missing dedicated registry PR clause is waived.
