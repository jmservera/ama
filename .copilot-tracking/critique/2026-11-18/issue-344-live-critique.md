# Issue 344 live critique (executed once)

Verdict: proceed.
* Risk: overclaiming "401" when browsers see redirects. Disposition: the note states the split and cites #350 (applied).
* Risk: 200 on a route read as feature parity. Disposition: note says reachability only (applied).
* Risk: credentials in evidence. Disposition: literal scan before commit (applied).
* Risk: /api/time/status 500 tempts a source fix. Disposition: rejected for this task; src change would need FULL tier; filed as follow-up.
