# Changes: issue 360 live re-run (2026-11-18)

Docs-only candidate, tier FOCUSED. Refs #360. No Azure resource was created or changed; no throwaway resource exists.

## Files

* `docs/reference/research/direct-ingress-live-demo-2026-11-18.md`: appended re-run section.
* `docs/reference/log.md`: appended entry.
* `.copilot-tracking/evidence/2026-11-18/issue-360-live-rerun/`: scripts, raw outputs, screenshot.

## Per-criterion table (re-run 11:30 UTC)

| Criterion | Result | Basis |
| --- | --- | --- |
| a | Proven (live config reconfirmed) | external env, own subnet, NSG 443; SQL, Key Vault, storage, ACR, Foundry, IoT Hub public access disabled |
| b | Not re-tested | offline tests |
| c | Unproven | no recorded owner approval of the migration plan |
| d | Partly proven | health/welcome 200, HTTPS, non-browser 401, sign-in, role claim, 443 cases; browser-mode 401 fails (302); second-role denial and restart persistence unproven |
| e | Unproven | no Front Door resources exist, but owner authorisation and order after d not recorded |
| f | Not re-tested | docs |
