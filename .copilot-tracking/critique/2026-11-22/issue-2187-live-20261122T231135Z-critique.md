# Critique: issue 2187 (run 20261122T231135Z)

Verdict: proceed. Executed once.

* Behaviour already delivered; do not change src. Compatible: add one test with a real held lock.
* Rejected: re-implementing the skip (would duplicate 46c328182a).
* Risk: flock on a second descriptor in the same process still conflicts; the heavy-group case in the test confirms it.
