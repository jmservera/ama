# Changes: remove the obsolete synthetic proof case (issue 360)

Date: 2026-10-25. Phase order actually followed: research (12:30Z), plan and details (written before the critique), one independent critique at about 12:32Z (file times) (FAIL as drafted, six findings, all accepted, appended to the plan), implementation, review. No retrospective artifact.

## Live operation (12:45Z, existing app runtime, no source change)
* A rolled-back dry run of the final script ran first (all guards passed, rollback on purpose), then one committed run. A first dry-run attempt failed with HTTP 404 (exec command too long) and a second with 429 (rate limit, retry after 600 s); neither reached the database. The script was then split into two exec calls.
* Result read back from the database: 981 to 980 cases, 444 to 443 open, exact match 0, 17 to 18 audit entries with the chain intact, 7 recommendations and 0 staff unchanged, other-980 digest unchanged, `meta.seq` 9 to 10.
* Revision `0000006` restarted between 12:45:28Z and 12:46:58Z so the in-memory cache dropped the case (replica `6tvdg` replaced by `gn2zz`). A fresh load shows 980 cases and the map projection (443 points) excludes the id. Health 200, anonymous and forged-header APIs 401, image `0769b52d` and the OSM tile env unchanged.
* External evidence: `/tmp/ama-360-remove-example-live.md`; issue 360 comment 6397824469. Private row backup `/tmp/ama-360-rm/base-out.txt` (mode 600, not committed).

## Files changed in the branch
* `.copilot-tracking/{research,plans,details,changes,reviews}/2026-10-25/remove-synthetic-example-360-*`
* `infra/README.md` runbook bullet (route, guards, restart after an external delete)
* `docs/reference/log.md` appended entry

## Limits
Owner browser view of the map is not verified. No eviction helper exists, so each external delete needs a restart; possible follow-up. The earlier 12:33Z script and its first dry run are recorded above, not hidden.
