# Issue 220 live r7 research (2026-11-19)

Refs #220. Synthetic demo, desktop only, owner decisions of 2026-11-18.

* Only criterion 5 is unticked: "No retaliation, inferred refusal or delayed hazard response".
* Code and tests exist on main (`no_retaliation_guard.py`, `challenges.py`, 30 offline tests pass).
* Live app `ca-cutover-test-demo-api` revision 0000033 still runs digest `sha256:5368f4e4...c17e5fb`, the image before the identity fix. A successful live write needs a rebuild and deploy, not authorised.
* Real retaliation over time is production-only.
* Research disposition: executed. Planning readiness: Ready for a docs-only record; no buildable gap.
