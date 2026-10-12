---
title: Repair Account Photo Blob Rendering
description: Necessary scoped child repair for the reproduced CSP failure
ms.date: 2026-10-12
---

## Task Metadata

Task zava-account-photo-rendering-2026-10-12; automatic.
Parent zava-workbench-entry-2026-10-12, RV-001.

## Executive Summary

Permit Blob object URLs only in img-src, so the server-proxied Microsoft photo
can render. Keep script/default/frame/network policy and all auth unchanged.
Add success regressions, rebuild/redeploy and repeat the real binary-image
check. Actual user photo/consent acceptance remains separate.

## User Decisions and Requirements

* Show the Entra account picture; continue the necessary full-RPI repair loop.
* Do not fake a live personal session or expose credentials.

## Goals

Correct the reproduced success-path photo failure with the smallest safe change.

## Scope and Non-Goals

server.py image CSP; two auth tests; directly related guide/log; real image,
deployment and evidence. No broader CSP permissions, new auth/storage,
personal photo capture or parent Review repeat.

## Functional Requirements

The existing photo Blob URL loads as an image under the deployed response CSP.

## Non-Functional Requirements

blob: is allowed only for images; existing self/data/map sources and other
directives remain unchanged. Auth boundaries and token secrecy remain intact.

## Acceptance Criteria

* CSP regression and authenticated photo HTTP binary/no-store test pass.
* Full regression passes; real non-root image built and deployed.
* Live public-logo-as-binary Blob test loads successfully, without real photos.
* Anonymous welcome remains 200; API remains 401.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Repair, verify and publish
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Scope Blob image permission and add regressions
<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Build/deploy, prove real binary rendering and publish

## Test Ownership and Candidate Lock

Parent owns tests; no removals; maximum two additions in test_auth.py.
The existing exact tile-host CSP assertions in test_auth.py and
test_ui_support.py may be updated to the new
`img-src 'self' data: blob: <existing-host>;` value; it is not removed.
Semantic: CSP image scope and authenticated binary delivery.
Regression: full existing suite and anonymous boundaries.
Generated evidence stays in the session. No personal photos/tokens.

## Critique Disposition

One critique executed, verdict Revise. PC-001 disposed directly: explicitly
update the pre-existing exact CSP assertion alongside the image-only source
change. Maximum two additions and no removals unchanged. Planning Ready;
no second critique or significant user decision needed.

## Follow-Up Items

Parent RV-002 fresh user acceptance remains outside this necessary repair.

## Handoff

Research reused from reproduced parent RV-001; Planning Ready. After the
single critique, implement P01 and execute this child's single Review.
