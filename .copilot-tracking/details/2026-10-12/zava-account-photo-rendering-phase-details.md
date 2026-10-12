---
title: Photo Rendering Repair Details
description: Exact source and deployment boundaries
ms.date: 2026-10-12
---

## P01-T01

App.csp in mvp/zavaforward_mvp/server.py currently lacks blob: in img-src;
app.js uses URL.createObjectURL for binary proxy response. Add that source
only to img-src. Do not allow Blob scripts/default/frame sources.
Target `img-src 'self' data: blob:` followed by any existing map host.
Update the existing exact custom-tile CSP assertion in scope, preserving it.
Add two tests in test_auth.py: CSP exact scope and authenticated PNG response
with image MIME/no-store/nosniff and no token payload. Use synthetic inputs.

## P01-T02

Run targeted and full suites, build a versioned image, update only the API
image retaining existing SQL, AI, roles and private token-store configuration.
Check ready rollout and repeat the actual HTTPS public-logo Blob load that
failed in parent RV-001. Update guide/index/log for the security-policy finding,
publish through #65, and execute one new-child Review. Parent Review is final
historical evidence, not a closure check to rewrite.
