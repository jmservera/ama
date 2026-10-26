---
title: Resident Azure release 462 - research (2026-10-26)
description: Evidence gathered while releasing the resident showcase. Counts and names only.
ms.date: 2026-10-26
---

Written after the interim deployment from the notes taken at the time; it records what was found, not a pre-implementation phase.

* Image `zava-resident-demo` built `--no-cache` and scanned with Trivy 0.76.0 (`src/trivy.yaml`): 0 HIGH or CRITICAL. An earlier cached build had a HIGH openssl finding, so the cache was dropped.
* ACR `crcutovertestrzsrg` was Premium with public access and exports disabled; a local push was impossible without an owner-approved temporary export-policy change and single-IP rule (approved 2026-10-26 23:12Z). Restore must remove the rule by bare IP, not `/32`, and set default action back to Allow; read back identical to the saved before file both times.
* The private allowlist yields 522 unique usable emails; one duplicate email across two cases stays excluded.
* On first deployment the app refused to start: `The allowlist supplies more than 25 showcase mappings`. The cap `MAX_MAPPINGS = 25` came from the local showcase slice and conflicts with the owner-approved 522.
* The cap is applied only at startup (`__main__.py` builds the identity map once from `list_rows`), and the SQL reader fetches `MAX_MAPPINGS + 2` rows, so the read is bounded.
