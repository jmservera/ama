# Research: issue 144 queue-slice recovery (2026-11-09)

Disposition: executed. Planning readiness: Ready.

* Seed: PR #1141 head `1a9616d4e` (base main, open, mergeable). Adds `queue_azure.py`, its tests, RPI evidence, one infra README row.
* Local unpublished `feat/slice-144` (`a482d787c`) descends from the seed with 31 further commits (slice 3 post-back, worker role, dispatch permit, core ledger events, SQL tests; 127 files vs main). That is a different, much larger scope, not frozen or independently reviewable here. Not reset or modified.
* The only small, self-contained improvement on that branch is `f7cb6dea4`: the seed poison copy slices `MAX_MESSAGE_CHARS*2` characters, so multibyte text can base64-encode beyond Azure's 64 KiB limit; the poison write fails and the message is never moved. Fix bounds the copy by encoded bytes with a truncation marker. Cherry-picked.
* Original adverse evidence kept: original review (2026-11-04) is a self-review; residual risks routed to slice 3 (token source, post-back, live Azure, duplicate post fence).
* Stack: PR #1272 (`feat/infrastructure-integration-136`, base main, docs/tracking parent; its tree is stale against main and removes later main files) merges cleanly (`git merge-tree`) with this candidate. It does not touch `queue_azure.py`. #107 and #118 are OPEN; the slice has no source dependency on them. PR #1141 stays on main.
* Unmet and not claimed: worker identity, wiring, image deployment, Azure runs.
