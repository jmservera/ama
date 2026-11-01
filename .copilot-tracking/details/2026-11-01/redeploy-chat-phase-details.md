---
title: Redeploy chat changes from main 398e846fd, phase details
ms.date: 2026-11-01
---

## Tag and digests

Tag stem `main-20261101-398e846fd8ed-redeploy-{resident,employee,agents}`; source `org.opencontainers.image.revision` label is the main SHA.

| Image | Digest |
| --- | --- |
| zava-resident-demo | sha256:706b9db4e49a9c6b196758aa7cfd3d8f901b5842260635339bdd9b31019d6d5f |
| zava-forward-api | sha256:7aa2a317a1fe52ddb22ee72a6489ed7addaab245728f99dc047c8c2ab7b25289 |
| zava-forward-agents | sha256:2217d94d1c23e0e076d22d09896781a0c64581fe2eb4de547bf7fe919d56ebae |

## Rollback

Resident: rerun the helper with the previous digest `9ce989d9...`; others: `az containerapp ingress traffic set --revision-weight <previous>=100` after `az containerapp revision activate`. Previous revisions: resident `--0000006`, demo API `--0000007`, API `--0000001`, agents `--z34vcua`. Not needed: all new revisions Healthy.

## Live checks

Playwright (Chromium, 1280x900) with the test users; credentials read inside the script only. Resident: sign-in, three chat questions, sensors card. Employee: Entra sign-in, case chat (size, notice, grounding, stays open, storage API), capacity and work orders paging.
