---
title: API Authentication Initialization Changes
description: Evidence for the owner-requested repeatable initialization
ms.date: 2026-10-12
---

## Invocation boundary

P01 only is approved for this invocation. The existing creation helper selects
by display name and manages roles/secrets, so do not reuse it as a callback-only
repair against the renamed existing registration. Add a focused post-deployment
initializer using the live client ID and FQDN, preserving unrelated settings.
Source write boundary: initializer, its tests/CI, infrastructure guidance,
knowledge-base index/log and current child tracking. P02 remains separate.

## P01-T01 and P01-T02: Initializer and isolated test evidence

Added the callback-only initializer and its CI regression suite. All 13
mocked-CLI tests passed, covering idempotence, redirect/settings preservation,
read/write denial, tenant/client validation, check-only operation, verification
failure and isolated login. No live Graph update or device-code login was
performed; the current operator still lacks application-management authority.

## P03: Owner-requested logo repair and diagnosed cause

The owner reports the logo is not showing. The deployed API's internal static
request closed without a response. Its console traceback establishes
PermissionError reading `/app/web/zava-logo.png`. The tracked source file has
mode 0600 and Docker COPY retains root ownership; the runtime UID 10001 cannot
read it. The PNG itself is valid and displays correctly on white.

Expanded the owner-approved boundary to migration asset permissions and tests,
MVP image packaging and static/image tests, rebuild/deployment and durable
guidance. P03 is active; P02 is not included. No repeated parent Review or
authentication bypass is authorised or needed.

## P03-T01: Public asset generation and image regression

New atomic migration outputs use mode 0644 while existing target modes are
preserved. The Dockerfile normalizes packaged web readability before retaining
USER 10001. CI intentionally builds from a mode-0600 logo and requires the
running read-only/non-root image to return the exact PNG with image/png.
All 22 migration tests and 273 MVP tests pass, with 26 existing MVP skips.
The new HTTP regression checks the header URL, PNG signature and exact bytes.

## P03-T02: Rebuilt deployment and served asset

ACR run db2 succeeded from the still-mode-0600 source asset. Deployed
crforwardtestrzsrg.azurecr.io/zava-forward-mvp:logo-20261012-permissions,
digest sha256:3cfb24d13eba6ede91efaebb15548896a58f8a37b47d412ceaa0efa80b36f981,
as ca-forward-test-api--0000001.

The running UID 10001 now reads a mode-0644 logo and its static server returns
200 image/png, 14325 bytes, 644 x 225. Its SHA-256 matches the source:
92a6cd06c63f978ad1a2d8f8a07b2899819ebf0f6bc6f5042bd23f3adc249895.
Public health remains 200, unauthenticated API/logo requests remain 401, and
browser entry remains 302 to Entra. No tenant registration was changed.
Evidence is recorded in the session's zava-live-logo-check.json and build log.
Publication remains pending; P02 browser/name/role acceptance is not claimed.
